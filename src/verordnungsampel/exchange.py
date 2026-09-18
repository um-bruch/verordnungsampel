"""Austauschformate fuer VerordnungsAmpel (EXPORTFORMAT.md).

Definiert die beiden standardisierten, versionierten Schemas fuer die
dateibasierte Weitergabe zwischen Desktop, lokaler Web/PWA und externem
Audit/Review:

1. ``verordnungsampel-casebundle-v1``:
   Pseudonymisierte Fallbuendel (Checks, Begruendungen, Vorab-Workflows, Audit).
   Enthaelt strenge Datenschutz- und Datenminimierungsschranken:
   - Keine Klartext-Patientendaten (contains_clear_patient_data=True blockiert den Import)
   - Nur Pseudonyme in patient_ref (Klartextnamen werden zurueckgewiesen)
   - Keine Credentials, Tokens, absolute Pfade oder Telemetriedaten
   - Workflow-Texte werden beim Import standardmaessig als unverified markiert

2. ``verordnungsampel-ruleset-v1``:
   Regelwerks-Snapshots mit Quellenstand, Checksummen und Code-Relationen.
   - Idempotenter, atomarer Import
   - Erfordert explizite Bestaetigung (confirmed=True) vor dem Ueberschreiben
   - Pruefsummen- und Provenienz-Transparenz
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from verordnungsampel import __version__
from verordnungsampel.audit.compliance_log import ComplianceLog
from verordnungsampel.db.schema import create_schema, save_setting
from verordnungsampel.utils.logger import get_logger
from verordnungsampel.utils.paths import project_data_dir

logger = get_logger(__name__)

CASEBUNDLE_SCHEMA_VERSION = "verordnungsampel-casebundle-v1"
RULESET_SCHEMA_VERSION = "verordnungsampel-ruleset-v1"
APP_NAME = "VerordnungsAmpel"

VALID_TRAFFIC_LIGHTS = {"rot", "gelb", "gruen"}
VALID_JUSTIFICATION_STATUS = {"draft", "complete", "not_applicable"}
VALID_WORKFLOW_TYPES = {
    "pflicht_antrag",
    "verboten_hinweis",
    "stellungnahme",
    "keine_aktion",
}

# Heuristik zur Erkennung potenzieller Klartextnamen in patient_ref
# z.B. "Max Mustermann", "Dr. Müller, Hans", "Mueller, Hans" oder E-Mail-Adressen
_CLEARNAME_PATTERN = re.compile(
    r"(?:^[A-ZÄÖÜ][a-zäöüß]+(?:,\s*|\s+)[A-ZÄÖÜ][a-zäöüß]+)|(?:@)|(?:Herr|Frau|Dr\.|Prof\.)",
    re.IGNORECASE,
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# =============================================================================
# 1. CASEBUNDLE-V1 (Fallbuendel)
# =============================================================================


def export_casebundle(
    cases: List[Dict[str, Any]],
    audit_entries: Optional[List[Dict[str, Any]]] = None,
    *,
    contains_clear_patient_data: bool = False,
    pseudonymized: bool = True,
    notes: Optional[str] = None,
    hash_chain_exported: bool = False,
) -> Dict[str, Any]:
    """Erzeugt ein serialisierbares Fallbuendel-Paket nach `verordnungsampel-casebundle-v1`.

    Args:
        cases: Liste von Fall-Dictionaries.
        audit_entries: Optionale Audit-Log-Eintraege.
        contains_clear_patient_data: Datenschutz-Flag (muss False sein).
        pseudonymized: Ob die Daten pseudonymisiert sind (Standard: True).
        notes: Optionale Hinweise zum Datenschutz.
        hash_chain_exported: Ob kryptografische Hash-Chain-Eintraege enthalten sind.

    Returns:
        Strukturiertes Dictionary gemaess Schema-Spezifikation.
    """
    if contains_clear_patient_data:
        raise ValueError(
            "Export von Klartext-Patientendaten ist unzulaessig "
            "(contains_clear_patient_data darf nicht True sein)."
        )

    # Bereinige und normalisiere Faelle
    normalized_cases: List[Dict[str, Any]] = []
    for idx, c in enumerate(cases, 1):
        case_dict = dict(c)
        case_ref = case_dict.get("case_ref") or f"case-{idx:04d}"
        patient_ref = case_dict.get("patient_ref")

        if patient_ref and _CLEARNAME_PATTERN.search(str(patient_ref)):
            raise ValueError(
                f"Klartext-Name in patient_ref bei Fall '{case_ref}' entdeckt: {patient_ref!r}. "
                "Nur Pseudonyme (z.B. 'P-101') sind zulaessig."
            )

        # Sichere Struktur (Resilienz gegen None und inkompatible Typen)
        res_raw = case_dict.get("result")
        res = res_raw if isinstance(res_raw, dict) else {}

        just_raw = case_dict.get("justification")
        just = just_raw if isinstance(just_raw, dict) else {}

        wf_raw = case_dict.get("workflow")
        wf = wf_raw if isinstance(wf_raw, dict) else {}

        traffic_light = res.get("traffic_light")
        if not traffic_light:
            traffic_light = "gruen"
        else:
            traffic_light = str(traffic_light).lower()

        matched_rules = res.get("matched_rules")
        matched_rules_list = list(matched_rules) if isinstance(matched_rules, (list, tuple)) else []

        source_refs = res.get("source_refs")
        source_refs_list = list(source_refs) if isinstance(source_refs, (list, tuple)) else []

        just_status = just.get("status")
        if not just_status:
            just_status = "not_applicable"
        else:
            just_status = str(just_status).lower()

        just_steps = just.get("steps")
        just_steps_list = list(just_steps) if isinstance(just_steps, (list, tuple)) else []

        wf_type = wf.get("type") or "keine_aktion"

        alter_val = case_dict.get("alter")
        if alter_val is None:
            alter_val = case_dict.get("age_years")

        norm_item: Dict[str, Any] = {
            "case_ref": str(case_ref),
            "patient_ref": str(patient_ref) if patient_ref else None,
            "icd": str(case_dict.get("icd", "")).strip().upper(),
            "atc": str(case_dict.get("atc", "")).strip().upper(),
            "alter": alter_val,
            "checked_at": case_dict.get("checked_at") or _utc_now_iso(),
            "result": {
                "traffic_light": traffic_light,
                "matched_rules": matched_rules_list,
                "source_refs": source_refs_list,
            },
            "justification": {
                "status": just_status,
                "steps": just_steps_list,
            },
            "workflow": {
                "type": wf_type,
                "text": wf.get("text"),
            },
        }
        # Behalte optionale Zusatzfelder tolerant bei
        for k, v in case_dict.items():
            if k not in norm_item and k not in ("age_years",):
                norm_item[k] = v

        normalized_cases.append(norm_item)

    payload: Dict[str, Any] = {
        "schema_version": CASEBUNDLE_SCHEMA_VERSION,
        "created_at": _utc_now_iso(),
        "created_by_app": {
            "name": APP_NAME,
            "version": __version__,
        },
        "privacy": {
            "contains_clear_patient_data": False,
            "pseudonymized": bool(pseudonymized),
            "notes": notes or "Keine Namen, Geburtsdaten, Versichertennummern oder Praxisgeheimnisse.",
        },
        "cases": normalized_cases,
        "audit": {
            "hash_chain_exported": bool(hash_chain_exported),
            "entries": list(audit_entries or []),
        },
    }
    return payload


def export_casebundle_from_log(
    log: ComplianceLog,
    *,
    pseudonymize: bool = True,
    prefix: str = "case-",
    include_audit_chain: bool = False,
) -> Dict[str, Any]:
    """Liest den lokalen ComplianceLog aus und exportiert ihn als casebundle-v1."""
    entries = log.all_entries()
    cases: List[Dict[str, Any]] = []
    audit_chain: List[Dict[str, Any]] = []

    for e in entries:
        extra = e.extra or {}
        patient_ref = extra.get("patient") or extra.get("patient_ref")
        if pseudonymize and (not patient_ref or _CLEARNAME_PATTERN.search(str(patient_ref))):
            patient_ref = f"P-{e.seq:04d}"

        wf_data = extra.get("workflow") or {}
        just_data = extra.get("justification") or {}

        matched_rules = extra.get("matched_rules", [])
        if not matched_rules and extra.get("regel"):
            matched_rules = [extra["regel"]]

        source_refs = extra.get("source_refs", [])
        if not source_refs and extra.get("quelle"):
            source_refs = [extra["quelle"]]

        case_item = {
            "case_ref": f"{prefix}{e.seq:04d}",
            "patient_ref": patient_ref,
            "icd": e.icd,
            "atc": e.atc,
            "alter": e.alter,
            "checked_at": e.timestamp,
            "result": {
                "traffic_light": e.ampel,
                "matched_rules": matched_rules,
                "source_refs": source_refs,
            },
            "justification": {
                "status": just_data.get("status", "complete" if just_data else "not_applicable"),
                "steps": just_data.get("steps", []),
            },
            "workflow": {
                "type": e.container or wf_data.get("type", "keine_aktion"),
                "text": wf_data.get("text"),
            },
        }
        cases.append(case_item)

        if include_audit_chain:
            audit_chain.append(
                {
                    "seq": e.seq,
                    "timestamp": e.timestamp,
                    "prev_hash": e.prev_hash,
                    "hash": e.hash,
                    "ampel": e.ampel,
                }
            )

    return export_casebundle(
        cases,
        audit_entries=audit_chain if include_audit_chain else None,
        hash_chain_exported=include_audit_chain,
        pseudonymized=True,
    )


def export_casebundle_json(
    cases: List[Dict[str, Any]],
    audit_entries: Optional[List[Dict[str, Any]]] = None,
    *,
    pseudonymized: bool = True,
    hash_chain_exported: bool = False,
    indent: int = 2,
) -> str:
    """Serialisiert das Fallbuendel als UTF-8-JSON-String mit echten Umlauten."""
    bundle = export_casebundle(
        cases,
        audit_entries=audit_entries,
        pseudonymized=pseudonymized,
        hash_chain_exported=hash_chain_exported,
    )
    return json.dumps(bundle, ensure_ascii=False, indent=indent)


def validate_casebundle(payload: Any) -> List[str]:
    """Validiert ein Rohes Dictionary gegen den `verordnungsampel-casebundle-v1`-Vertrag.

    Gibt eine Liste von Fehlermeldungen zurueck (leer, wenn gueltig).
    Bekannte Felder werden strikt geprueft, unbekannte tolerant ignoriert.
    """
    errors: List[str] = []
    if not isinstance(payload, dict):
        return ["Payload muss ein JSON-Objekt sein."]

    # Schema-Version
    schema_version = payload.get("schema_version")
    if schema_version != CASEBUNDLE_SCHEMA_VERSION:
        errors.append(
            f"Ungueltige schema_version: erwartet '{CASEBUNDLE_SCHEMA_VERSION}', "
            f"erhalten '{schema_version}'."
        )

    # Privacy-Block
    privacy = payload.get("privacy")
    if not isinstance(privacy, dict):
        errors.append("Feld 'privacy' fehlt oder ist kein JSON-Objekt.")
    else:
        if privacy.get("contains_clear_patient_data") is True:
            errors.append(
                "Import verweigert: contains_clear_patient_data ist True "
                "(Klartext-Patientendaten unzulaessig)."
            )

    # Cases-Liste
    cases = payload.get("cases")
    if not isinstance(cases, list):
        errors.append("Feld 'cases' fehlt oder ist keine Liste.")
        return errors

    for idx, c in enumerate(cases, 1):
        prefix = f"Fall #{idx}"
        if not isinstance(c, dict):
            errors.append(f"{prefix}: Muss ein JSON-Objekt sein.")
            continue

        case_ref = c.get("case_ref")
        if not case_ref or not str(case_ref).strip():
            errors.append(f"{prefix}: 'case_ref' fehlt oder ist leer.")

        icd = c.get("icd")
        if not icd or not str(icd).strip():
            errors.append(f"{prefix}: 'icd' fehlt oder ist leer.")

        atc = c.get("atc")
        if not atc or not str(atc).strip():
            errors.append(f"{prefix}: 'atc' fehlt oder ist leer.")

        # Pruefe patient_ref auf Klartext-Namen
        patient_ref = c.get("patient_ref")
        if patient_ref and _CLEARNAME_PATTERN.search(str(patient_ref)):
            errors.append(
                f"{prefix}: Klartext-Muster in 'patient_ref' erkannt ({patient_ref!r}). "
                "Nur Pseudonyme gestattet."
            )

        # Result
        res = c.get("result")
        if res is not None:
            if not isinstance(res, dict):
                errors.append(f"{prefix}: 'result' muss ein JSON-Objekt sein.")
            else:
                tl = str(res.get("traffic_light", "")).lower()
                if tl not in VALID_TRAFFIC_LIGHTS:
                    errors.append(
                        f"{prefix}: traffic_light '{tl}' ungueltig (erlaubt: {sorted(VALID_TRAFFIC_LIGHTS)})."
                    )

        # Justification
        just = c.get("justification")
        if just is not None:
            if not isinstance(just, dict):
                errors.append(f"{prefix}: 'justification' muss ein JSON-Objekt sein.")
            else:
                st = str(just.get("status", "")).lower()
                if st and st not in VALID_JUSTIFICATION_STATUS:
                    errors.append(
                        f"{prefix}: justification.status '{st}' ungueltig (erlaubt: {sorted(VALID_JUSTIFICATION_STATUS)})."
                    )

        # Workflow
        wf = c.get("workflow")
        if wf is not None:
            if not isinstance(wf, dict):
                errors.append(f"{prefix}: 'workflow' muss ein JSON-Objekt sein.")
            else:
                wt = wf.get("type")
                if wt is not None and str(wt).lower() not in VALID_WORKFLOW_TYPES:
                    errors.append(
                        f"{prefix}: workflow.type '{wt}' ungueltig (erlaubt: {sorted(VALID_WORKFLOW_TYPES)})."
                    )

    return errors


def import_casebundle(
    payload: Dict[str, Any],
    *,
    target_log: Optional[ComplianceLog] = None,
    mark_workflow_unverified: bool = True,
) -> Dict[str, Any]:
    """Validiert und importiert ein Fallbuendel.

    Args:
        payload: Das eingelesene JSON-Dictionary.
        target_log: Optionaler ComplianceLog, in den die Faelle uebernommen werden sollen.
        mark_workflow_unverified: Ob Workflow-Texte als unueberprueft gekennzeichnet werden.

    Returns:
        Ergebnis-Dictionary mit 'cases' und 'imported_count'.

    Raises:
        ValueError: Bei Validierungsfehlern oder wenn contains_clear_patient_data True ist.
    """
    errors = validate_casebundle(payload)
    if errors:
        raise ValueError(
            "Casebundle-Validierung fehlgeschlagen:\n - " + "\n - ".join(errors)
        )

    cases = payload.get("cases", [])
    processed_cases: List[Dict[str, Any]] = []

    for c in cases:
        case_copy = dict(c)
        wf = dict(case_copy.get("workflow") or {})
        if mark_workflow_unverified and wf.get("text"):
            wf["verified"] = False
            wf["import_warning"] = "Unüberprüfter importierter Freitext (Nutzer-Ausgabe)."
        case_copy["workflow"] = wf
        processed_cases.append(case_copy)

    imported_count = 0
    if target_log is not None:
        for item in processed_cases:
            res_raw = item.get("result")
            res = res_raw if isinstance(res_raw, dict) else {}

            wf_raw = item.get("workflow")
            wf = wf_raw if isinstance(wf_raw, dict) else {}

            just_raw = item.get("justification")
            just = just_raw if isinstance(just_raw, dict) else {}

            alter_val = item.get("alter")
            if alter_val is None:
                alter_val = item.get("age_years")

            extra_payload = {
                "source": "casebundle_import",
                "schema_version": CASEBUNDLE_SCHEMA_VERSION,
                "case_ref": item.get("case_ref"),
                "patient_ref": item.get("patient_ref"),
                "matched_rules": list(res.get("matched_rules") or []),
                "source_refs": list(res.get("source_refs") or []),
                "justification": just,
                "workflow": wf,
            }
            target_log.append(
                icd=item["icd"],
                atc=item["atc"],
                alter=alter_val,
                ampel=res.get("traffic_light") or "gruen",
                begruendung=f"Importierter Fall {item.get('case_ref')}",
                container=wf.get("type"),
                nutzer="import",
                extra=extra_payload,
            )
            imported_count += 1

    return {
        "status": "ok",
        "schema_version": CASEBUNDLE_SCHEMA_VERSION,
        "case_count": len(processed_cases),
        "imported_into_log_count": imported_count,
        "cases": processed_cases,
    }


# =============================================================================
# 2. RULESET-V1 (Regelwerks-Snapshots)
# =============================================================================


def _calculate_file_checksum(filepath: Path) -> str:
    """Berechnet die SHA-256-Pruefsumme einer Datei."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as fh:
        while chunk := fh.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def export_ruleset(
    conn: sqlite3.Connection,
    seed_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Exportiert den aktuellen Stand des Regelwerks als `verordnungsampel-ruleset-v1`.

    Args:
        conn: SQLite-Verbindung zur aktuellen Regel-Datenbank.
        seed_dir: Pfad zum `data/seed`-Verzeichnis fuer Pruefsummen.

    Returns:
        Strukturiertes Dictionary gemaess ruleset-v1-Spezifikation.
    """
    if seed_dir is None:
        seed_dir = project_data_dir() / "seed"

    # 1. Pruefsummen der Seed-Dateien
    checksum_files: List[Dict[str, str]] = []
    source_state: Dict[str, str] = {
        "amrl_iii": "2025-10-09",
        "amrl_v": "2026-03-24",
        "amrl_vi": "2025-05-07",
    }

    if seed_dir.exists() and seed_dir.is_dir():
        for p in sorted(seed_dir.glob("*.json")):
            if p.name.startswith("_") or p.name.startswith("."):
                continue
            sha = _calculate_file_checksum(p)
            checksum_files.append({"file": p.name, "sha256": sha})
            # Versuche Stand-Datum aus Metadaten zu lesen
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    raw = json.load(fh)
                    if isinstance(raw, dict) and "_meta" in raw:
                        meta = raw["_meta"]
                        stand = meta.get("stand")
                        anlage = meta.get("anlage")
                        if stand and anlage:
                            key = f"amrl_{str(anlage).lower()}"
                            source_state[key] = str(stand)
            except Exception:
                pass

    # 2. Quellen aus DB
    quellen_map: Dict[int, Dict[str, Any]] = {}
    cur = conn.cursor()
    cur.execute("SELECT id, kuerzel, titel, url, stand FROM quelle")
    for r in cur.fetchall():
        quellen_map[r[0]] = {
            "kuerzel": r[1],
            "titel": r[2],
            "url": r[3],
            "stand": r[4],
        }

    # 3. Regeln aus DB
    rules: List[Dict[str, Any]] = []
    cur.execute(
        """
        SELECT id, kuerzel, atc_pattern, icd_pattern, altersgrenze, ampel, begruendung, container, quelle_id
        FROM regel
        ORDER BY id
        """
    )
    for r in cur.fetchall():
        q_id = r[8]
        rules.append(
            {
                "kuerzel": r[1],
                "atc_pattern": r[2],
                "icd_pattern": r[3],
                "altersgrenze": r[4],
                "ampel": r[5],
                "begruendung": r[6],
                "container": r[7],
                "quelle": quellen_map.get(q_id),
            }
        )

    # 4. ICD10
    icd10: List[Dict[str, Any]] = []
    cur.execute("SELECT code, bezeichnung, kapitel FROM icd10 ORDER BY code")
    for r in cur.fetchall():
        icd10.append({"code": r[0], "bezeichnung": r[1], "kapitel": r[2]})

    # 5. ATC
    atc: List[Dict[str, Any]] = []
    cur.execute("SELECT code, bezeichnung, wirkstoff, ddd, ddd_einheit FROM atc ORDER BY code")
    for r in cur.fetchall():
        atc.append(
            {
                "code": r[0],
                "bezeichnung": r[1],
                "wirkstoff": r[2],
                "ddd": r[3],
                "ddd_einheit": r[4],
            }
        )

    # 6. Praxisbesonderheiten
    praxisbesonderheiten: List[Dict[str, Any]] = []
    cur.execute(
        """
        SELECT id, atc_pattern, icd_pattern, bezeichnung, gueltig_ab, gueltig_bis, quelle_id
        FROM praxisbesonderheit
        ORDER BY id
        """
    )
    for r in cur.fetchall():
        q_id = r[6]
        praxisbesonderheiten.append(
            {
                "atc_pattern": r[1],
                "icd_pattern": r[2],
                "bezeichnung": r[3],
                "gueltig_ab": r[4],
                "gueltig_bis": r[5],
                "quelle": quellen_map.get(q_id),
            }
        )

    # 7. Relationen
    relations: List[Dict[str, Any]] = []
    cur.execute(
        """
        SELECT r.kuerzel, ra.atc_code, ra.match_pattern
        FROM regel_atc ra JOIN regel r ON ra.regel_id = r.id
        """
    )
    for r in cur.fetchall():
        relations.append(
            {
                "type": "regel_atc",
                "regel_kuerzel": r[0],
                "atc_code": r[1],
                "match_pattern": r[2],
            }
        )

    cur.execute(
        """
        SELECT r.kuerzel, ri.icd10_code, ri.match_pattern
        FROM regel_icd10 ri JOIN regel r ON ri.regel_id = r.id
        """
    )
    for r in cur.fetchall():
        relations.append(
            {
                "type": "regel_icd10",
                "regel_kuerzel": r[0],
                "icd10_code": r[1],
                "match_pattern": r[2],
            }
        )

    payload: Dict[str, Any] = {
        "schema_version": RULESET_SCHEMA_VERSION,
        "created_at": _utc_now_iso(),
        "created_by_app": {
            "name": APP_NAME,
            "version": __version__,
        },
        "source_state": source_state,
        "checksums": {
            "algorithm": "sha256",
            "files": checksum_files,
        },
        "rules": rules,
        "icd10": icd10,
        "atc": atc,
        "praxisbesonderheiten": praxisbesonderheiten,
        "relations": relations,
    }
    return payload


def export_ruleset_json(
    conn: sqlite3.Connection,
    seed_dir: Optional[Path] = None,
    indent: int = 2,
) -> str:
    """Serialisiert das Regelwerk als UTF-8-JSON-String mit echten Umlauten."""
    ruleset = export_ruleset(conn, seed_dir=seed_dir)
    return json.dumps(ruleset, ensure_ascii=False, indent=indent)


def validate_ruleset(payload: Any) -> List[str]:
    """Validiert ein Rohes Dictionary gegen den `verordnungsampel-ruleset-v1`-Vertrag."""
    errors: List[str] = []
    if not isinstance(payload, dict):
        return ["Payload muss ein JSON-Objekt sein."]

    schema_version = payload.get("schema_version")
    if schema_version != RULESET_SCHEMA_VERSION:
        errors.append(
            f"Ungueltige schema_version: erwartet '{RULESET_SCHEMA_VERSION}', "
            f"erhalten '{schema_version}'."
        )

    if not isinstance(payload.get("source_state"), dict):
        errors.append("Feld 'source_state' fehlt oder ist kein JSON-Objekt.")

    checksums = payload.get("checksums")
    if not isinstance(checksums, dict) or "files" not in checksums:
        errors.append("Feld 'checksums' fehlt oder enthaelt keine 'files'-Liste.")

    rules = payload.get("rules")
    if not isinstance(rules, list):
        errors.append("Feld 'rules' fehlt oder ist keine Liste.")
    else:
        for idx, r in enumerate(rules, 1):
            if not isinstance(r, dict):
                errors.append(f"Regel #{idx}: Muss ein JSON-Objekt sein.")
                continue
            if not r.get("kuerzel"):
                errors.append(f"Regel #{idx}: 'kuerzel' fehlt oder ist leer.")
            ampel = str(r.get("ampel", "")).lower()
            if ampel not in VALID_TRAFFIC_LIGHTS:
                errors.append(
                    f"Regel #{idx}: Ampel '{ampel}' ungueltig (erlaubt: {sorted(VALID_TRAFFIC_LIGHTS)})."
                )

    if not isinstance(payload.get("icd10"), list):
        errors.append("Feld 'icd10' fehlt oder ist keine Liste.")

    if not isinstance(payload.get("atc"), list):
        errors.append("Feld 'atc' fehlt oder ist keine Liste.")

    if not isinstance(payload.get("praxisbesonderheiten"), list):
        errors.append("Feld 'praxisbesonderheiten' fehlt oder ist keine Liste.")

    return errors


def import_ruleset(
    payload: Dict[str, Any],
    conn: sqlite3.Connection,
    *,
    confirmed: bool = False,
) -> Dict[str, int]:
    """Importiert einen Regelwerks-Snapshot atomar in die lokale SQLite-Datenbank.

    Gemaess EXPORTFORMAT.md:
    "Regelwerks-Snapshots dürfen bestehende lokale Daten nur nach expliziter
    Nutzerbestätigung ersetzen."
    Daher ist confirmed=True verpflichtend.
    """
    if not confirmed:
        raise ValueError(
            "Regelwerks-Snapshots duerfen bestehende lokale Daten nur nach expliziter "
            "Bestaetigung ersetzen. Setzen Sie `confirmed=True` bzw. `--confirm`."
        )

    errors = validate_ruleset(payload)
    if errors:
        raise ValueError(
            "Ruleset-Validierung fehlgeschlagen:\n - " + "\n - ".join(errors)
        )

    # Sicherstellen, dass das Schema existiert
    create_schema(conn)

    cur = conn.cursor()
    imported_counts: Dict[str, int] = {
        "rules": 0,
        "icd10": 0,
        "atc": 0,
        "praxisbesonderheiten": 0,
        "relations": 0,
    }

    # Atomare Transaktion: Entweder alles oder Rollback
    try:
        cur.execute("BEGIN TRANSACTION")

        # 1. Quellen importieren / updaten
        quellen_seen: Dict[str, int] = {}
        all_sources: List[Dict[str, Any]] = []
        for r in payload.get("rules", []):
            q = r.get("quelle")
            if isinstance(q, dict) and q.get("kuerzel"):
                all_sources.append(q)
        for pb in payload.get("praxisbesonderheiten", []):
            q = pb.get("quelle")
            if isinstance(q, dict) and q.get("kuerzel"):
                all_sources.append(q)

        for q in all_sources:
            kuerzel = q["kuerzel"]
            if kuerzel in quellen_seen:
                continue
            cur.execute(
                """
                INSERT OR REPLACE INTO quelle (kuerzel, titel, url, stand)
                VALUES (?, ?, ?, ?)
                """,
                (kuerzel, q.get("titel", kuerzel), q.get("url"), q.get("stand")),
            )
            cur.execute("SELECT id FROM quelle WHERE kuerzel = ?", (kuerzel,))
            row = cur.fetchone()
            if row:
                quellen_seen[kuerzel] = row[0]

        # 2. ICD10
        for item in payload.get("icd10", []):
            if isinstance(item, dict) and item.get("code"):
                cur.execute(
                    """
                    INSERT OR REPLACE INTO icd10 (code, bezeichnung, kapitel)
                    VALUES (?, ?, ?)
                    """,
                    (item["code"], item.get("bezeichnung", ""), item.get("kapitel")),
                )
                imported_counts["icd10"] += 1

        # 3. ATC
        for item in payload.get("atc", []):
            if isinstance(item, dict) and item.get("code"):
                cur.execute(
                    """
                    INSERT OR REPLACE INTO atc (code, bezeichnung, wirkstoff, ddd, ddd_einheit)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        item["code"],
                        item.get("bezeichnung", ""),
                        item.get("wirkstoff"),
                        item.get("ddd"),
                        item.get("ddd_einheit"),
                    ),
                )
                imported_counts["atc"] += 1

        # 4. Regeln (bestehende ersetzen)
        cur.execute("DELETE FROM regel_atc")
        cur.execute("DELETE FROM regel_icd10")
        cur.execute("DELETE FROM regel")

        rule_id_map: Dict[str, int] = {}
        for r in payload.get("rules", []):
            kuerzel = r["kuerzel"]
            q_id = None
            if isinstance(r.get("quelle"), dict):
                q_id = quellen_seen.get(r["quelle"].get("kuerzel"))

            cur.execute(
                """
                INSERT INTO regel (kuerzel, atc_pattern, icd_pattern, altersgrenze, ampel, begruendung, container, quelle_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    kuerzel,
                    r.get("atc_pattern"),
                    r.get("icd_pattern"),
                    r.get("altersgrenze"),
                    r.get("ampel"),
                    r.get("begruendung", ""),
                    r.get("container"),
                    q_id,
                ),
            )
            rule_id_map[kuerzel] = cur.lastrowid
            imported_counts["rules"] += 1

        # 5. Praxisbesonderheiten (bestehende ersetzen)
        cur.execute("DELETE FROM praxisbesonderheit_atc")
        cur.execute("DELETE FROM praxisbesonderheit_icd10")
        cur.execute("DELETE FROM praxisbesonderheit")

        for pb in payload.get("praxisbesonderheiten", []):
            q_id = None
            if isinstance(pb.get("quelle"), dict):
                q_id = quellen_seen.get(pb["quelle"].get("kuerzel"))

            cur.execute(
                """
                INSERT INTO praxisbesonderheit (atc_pattern, icd_pattern, bezeichnung, gueltig_ab, gueltig_bis, quelle_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    pb.get("atc_pattern", ""),
                    pb.get("icd_pattern"),
                    pb.get("bezeichnung", ""),
                    pb.get("gueltig_ab"),
                    pb.get("gueltig_bis"),
                    q_id,
                ),
            )
            imported_counts["praxisbesonderheiten"] += 1

        # 6. Relationen
        for rel in payload.get("relations", []):
            rel_type = rel.get("type")
            if rel_type == "regel_atc":
                r_kuerzel = rel.get("regel_kuerzel")
                r_id = rule_id_map.get(r_kuerzel)
                if r_id:
                    cur.execute(
                        """
                        INSERT OR IGNORE INTO regel_atc (regel_id, atc_code, match_pattern)
                        VALUES (?, ?, ?)
                        """,
                        (r_id, rel.get("atc_code"), rel.get("match_pattern", "")),
                    )
                    imported_counts["relations"] += 1
            elif rel_type == "regel_icd10":
                r_kuerzel = rel.get("regel_kuerzel")
                r_id = rule_id_map.get(r_kuerzel)
                if r_id:
                    cur.execute(
                        """
                        INSERT OR IGNORE INTO regel_icd10 (regel_id, icd10_code, match_pattern)
                        VALUES (?, ?, ?)
                        """,
                        (r_id, rel.get("icd10_code"), rel.get("match_pattern", "")),
                    )
                    imported_counts["relations"] += 1

        # Status in settings festhalten
        save_setting(conn, "last_ruleset_import_at", _utc_now_iso())
        save_setting(conn, "last_ruleset_schema", RULESET_SCHEMA_VERSION)

        conn.commit()
    except Exception as exc:
        conn.rollback()
        logger.error("Fehler beim atomaren Import des Rulesets: %s", exc)
        raise

    return imported_counts
