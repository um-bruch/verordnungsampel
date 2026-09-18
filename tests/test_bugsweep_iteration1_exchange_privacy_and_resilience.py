"""Regressionstests fuer Bugsweep-Iteration 1 (Exchange-Datenschutz & Resilienz).

Befunde:
1. PII-Leck: _CLEARNAME_PATTERN erkannte keine durch Komma getrennten Namen (z.B.
   'Mueller, Hans' oder 'Müller, Hans'), wodurch Klartext-Patientendaten unbemerkt
   exportiert, validiert und nicht pseudonymisiert wurden.
2. Resilienz: export_casebundle stuerzte mit AttributeError ab, wenn result,
   justification oder workflow None waren, oder mit TypeError bei None-Listen.
3. Schema-Kompatibilitaet: import_casebundle verlor das Alter bei Faellen, die gemaess
   EXPORTFORMAT.md das Feld 'age_years' statt 'alter' nutzen.
"""

from __future__ import annotations

import pytest

from verordnungsampel import (
    CASEBUNDLE_SCHEMA_VERSION,
    export_casebundle,
    export_casebundle_from_log,
    import_casebundle,
    validate_casebundle,
)
from verordnungsampel.audit.compliance_log import ComplianceLog
from verordnungsampel.exchange import _CLEARNAME_PATTERN


def test_clearname_pattern_detects_comma_separated_names():
    """Prueft, dass _CLEARNAME_PATTERN sowohl 'Vorname Nachname' als auch 'Nachname, Vorname' erkennt."""
    assert _CLEARNAME_PATTERN.search("Max Mustermann")
    assert _CLEARNAME_PATTERN.search("Mueller, Hans")
    assert _CLEARNAME_PATTERN.search("Müller, Hans")
    assert _CLEARNAME_PATTERN.search("Müller,Hans")
    assert _CLEARNAME_PATTERN.search("Dr. Klaus Mueller")
    assert _CLEARNAME_PATTERN.search("Frau Schmidt")
    assert _CLEARNAME_PATTERN.search("patient@klinik.de")

    # Pseudonyme duerfen nicht anschlagen
    assert not _CLEARNAME_PATTERN.search("P-101")
    assert not _CLEARNAME_PATTERN.search("P-0042")
    assert not _CLEARNAME_PATTERN.search("CASE-99")
    assert not _CLEARNAME_PATTERN.search("PAT_4711")
    assert not _CLEARNAME_PATTERN.search("anon-123")


def test_export_casebundle_rejects_comma_separated_patient_name():
    """export_casebundle muss bei 'Nachname, Vorname' ValueError werfen."""
    cases = [
        {
            "case_ref": "c-01",
            "patient_ref": "Mueller, Hans",
            "icd": "I10",
            "atc": "C09AA02",
        }
    ]
    with pytest.raises(ValueError, match="Klartext-Name in patient_ref"):
        export_casebundle(cases)


def test_validate_casebundle_detects_comma_separated_patient_name():
    """validate_casebundle muss bei 'Nachname, Vorname' Validierungsfehler melden."""
    bundle = {
        "schema_version": CASEBUNDLE_SCHEMA_VERSION,
        "privacy": {"contains_clear_patient_data": False},
        "cases": [
            {
                "case_ref": "c-01",
                "patient_ref": "Schmidt, Klaus",
                "icd": "I10",
                "atc": "C09AA02",
            }
        ],
    }
    errors = validate_casebundle(bundle)
    assert any("Klartext-Muster in 'patient_ref'" in e for e in errors)


def test_export_casebundle_from_log_pseudonymizes_comma_separated_patient_name(tmp_path):
    """export_casebundle_from_log muss 'Nachname, Vorname' pseudonymisieren."""
    db_path = tmp_path / "compliance.db"
    log = ComplianceLog(db_path=str(db_path))
    log.append(
        icd="I10",
        atc="C09AA02",
        alter=65,
        ampel="gruen",
        begruendung="Routine",
        extra={"patient": "Müller, Erika"},
    )

    bundle = export_casebundle_from_log(log, pseudonymize=True)
    c0 = bundle["cases"][0]
    assert c0["patient_ref"] == "P-0001"
    assert "Müller" not in str(c0)


def test_export_casebundle_handles_none_values_resiliently():
    """export_casebundle darf bei None-Werten in verschachtelten Feldern nicht abstuerzen."""
    cases = [
        {
            "case_ref": "c-none-01",
            "patient_ref": "P-1234",
            "icd": "I10",
            "atc": "C09AA02",
            "result": None,
            "justification": None,
            "workflow": None,
        },
        {
            "case_ref": "c-none-02",
            "patient_ref": "P-5678",
            "icd": "K21.0",
            "atc": "A02BC02",
            "result": {"traffic_light": None, "matched_rules": None, "source_refs": None},
            "justification": {"status": None, "steps": None},
            "workflow": {"type": None, "text": None},
        },
    ]

    bundle = export_casebundle(cases)
    assert len(bundle["cases"]) == 2
    c1 = bundle["cases"][0]
    assert c1["result"]["traffic_light"] == "gruen"
    assert c1["result"]["matched_rules"] == []
    assert c1["justification"]["status"] == "not_applicable"
    assert c1["workflow"]["type"] == "keine_aktion"

    c2 = bundle["cases"][1]
    assert c2["result"]["traffic_light"] == "gruen"
    assert c2["result"]["matched_rules"] == []
    assert c2["justification"]["status"] == "not_applicable"
    assert c2["workflow"]["type"] == "keine_aktion"


def test_import_casebundle_preserves_age_years_from_exportformat(tmp_path):
    """import_casebundle muss das Alter auch uebernehmen, wenn es gemaess EXPORTFORMAT.md 'age_years' heisst."""
    db_path = tmp_path / "compliance.db"
    log = ComplianceLog(db_path=str(db_path))

    bundle = {
        "schema_version": CASEBUNDLE_SCHEMA_VERSION,
        "privacy": {"contains_clear_patient_data": False},
        "cases": [
            {
                "case_ref": "case-format-01",
                "patient_ref": "P-4711",
                "icd": "F41",
                "atc": "N05BA01",
                "age_years": 72,  # Feldname aus EXPORTFORMAT.md
                "result": {"traffic_light": "rot"},
            }
        ],
    }

    res = import_casebundle(bundle, target_log=log)
    assert res["imported_into_log_count"] == 1

    entries = log.all_entries()
    assert len(entries) == 1
    assert entries[0].alter == 72
