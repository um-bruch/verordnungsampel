"""Workflow-Tab: Vorab-Klärungs-Workflow-Text generieren.

Zieht das ``AmpelErgebnis`` aus dem Check-Tab und nutzt
:func:`output.vorab_workflow.build_workflow`, um den passenden
Antrags-/Hinweis-/Stellungnahme-Text zu erzeugen. Mit Buttons zum
Kopieren in die Zwischenablage und zum Speichern als TXT-Datei.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from verordnungsampel.engine.evaluator import AmpelErgebnis
from verordnungsampel.gui import strings_de as S
from verordnungsampel.output import (
    WorkflowContext,
    WorkflowType,
    build_workflow,
    determine_workflow,
)


class WorkflowTab(QWidget):
    """Generiert den Vorab-Klärungs-Workflow-Text."""

    def __init__(self) -> None:
        super().__init__()
        self._ergebnis: Optional[AmpelErgebnis] = None
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        self.hint_label = QLabel(S.WORKFLOW_INTRO)
        self.hint_label.setWordWrap(True)
        root.addWidget(self.hint_label)

        context_box = QGroupBox("Praxis- / Arzt- / KK-Daten (alle optional)")
        form = QFormLayout(context_box)
        self.praxis_edit = QLineEdit()
        self.praxis_adr_edit = QLineEdit()
        self.arzt_edit = QLineEdit()
        self.bsnr_edit = QLineEdit()
        self.lanr_edit = QLineEdit()
        self.kk_edit = QLineEdit()
        self.patient_edit = QLineEdit()
        self.patient_edit.setPlaceholderText("Praxis-internes Kürzel (NICHT Klarname!)")

        form.addRow(S.WORKFLOW_PRAXIS, self.praxis_edit)
        form.addRow(S.WORKFLOW_PRAXIS_ADRESSE, self.praxis_adr_edit)
        form.addRow(S.WORKFLOW_ARZT, self.arzt_edit)
        form.addRow(S.WORKFLOW_BSNR, self.bsnr_edit)
        form.addRow(S.WORKFLOW_LANR, self.lanr_edit)
        form.addRow(S.WORKFLOW_KK, self.kk_edit)
        form.addRow(S.WORKFLOW_PATIENT, self.patient_edit)
        root.addWidget(context_box)

        btn_row = QHBoxLayout()
        self.generate_btn = QPushButton(S.WORKFLOW_GENERATE)
        self.generate_btn.clicked.connect(self.on_generate)
        btn_row.addWidget(self.generate_btn)
        btn_row.addStretch()
        self.copy_btn = QPushButton(S.WORKFLOW_COPY)
        self.copy_btn.clicked.connect(self.on_copy)
        self.copy_btn.setEnabled(False)
        btn_row.addWidget(self.copy_btn)
        self.save_btn = QPushButton(S.WORKFLOW_SAVE)
        self.save_btn.clicked.connect(self.on_save)
        self.save_btn.setEnabled(False)
        btn_row.addWidget(self.save_btn)
        root.addLayout(btn_row)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlainText(S.WORKFLOW_NO_DATA)
        root.addWidget(self.output, stretch=1)

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_ergebnis(self, ergebnis: Optional[AmpelErgebnis]) -> None:
        self._ergebnis = ergebnis
        if ergebnis is None:
            self.output.setPlainText(S.WORKFLOW_NO_DATA)
            self.generate_btn.setEnabled(False)
            self.copy_btn.setEnabled(False)
            self.save_btn.setEnabled(False)
            return
        self.generate_btn.setEnabled(True)
        wf_type = determine_workflow(ergebnis)
        if wf_type == WorkflowType.KEINE_AKTION:
            self.output.setPlainText(S.WORKFLOW_KEINE_AKTION)
        else:
            self.output.setPlainText(
                f"Workflow-Typ: {wf_type.value}\n\n"
                "Trage Praxis-/Arzt-/KK-Daten ein und klicke auf "
                "'Text generieren', um das Dokument zu erzeugen."
            )
        self.copy_btn.setEnabled(False)
        self.save_btn.setEnabled(False)

    # ------------------------------------------------------------------
    # Handler
    # ------------------------------------------------------------------

    def _context(self) -> WorkflowContext:
        return WorkflowContext(
            praxis_name=self.praxis_edit.text().strip() or None,
            praxis_adresse=self.praxis_adr_edit.text().strip() or None,
            arzt_name=self.arzt_edit.text().strip() or None,
            bsnr=self.bsnr_edit.text().strip() or None,
            lanr=self.lanr_edit.text().strip() or None,
            kk_name=self.kk_edit.text().strip() or None,
            patient_kennung=self.patient_edit.text().strip() or None,
        )

    def on_generate(self) -> None:
        if self._ergebnis is None:
            return
        output = build_workflow(self._ergebnis, self._context())
        self.output.setPlainText(output.render_full())
        has_text = output.workflow_type != WorkflowType.KEINE_AKTION
        self.copy_btn.setEnabled(has_text)
        self.save_btn.setEnabled(has_text)

    def on_copy(self) -> None:
        from PySide6.QtWidgets import QApplication

        QApplication.clipboard().setText(self.output.toPlainText())
        QMessageBox.information(self, S.APP_TITLE, S.WORKFLOW_COPIED)

    def on_save(self) -> None:
        erg = self._ergebnis
        default_name = "workflow.txt"
        if erg is not None:
            default_name = f"workflow_{erg.icd}_{erg.atc}.txt".replace("/", "_")
        path, _ = QFileDialog.getSaveFileName(
            self, S.WORKFLOW_SAVE, default_name, "Textdateien (*.txt)"
        )
        if not path:
            return
        Path(path).write_text(self.output.toPlainText(), encoding="utf-8")
        QMessageBox.information(
            self, S.APP_TITLE, S.WORKFLOW_SAVED.format(path=path)
        )


__all__ = ["WorkflowTab"]
