"""Hierarchical State Machine fuer die strukturierte Begruendungspflicht.

Juristischer Hintergrund:
    - BSG B 6 KA 26/13: Nachtraeglich eingereichte Dokumentation reicht
      NICHT zur Rechtfertigung einer regressanfaelligen Verordnung.
    - SG Marburg 14.02.2024 (S 18 KA 96/23): Dokumentation muss ZUM
      ZEITPUNKT der Verordnung erfolgen.
    - BSG-Off-Label-Rechtsprechung: Drei kumulative Kriterien noetig
      (schwerwiegende Erkrankung, keine Alternative, begruendete Aussicht).

Pattern:
    Inspiriert vom "Hierarchical State Machine"-Pattern im Multiaxial
    Diagnostic Expert System (Geiger 2026, DOI 10.5281/zenodo.18736725),
    Section 9 des Papers. Dort als Decision-Engine fuer die 6-Achsen-
    Diagnostik verwendet, hier adaptiert auf die Begruendungskette einer
    regressanfaelligen Verordnung.

Ablauf:
    Ausgehend von einem :class:`AmpelErgebnis` bestimmt
    :func:`required_steps_for` die noetigen Begruendungs-Schritte:

    - GRUEN: keine Schritte erforderlich (optional abgebbar)
    - GELB:  DIAGNOSE -> VORBEHANDLUNG -> CONFIRM
    - ROT:   DIAGNOSE -> VORBEHANDLUNG -> THERAPIEVERSAGEN ->
             (BSG_OFF_LABEL wenn off_label-Container) ->
             (PRAXISBESONDERHEIT wenn verboten_vorab-Container) ->
             CONFIRM

    Die :class:`JustificationFSM` fuehrt durch die Schritte, sammelt die
    Antworten, validiert sie und liefert am Ende ein :class:`Justification`-
    Ergebnis, das als strukturiertes Dict im Compliance-Log versiegelt wird.

Design-Entscheidung:
    Strikt nicht-interaktiv. Die FSM nimmt ein :class:`JustificationAnswers`-
    Dict entgegen und liefert ein Ergebnis oder eine Liste von Fehlermeldungen.
    Die interaktive CLI-Abfrage liegt in :mod:`verordnungsampel.cli.main`
    als duenner Wrapper darueber. So bleibt das Modul 100% testbar ohne
    stdin-Mocks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence

from verordnungsampel.engine.evaluator import Ampel, AmpelErgebnis


class JustificationState(str, Enum):
    """Einzelne Schritte der Begruendungskette."""

    DIAGNOSE = "diagnose"
    VORBEHANDLUNG = "vorbehandlung"
    THERAPIEVERSAGEN = "therapieversagen"
    BSG_OFF_LABEL = "bsg_off_label"
    PRAXISBESONDERHEIT = "praxisbesonderheit"
    CONFIRM = "confirm"


# Container-Marker die die Container-sensitive Logik steuern.
CONTAINER_OFF_LABEL = "off_label"
CONTAINER_VERBOTEN_VORAB = "verboten_vorab"
CONTAINER_PFLICHT_VORAB = "pflicht_vorab"
CONTAINER_STELLUNGNAHME = "stellungnahme"


@dataclass(frozen=True)
class JustificationStep:
    """Ein einzelner Schritt der FSM.

    Felder:
        state: Eindeutiger State-Bezeichner.
        prompt: Benutzerseitige Frage (fuer CLI/UI).
        help_text: Erklaerender Text, warum dieser Schritt noetig ist
            (inkl. juristischer Verweis wenn anwendbar).
        min_length: Minimale Zeichenanzahl fuer die Antwort. Wenn ``0``
            ist die Antwort optional (z.B. PRAXISBESONDERHEIT).
        subfields: Optionale Liste von Unter-Feldern. Wird fuer den
            BSG-Off-Label-Schritt genutzt (3 Kriterien-Checkboxen).
    """

    state: JustificationState
    prompt: str
    help_text: str
    min_length: int = 10
    subfields: Sequence[str] = field(default_factory=tuple)


# Die BSG-Off-Label-Kriterien (BVerfG/BSG, sog. "Nikolaus-Beschluss" und
# Folgerechtsprechung). Alle drei muessen kumulativ erfuellt sein, damit
# ein Off-Label-Use gegenueber der KV verteidigbar ist.
BSG_OFF_LABEL_SUBFIELDS: Sequence[str] = (
    "schwerwiegende_erkrankung",        # Schwerwiegende Erkrankung
    "keine_alternative",                # Keine andere Therapie verfuegbar
    "begruendete_erfolgsaussicht",      # Begruendete Aussicht auf Erfolg
)


# Kanonische Step-Definitionen. Reihenfolge = Ablauf der FSM.
STEPS: Dict[JustificationState, JustificationStep] = {
    JustificationState.DIAGNOSE: JustificationStep(
        state=JustificationState.DIAGNOSE,
        prompt="Bitte bestaetige oder konkretisiere die Diagnose (inkl. Schweregrad/Verlauf).",
        help_text=(
            "Die Diagnose ist der Anker der Begruendung. Sie muss im Moment der "
            "Verordnung festgehalten sein (SG Marburg 14.02.2024)."
        ),
        min_length=10,
    ),
    JustificationState.VORBEHANDLUNG: JustificationStep(
        state=JustificationState.VORBEHANDLUNG,
        prompt="Welche Vorbehandlungen wurden bereits versucht? (Substanzen/Dauer/Dosis)",
        help_text=(
            "Die Vorbehandlung dokumentiert, warum die regressanfaellige "
            "Verordnung notwendig wurde. Ohne Vorbehandlungs-Doku greift die "
            "'Therapiealternativen-hoeher-gewichten'-Argumentation der KV."
        ),
        min_length=10,
    ),
    JustificationState.THERAPIEVERSAGEN: JustificationStep(
        state=JustificationState.THERAPIEVERSAGEN,
        prompt="Warum war die Vorbehandlung nicht ausreichend? (Unvertraeglichkeit/Wirkungslosigkeit/Kontraindikation)",
        help_text=(
            "Erforderlich bei ROT-Bewertungen. Muss konkret auf die vorhandene "
            "Vorbehandlung Bezug nehmen (Therapieversagen = nicht bloss "
            "'nicht gewuenscht')."
        ),
        min_length=15,
    ),
    JustificationState.BSG_OFF_LABEL: JustificationStep(
        state=JustificationState.BSG_OFF_LABEL,
        prompt="BSG-Off-Label-Kriterien (alle drei muessen erfuellt sein)",
        help_text=(
            "Gemaess BSG-Rechtsprechung (z.B. BVerfG 06.12.2005, 1 BvR 347/98) "
            "muessen bei Off-Label-Verordnungen drei Kriterien kumulativ erfuellt "
            "sein. Jedes Kriterium ist separat zu bestaetigen und zu begruenden."
        ),
        min_length=10,
        subfields=BSG_OFF_LABEL_SUBFIELDS,
    ),
    JustificationState.PRAXISBESONDERHEIT: JustificationStep(
        state=JustificationState.PRAXISBESONDERHEIT,
        prompt="Praxisbesonderheit vorhanden? (Leer lassen wenn keine.)",
        help_text=(
            "Substanziierter Vortrag bereits im Verwaltungsverfahren "
            "(LSG BW 15.11.2023; SG Marburg 31.01.2024). Kann die entscheidende "
            "Verteidigung im Regress-Verfahren sein."
        ),
        min_length=0,  # Optional — nicht jede Verordnung hat eine
    ),
    JustificationState.CONFIRM: JustificationStep(
        state=JustificationState.CONFIRM,
        prompt="Ich bestaetige, dass die Angaben im Moment der Verordnung zutreffen.",
        help_text=(
            "Ohne diese Bestaetigung gilt die Begruendung als nicht abgeschlossen "
            "und wird NICHT in den Compliance-Log aufgenommen."
        ),
        min_length=0,  # Boolean-Confirm — nicht laengenbasiert
    ),
}


# ---------------------------------------------------------------------------
# Ergebnisdatentypen
# ---------------------------------------------------------------------------


@dataclass
class JustificationAnswers:
    """Eingabedaten fuer die FSM (non-interactive Variante).

    Das Dict ``data`` bildet :class:`JustificationState`-Werte auf Antworten ab.
    Fuer Schritte ohne Subfields ist die Antwort ein String; fuer Schritte
    mit Subfields ein Dict von Subfield-Namen auf Strings.
    Der CONFIRM-Schritt erwartet einen Bool ``True``.
    """

    data: Dict[str, Any] = field(default_factory=dict)

    def get(self, state: JustificationState) -> Any:
        return self.data.get(state.value)

    def set(self, state: JustificationState, value: Any) -> None:
        self.data[state.value] = value


@dataclass
class Justification:
    """Fertige, validierte Begruendungskette.

    Wird als ``extra["justification"]`` im Compliance-Log versiegelt und
    ist damit Bestandteil der Hash-Chain.
    """

    ampel: str
    required_states: List[str]
    answers: Dict[str, Any]
    confirmed: bool
    off_label: bool
    praxisbesonderheit: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ampel": self.ampel,
            "required_states": list(self.required_states),
            "answers": dict(self.answers),
            "confirmed": self.confirmed,
            "off_label": self.off_label,
            "praxisbesonderheit": self.praxisbesonderheit,
        }


class JustificationError(ValueError):
    """Wird geworfen wenn Pflichtfelder fehlen oder zu kurz sind."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors: List[str] = list(errors)
        super().__init__("; ".join(self.errors))


# ---------------------------------------------------------------------------
# Ablauf-Logik
# ---------------------------------------------------------------------------


def required_steps_for(ergebnis: AmpelErgebnis) -> List[JustificationState]:
    """Bestimmt die erforderlichen FSM-States fuer ein gegebenes Ampelergebnis.

    Regeln:
        - GRUEN: leere Liste (keine Begruendung erforderlich, trotzdem
          freiwillig abgebbar)
        - GELB:  DIAGNOSE, VORBEHANDLUNG, CONFIRM
        - ROT:   DIAGNOSE, VORBEHANDLUNG, THERAPIEVERSAGEN,
                 optional BSG_OFF_LABEL (wenn Container ``off_label``),
                 PRAXISBESONDERHEIT, CONFIRM

    Die Reihenfolge der zurueckgegebenen Liste ist der Abfrage-Ablauf.
    """
    if ergebnis.gesamt == Ampel.GRUEN:
        return []

    steps: List[JustificationState] = [
        JustificationState.DIAGNOSE,
        JustificationState.VORBEHANDLUNG,
    ]
    if ergebnis.gesamt == Ampel.ROT:
        steps.append(JustificationState.THERAPIEVERSAGEN)
        if CONTAINER_OFF_LABEL in ergebnis.container_hinweise:
            steps.append(JustificationState.BSG_OFF_LABEL)
        steps.append(JustificationState.PRAXISBESONDERHEIT)
    steps.append(JustificationState.CONFIRM)
    return steps


def _validate_subfields_answer(
    step: JustificationStep, value: Any, errors: List[str]
) -> Dict[str, str]:
    """Validiert einen Schritt mit Subfields (z.B. BSG-Kriterien)."""
    if not isinstance(value, dict):
        errors.append(f"{step.state.value}: erwartet Dict mit Feldern {list(step.subfields)}")
        return {}
    cleaned: Dict[str, str] = {}
    for sub in step.subfields:
        sub_val = value.get(sub)
        if not isinstance(sub_val, str) or len(sub_val.strip()) < step.min_length:
            errors.append(
                f"{step.state.value}.{sub}: mindestens {step.min_length} Zeichen erforderlich"
            )
            continue
        cleaned[sub] = sub_val.strip()
    return cleaned


def _validate_string_answer(
    step: JustificationStep, value: Any, errors: List[str]
) -> Optional[str]:
    """Validiert einen Schritt mit String-Antwort."""
    if value is None or value == "":
        if step.min_length == 0:
            return None  # optional leer erlaubt
        errors.append(f"{step.state.value}: Pflichtfeld (mindestens {step.min_length} Zeichen)")
        return None
    if not isinstance(value, str):
        errors.append(f"{step.state.value}: erwartet String, erhalten {type(value).__name__}")
        return None
    trimmed = value.strip()
    if len(trimmed) < step.min_length:
        errors.append(
            f"{step.state.value}: mindestens {step.min_length} Zeichen "
            f"erforderlich (erhalten: {len(trimmed)})"
        )
        return None
    return trimmed


def _validate_confirm(value: Any, errors: List[str]) -> bool:
    """CONFIRM-Schritt: explizites Boolean ``True`` erwartet."""
    if value is True:
        return True
    errors.append(
        "confirm: Bestaetigung fehlt. Setze den CONFIRM-Schritt auf True, "
        "um die Begruendung abzuschliessen."
    )
    return False


class JustificationFSM:
    """State-Machine, die eine Verordnung gegen eine Begruendungskette prueft.

    Typische Benutzung (non-interactive):

        >>> fsm = JustificationFSM(ergebnis)
        >>> answers = JustificationAnswers({"diagnose": "...", ...})
        >>> justification = fsm.run(answers)
    """

    def __init__(self, ergebnis: AmpelErgebnis) -> None:
        self.ergebnis = ergebnis
        self.required: List[JustificationState] = required_steps_for(ergebnis)

    # ------------------------------------------------------------------
    # Schritte
    # ------------------------------------------------------------------

    @property
    def is_empty(self) -> bool:
        """True wenn die Verordnung keine Begruendung erfordert (GRUEN)."""
        return not self.required

    def iter_steps(self) -> List[JustificationStep]:
        """Liefert die Steps in ihrer Abfrage-Reihenfolge."""
        return [STEPS[state] for state in self.required]

    # ------------------------------------------------------------------
    # Validierung & Lauf
    # ------------------------------------------------------------------

    def validate(self, answers: JustificationAnswers) -> List[str]:
        """Validiert die Antworten gegen die erforderliche Kette.

        Returns:
            Liste von Fehlermeldungen. Leere Liste = alles OK.
        """
        errors: List[str] = []
        for state in self.required:
            step = STEPS[state]
            value = answers.get(state)
            if state == JustificationState.CONFIRM:
                _validate_confirm(value, errors)
            elif step.subfields:
                _validate_subfields_answer(step, value, errors)
            else:
                _validate_string_answer(step, value, errors)
        return errors

    def run(self, answers: JustificationAnswers) -> Justification:
        """Fuehrt die FSM gegen die gegebenen Antworten aus.

        Raises:
            JustificationError: Wenn Pflichtfelder fehlen oder ungueltig sind.
        """
        if self.is_empty:
            # GRUEN: keine Pflicht. Wir liefern trotzdem ein Justification-
            # Objekt zurueck, damit die Aufrufer einen einheitlichen Typ
            # sehen (und um die GRUEN-Entscheidung zu versiegeln).
            return Justification(
                ampel=self.ergebnis.gesamt.value,
                required_states=[],
                answers={},
                confirmed=True,  # implizit, da nichts zu bestaetigen
                off_label=False,
                praxisbesonderheit=None,
            )

        errors = self.validate(answers)
        if errors:
            raise JustificationError(errors)

        cleaned_answers: Dict[str, Any] = {}
        for state in self.required:
            step = STEPS[state]
            raw = answers.get(state)
            if state == JustificationState.CONFIRM:
                cleaned_answers[state.value] = True
                continue
            if step.subfields:
                # Alle Subfields wurden oben validiert; re-use dieselbe
                # Funktion ohne errors-Sammlung, weil hier schon sauber.
                sub_errors: List[str] = []
                cleaned_answers[state.value] = _validate_subfields_answer(
                    step, raw, sub_errors
                )
                continue
            cleaned_answers[state.value] = _validate_string_answer(
                step, raw, []
            )

        praxisbesonderheit = cleaned_answers.get(
            JustificationState.PRAXISBESONDERHEIT.value
        )

        return Justification(
            ampel=self.ergebnis.gesamt.value,
            required_states=[s.value for s in self.required],
            answers=cleaned_answers,
            confirmed=True,
            off_label=JustificationState.BSG_OFF_LABEL in self.required,
            praxisbesonderheit=praxisbesonderheit,
        )
