"""Tests fuer die Ampel-Engine (Evaluator)."""

import pytest

from verordnungsampel.engine.evaluator import Ampel, evaluate
from verordnungsampel.engine.rules import Quelle, Regel


@pytest.fixture
def regelsatz():
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
        Regel(
            kuerzel="PPI_GENERELL",
            atc_pattern="A02BC%",
            ampel="gelb",
            begruendung="PPI: Indikation dokumentieren",
            quelle=quelle,
        ),
        Regel(
            kuerzel="CANNABIS_VORAB",
            atc_pattern="QV12",
            ampel="gelb",
            begruendung="Cannabis: Vorab-Genehmigung erforderlich",
            container="pflicht_vorab",
            quelle=quelle,
        ),
    ]


def test_no_rules_returns_default_gruen():
    erg = evaluate("I10", "C09AA02", regeln=[])
    assert erg.gesamt is Ampel.GRUEN
    assert len(erg.treffer) == 1
    assert erg.treffer[0].regel_kuerzel == "DEFAULT_GRUEN"


def test_ace_hemmer_bei_hypertonie_ist_gruen(regelsatz):
    erg = evaluate("I10", "C09AA02", regeln=regelsatz)
    assert erg.gesamt is Ampel.GRUEN
    assert any(t.regel_kuerzel == "ACE_HYPERTONIE_OK" for t in erg.treffer)


def test_benzodiazepin_unter_65_kein_priscus_treffer(regelsatz):
    erg = evaluate("F32.1", "N05BA01", alter=40, regeln=regelsatz)
    # Keine Regel greift -> default gruen
    assert erg.gesamt is Ampel.GRUEN


def test_benzodiazepin_ueber_65_priscus_rot(regelsatz):
    erg = evaluate("F32.1", "N05BA01", alter=70, regeln=regelsatz)
    assert erg.gesamt is Ampel.ROT
    assert any(t.regel_kuerzel == "PRISCUS_BENZO_65" for t in erg.treffer)


def test_ppi_loest_gelb_aus(regelsatz):
    erg = evaluate("K21.0", "A02BC02", regeln=regelsatz)
    assert erg.gesamt is Ampel.GELB
    assert any(t.regel_kuerzel == "PPI_GENERELL" for t in erg.treffer)


def test_cannabis_setzt_container_hinweis(regelsatz):
    erg = evaluate("R52.1", "QV12", regeln=regelsatz)
    assert "pflicht_vorab" in erg.container_hinweise


def test_schaerfste_ampel_gewinnt():
    quelle = Quelle(kuerzel="X", titel="X")
    regeln = [
        Regel(kuerzel="GRUEN_REGEL", atc_pattern="X%", ampel="gruen", begruendung="g", quelle=quelle),
        Regel(kuerzel="GELB_REGEL",  atc_pattern="X%", ampel="gelb",  begruendung="y", quelle=quelle),
        Regel(kuerzel="ROT_REGEL",   atc_pattern="X%", ampel="rot",   begruendung="r", quelle=quelle),
    ]
    erg = evaluate("I10", "X123", regeln=regeln)
    assert erg.gesamt is Ampel.ROT
    assert len(erg.treffer) == 3


def test_to_dict_serialisierbar(regelsatz):
    erg = evaluate("I10", "C09AA02", regeln=regelsatz)
    d = erg.to_dict()
    assert d["gesamt"] == "gruen"
    assert d["icd"] == "I10"
    assert d["atc"] == "C09AA02"
