"""Tests fuer Coverage-Analyse des Ampel-Regelwerks."""

from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from verordnungsampel.engine.coverage import (
    CoverageCase,
    CoverageReport,
    analyze_cases,
    normalize_cases,
)
from verordnungsampel.engine.rules import Quelle, Regel


@pytest.fixture
def coverage_rules() -> list[Regel]:
    quelle = Quelle(kuerzel="TEST", titel="Test-Quelle")
    return [
        Regel(
            kuerzel="ACE_HYPERTONIE_OK",
            atc_pattern="C09AA%",
            icd_pattern="I10",
            ampel="gruen",
            begruendung="ACE-Hemmer bei Hypertonie",
            quelle=quelle,
        ),
        Regel(
            kuerzel="PRISCUS_BENZO_65",
            atc_pattern="N05BA%",
            altersgrenze=65,
            ampel="rot",
            begruendung="Benzodiazepine bei aelteren Patienten",
            quelle=quelle,
        ),
    ]


def test_coverage_zaehlt_nur_echte_regeltreffer(coverage_rules: list[Regel]) -> None:
    report = analyze_cases(
        [
            CoverageCase(case_id="explizit-gruen", icd="I10", atc="C09AA02"),
            CoverageCase(case_id="explizit-rot", icd="F32.1", atc="N05BA01", alter=70),
            CoverageCase(case_id="default-gruen", icd="X99", atc="Z99"),
        ],
        regeln=coverage_rules,
    )

    assert report.total == 3
    assert report.explained_count == 2
    assert report.unexplained_count == 1
    assert report.coverage_ratio == pytest.approx(2 / 3)
    assert report.by_ampel == {"rot": 1, "gelb": 0, "gruen": 2}
    assert report.rule_hits == {
        "ACE_HYPERTONIE_OK": 1,
        "PRISCUS_BENZO_65": 1,
    }
    assert report.unexplained_cases[0].case_id == "default-gruen"


def test_coverage_report_json_serialisierbar(coverage_rules: list[Regel]) -> None:
    report = analyze_cases(
        [{"id": "fall-1", "icd": "I10", "atc": "C09AA02"}],
        regeln=coverage_rules,
    )

    data = report.to_dict()
    assert data["metric"] == "C(S)=explained/total"
    assert data["coverage_percent"] == 100.0
    assert data["results"][0]["explained"] is True
    json.dumps(data, ensure_ascii=False)


def test_normalize_cases_validiert_pflichtfelder() -> None:
    with pytest.raises(ValueError):
        normalize_cases([{"icd": "I10"}])

    with pytest.raises(TypeError):
        normalize_cases([object()])


def test_empty_report_hat_coverage_null() -> None:
    report = CoverageReport()
    assert report.total == 0
    assert report.coverage_ratio == 0.0
    assert report.to_dict()["coverage_percent"] == 0.0


def _run_cli(argv: list[str]) -> tuple[int, str]:
    from verordnungsampel.cli.main import main

    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = main(argv)
    return rc, buf.getvalue()


def test_cli_coverage_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("APPDATA", str(tmp_path / "appdata"))
    _run_cli(["init"])

    cases_path = tmp_path / "coverage_cases.json"
    cases_path.write_text(
        json.dumps(
            [
                {"id": "bekannt", "icd": "I10", "atc": "C09AA02"},
                {"id": "unbekannt", "icd": "X99", "atc": "Z99"},
            ]
        ),
        encoding="utf-8",
    )

    rc, out = _run_cli(["coverage", "--cases", str(cases_path), "--json"])

    assert rc == 0
    data = json.loads(out)
    assert data["total"] == 2
    assert data["explained"] == 1
    assert data["unexplained"] == 1
    assert data["unexplained_cases"][0]["id"] == "unbekannt"


def test_cli_coverage_invalid_file(capsys: pytest.CaptureFixture) -> None:
    from verordnungsampel.cli.main import main

    rc = main(["coverage", "--cases", "does-not-exist.json"])

    assert rc == 2
    assert "Coverage-Faelle konnten nicht geladen werden" in capsys.readouterr().err
