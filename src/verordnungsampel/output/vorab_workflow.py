"""Vorab-Klaerungs-Workflow (KONZEPT Funktion 3).

Juristischer Hintergrund:
    Das deutsche GKV-Recht kennt drei disjunkte Situationen fuer
    Vorab-Genehmigungen/Klaerungen. Der Vorab-Workflow muss zwischen
    ihnen sauber trennen — Vermischung fuehrt zu Regressrisiko:

    1. **Pflicht-Vorabgenehmigung**
       - Cannabis als Medizin: § 31 Abs. 6 SGB V (Erstverordnung)
       - Soziotherapie: § 37a SGB V
       - Haeusliche Krankenpflege: § 37 SGB V
       - Stationaere Reha: § 40 SGB V
       - Bestimmte Heil-/Hilfsmittel: AM-RL / Hilfsmittel-RL
       -> Antrag an Krankenkasse erforderlich, Genehmigung ABWARTEN

    2. **Verbotene Einzelfall-Vorabgenehmigung**
       - Normale Arzneimittel mit Indikation: § 29 BMV-AE
       -> Kasse darf NICHT genehmigen; defensiv dokumentieren statt Antrag

    3. **Stellungnahme-Moeglichkeit** (Grauzonen)
       - Off-Label wo Anlage VI G-BA schweigt
       - GLP-1-Agonisten bei Adipositas ohne Diabetes
       - Praeparate mit vertraulichem Erstattungsbetrag
       -> BSG B 6 KA 27/12 R: Bitte um Stellungnahme an KK/KV ist zulaessig
          und kann spaeter im Regressverfahren den "substanziierten
          Vortrag im Verwaltungsverfahren"-Standard erfuellen

Pattern:
    Der Workflow ist ein **pure function** vom AmpelErgebnis (plus
    optionalem Kontext) zu einem textuellen WorkflowOutput. Keine I/O
    im Kernmodul — Datei-Ausgabe liegt im CLI.

    Container-Hinweise aus der Ampel-Engine (``pflicht_vorab``,
    ``verboten_vorab``, ``stellungnahme``) steuern die Auswahl des
    Workflow-Typs 1:1. Sind mehrere Container gesetzt, gewinnt
    ``pflicht_vorab`` > ``stellungnahme`` > ``verboten_vorab``
    (je nach Dringlichkeit fuer den verordnenden Arzt).

Templates:
    Sind Python-Konstanten mit ``str.format()``-Placeholdern. Das reicht
    fuer den MVP. Bei haeufiger Textpflege kann spaeter eine JSON-Quelle
    hinzukommen.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from verordnungsampel.engine.evaluator import Ampel, AmpelErgebnis
from verordnungsampel.engine.justification_fsm import (
    CONTAINER_OFF_LABEL,
    CONTAINER_PFLICHT_VORAB,
    CONTAINER_STELLUNGNAHME,
    CONTAINER_VERBOTEN_VORAB,
    Justification,
)


class WorkflowType(str, Enum):
    """Disjunkte Typen des Vorab-Klaerungs-Workflows."""

    KEINE_AKTION = "keine_aktion"
    PFLICHT_ANTRAG = "pflicht_antrag"
    VERBOTEN_HINWEIS = "verboten_hinweis"
    STELLUNGNAHME = "stellungnahme"


# Dringlichkeits-Ranking wenn mehrere Container gleichzeitig gesetzt sind.
# Reihenfolge: je frueher in der Liste, desto vorrangiger der Workflow-Typ.
_CONTAINER_PRIORITY: List[tuple[str, WorkflowType]] = [
    (CONTAINER_PFLICHT_VORAB, WorkflowType.PFLICHT_ANTRAG),
    (CONTAINER_STELLUNGNAHME, WorkflowType.STELLUNGNAHME),
    (CONTAINER_VERBOTEN_VORAB, WorkflowType.VERBOTEN_HINWEIS),
]


# ---------------------------------------------------------------------------
# Eingabe- und Ausgabe-Typen
# ---------------------------------------------------------------------------


@dataclass
class WorkflowContext:
    """Eingabe-Kontext fuer die Text-Generierung.

    Alle Felder sind optional. Fehlende Felder werden mit Platzhaltern
    ersetzt (z.B. ``[Praxis einsetzen]``), damit der generierte Text
    immer druckbar bleibt.
    """

    praxis_name: Optional[str] = None
    praxis_adresse: Optional[str] = None
    arzt_name: Optional[str] = None
    bsnr: Optional[str] = None  # Betriebsstaettennummer
    lanr: Optional[str] = None  # Lebenslange Arztnummer
    kk_name: Optional[str] = None
    patient_kennung: Optional[str] = None  # Praxis-internes Kuerzel, NICHT Klarname
    datum: Optional[date] = None

    def resolved(self) -> Dict[str, str]:
        """Fuellt fehlende Felder mit lesbaren Platzhaltern."""
        d = self.datum or date.today()
        return {
            "praxis_name": self.praxis_name or "[Praxisname einsetzen]",
            "praxis_adresse": self.praxis_adresse or "[Praxisadresse einsetzen]",
            "arzt_name": self.arzt_name or "[Behandelnder Arzt einsetzen]",
            "bsnr": self.bsnr or "[BSNR einsetzen]",
            "lanr": self.lanr or "[LANR einsetzen]",
            "kk_name": self.kk_name or "[Krankenkasse einsetzen]",
            "patient_kennung": self.patient_kennung or "[Patienten-Kuerzel einsetzen]",
            "datum": d.strftime("%d.%m.%Y"),
        }


@dataclass
class WorkflowOutput:
    """Ergebnis der Workflow-Generierung."""

    workflow_type: WorkflowType
    empfaenger: Optional[str]
    betreff: str
    text: str
    rechtsgrundlage: Optional[str]
    naechster_schritt: str
    containers: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_type": self.workflow_type.value,
            "empfaenger": self.empfaenger,
            "betreff": self.betreff,
            "text": self.text,
            "rechtsgrundlage": self.rechtsgrundlage,
            "naechster_schritt": self.naechster_schritt,
            "containers": list(self.containers),
        }

    def render_full(self) -> str:
        """Druckfertiger Komplett-Text inklusive Kopfzeile."""
        lines: List[str] = []
        lines.append("=" * 72)
        lines.append(f"VORAB-KLAERUNGS-WORKFLOW: {self.workflow_type.value.upper()}")
        lines.append("=" * 72)
        if self.empfaenger:
            lines.append(f"An: {self.empfaenger}")
        lines.append(f"Betreff: {self.betreff}")
        if self.rechtsgrundlage:
            lines.append(f"Rechtsgrundlage: {self.rechtsgrundlage}")
        lines.append("-" * 72)
        lines.append(self.text)
        lines.append("-" * 72)
        lines.append(f"Naechster Schritt: {self.naechster_schritt}")
        lines.append("=" * 72)
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Typ-Erkennung
# ---------------------------------------------------------------------------


def determine_workflow(ergebnis: AmpelErgebnis) -> WorkflowType:
    """Leitet den Workflow-Typ aus den Container-Hinweisen eines Ergebnisses ab.

    Regeln:
        - Kein Container: ``KEINE_AKTION``
        - ``pflicht_vorab`` vorhanden: ``PFLICHT_ANTRAG`` (hoechste Prio,
          weil Genehmigung abgewartet werden muss)
        - ``stellungnahme`` vorhanden: ``STELLUNGNAHME``
        - ``verboten_vorab`` vorhanden: ``VERBOTEN_HINWEIS``

    Kommen mehrere Container vor, gewinnt die hoehere Prioritaet.
    """
    containers = set(ergebnis.container_hinweise)
    for marker, wf_type in _CONTAINER_PRIORITY:
        if marker in containers:
            return wf_type
    return WorkflowType.KEINE_AKTION


# ---------------------------------------------------------------------------
# Template-Texte
# ---------------------------------------------------------------------------

_TEMPLATE_PFLICHT_ANTRAG = """\
Sehr geehrte Damen und Herren,

im Namen meines Patienten (Kuerzel: {patient_kennung}) beantrage ich hiermit die
Genehmigung der nachfolgend bezeichneten Leistung gemaess den Vorgaben des SGB V.

Verordnungsdaten:
  - Diagnose (ICD-10-GM): {icd}
  - Wirkstoff/Leistung (ATC): {atc}
  - Datum der geplanten Verordnung: {datum}

Begruendung der medizinischen Notwendigkeit:
{begruendung_block}

Angaben zur Verordnenden Praxis:
  - Praxis: {praxis_name}, {praxis_adresse}
  - Arzt:  {arzt_name} (BSNR: {bsnr}, LANR: {lanr})

Ich bitte um zeitnahe Pruefung und Bescheidung des Antrags. Die Verordnung
erfolgt erst nach schriftlicher Genehmigung bzw. bei Fristablauf nach den
gesetzlichen Fiktionsregeln.

Mit freundlichen Gruessen

{arzt_name}
{datum}
"""


_TEMPLATE_VERBOTEN_HINWEIS = """\
DEFENSIVER DOKUMENTATIONS-HINWEIS (keine Antragsstellung!)

Fuer die Verordnung ICD={icd} / ATC={atc} am {datum} gilt:

Eine Einzelfall-Vorabgenehmigung durch die Krankenkasse ist nach § 29 BMV-AE
AUSDRUECKLICH NICHT zulaessig. Ein entsprechender Antrag wuerde abgelehnt
werden und kann im Regressverfahren NICHT als Schutz-Argument verwendet werden.

Stattdessen:
  1. Strukturierte Indikationsbegruendung im Moment der Verordnung
     dokumentieren (siehe ggf. begleitendes Begruendungs-Formular).
  2. Vorbehandlung und Therapieversagen sauber festhalten (BSG B 6 KA 26/13 R:
     nachgereichte Doku reicht NICHT).
  3. Praxisbesonderheiten pruefen und — falls einschlaegig — sofort im
     Verwaltungsverfahren substanziiert vortragen (LSG BW 15.11.2023).

{begruendung_block}

Angaben zur Verordnenden Praxis:
  - Praxis: {praxis_name}, {praxis_adresse}
  - Arzt:  {arzt_name} (BSNR: {bsnr}, LANR: {lanr})

Dieser Hinweis ist NICHT zur Weiterleitung an die Krankenkasse bestimmt.
Er ist ausschliesslich interne Dokumentation fuer den Compliance-Log.
"""


_TEMPLATE_STELLUNGNAHME = """\
Sehr geehrte Damen und Herren,

im Fall meines Patienten (Kuerzel: {patient_kennung}) stehe ich vor einer
Verordnungsentscheidung in einem Bereich, in dem die Erstattungsfaehigkeit
nach aktueller Rechtslage und Leitlinien nicht eindeutig geklaert ist.

Bevor ich eine endgueltige Verordnungsentscheidung treffe, bitte ich Sie
hoeflich um eine schriftliche Stellungnahme der Krankenkasse zur geplanten
Verordnung:

Verordnungsdaten:
  - Diagnose (ICD-10-GM): {icd}
  - Wirkstoff/Leistung (ATC): {atc}
  - Geplantes Verordnungsdatum: {datum}

Hintergrund der Stellungnahmebitte:
{begruendung_block}

Dieser Schritt erfolgt ausdruecklich NICHT als Antrag auf Einzelfall-
Vorabgenehmigung im Sinne des § 29 BMV-AE, sondern als bitte um Stellungnahme
nach der Rechtsprechung des Bundessozialgerichts (BSG B 6 KA 27/12 R). Ziel
ist es, Ihre Rechtsauffassung vor einer eventuell streitigen Verordnung
transparent zu machen und im Falle spaeterer Pruefverfahren einen
substanziierten Vortrag bereits im Verwaltungsverfahren zu ermoeglichen
(vgl. LSG Baden-Wuerttemberg, 15.11.2023).

Angaben zur Verordnenden Praxis:
  - Praxis: {praxis_name}, {praxis_adresse}
  - Arzt:  {arzt_name} (BSNR: {bsnr}, LANR: {lanr})

Ich bitte um Ihre Rueckmeldung innerhalb einer angemessenen Frist.

Mit freundlichen Gruessen

{arzt_name}
{datum}
"""


_TEMPLATE_KEINE_AKTION = """\
Fuer die Verordnung ICD={icd} / ATC={atc} ist kein Vorab-Klaerungs-Schritt
erforderlich. Die Verordnung kann regulaer erfolgen; Dokumentation nach
allgemeiner aerztlicher Sorgfaltspflicht genuegt.
"""


# ---------------------------------------------------------------------------
# Begruendungs-Block Helper
# ---------------------------------------------------------------------------


def _collect_begruendungen(ergebnis: AmpelErgebnis) -> List[str]:
    """Sammelt Ampel-Begruendungen als eingerueckte Liste."""
    lines: List[str] = []
    for i, t in enumerate(ergebnis.treffer, 1):
        lines.append(f"  {i}. [{t.ampel.value.upper()}] {t.begruendung}")
        if t.quelle:
            lines.append(f"     Quelle: {t.quelle.kuerzel} — {t.quelle.titel}")
    return lines


def _format_justification_block(justification: Optional[Justification]) -> List[str]:
    """Rendert die strukturierte Begruendung als Einschub fuer den Text."""
    if justification is None or not justification.required_states:
        return []
    lines: List[str] = ["", "Strukturierte Begruendung (aus Compliance-Log):"]
    for state_str, answer in justification.answers.items():
        if state_str == "confirm":
            continue
        if isinstance(answer, dict):
            lines.append(f"  - {state_str}:")
            for sub, val in answer.items():
                lines.append(f"      {sub}: {val}")
        elif answer:
            lines.append(f"  - {state_str}: {answer}")
    return lines


def _collect_rechtsgrundlagen(ergebnis: AmpelErgebnis) -> Optional[str]:
    """Sammelt eindeutige Quellen-Kuerzel als Rechtsgrundlage-String."""
    kuerzel = []
    seen = set()
    for t in ergebnis.treffer:
        if t.quelle and t.quelle.kuerzel and t.quelle.kuerzel not in seen:
            kuerzel.append(t.quelle.kuerzel)
            seen.add(t.quelle.kuerzel)
    return ", ".join(kuerzel) if kuerzel else None


# ---------------------------------------------------------------------------
# Build-Funktionen
# ---------------------------------------------------------------------------


def build_workflow(
    ergebnis: AmpelErgebnis,
    context: Optional[WorkflowContext] = None,
    justification: Optional[Justification] = None,
) -> WorkflowOutput:
    """Generiert einen WorkflowOutput fuer ein Ampelergebnis.

    Args:
        ergebnis: Das Ergebnis aus :func:`engine.evaluate`.
        context: Optionale Stammdaten (Praxis, Arzt, Patient-Kuerzel).
            Fehlende Felder werden mit lesbaren Platzhaltern ersetzt.
        justification: Optional das HSM-Ergebnis einer strukturierten
            Begruendung. Wenn vorhanden, wird sie in den Antragstext
            eingebettet.

    Returns:
        Ein :class:`WorkflowOutput` mit gerendertem Text und Metadaten.
    """
    ctx = context or WorkflowContext()
    wf_type = determine_workflow(ergebnis)

    fields = ctx.resolved()
    fields["icd"] = ergebnis.icd
    fields["atc"] = ergebnis.atc
    fields["ampel"] = ergebnis.gesamt.value

    # Begruendungsblock aus Ampel + optional Justification
    block_lines = _collect_begruendungen(ergebnis)
    block_lines.extend(_format_justification_block(justification))
    fields["begruendung_block"] = "\n".join(block_lines) if block_lines else "  (keine)"

    rechtsgrundlage = _collect_rechtsgrundlagen(ergebnis)

    if wf_type == WorkflowType.PFLICHT_ANTRAG:
        text = _TEMPLATE_PFLICHT_ANTRAG.format(**fields)
        return WorkflowOutput(
            workflow_type=wf_type,
            empfaenger=fields["kk_name"],
            betreff=f"Antrag auf Genehmigung nach SGB V — {ergebnis.icd} / {ergebnis.atc}",
            text=text,
            rechtsgrundlage=rechtsgrundlage,
            naechster_schritt=(
                "Antrag an die Krankenkasse senden. Genehmigung ODER Fristablauf "
                "(Fiktionswirkung) abwarten, erst DANN verordnen."
            ),
            containers=list(ergebnis.container_hinweise),
        )

    if wf_type == WorkflowType.VERBOTEN_HINWEIS:
        text = _TEMPLATE_VERBOTEN_HINWEIS.format(**fields)
        return WorkflowOutput(
            workflow_type=wf_type,
            empfaenger=None,  # nur intern
            betreff=f"Interner Doku-Hinweis (§ 29 BMV-AE) — {ergebnis.icd} / {ergebnis.atc}",
            text=text,
            rechtsgrundlage=rechtsgrundlage or "BMV_AE_29",
            naechster_schritt=(
                "KEIN Antrag. Strukturierte Begruendung im Moment der Verordnung "
                "dokumentieren (CLI: `justify`). Compliance-Log wird versiegelt."
            ),
            containers=list(ergebnis.container_hinweise),
        )

    if wf_type == WorkflowType.STELLUNGNAHME:
        text = _TEMPLATE_STELLUNGNAHME.format(**fields)
        return WorkflowOutput(
            workflow_type=wf_type,
            empfaenger=fields["kk_name"],
            betreff=f"Bitte um Stellungnahme (BSG B 6 KA 27/12 R) — {ergebnis.icd} / {ergebnis.atc}",
            text=text,
            rechtsgrundlage=rechtsgrundlage,
            naechster_schritt=(
                "Bitte um Stellungnahme an die Krankenkasse senden. Dies ist KEIN "
                "Antrag auf Einzelfall-Vorabgenehmigung. Rueckmeldung der KK "
                "dokumentieren und in Verordnungsentscheidung einbeziehen."
            ),
            containers=list(ergebnis.container_hinweise),
        )

    # KEINE_AKTION
    text = _TEMPLATE_KEINE_AKTION.format(**fields)
    return WorkflowOutput(
        workflow_type=wf_type,
        empfaenger=None,
        betreff=f"Kein Vorab-Klaerungs-Schritt — {ergebnis.icd} / {ergebnis.atc}",
        text=text,
        rechtsgrundlage=None,
        naechster_schritt="Regulaer verordnen. Allgemeine Doku-Sorgfalt beachten.",
        containers=list(ergebnis.container_hinweise),
    )
