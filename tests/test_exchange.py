"""Tests fuer das Austauschformat (verordnungsampel-casebundle-v1 und ruleset-v1).

Gemaess EXPORTFORMAT.md:
- Dateibasierte Export-/Importvertraege
- Datenschutz- und PII-Gates (contains_clear_patient_data, patient_ref Klartext-Abweisung)
- Bekannte Felder strikt, unbekannte Felder tolerant
- Atomarer Import mit Rollback bei Fehlern
- Pruefsummen und Quell-Metadaten
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from unittest.mock import patch

import pytest

from verordnungsampel import (
    CASEBUNDLE_SCHEMA_VERSION,
    RULESET_SCHEMA_VERSION,
    export_casebundle,
    export_casebundle_from_log,
    export_casebundle_json,
    export_ruleset,
    export_ruleset_json,
    import_casebundle,
    import_ruleset,
    validate_casebundle,
    validate_ruleset,
)
from verordnungsampel.audit.compliance_log import ComplianceLog
from verordnungsampel.cli.main import main
from verordnungsampel.db.connection import open_database
from verordnungsampel.db.seed import ensure_seed_data


@pytest.fixture
def sample_cases():
    return [
        {
            "case_ref": "case-001",
            "patient_ref": "P-4711",
            "icd": "F41",
            "atc": "N05BA01",
            "alter": 72,
            "result": {
                "traffic_light": "rot",
                "matched_rules": ["PRISCUS_BENZO_GERIATRIE"],
                "source_refs": ["PRISCUS_2_0"],
            },
            "justification": {
                "status": "complete",
                "steps": [{"step": "anamnese", "ergebnis": "erhoehte Sturzgefahr"}],
            },
            "workflow": {
                "type": "stellungnahme",
                "text": "Stellungnahme zur Priscus-Indikation verfasst.",
            },
        },
        {
            "case_ref": "case-002",
            "patient_ref": "P-1002",
            "icd": "I10",
            "atc": "C09AA02",
            "alter": 55,
            "result": {
                "traffic_light": "gruen",
                "matched_rules": [],
                "source_refs": [],
            },
            "justification": {"status": "not_applicable", "steps": []},
            "workflow": {"type": "keine_aktion", "text": None},
        },
    ]


# =============================================================================
# 1. CASEBUNDLE TESTS
# =============================================================================


def test_export_casebundle_structure_and_schema(sample_cases):
    bundle = export_casebundle(sample_cases)

    assert bundle["schema_version"] == CASEBUNDLE_SCHEMA_VERSION
    assert "created_at" in bundle
    assert bundle["created_by_app"]["name"] == "VerordnungsAmpel"
    assert bundle["privacy"]["contains_clear_patient_data"] is False
    assert bundle["privacy"]["pseudonymized"] is True
    assert len(bundle["cases"]) == 2

    c1 = bundle["cases"][0]
    assert c1["case_ref"] == "case-001"
    assert c1["patient_ref"] == "P-4711"
    assert c1["icd"] == "F41"
    assert c1["atc"] == "N05BA01"
    assert c1["alter"] == 72
    assert c1["result"]["traffic_light"] == "rot"
    assert c1["workflow"]["type"] == "stellungnahme"


def test_export_casebundle_json_utf8_roundtrip(sample_cases):
    json_str = export_casebundle_json(sample_cases)
    # Echte Umlaute vorhanden und kein BOM
    assert "\ufeff" not in json_str
    assert "Stellungnahme" in json_str

    parsed = json.loads(json_str)
    assert parsed["schema_version"] == CASEBUNDLE_SCHEMA_VERSION
    errors = validate_casebundle(parsed)
    assert errors == []


def test_export_casebundle_rejects_clear_patient_data_flag(sample_cases):
    with pytest.raises(ValueError, match="Klartext-Patientendaten ist unzulaessig"):
        export_casebundle(sample_cases, contains_clear_patient_data=True)


def test_export_casebundle_rejects_clear_name_in_patient_ref(sample_cases):
    cases_with_name = [
        {
            "case_ref": "case-bad",
            "patient_ref": "Max Mustermann",
            "icd": "I10",
            "atc": "C09AA02",
        }
    ]
    with pytest.raises(ValueError, match="Klartext-Name in patient_ref"):
        export_casebundle(cases_with_name)

    cases_with_email = [
        {
            "case_ref": "case-bad-2",
            "patient_ref": "patient@hospital.org",
            "icd": "I10",
            "atc": "C09AA02",
        }
    ]
    with pytest.raises(ValueError, match="Klartext-Name in patient_ref"):
        export_casebundle(cases_with_email)


def test_validate_casebundle_detects_malformed_structures():
    # Keine Dict-Wurzel
    assert "muss ein JSON-Objekt sein" in validate_casebundle(["not a dict"])[0]

    # Falsches Schema
    assert "Ungueltige schema_version" in validate_casebundle(
        {"schema_version": "wrong-schema-v1", "privacy": {}, "cases": []}
    )[0]

    # contains_clear_patient_data == True wird blockiert
    bad_privacy = {
        "schema_version": CASEBUNDLE_SCHEMA_VERSION,
        "privacy": {"contains_clear_patient_data": True},
        "cases": [],
    }
    assert any("contains_clear_patient_data ist True" in e for e in validate_casebundle(bad_privacy))

    # Pflichtfelder in cases fehlen
    bad_cases = {
        "schema_version": CASEBUNDLE_SCHEMA_VERSION,
        "privacy": {"contains_clear_patient_data": False},
        "cases": [{"icd": "I10"}],  # fehlt case_ref, atc
    }
    errs = validate_casebundle(bad_cases)
    assert any("case_ref" in e for e in errs)
    assert any("atc" in e for e in errs)


def test_validate_casebundle_validates_traffic_light():
    bad_traffic = {
        "schema_version": CASEBUNDLE_SCHEMA_VERSION,
        "privacy": {"contains_clear_patient_data": False},
        "cases": [
            {
                "case_ref": "case-01",
                "icd": "I10",
                "atc": "C09AA02",
                "result": {"traffic_light": "blau"},
            }
        ],
    }
    errs = validate_casebundle(bad_traffic)
    assert any("traffic_light 'blau' ungueltig" in e for e in errs)


def test_validate_casebundle_tolerant_of_unknown_fields(sample_cases):
    bundle = export_casebundle(sample_cases)
    # Fuege unbekannte Zusatzfelder ein (Vorwaertskompatibilitaet)
    bundle["custom_lab_info"] = {"some": "value"}
    bundle["cases"][0]["extra_doctor_note"] = "Toleriert"
    bundle["cases"][0]["result"]["confidence_score"] = 0.95

    errors = validate_casebundle(bundle)
    assert errors == []


def test_import_casebundle_marks_workflow_text_unverified(sample_cases):
    bundle = export_casebundle(sample_cases)
    res = import_casebundle(bundle, mark_workflow_unverified=True)

    assert res["status"] == "ok"
    assert res["case_count"] == 2
    c1 = res["cases"][0]
    assert c1["workflow"]["verified"] is False
    assert "Unüberprüfter" in c1["workflow"]["import_warning"]


def test_import_casebundle_into_target_log(tmp_path, sample_cases):
    db_path = tmp_path / "compliance.db"
    log = ComplianceLog(db_path=str(db_path))

    bundle = export_casebundle(sample_cases)
    res = import_casebundle(bundle, target_log=log)

    assert res["imported_into_log_count"] == 2
    assert len(log) == 2
    assert log.verify_chain() is True

    entries = log.all_entries()
    assert entries[0].icd == "F41"
    assert entries[0].atc == "N05BA01"
    assert entries[0].extra["source"] == "casebundle_import"
    assert entries[0].extra["case_ref"] == "case-001"


def test_export_casebundle_from_log_pseudonymizes(tmp_path):
    db_path = tmp_path / "compliance.db"
    log = ComplianceLog(db_path=str(db_path))
    # Schreibe Eintrag mit potenziell klaerungsbeduerftigem Patientennamen
    log.append(
        icd="I10",
        atc="C09AA02",
        alter=60,
        ampel="gruen",
        begruendung="Test",
        extra={"patient": "Dr. Klaus Mueller", "quelle": "KBV_PB"},
    )

    bundle = export_casebundle_from_log(log, pseudonymize=True, include_audit_chain=True)
    assert bundle["schema_version"] == CASEBUNDLE_SCHEMA_VERSION
    assert bundle["audit"]["hash_chain_exported"] is True
    assert len(bundle["audit"]["entries"]) == 1

    case_exported = bundle["cases"][0]
    # Name wurde durch Pseudonym P-0001 ersetzt
    assert case_exported["patient_ref"] == "P-0001"
    assert case_exported["result"]["source_refs"] == ["KBV_PB"]


# =============================================================================
# 2. RULESET TESTS
# =============================================================================


def test_export_ruleset_structure_and_checksums(tmp_path):
    db_path = tmp_path / "rules.db"
    conn, _ = open_database(str(db_path))
    try:
        ensure_seed_data(conn)
        ruleset = export_ruleset(conn)
    finally:
        conn.close()

    assert ruleset["schema_version"] == RULESET_SCHEMA_VERSION
    assert "source_state" in ruleset
    assert "amrl_iii" in ruleset["source_state"]

    checksums = ruleset["checksums"]
    assert checksums["algorithm"] == "sha256"
    assert len(checksums["files"]) > 0
    for f in checksums["files"]:
        assert len(f["sha256"]) == 64

    assert len(ruleset["rules"]) > 0
    assert len(ruleset["icd10"]) > 0
    assert len(ruleset["atc"]) > 0
    assert len(ruleset["praxisbesonderheiten"]) > 0
    assert len(ruleset["relations"]) > 0

    errors = validate_ruleset(ruleset)
    assert errors == []


def test_export_ruleset_json_roundtrip(tmp_path):
    db_path = tmp_path / "rules.db"
    conn, _ = open_database(str(db_path))
    try:
        ensure_seed_data(conn)
        json_str = export_ruleset_json(conn)
    finally:
        conn.close()

    assert "\ufeff" not in json_str
    parsed = json.loads(json_str)
    assert parsed["schema_version"] == RULESET_SCHEMA_VERSION
    assert validate_ruleset(parsed) == []


def test_import_ruleset_requires_confirmation(tmp_path):
    db_path = tmp_path / "rules.db"
    conn, _ = open_database(str(db_path))
    try:
        ensure_seed_data(conn)
        ruleset = export_ruleset(conn)

        target_conn, _ = open_database(str(tmp_path / "target.db"))
        try:
            with pytest.raises(ValueError, match="confirmed=True"):
                import_ruleset(ruleset, target_conn, confirmed=False)
        finally:
            target_conn.close()
    finally:
        conn.close()


def test_import_ruleset_atomic_success(tmp_path):
    db_path = tmp_path / "source.db"
    conn, _ = open_database(str(db_path))
    try:
        ensure_seed_data(conn)
        ruleset = export_ruleset(conn)
    finally:
        conn.close()

    target_path = tmp_path / "target.db"
    target_conn, _ = open_database(str(target_path))
    try:
        counts = import_ruleset(ruleset, target_conn, confirmed=True)
        assert counts["rules"] > 0
        assert counts["icd10"] > 0
        assert counts["atc"] > 0
        assert counts["praxisbesonderheiten"] > 0
        assert counts["relations"] > 0

        # Verifiziere Settings-Eintrag
        cur = target_conn.cursor()
        cur.execute("SELECT value FROM settings WHERE key='last_ruleset_schema'")
        row = cur.fetchone()
        assert row is not None
        assert row[0] == RULESET_SCHEMA_VERSION
    finally:
        target_conn.close()


def test_import_ruleset_atomic_rollback_on_failure(tmp_path):
    target_path = tmp_path / "target.db"
    target_conn, _ = open_database(str(target_path))
    try:
        ensure_seed_data(target_conn)
        initial_rules = target_conn.execute("SELECT COUNT(*) FROM regel").fetchone()[0]

        # Erstelle Ruleset mit Fehler (z.B. falsche Ampelfarbe)
        corrupted_ruleset = {
            "schema_version": RULESET_SCHEMA_VERSION,
            "source_state": {},
            "checksums": {"algorithm": "sha256", "files": []},
            "rules": [
                {
                    "kuerzel": "BAD_RULE",
                    "ampel": "lila",  # ungueltig
                }
            ],
            "icd10": [],
            "atc": [],
            "praxisbesonderheiten": [],
            "relations": [],
        }

        with pytest.raises(ValueError, match="Ruleset-Validierung fehlgeschlagen"):
            import_ruleset(corrupted_ruleset, target_conn, confirmed=True)

        # Die urspruenglichen Regeln muessen unberuehrt geblieben sein
        post_rules = target_conn.execute("SELECT COUNT(*) FROM regel").fetchone()[0]
        assert post_rules == initial_rules
    finally:
        target_conn.close()


# =============================================================================
# 3. CLI INTEGRATION TESTS
# =============================================================================


def test_cli_export_and_import_casebundle(tmp_path, sample_cases, capsys):
    cases_file = tmp_path / "input_cases.json"
    cases_file.write_text(json.dumps({"cases": sample_cases}), encoding="utf-8")

    bundle_out = tmp_path / "exported_bundle.json"

    # 1. Export CLI
    ret = main(["export-casebundle", "--cases", str(cases_file), "--out", str(bundle_out)])
    assert ret == 0
    assert bundle_out.exists()

    # 2. Import CLI (Dry-Run)
    ret = main(["import-casebundle", "--file", str(bundle_out), "--dry-run"])
    assert ret == 0
    out = capsys.readouterr().out
    assert "Casebundle-Validierung erfolgreich" in out
    assert "Dry-Run" in out


def test_cli_export_and_import_ruleset(tmp_path, capsys):
    ruleset_out = tmp_path / "exported_ruleset.json"

    # 1. Export CLI
    ret = main(["export-ruleset", "--out", str(ruleset_out)])
    assert ret == 0
    assert ruleset_out.exists()

    # 2. Import CLI ohne --confirm -> Exit 1 mit Hinweis
    ret = main(["import-ruleset", "--file", str(ruleset_out)])
    assert ret == 1
    err = capsys.readouterr().err
    assert "--confirm" in err

    # 3. Import CLI mit --confirm -> Exit 0
    target_db = tmp_path / "cli_target.db"
    ret = main(["import-ruleset", "--file", str(ruleset_out), "--db", str(target_db), "--confirm"])
    assert ret == 0
    out = capsys.readouterr().out
    assert "Ruleset erfolgreich atomar importiert" in out
