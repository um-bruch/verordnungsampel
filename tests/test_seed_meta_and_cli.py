"""Tests fuer den neuen _meta-Block im Seed-Loader und die CLI-Befehle
`sources` und `rules`.
"""

from __future__ import annotations

import io
import json
import sqlite3
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from verordnungsampel.db.connection import open_in_memory
from verordnungsampel.db.seed import (
    _load_json,
    ensure_seed_data,
    get_last_meta,
    load_meta_only,
    load_seed_data,
)


# ---------------------------------------------------------------------------
# Loader: neues Format vs. Legacy
# ---------------------------------------------------------------------------


def test_load_json_neues_format(tmp_path: Path) -> None:
    """Der Loader akzeptiert {_meta, eintraege}-Format und liefert Liste."""
    path = tmp_path / "amrl_anlage_X.json"
    path.write_text(json.dumps({
        "_meta": {"anlage": "X", "stand": "2025-01-01", "eintraege_anzahl": 1},
        "eintraege": [
            {"anlage": "X", "atc_pattern": "A%", "ampel": "rot",
             "begruendung": "test", "bedingung": "test"},
        ],
    }), encoding="utf-8")
    result = _load_json(path)
    assert isinstance(result, list)
    assert len(result) == 1
    # Meta muss im Cache liegen
    meta = get_last_meta()
    assert path.name in meta
    assert meta[path.name]["anlage"] == "X"


def test_load_json_legacy_liste(tmp_path: Path) -> None:
    """Loader akzeptiert flache Liste (Legacy-Format, vor Seed-Version 1.0.0)."""
    path = tmp_path / "legacy.json"
    path.write_text(json.dumps([
        {"anlage": "III", "atc_pattern": "B%", "ampel": "gelb",
         "begruendung": "x", "bedingung": "x"},
    ]), encoding="utf-8")
    result = _load_json(path)
    assert isinstance(result, list)
    assert len(result) == 1


def test_load_json_unbekanntes_format(tmp_path: Path) -> None:
    """Integer o.ae. -> None + Warning."""
    path = tmp_path / "broken.json"
    path.write_text("42", encoding="utf-8")
    result = _load_json(path)
    assert result is None


# ---------------------------------------------------------------------------
# Seed-Laden mit echten Dateien
# ---------------------------------------------------------------------------


def test_load_seed_fuellt_meta_cache() -> None:
    """Nach load_seed_data() sind fuer die 4 Anlagen _meta-Eintraege da."""
    conn = open_in_memory()
    counts = load_seed_data(conn)
    assert counts["amrl_anlage"] == 129  # 56 + 21 + 36 + 16
    meta = get_last_meta()
    for fname in ("amrl_anlage_III.json", "amrl_anlage_V.json",
                  "amrl_anlage_VI_A.json", "amrl_anlage_VI_B.json"):
        assert fname in meta, f"_meta fehlt fuer {fname}"
        assert meta[fname]["stand"], f"stand-Datum fehlt in {fname}"
        assert meta[fname]["eintraege_anzahl"] > 0


def test_load_seed_persistiert_meta_in_settings() -> None:
    """seed_meta_json liegt nach init in der settings-Tabelle."""
    conn = open_in_memory()
    load_seed_data(conn)
    row = conn.execute(
        "SELECT value FROM settings WHERE key='seed_meta_json'"
    ).fetchone()
    assert row is not None
    meta = json.loads(row[0])
    assert "amrl_anlage_III.json" in meta
    last_init = conn.execute(
        "SELECT value FROM settings WHERE key='last_init'"
    ).fetchone()
    assert last_init is not None


def test_load_seed_idempotent() -> None:
    """Mehrfaches Laden liefert identische Zahlen (DELETE+INSERT)."""
    conn = open_in_memory()
    c1 = load_seed_data(conn)
    c2 = load_seed_data(conn)
    assert c1["amrl_anlage"] == c2["amrl_anlage"] == 129


def test_ensure_seed_data_laedt_frische_db_genau_einmal() -> None:
    """Fresh DBs werden automatisch befuellt, spaetere Aufrufe bleiben no-op."""
    conn = open_in_memory()
    loaded = ensure_seed_data(conn)
    assert loaded is not None
    assert loaded["regel"] == 10
    assert ensure_seed_data(conn) is None


def test_load_meta_only_liest_ohne_db() -> None:
    """load_meta_only liest frisch von Platte, unabhaengig von der DB."""
    meta = load_meta_only()
    assert "amrl_anlage_III.json" in meta
    assert meta["amrl_anlage_III.json"]["stand"] == "2025-10-09"
    assert meta["amrl_anlage_V.json"]["stand"] == "2026-03-24"


# ---------------------------------------------------------------------------
# CLI-Befehle: sources / rules
# ---------------------------------------------------------------------------


def _run_cli(argv: list[str]) -> tuple[int, str]:
    """Fuehrt `verordnungsampel.cli.main` aus und sammelt stdout."""
    from verordnungsampel.cli.main import main
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = main(argv)
    return rc, buf.getvalue()


def test_cli_sources_text(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`sources` zeigt alle 4 Anlagen mit Stand und Eintragszahlen."""
    # DB ins tmp_path umlenken
    monkeypatch.setenv("APPDATA", str(tmp_path))
    _run_cli(["init"])  # vorheriges init, damit settings gefuellt ist
    rc, out = _run_cli(["sources"])
    assert rc == 0
    assert "AM-RL Anlage III" in out
    assert "2025-10-09" in out
    assert "AM-RL Anlage V" in out
    assert "2026-03-24" in out
    assert "AM-RL Anlage VI-A" in out
    assert "AM-RL Anlage VI-B" in out
    assert "56" in out  # III
    assert "21" in out  # V


def test_cli_sources_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`sources --json` liefert parsebares JSON mit allen Feldern."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    _run_cli(["init"])
    rc, out = _run_cli(["sources", "--json"])
    assert rc == 0
    data = json.loads(out)
    assert len(data["anlagen"]) == 4
    for a in data["anlagen"]:
        assert "stand" in a
        assert "extraktion_datum" in a


def test_cli_status_alias(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`status` funktioniert als Alias fuer `sources`."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    _run_cli(["init"])
    rc, out = _run_cli(["status"])
    assert rc == 0
    assert "AM-RL Anlage III" in out


def test_cli_rules_anlage_III(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`rules --anlage III` listet alle 56 Einteige."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    _run_cli(["init"])
    rc, out = _run_cli(["rules", "--anlage", "III"])
    assert rc == 0
    assert "56 Treffer" in out


def test_cli_rules_filter_ampel(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`rules --anlage III --ampel ROT` filtert korrekt."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    _run_cli(["init"])
    rc, out = _run_cli(["rules", "--anlage", "III", "--ampel", "ROT"])
    assert rc == 0
    # Weniger als 56 Treffer, aber mindestens einer
    assert "Treffer" in out
    assert "ROT" in out


def test_cli_rules_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`rules --output json` gibt parsebares JSON aus."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    _run_cli(["init"])
    rc, out = _run_cli(["rules", "--anlage", "V", "--output", "json"])
    assert rc == 0
    data = json.loads(out)
    assert isinstance(data, list)
    assert len(data) == 21
    for r in data:
        assert r["anlage"] == "V"


def test_cli_rules_invalid_anlage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    """Unbekannte Anlage -> Exit 2."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    _run_cli(["init"])
    from verordnungsampel.cli.main import main
    rc = main(["rules", "--anlage", "UNSINN"])
    assert rc == 2


def test_cli_rules_atc_filter(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`--atc A10` findet nur A10-Eintraege."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    _run_cli(["init"])
    rc, out = _run_cli([
        "rules", "--anlage", "alle", "--atc", "A10", "--output", "json"
    ])
    assert rc == 0
    data = json.loads(out)
    for r in data:
        assert r["atc_pattern"].startswith("A10")


def test_cli_check_seedet_frische_installation_automatisch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`check` darf vor dem ersten `init` kein false-green mit leerer DB liefern."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    rc, out = _run_cli([
        "check",
        "--icd",
        "F41",
        "--atc",
        "N05BA01",
        "--alter",
        "72",
        "--json",
        "--no-log",
    ])
    assert rc == 0
    data = json.loads(out)
    assert data["gesamt"] == "rot"
    assert data["treffer"][0]["regel"] == "PRISCUS_BENZO_AELTER65"


def test_cli_workflow_seedet_frische_installation_automatisch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`workflow` soll dokumentierte Container-Treffer auch ohne `init` liefern."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    rc, out = _run_cli([
        "workflow",
        "--icd",
        "R52.1",
        "--atc",
        "QV12",
        "--kk",
        "AOK",
        "--praxis",
        "Praxis X",
        "--json",
        "--no-log",
    ])
    assert rc == 0
    data = json.loads(out)
    assert data["workflow_type"] == "pflicht_antrag"
    assert data["containers"] == ["pflicht_vorab"]
