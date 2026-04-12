"""Tests fuer DB-Schema, Seed-Loader und DB-basierte Auswertung."""

from pathlib import Path

import pytest

from verordnungsampel.db.connection import open_database, open_in_memory
from verordnungsampel.db.schema import get_setting, save_setting, schema_version
from verordnungsampel.db.seed import load_seed_data
from verordnungsampel.engine.evaluator import Ampel, evaluate


def test_schema_version_aktuell():
    assert schema_version() == 1


def test_in_memory_schema_anlegt():
    conn = open_in_memory()
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = {row[0] for row in cur.fetchall()}
    expected = {
        "amrl_anlage",
        "atc",
        "icd10",
        "praxisbesonderheit",
        "quelle",
        "regel",
        "settings",
    }
    assert expected.issubset(tables)


def test_settings_upsert():
    conn = open_in_memory()
    save_setting(conn, "warn_days", "14")
    assert get_setting(conn, "warn_days") == "14"
    save_setting(conn, "warn_days", "21")
    assert get_setting(conn, "warn_days") == "21"


def test_open_database_in_tempdir(tmp_path: Path):
    db_path = tmp_path / "regelwerk.db"
    conn, used = open_database(db_path)
    assert used == db_path
    assert db_path.exists()
    conn.close()


def test_seed_laden_mit_default_pfad():
    """Laedt die echten Seed-Dateien aus data/seed/."""
    conn = open_in_memory()
    counts = load_seed_data(conn)
    assert counts["quelle"] > 0
    assert counts["regel"] > 0
    assert counts["amrl_anlage"] > 0


def test_evaluate_ueber_db_priscus_benzo():
    conn = open_in_memory()
    load_seed_data(conn)
    # Diazepam (N05BA01) bei 70-Jaehrigem -> rot via PRISCUS
    erg = evaluate("F32.1", "N05BA01", alter=70, conn=conn)
    assert erg.gesamt is Ampel.ROT
    assert any("PRISCUS" in t.regel_kuerzel for t in erg.treffer)


def test_evaluate_ueber_db_ace_hypertonie_gruen():
    conn = open_in_memory()
    load_seed_data(conn)
    erg = evaluate("I10", "C09AA02", conn=conn)
    assert erg.gesamt is Ampel.GRUEN


def test_evaluate_ueber_db_ppi_ohne_indikation_gelb():
    conn = open_in_memory()
    load_seed_data(conn)
    erg = evaluate("M54.5", "A02BC02", conn=conn)
    # PPI ohne K21 -> mindestens gelb durch PPI_KEINE_REFLUX_HINT/AM-RL Anlage III
    assert erg.gesamt in (Ampel.GELB, Ampel.ROT)
