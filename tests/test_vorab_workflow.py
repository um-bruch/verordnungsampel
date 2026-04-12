"""Tests fuer den Vorab-Klaerungs-Workflow (Funktion 3).

Testet:
    - determine_workflow: Container-zu-Typ-Mapping + Prioritaet
    - build_workflow: Template-Rendering mit/ohne Kontext
    - WorkflowContext.resolved: Platzhalter bei fehlenden Feldern
    - Justification-Einbettung in den Text
    - Integration mit AmpelErgebnis aus der Engine
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from verordnungsampel.engine.evaluator import (
    Ampel,
    AmpelErgebnis,
    Treffer,
)
from verordnungsampel.engine.justification_fsm import (
    CONTAINER_PFLICHT_VORAB,
    CONTAINER_STELLUNGNAHME,
    CONTAINER_VERBOTEN_VORAB,
    Justification,
)
from verordnungsampel.engine.rules import Quelle
from verordnungsampel.output.vorab_workflow import (
    WorkflowContext,
    WorkflowOutput,
    WorkflowType,
    build_workflow,
    determine_workflow,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_ergebnis(
    ampel: Ampel,
    *,
    containers: list[str] | None = None,
    quelle_kuerzel: str | None = "TESTQ",
    icd: str = "I10",
    atc: str = "C09AA02",
) -> AmpelErgebnis:
    """Baut ein AmpelErgebnis mit beliebig vielen Container-Treffern."""
    containers = containers or []
    if not containers:
        treffer = [
            Treffer(
                regel_kuerzel="TEST",
                ampel=ampel,
                begruendung=f"Testregel {ampel.value}",
                quelle=Quelle(kuerzel=quelle_kuerzel, titel="Testquelle")
                if quelle_kuerzel
                else None,
            )
        ]
    else:
        treffer = [
            Treffer(
                regel_kuerzel=f"TEST_{c.upper()}",
                ampel=ampel,
                begruendung=f"Regel mit Container {c}",
                container=c,
                quelle=Quelle(kuerzel=quelle_kuerzel, titel="Testquelle")
                if quelle_kuerzel
                else None,
            )
            for c in containers
        ]
    return AmpelErgebnis(
        icd=icd, atc=atc, alter=None, gesamt=ampel, treffer=treffer
    )


@pytest.fixture
def erg_pflicht():
    return _make_ergebnis(
        Ampel.GELB,
        containers=[CONTAINER_PFLICHT_VORAB],
        quelle_kuerzel="SGB_V_31_6",
        icd="R52.1",
        atc="QV12",
    )


@pytest.fixture
def erg_verboten():
    return _make_ergebnis(
        Ampel.GRUEN,
        containers=[CONTAINER_VERBOTEN_VORAB],
        quelle_kuerzel="BMV_AE_29",
    )


@pytest.fixture
def erg_stellungnahme():
    return _make_ergebnis(
        Ampel.ROT,
        containers=[CONTAINER_STELLUNGNAHME],
        quelle_kuerzel="AMRL_III_GLP1",
        icd="E66.01",
        atc="A10BJ06",
    )


@pytest.fixture
def erg_ohne_container():
    return _make_ergebnis(Ampel.ROT, containers=None, icd="F41", atc="N05BA01")


# ---------------------------------------------------------------------------
# determine_workflow
# ---------------------------------------------------------------------------


class TestDetermineWorkflow:
    def test_ohne_container_keine_aktion(self, erg_ohne_container):
        assert determine_workflow(erg_ohne_container) == WorkflowType.KEINE_AKTION

    def test_pflicht_vorab_wird_pflicht_antrag(self, erg_pflicht):
        assert determine_workflow(erg_pflicht) == WorkflowType.PFLICHT_ANTRAG

    def test_verboten_vorab_wird_verboten_hinweis(self, erg_verboten):
        assert determine_workflow(erg_verboten) == WorkflowType.VERBOTEN_HINWEIS

    def test_stellungnahme_wird_stellungnahme(self, erg_stellungnahme):
        assert determine_workflow(erg_stellungnahme) == WorkflowType.STELLUNGNAHME

    def test_prioritaet_pflicht_schlaegt_stellungnahme(self):
        erg = _make_ergebnis(
            Ampel.ROT,
            containers=[CONTAINER_STELLUNGNAHME, CONTAINER_PFLICHT_VORAB],
        )
        assert determine_workflow(erg) == WorkflowType.PFLICHT_ANTRAG

    def test_prioritaet_stellungnahme_schlaegt_verboten(self):
        erg = _make_ergebnis(
            Ampel.ROT,
            containers=[CONTAINER_VERBOTEN_VORAB, CONTAINER_STELLUNGNAHME],
        )
        assert determine_workflow(erg) == WorkflowType.STELLUNGNAHME


# ---------------------------------------------------------------------------
# WorkflowContext.resolved
# ---------------------------------------------------------------------------


class TestWorkflowContext:
    def test_leerer_kontext_liefert_platzhalter(self):
        ctx = WorkflowContext()
        resolved = ctx.resolved()
        assert resolved["praxis_name"] == "[Praxisname einsetzen]"
        assert resolved["kk_name"] == "[Krankenkasse einsetzen]"
        assert resolved["bsnr"] == "[BSNR einsetzen]"
        # datum wird immer auf heute gesetzt, ist also nie Platzhalter
        assert "[" not in resolved["datum"]

    def test_kontext_ueberschreibt_platzhalter(self):
        ctx = WorkflowContext(
            praxis_name="Praxis Dr. Mueller",
            kk_name="AOK Nordost",
            arzt_name="Dr. med. Mueller",
        )
        resolved = ctx.resolved()
        assert resolved["praxis_name"] == "Praxis Dr. Mueller"
        assert resolved["kk_name"] == "AOK Nordost"
        assert resolved["arzt_name"] == "Dr. med. Mueller"
        # nicht gesetzte Felder bleiben Platzhalter
        assert resolved["bsnr"] == "[BSNR einsetzen]"


# ---------------------------------------------------------------------------
# build_workflow — happy paths
# ---------------------------------------------------------------------------


class TestBuildWorkflow:
    def test_pflicht_antrag_enthaelt_kk_und_sgb_verweis(self, erg_pflicht):
        ctx = WorkflowContext(kk_name="AOK Nordost")
        out = build_workflow(erg_pflicht, ctx)
        assert out.workflow_type == WorkflowType.PFLICHT_ANTRAG
        assert out.empfaenger == "AOK Nordost"
        assert "R52.1" in out.text
        assert "QV12" in out.text
        assert "SGB V" in out.text
        assert "AOK Nordost" not in out.text or "AOK" in out.text  # KK taucht nicht zwingend im Text auf
        assert "Genehmigung" in out.naechster_schritt

    def test_verboten_hinweis_nennt_keine_kk_als_empfaenger(self, erg_verboten):
        out = build_workflow(erg_verboten)
        assert out.workflow_type == WorkflowType.VERBOTEN_HINWEIS
        assert out.empfaenger is None
        assert "§ 29 BMV-AE" in out.text
        assert "KEIN Antrag" in out.naechster_schritt

    def test_stellungnahme_verweist_auf_bsg_b6ka2712(self, erg_stellungnahme):
        out = build_workflow(erg_stellungnahme, WorkflowContext(kk_name="TK"))
        assert out.workflow_type == WorkflowType.STELLUNGNAHME
        assert out.empfaenger == "TK"
        assert "B 6 KA 27/12" in out.text
        # Substring-Check robust gegen Zeilenumbrueche im Template
        flat = " ".join(out.text.split())
        assert "NICHT als Antrag auf Einzelfall- Vorabgenehmigung" in flat

    def test_keine_aktion_ohne_containerr(self, erg_ohne_container):
        out = build_workflow(erg_ohne_container)
        assert out.workflow_type == WorkflowType.KEINE_AKTION
        assert "kein Vorab-Klaerungs-Schritt" in out.text
        assert out.rechtsgrundlage is None


# ---------------------------------------------------------------------------
# build_workflow mit Justification
# ---------------------------------------------------------------------------


class TestBuildWorkflowMitJustification:
    def test_strukturierte_begruendung_wird_eingefuegt(self, erg_stellungnahme):
        just = Justification(
            ampel="rot",
            required_states=["diagnose", "vorbehandlung", "therapieversagen", "confirm"],
            answers={
                "diagnose": "Adipositas Grad II (E66.01) mit hypertensiven Krisen",
                "vorbehandlung": "Diaet + Bewegungstherapie 6 Monate, Orlistat 3 Monate",
                "therapieversagen": "Kein nachhaltiger Gewichtsverlust, Orlistat gastrointestinal unvertraeglich",
                "confirm": True,
            },
            confirmed=True,
            off_label=False,
            praxisbesonderheit=None,
        )
        out = build_workflow(
            erg_stellungnahme,
            WorkflowContext(kk_name="TK"),
            justification=just,
        )
        assert "Strukturierte Begruendung" in out.text
        assert "Orlistat" in out.text
        assert "diagnose:" in out.text or "Diagnose" in out.text


# ---------------------------------------------------------------------------
# WorkflowOutput.render_full + to_dict
# ---------------------------------------------------------------------------


class TestWorkflowOutput:
    def test_render_full_enthaelt_header_und_naechster_schritt(self, erg_pflicht):
        out = build_workflow(erg_pflicht, WorkflowContext(kk_name="TK"))
        rendered = out.render_full()
        assert "VORAB-KLAERUNGS-WORKFLOW: PFLICHT_ANTRAG" in rendered
        assert "Naechster Schritt" in rendered
        assert "Betreff:" in rendered

    def test_to_dict_roundtrip(self, erg_pflicht):
        out = build_workflow(erg_pflicht, WorkflowContext(kk_name="TK"))
        d = out.to_dict()
        assert d["workflow_type"] == "pflicht_antrag"
        assert d["empfaenger"] == "TK"
        assert "containers" in d
        assert CONTAINER_PFLICHT_VORAB in d["containers"]


# ---------------------------------------------------------------------------
# Rechtsgrundlage-Aggregation
# ---------------------------------------------------------------------------


class TestRechtsgrundlage:
    def test_eine_quelle_wird_uebernommen(self, erg_pflicht):
        out = build_workflow(erg_pflicht)
        assert out.rechtsgrundlage == "SGB_V_31_6"

    def test_mehrere_quellen_werden_kommasepariert(self):
        treffer = [
            Treffer(
                regel_kuerzel="R1",
                ampel=Ampel.GELB,
                begruendung="R1",
                container=CONTAINER_PFLICHT_VORAB,
                quelle=Quelle(kuerzel="Q1", titel="Q1"),
            ),
            Treffer(
                regel_kuerzel="R2",
                ampel=Ampel.GELB,
                begruendung="R2",
                container=CONTAINER_PFLICHT_VORAB,
                quelle=Quelle(kuerzel="Q2", titel="Q2"),
            ),
        ]
        erg = AmpelErgebnis(
            icd="I10", atc="X123", alter=None, gesamt=Ampel.GELB, treffer=treffer
        )
        out = build_workflow(erg)
        assert out.rechtsgrundlage == "Q1, Q2"

    def test_duplikate_in_quellen_werden_entfernt(self):
        q = Quelle(kuerzel="SAME", titel="X")
        treffer = [
            Treffer(regel_kuerzel="A", ampel=Ampel.GELB, begruendung="a", container=CONTAINER_PFLICHT_VORAB, quelle=q),
            Treffer(regel_kuerzel="B", ampel=Ampel.GELB, begruendung="b", container=CONTAINER_PFLICHT_VORAB, quelle=q),
        ]
        erg = AmpelErgebnis(
            icd="I10", atc="X", alter=None, gesamt=Ampel.GELB, treffer=treffer
        )
        out = build_workflow(erg)
        assert out.rechtsgrundlage == "SAME"
