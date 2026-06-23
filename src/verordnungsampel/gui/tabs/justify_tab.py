"""Justify-Tab: strukturierte Begründungspflicht als Formular.

Erst aktiv, wenn ein GELB/ROT-Ergebnis vom Check-Tab kommt. Die Felder
werden dynamisch aus :class:`JustificationFSM` rekonstruiert, damit die
Reihenfolge (inkl. optionalem BSG-Off-Label und Praxisbesonderheit)
immer der Engine-Logik folgt.

Versiegelung läuft identisch zur CLI: ``ComplianceLog.append`` mit
``extra.justification`` = :meth:`Justification.to_dict`.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from verordnungsampel import __version__
from verordnungsampel.audit.compliance_log import ComplianceLog
from verordnungsampel.engine.evaluator import AmpelErgebnis
from verordnungsampel.engine.justification_fsm import (
    STEPS,
    Justification,
    JustificationAnswers,
    JustificationError,
    JustificationFSM,
    JustificationState,
)
from verordnungsampel.gui import strings_de as S


class JustifyTab(QWidget):
    """Formular für die strukturierte Begründungskette."""

    def __init__(self) -> None:
        super().__init__()
        self._ergebnis: Optional[AmpelErgebnis] = None
        self._fsm: Optional[JustificationFSM] = None
        # Widgets pro State: Dict[JustificationState, widget-spec]
        self._widgets: Dict[JustificationState, Any] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        self.hint_label = QLabel(S.JUSTIFY_NO_DATA)
        self.hint_label.setWordWrap(True)
        root.addWidget(self.hint_label)

        # Scrollbarer Container für Formular
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.form_host = QWidget()
        self.form_layout = QVBoxLayout(self.form_host)
        self.form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.form_host)
        root.addWidget(self.scroll, stretch=1)

        # Bestätigung + Submit
        self.confirm_chk = QCheckBox(S.JUSTIFY_CONFIRM)
        root.addWidget(self.confirm_chk)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.submit_btn = QPushButton(S.JUSTIFY_SUBMIT)
        self.submit_btn.clicked.connect(self.on_submit)
        btn_row.addWidget(self.submit_btn)
        root.addLayout(btn_row)

        self._set_form_enabled(False)

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_ergebnis(self, ergebnis: Optional[AmpelErgebnis]) -> None:
        """Wird vom MainWindow aufgerufen, wenn der Check ein neues Ergebnis liefert."""
        self._ergebnis = ergebnis
        self._clear_form()

        if ergebnis is None:
            self.hint_label.setText(S.JUSTIFY_NO_DATA)
            self._set_form_enabled(False)
            return

        self._fsm = JustificationFSM(ergebnis)
        if self._fsm.is_empty:
            self.hint_label.setText(S.JUSTIFY_GRUEN_HINT)
            self._set_form_enabled(False)
            return

        self.hint_label.setText(
            f"{S.JUSTIFY_INTRO}\n\nAmpel: {ergebnis.gesamt.value.upper()}  |  "
            f"ICD={ergebnis.icd}  ATC={ergebnis.atc}"
        )
        self._build_form(self._fsm)
        self._set_form_enabled(True)

    def _clear_form(self) -> None:
        # Alle Child-Widgets im form_layout entfernen
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        self._widgets.clear()
        self.confirm_chk.setChecked(False)

    def _set_form_enabled(self, enabled: bool) -> None:
        self.scroll.setEnabled(enabled)
        self.confirm_chk.setEnabled(enabled)
        self.submit_btn.setEnabled(enabled)

    def _build_form(self, fsm: JustificationFSM) -> None:
        """Legt pro erforderlichem State ein Eingabe-Widget an."""
        for step in fsm.iter_steps():
            if step.state == JustificationState.CONFIRM:
                continue

            box = QGroupBox(step.prompt)
            box_layout = QVBoxLayout(box)
            hint = QLabel(step.help_text)
            hint.setWordWrap(True)
            hint.setStyleSheet("color:#555; font-size:10px;")
            box_layout.addWidget(hint)

            if step.subfields:
                form = QFormLayout()
                sub_edits: Dict[str, QLineEdit] = {}
                for sub in step.subfields:
                    edit = QLineEdit()
                    label = sub.replace("_", " ").capitalize() + ":"
                    form.addRow(label, edit)
                    sub_edits[sub] = edit
                box_layout.addLayout(form)
                self._widgets[step.state] = ("subfields", sub_edits)
            else:
                edit = QTextEdit()
                edit.setPlaceholderText(
                    "(optional)" if step.min_length == 0 else "Pflichtfeld"
                )
                edit.setFixedHeight(70)
                box_layout.addWidget(edit)
                self._widgets[step.state] = ("text", edit)

            self.form_layout.addWidget(box)

    # ------------------------------------------------------------------
    # Submit
    # ------------------------------------------------------------------

    def _collect_answers(self) -> JustificationAnswers:
        answers = JustificationAnswers()
        for state, spec in self._widgets.items():
            kind, widget = spec
            if kind == "text":
                answers.set(state, widget.toPlainText().strip())
            elif kind == "subfields":
                sub_dict: Dict[str, str] = {}
                for sub_name, edit in widget.items():
                    sub_dict[sub_name] = edit.text().strip()
                answers.set(state, sub_dict)
        answers.set(JustificationState.CONFIRM, bool(self.confirm_chk.isChecked()))
        return answers

    def on_submit(self) -> None:
        if self._fsm is None or self._ergebnis is None:
            return
        answers = self._collect_answers()
        try:
            justification = self._fsm.run(answers)
        except JustificationError as exc:
            QMessageBox.warning(
                self,
                S.APP_TITLE,
                S.JUSTIFY_ERROR_HEAD + "\n\n- " + "\n- ".join(exc.errors),
            )
            return

        try:
            self._seal(justification)
        except Exception as exc:  # pragma: no cover - DB-Robustheit
            QMessageBox.critical(
                self,
                S.APP_TITLE,
                f"Log-Versiegelung fehlgeschlagen: {exc}",
            )
            return

        QMessageBox.information(self, S.APP_TITLE, S.JUSTIFY_SUCCESS)

    def _seal(self, justification: Justification) -> None:
        erg = self._ergebnis
        extra: Dict[str, Any] = {
            "version": __version__,
            "source": "gui",
            "justification": justification.to_dict(),
        }
        zusammenfassung = "; ".join(t.begruendung for t in erg.treffer)
        with ComplianceLog() as log:
            log.append(
                icd=erg.icd,
                atc=erg.atc,
                alter=erg.alter,
                ampel=erg.gesamt.value,
                begruendung=zusammenfassung,
                container=";".join(erg.container_hinweise) or None,
                nutzer="gui",
                extra=extra,
            )


__all__ = ["JustifyTab"]
