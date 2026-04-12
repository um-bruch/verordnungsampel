"""Seed-Loader: laedt JSON-Dateien aus ``data/seed/`` in die DB.

Erwartete Struktur (siehe data/seed/README.md):
    quellen.json             -> quelle
    icd10.json               -> icd10
    atc.json                 -> atc
    amrl_anlagen.json        -> amrl_anlage (Legacy-Sammeldatei, kann leer sein)
    amrl_anlage_III.json     -> amrl_anlage (AM-RL Anlage III, vollstaendig)
    amrl_anlage_V.json       -> amrl_anlage (AM-RL Anlage V, Medizinprodukte)
    amrl_anlage_VI_A.json    -> amrl_anlage (AM-RL Anlage VI Teil A, anerkannt)
    amrl_anlage_VI_B.json    -> amrl_anlage (AM-RL Anlage VI Teil B, nicht anerkannt)
    praxisbesonderheiten.json -> praxisbesonderheit
    regeln.json              -> regel

Alle Dateien sind optional. Fehlt eine, wird die jeweilige Tabelle leer
gelassen (mit Warning-Log).

Die vier Anlagen-spezifischen Dateien werden additiv zur Legacy-Sammeldatei
``amrl_anlagen.json`` geladen. Die Tabelle ``amrl_anlage`` wird vor dem
Insert geleert (DELETE), damit mehrfaches Aufrufen von ``init`` idempotent
bleibt.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

from verordnungsampel.utils.logger import get_logger
from verordnungsampel.utils.paths import project_data_dir

logger = get_logger(__name__)

# Speicher fuer geladene Metadaten (fuer CLI-Befehle `sources` / `rules`).
# Wird beim Seed-Laden gefuellt und kann via :func:`get_last_meta` abgerufen
# werden. Pro Dateiname ein Eintrag (z.B. ``amrl_anlage_III.json``).
_LAST_META: Dict[str, Dict[str, Any]] = {}


def _load_json(path: Path) -> List[Dict[str, Any]] | None:
    """Laedt eine Seed-Datei und liefert die Eintragsliste.

    Unterstuetzt zwei Formate fuer Rueckwaerts-Kompatibilitaet:

    1. **Neues Format** (ab Seed-Version 1.0.0):

       .. code-block:: json

          {
            "_meta": { "anlage": "III", "stand": "2025-10-09", ... },
            "eintraege": [ { ... }, ... ]
          }

    2. **Altes Format** (Legacy — flache Liste):

       .. code-block:: json

          [ { ... }, ... ]

    Der ``_meta``-Block wird — sofern vorhanden — in ``_LAST_META``
    abgelegt, damit CLI-Befehle (z.B. ``sources``) ihn ausgeben koennen.
    """
    if not path.exists():
        logger.info("Seed-Datei nicht gefunden, ueberspringe: %s", path.name)
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Seed-Datei %s konnte nicht gelesen werden: %s", path, exc)
        return None
    # Neues Format: dict mit _meta + eintraege
    if isinstance(data, dict):
        meta = data.get("_meta")
        eintraege = data.get("eintraege")
        if isinstance(meta, dict):
            _LAST_META[path.name] = dict(meta)
        if not isinstance(eintraege, list):
            logger.warning(
                "Seed-Datei %s hat kein gueltiges 'eintraege'-Feld — ignoriert",
                path,
            )
            return None
        return eintraege
    # Legacy-Format: flache Liste
    if isinstance(data, list):
        return data
    logger.warning(
        "Seed-Datei %s hat unbekanntes Format (weder dict noch list) — ignoriert",
        path,
    )
    return None


def get_last_meta() -> Dict[str, Dict[str, Any]]:
    """Liefert eine Kopie der zuletzt geladenen ``_meta``-Bloecke.

    Wird von CLI-Befehlen (``sources``, ``rules``) und der GUI genutzt,
    um Stand-Datum, Extraktionsmethode etc. anzuzeigen.
    """
    return {k: dict(v) for k, v in _LAST_META.items()}


def load_meta_only(seed_dir: Path | None = None) -> Dict[str, Dict[str, Any]]:
    """Liest nur die ``_meta``-Bloecke, ohne die DB zu beruehren.

    Praktisch fuer `sources`-Ausgaben, wenn man keine DB-Verbindung
    aufmachen moechte. Ergebnis: ``{dateiname: meta_dict}``.
    """
    if seed_dir is None:
        seed_dir = project_data_dir() / "seed"
    seed_dir = Path(seed_dir)
    result: Dict[str, Dict[str, Any]] = {}
    for fname in (
        "amrl_anlage_III.json",
        "amrl_anlage_V.json",
        "amrl_anlage_VI_A.json",
        "amrl_anlage_VI_B.json",
    ):
        path = seed_dir / fname
        if not path.exists():
            continue
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and isinstance(data.get("_meta"), dict):
            result[fname] = dict(data["_meta"])
    return result


def _resolve_quelle_id(conn: sqlite3.Connection, kuerzel: str | None) -> int | None:
    if not kuerzel:
        return None
    row = conn.execute("SELECT id FROM quelle WHERE kuerzel=?", (kuerzel,)).fetchone()
    return row[0] if row else None


def load_seed_data(conn: sqlite3.Connection, seed_dir: Path | None = None) -> Dict[str, int]:
    """Laedt Seed-Daten aus JSON-Dateien in die DB.

    Args:
        conn: Aktive Verbindung mit angelegtem Schema.
        seed_dir: Verzeichnis mit den JSON-Dateien. Default: ``data/seed`` im Projektroot.

    Returns:
        Mapping ``tabelle -> anzahl_eingefuegt`` (gibt 0 zurueck, wenn nichts geladen).
    """
    if seed_dir is None:
        seed_dir = project_data_dir() / "seed"
    seed_dir = Path(seed_dir)
    # Reset Meta-Cache vor jedem Lauf (sonst verschmilzt er mit Vorlauf).
    _LAST_META.clear()
    counts: Dict[str, int] = {
        "quelle": 0,
        "icd10": 0,
        "atc": 0,
        "amrl_anlage": 0,
        "praxisbesonderheit": 0,
        "regel": 0,
    }

    quellen = _load_json(seed_dir / "quellen.json") or []
    for q in quellen:
        conn.execute(
            """
            INSERT OR IGNORE INTO quelle (kuerzel, titel, url, stand)
            VALUES (?, ?, ?, ?)
            """,
            (q.get("kuerzel"), q.get("titel"), q.get("url"), q.get("stand")),
        )
        counts["quelle"] += 1

    icd10 = _load_json(seed_dir / "icd10.json") or []
    for entry in icd10:
        conn.execute(
            "INSERT OR IGNORE INTO icd10 (code, bezeichnung, kapitel) VALUES (?, ?, ?)",
            (entry.get("code"), entry.get("bezeichnung"), entry.get("kapitel")),
        )
        counts["icd10"] += 1

    atc = _load_json(seed_dir / "atc.json") or []
    for entry in atc:
        conn.execute(
            """
            INSERT OR IGNORE INTO atc (code, bezeichnung, wirkstoff, ddd, ddd_einheit)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                entry.get("code"),
                entry.get("bezeichnung"),
                entry.get("wirkstoff"),
                entry.get("ddd"),
                entry.get("ddd_einheit"),
            ),
        )
        counts["atc"] += 1

    # amrl_anlage und praxisbesonderheit haben keinen UNIQUE-Constraint,
    # daher vor dem Insert leeren, damit init idempotent bleibt.
    conn.execute("DELETE FROM amrl_anlage")
    conn.execute("DELETE FROM praxisbesonderheit")

    amrl_files = (
        "amrl_anlagen.json",      # Legacy-Sammeldatei (kann leer sein)
        "amrl_anlage_III.json",   # Anlage III
        "amrl_anlage_V.json",     # Anlage V
        "amrl_anlage_VI_A.json",  # Anlage VI Teil A (anerkannt)
        "amrl_anlage_VI_B.json",  # Anlage VI Teil B (nicht anerkannt)
    )
    for fname in amrl_files:
        amrl = _load_json(seed_dir / fname) or []
        for entry in amrl:
            quelle_id = _resolve_quelle_id(conn, entry.get("quelle"))
            conn.execute(
                """
                INSERT INTO amrl_anlage
                    (anlage, atc_pattern, bedingung, ampel, begruendung, quelle_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.get("anlage"),
                    entry.get("atc_pattern"),
                    entry.get("bedingung"),
                    entry.get("ampel"),
                    entry.get("begruendung"),
                    quelle_id,
                ),
            )
            counts["amrl_anlage"] += 1

    pb = _load_json(seed_dir / "praxisbesonderheiten.json") or []
    for entry in pb:
        quelle_id = _resolve_quelle_id(conn, entry.get("quelle"))
        conn.execute(
            """
            INSERT INTO praxisbesonderheit
                (atc_pattern, icd_pattern, bezeichnung, gueltig_ab, gueltig_bis, quelle_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                entry.get("atc_pattern"),
                entry.get("icd_pattern"),
                entry.get("bezeichnung"),
                entry.get("gueltig_ab"),
                entry.get("gueltig_bis"),
                quelle_id,
            ),
        )
        counts["praxisbesonderheit"] += 1

    regeln = _load_json(seed_dir / "regeln.json") or []
    for entry in regeln:
        quelle_id = _resolve_quelle_id(conn, entry.get("quelle"))
        conn.execute(
            """
            INSERT OR IGNORE INTO regel
                (kuerzel, atc_pattern, icd_pattern, altersgrenze, ampel, begruendung, container, quelle_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.get("kuerzel"),
                entry.get("atc_pattern"),
                entry.get("icd_pattern"),
                entry.get("altersgrenze"),
                entry.get("ampel"),
                entry.get("begruendung"),
                entry.get("container"),
                quelle_id,
            ),
        )
        counts["regel"] += 1

    # Seed-Metadaten in settings persistieren, damit sie auch nach einem
    # App-Restart verfuegbar sind (z.B. fuer `sources` ohne Zugriff auf
    # das Projektverzeichnis).
    if _LAST_META:
        try:
            conn.execute(
                "INSERT OR REPLACE INTO settings(key, value) VALUES (?, ?)",
                ("seed_meta_json", json.dumps(_LAST_META, ensure_ascii=False)),
            )
            from datetime import datetime
            conn.execute(
                "INSERT OR REPLACE INTO settings(key, value) VALUES (?, ?)",
                ("last_init", datetime.now().isoformat(timespec="seconds")),
            )
        except sqlite3.Error:
            logger.warning("Konnte seed_meta_json nicht in settings schreiben", exc_info=True)

    conn.commit()
    logger.info("Seed-Daten geladen: %s", counts)
    return counts
