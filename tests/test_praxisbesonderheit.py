"""Tests fuer das Praxisbesonderheiten-Modul (Funktion 4)."""

from __future__ import annotations

from datetime import date

import pytest

from verordnungsampel.engine.praxisbesonderheit import (
    Praxisbesonderheit,
    build_quartal_reminder,
    find_matching,
    is_valid_at,
    parse_quartal,
    render_reminder,
)
from verordnungsampel.engine.rules import Quelle


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def quelle():
    return Quelle(kuerzel="GKV_SV_PB", titel="GKV-SV Praxisbesonderheiten")


@pytest.fixture
def pbs(quelle):
    """Kleine Beispiel-Liste fuer Tests."""
    return [
        Praxisbesonderheit(
            id=1,
            atc_pattern="L03AB%",
            icd_pattern="G35",
            bezeichnung="MS-Therapie",
            gueltig_ab="2024-01-01",
            gueltig_bis=None,
            quelle=quelle,
        ),
        Praxisbesonderheit(
            id=2,
            atc_pattern="QV12",
            icd_pattern="R52.1",
            bezeichnung="Cannabis Schmerz",
            gueltig_ab="2024-01-01",
            gueltig_bis=None,
            quelle=quelle,
        ),
        Praxisbesonderheit(
            id=3,
            atc_pattern="L01XC03",
            icd_pattern="C50%",
            bezeichnung="Trastuzumab Mamma-Ca",
            gueltig_ab="2023-01-01",
            gueltig_bis="2025-12-31",  # abgelaufen ab 2026
            quelle=quelle,
        ),
        Praxisbesonderheit(
            id=4,
            atc_pattern="A10BJ%",
            icd_pattern=None,  # icd_pattern optional -> matched alles
            bezeichnung="GLP-1 bei Diabetes",
            gueltig_ab=None,
            gueltig_bis=None,
            quelle=quelle,
        ),
    ]


# ---------------------------------------------------------------------------
# is_valid_at
# ---------------------------------------------------------------------------


class TestIsValidAt:
    def test_innerhalb_gueltigkeit(self, pbs):
        assert is_valid_at(pbs[0], date(2026, 4, 8)) is True

    def test_vor_gueltig_ab(self, pbs):
        assert is_valid_at(pbs[0], date(2023, 12, 31)) is False

    def test_nach_gueltig_bis(self, pbs):
        assert is_valid_at(pbs[2], date(2026, 1, 1)) is False

    def test_none_grenzen_sind_offen(self, pbs):
        # pb[3] hat weder gueltig_ab noch gueltig_bis
        assert is_valid_at(pbs[3], date(1900, 1, 1)) is True
        assert is_valid_at(pbs[3], date(9999, 12, 31)) is True


# ---------------------------------------------------------------------------
# find_matching
# ---------------------------------------------------------------------------


class TestFindMatching:
    def test_ms_therapie_matcht_bei_g35_l03ab07(self, pbs):
        matches = find_matching("G35", "L03AB07", pbs=pbs, stichtag=date(2026, 4, 8))
        assert len(matches) == 1
        assert matches[0].bezeichnung == "MS-Therapie"

    def test_falsche_diagnose_matcht_nicht(self, pbs):
        matches = find_matching("I10", "L03AB07", pbs=pbs, stichtag=date(2026, 4, 8))
        assert matches == []

    def test_atc_pattern_wildcard(self, pbs):
        matches = find_matching("G35", "L03AB01", pbs=pbs, stichtag=date(2026, 4, 8))
        assert len(matches) == 1

    def test_abgelaufene_pb_wird_nicht_geliefert(self, pbs):
        matches = find_matching(
            "C50.1", "L01XC03", pbs=pbs, stichtag=date(2026, 4, 8)
        )
        assert matches == []

    def test_abgelaufene_pb_vor_ablauf_matcht(self, pbs):
        matches = find_matching(
            "C50.1", "L01XC03", pbs=pbs, stichtag=date(2024, 6, 15)
        )
        assert len(matches) == 1
        assert matches[0].bezeichnung == "Trastuzumab Mamma-Ca"

    def test_pb_ohne_icd_pattern_matcht_jede_diagnose(self, pbs):
        m1 = find_matching("E11.9", "A10BJ06", pbs=pbs)
        m2 = find_matching("I10", "A10BJ06", pbs=pbs)
        assert len(m1) == 1 and m1[0].bezeichnung == "GLP-1 bei Diabetes"
        assert len(m2) == 1


# ---------------------------------------------------------------------------
# parse_quartal
# ---------------------------------------------------------------------------


class TestParseQuartal:
    @pytest.mark.parametrize(
        "spec,start,ende",
        [
            ("2026-Q1", date(2026, 1, 1), date(2026, 3, 31)),
            ("2026-Q2", date(2026, 4, 1), date(2026, 6, 30)),
            ("2026-Q3", date(2026, 7, 1), date(2026, 9, 30)),
            ("2026-Q4", date(2026, 10, 1), date(2026, 12, 31)),
        ],
    )
    def test_valide_quartale(self, spec, start, ende):
        s, e, label = parse_quartal(spec)
        assert s == start
        assert e == ende
        assert label == spec

    @pytest.mark.parametrize("spec", ["2026-Q5", "2026-Q0", "26-Q1", "2026Q2", "bla"])
    def test_ungueltige_eingabe_wirft(self, spec):
        with pytest.raises(ValueError):
            parse_quartal(spec)


# ---------------------------------------------------------------------------
# build_quartal_reminder
# ---------------------------------------------------------------------------


def _log_entry(
    seq: int,
    timestamp: str,
    icd: str,
    atc: str,
    ampel: str = "gelb",
    pbs_extra=None,
):
    """Hilft beim Bau von Compliance-Log-Dicts wie aus LogEintrag.to_dict()."""
    extra = {}
    if pbs_extra:
        extra["praxisbesonderheiten"] = pbs_extra
    return {
        "seq": seq,
        "timestamp": timestamp,
        "icd": icd,
        "atc": atc,
        "ampel": ampel,
        "extra": extra,
    }


class TestBuildQuartalReminder:
    def test_leerer_log_liefert_leeren_reminder(self):
        reminder = build_quartal_reminder([], "2026-Q2")
        assert reminder.anzahl == 0
        assert reminder.quartal == "2026-Q2"

    def test_filtert_nach_quartal(self):
        entries = [
            _log_entry(
                1, "2026-03-15T10:00:00+00:00", "G35", "L03AB07",
                pbs_extra=[{"id": 1, "bezeichnung": "MS"}],
            ),
            _log_entry(
                2, "2026-04-10T10:00:00+00:00", "G35", "L03AB07",
                pbs_extra=[{"id": 1, "bezeichnung": "MS"}],
            ),
            _log_entry(
                3, "2026-06-30T23:59:59+00:00", "R52.1", "QV12",
                pbs_extra=[{"id": 2, "bezeichnung": "Cannabis"}],
            ),
            _log_entry(
                4, "2026-07-01T00:00:00+00:00", "G35", "L03AB07",
                pbs_extra=[{"id": 1, "bezeichnung": "MS"}],
            ),
        ]
        reminder = build_quartal_reminder(entries, "2026-Q2")
        assert reminder.anzahl == 2
        assert [e["seq"] for e in reminder.eintraege] == [2, 3]

    def test_ignoriert_eintraege_ohne_pb(self):
        entries = [
            _log_entry(1, "2026-04-10T10:00:00+00:00", "I10", "C09AA02"),  # kein pb
            _log_entry(
                2, "2026-04-15T10:00:00+00:00", "G35", "L03AB07",
                pbs_extra=[{"id": 1, "bezeichnung": "MS"}],
            ),
        ]
        reminder = build_quartal_reminder(entries, "2026-Q2")
        assert reminder.anzahl == 1
        assert reminder.eintraege[0]["seq"] == 2

    def test_render_enthaelt_header_und_hinweise(self):
        entries = [
            _log_entry(
                1, "2026-05-01T12:00:00+00:00", "G35", "L03AB07",
                pbs_extra=[{"id": 1, "bezeichnung": "MS-Therapie"}],
            ),
        ]
        reminder = build_quartal_reminder(entries, "2026-Q2")
        txt = render_reminder(reminder)
        assert "QUARTALS-REMINDER" in txt
        assert "2026-Q2" in txt
        assert "MS-Therapie" in txt
        assert "KV-Kennziffer" in txt

    def test_render_leer_enthaelt_keine_eintraege_hinweis(self):
        reminder = build_quartal_reminder([], "2026-Q1")
        txt = render_reminder(reminder)
        assert "Keine Verordnungen" in txt

    def test_to_dict_roundtrip(self):
        entries = [
            _log_entry(
                1, "2026-04-10T10:00:00+00:00", "G35", "L03AB07",
                pbs_extra=[{"id": 1, "bezeichnung": "MS"}],
            ),
        ]
        d = build_quartal_reminder(entries, "2026-Q2").to_dict()
        assert d["quartal"] == "2026-Q2"
        assert d["anzahl"] == 1
        assert d["start"] == "2026-04-01"
        assert d["ende"] == "2026-06-30"
        assert len(d["eintraege"]) == 1


# ---------------------------------------------------------------------------
# Praxisbesonderheit.to_dict
# ---------------------------------------------------------------------------


class TestPraxisbesonderheitToDict:
    def test_to_dict_mit_quelle(self, pbs):
        d = pbs[0].to_dict()
        assert d["id"] == 1
        assert d["bezeichnung"] == "MS-Therapie"
        assert d["quelle"] is not None
        assert d["quelle"]["kuerzel"] == "GKV_SV_PB"

    def test_to_dict_ohne_quelle(self):
        pb = Praxisbesonderheit(
            id=99,
            atc_pattern="X",
            icd_pattern=None,
            bezeichnung="Test",
            gueltig_ab=None,
            gueltig_bis=None,
            quelle=None,
        )
        d = pb.to_dict()
        assert d["quelle"] is None
