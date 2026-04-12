"""Tests fuer die HSM-basierte Begruendungspflicht.

Testaufbau:
    - Synthetische AmpelErgebnisse (GRUEN/GELB/ROT mit Containern)
    - Non-interactive Laeufe via JustificationAnswers-Dict
    - Integrationstest mit ComplianceLog (Hash-Chain darf nicht brechen)
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from verordnungsampel.audit.compliance_log import ComplianceLog
from verordnungsampel.engine.evaluator import (
    Ampel,
    AmpelErgebnis,
    Treffer,
)
from verordnungsampel.engine.justification_fsm import (
    CONTAINER_OFF_LABEL,
    CONTAINER_VERBOTEN_VORAB,
    STEPS,
    Justification,
    JustificationAnswers,
    JustificationError,
    JustificationFSM,
    JustificationState,
    required_steps_for,
)


# ---------------------------------------------------------------------------
# Fixtures (synthetische Ampelergebnisse)
# ---------------------------------------------------------------------------


def _make_ergebnis(
    ampel: Ampel,
    *,
    container: str | None = None,
    icd: str = "F41",
    atc: str = "N05BA01",
    alter: int | None = None,
) -> AmpelErgebnis:
    """Baut ein AmpelErgebnis manuell (ohne DB/Evaluator-Roundtrip)."""
    treffer = [
        Treffer(
            regel_kuerzel="TEST",
            ampel=ampel,
            begruendung=f"Testregel mit {ampel.value}",
            container=container,
        )
    ]
    return AmpelErgebnis(
        icd=icd, atc=atc, alter=alter, gesamt=ampel, treffer=treffer
    )


@pytest.fixture
def ergebnis_gruen():
    return _make_ergebnis(Ampel.GRUEN)


@pytest.fixture
def ergebnis_gelb():
    return _make_ergebnis(Ampel.GELB, icd="K21.0", atc="A02BC02")


@pytest.fixture
def ergebnis_rot():
    return _make_ergebnis(Ampel.ROT, alter=72)


@pytest.fixture
def ergebnis_rot_off_label():
    return _make_ergebnis(
        Ampel.ROT, container=CONTAINER_OFF_LABEL, icd="C50", atc="L01XC03"
    )


@pytest.fixture
def valid_rot_answers() -> JustificationAnswers:
    return JustificationAnswers(
        {
            "diagnose": "Panikstoerung mit chronischen Schlafstoerungen (F41.0)",
            "vorbehandlung": "SSRI Sertralin 100mg, 8 Wochen, Schlafhygiene-Beratung",
            "therapieversagen": "SSRI-Wirkung unzureichend, Alternativen kontraindiziert wegen QTc-Verlaengerung",
            "praxisbesonderheit": "Geriatrischer Schwerpunkt der Praxis",
            "confirm": True,
        }
    )


@pytest.fixture
def valid_off_label_answers() -> JustificationAnswers:
    return JustificationAnswers(
        {
            "diagnose": "Metastasiertes Mammakarzinom, HER2-positiv, Stadium IV",
            "vorbehandlung": "Trastuzumab first line, Pertuzumab second line, beide progredient",
            "therapieversagen": "Tumor progredient trotz zweier Linien, keine weiteren zugelassenen Optionen",
            "bsg_off_label": {
                "schwerwiegende_erkrankung": "Fortgeschrittenes metastasiertes Karzinom mit eingeschraenkter Lebenserwartung",
                "keine_alternative": "Keine zugelassene Therapie verfuegbar, Studien nicht zugaenglich",
                "begruendete_erfolgsaussicht": "Phase-II-Daten zeigen Ansprechen in 40 Prozent der Faelle",
            },
            "praxisbesonderheit": "Onkologischer Schwerpunkt",
            "confirm": True,
        }
    )


# ---------------------------------------------------------------------------
# required_steps_for
# ---------------------------------------------------------------------------


class TestRequiredSteps:
    def test_gruen_braucht_keine_schritte(self, ergebnis_gruen):
        assert required_steps_for(ergebnis_gruen) == []

    def test_gelb_braucht_diagnose_vorbehandlung_confirm(self, ergebnis_gelb):
        states = required_steps_for(ergebnis_gelb)
        assert states == [
            JustificationState.DIAGNOSE,
            JustificationState.VORBEHANDLUNG,
            JustificationState.CONFIRM,
        ]

    def test_rot_braucht_therapieversagen_und_praxisbesonderheit(self, ergebnis_rot):
        states = required_steps_for(ergebnis_rot)
        assert JustificationState.THERAPIEVERSAGEN in states
        assert JustificationState.PRAXISBESONDERHEIT in states
        assert JustificationState.BSG_OFF_LABEL not in states

    def test_rot_off_label_fuegt_bsg_schritt_hinzu(self, ergebnis_rot_off_label):
        states = required_steps_for(ergebnis_rot_off_label)
        assert JustificationState.BSG_OFF_LABEL in states
        # Reihenfolge: therapieversagen kommt vor bsg_off_label
        idx_tv = states.index(JustificationState.THERAPIEVERSAGEN)
        idx_bsg = states.index(JustificationState.BSG_OFF_LABEL)
        assert idx_tv < idx_bsg

    def test_confirm_ist_immer_letzter_schritt_bei_gelb_oder_rot(
        self, ergebnis_gelb, ergebnis_rot, ergebnis_rot_off_label
    ):
        for erg in (ergebnis_gelb, ergebnis_rot, ergebnis_rot_off_label):
            states = required_steps_for(erg)
            assert states[-1] == JustificationState.CONFIRM


# ---------------------------------------------------------------------------
# JustificationFSM.run (happy path + error path)
# ---------------------------------------------------------------------------


class TestFSMRun:
    def test_gruen_liefert_leere_begruendung(self, ergebnis_gruen):
        fsm = JustificationFSM(ergebnis_gruen)
        assert fsm.is_empty is True
        just = fsm.run(JustificationAnswers())
        assert isinstance(just, Justification)
        assert just.required_states == []
        assert just.confirmed is True
        assert just.off_label is False

    def test_rot_happy_path(self, ergebnis_rot, valid_rot_answers):
        fsm = JustificationFSM(ergebnis_rot)
        just = fsm.run(valid_rot_answers)
        assert just.ampel == "rot"
        assert just.confirmed is True
        assert just.off_label is False
        assert "diagnose" in just.answers
        assert "therapieversagen" in just.answers
        assert just.praxisbesonderheit == "Geriatrischer Schwerpunkt der Praxis"

    def test_off_label_happy_path(
        self, ergebnis_rot_off_label, valid_off_label_answers
    ):
        fsm = JustificationFSM(ergebnis_rot_off_label)
        just = fsm.run(valid_off_label_answers)
        assert just.off_label is True
        bsg = just.answers["bsg_off_label"]
        assert set(bsg.keys()) == {
            "schwerwiegende_erkrankung",
            "keine_alternative",
            "begruendete_erfolgsaussicht",
        }

    def test_leere_antworten_werfen_justification_error(self, ergebnis_rot):
        fsm = JustificationFSM(ergebnis_rot)
        with pytest.raises(JustificationError) as exc_info:
            fsm.run(JustificationAnswers())
        errors = exc_info.value.errors
        assert any("diagnose" in e for e in errors)
        assert any("vorbehandlung" in e for e in errors)
        assert any("therapieversagen" in e for e in errors)
        assert any("confirm" in e for e in errors)

    def test_zu_kurze_diagnose_schlaegt_fehl(self, ergebnis_gelb):
        fsm = JustificationFSM(ergebnis_gelb)
        answers = JustificationAnswers(
            {
                "diagnose": "zu kurz",  # < 10 Zeichen
                "vorbehandlung": "Ausreichend lange Antwort hier drin",
                "confirm": True,
            }
        )
        with pytest.raises(JustificationError) as exc_info:
            fsm.run(answers)
        assert any("diagnose" in e and "mindestens" in e for e in exc_info.value.errors)

    def test_fehlende_confirm_schlaegt_fehl(self, ergebnis_gelb):
        fsm = JustificationFSM(ergebnis_gelb)
        answers = JustificationAnswers(
            {
                "diagnose": "Refluxoesophagitis mit Barrett-Schleimhaut",
                "vorbehandlung": "PPI Omeprazol 20mg, 8 Wochen, plus H2-Blocker",
                "confirm": False,  # explizit nein
            }
        )
        with pytest.raises(JustificationError) as exc_info:
            fsm.run(answers)
        assert any("confirm" in e for e in exc_info.value.errors)

    def test_off_label_unvollstaendige_subfields_schlaegt_fehl(
        self, ergebnis_rot_off_label
    ):
        fsm = JustificationFSM(ergebnis_rot_off_label)
        answers = JustificationAnswers(
            {
                "diagnose": "Metastasiertes Mammakarzinom, HER2-positiv",
                "vorbehandlung": "Trastuzumab und Pertuzumab progredient",
                "therapieversagen": "Zweitlinien-Therapie gescheitert, Progress in 3 Monaten",
                "bsg_off_label": {
                    "schwerwiegende_erkrankung": "Fortgeschrittenes Karzinom",
                    # keine_alternative fehlt
                    "begruendete_erfolgsaussicht": "Phase-II-Daten",
                },
                "praxisbesonderheit": "",
                "confirm": True,
            }
        )
        with pytest.raises(JustificationError) as exc_info:
            fsm.run(answers)
        assert any("keine_alternative" in e for e in exc_info.value.errors)

    def test_praxisbesonderheit_optional_leer_ok(self, ergebnis_rot):
        fsm = JustificationFSM(ergebnis_rot)
        answers = JustificationAnswers(
            {
                "diagnose": "Angststoerung mit Schlafstoerung, chronifiziert",
                "vorbehandlung": "SSRI Citalopram 20mg, 6 Wochen",
                "therapieversagen": "SSRI-Wirkung unzureichend, keine Besserung nach 6 Wochen",
                "praxisbesonderheit": "",  # optional
                "confirm": True,
            }
        )
        just = fsm.run(answers)
        assert just.praxisbesonderheit is None


# ---------------------------------------------------------------------------
# Step-Katalog Integrity
# ---------------------------------------------------------------------------


class TestStepCatalog:
    def test_alle_states_haben_steps(self):
        for state in JustificationState:
            assert state in STEPS
            assert STEPS[state].state == state

    def test_off_label_hat_genau_drei_subfields(self):
        assert len(STEPS[JustificationState.BSG_OFF_LABEL].subfields) == 3


# ---------------------------------------------------------------------------
# Integration mit ComplianceLog (Hash-Chain darf nicht brechen)
# ---------------------------------------------------------------------------


class TestComplianceLogIntegration:
    def test_justification_im_extra_feld_bricht_kette_nicht(
        self, ergebnis_rot, valid_rot_answers
    ):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "test_log.db"

            fsm = JustificationFSM(ergebnis_rot)
            just = fsm.run(valid_rot_answers)

            with ComplianceLog(db_path=db_path) as log:
                # Erster Eintrag ohne Justification (wie beim normalen check)
                log.append(
                    icd="I10",
                    atc="C09AA02",
                    ampel="gruen",
                    begruendung="ACE-Hemmer bei Hypertonie",
                )
                # Zweiter Eintrag MIT Justification im extra-Feld
                entry = log.append(
                    icd=ergebnis_rot.icd,
                    atc=ergebnis_rot.atc,
                    alter=ergebnis_rot.alter,
                    ampel=ergebnis_rot.gesamt.value,
                    begruendung="PRISCUS-Treffer",
                    extra={
                        "version": "0.1.0",
                        "justification": just.to_dict(),
                    },
                )
                assert entry.extra["justification"]["confirmed"] is True
                assert log.verify_chain() is True
                assert len(log) == 2

    def test_justification_roundtrip_ueber_datei(
        self, ergebnis_rot, valid_rot_answers
    ):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "rt_log.db"
            fsm = JustificationFSM(ergebnis_rot)
            just = fsm.run(valid_rot_answers)

            with ComplianceLog(db_path=db_path) as log:
                log.append(
                    icd="F41",
                    atc="N05BA01",
                    alter=72,
                    ampel="rot",
                    begruendung="PRISCUS",
                    extra={"justification": just.to_dict()},
                )

            # Neue Connection - Justification muss aus der DB wieder gelesen
            # werden koennen, inklusive Sub-Struktur
            with ComplianceLog(db_path=db_path) as log:
                entries = log.all_entries()
                assert len(entries) == 1
                payload = entries[0].extra["justification"]
                assert payload["ampel"] == "rot"
                assert "therapieversagen" in payload["answers"]
                assert log.verify_chain() is True
