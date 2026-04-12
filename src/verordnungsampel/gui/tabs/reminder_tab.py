"""Reminder-Tab: Quartals-Reminder für Praxisbesonderheiten.

Ruft :func:`engine.praxisbesonderheit.build_quartal_reminder` für das
eingegebene Quartal auf und zeigt das gerenderte Ergebnis an.
"""

from __future__ import annotations

from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from verordnungsampel.audit.compliance_log import ComplianceLog
from verordnungsampel.engine.praxisbesonderheit import (
    build_quartal_reminder,
    render_reminder,
)
from verordnungsampel.gui import strings_de as S


def _current_quartal() -> str:
    """Aktuelles Quartal als ``YYYY-Qn``-String."""
    today = date.today()
    q = (today.month - 1) // 3 + 1
    return f"{today.year}-Q{q}"


class ReminderTab(QWidget):
    """Quartalsreport über Praxisbesonderheiten im Compliance-Log."""

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        top = QHBoxLayout()
        top.addWidget(QLabel(S.REMINDER_QUARTAL))
        self.quartal_edit = QLineEdit(_current_quartal())
        self.quartal_edit.setMaximumWidth(120)
        top.addWidget(self.quartal_edit)
        self.generate_btn = QPushButton(S.REMINDER_GENERATE)
        self.generate_btn.clicked.connect(self.on_generate)
        top.addWidget(self.generate_btn)
        top.addStretch()
        root.addLayout(top)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText(
            "Klicke auf 'Reminder erzeugen', um die Verordnungen mit "
            "Praxisbesonderheit im angegebenen Quartal zu sehen."
        )
        root.addWidget(self.output, stretch=1)

    def on_generate(self) -> None:
        spec = self.quartal_edit.text().strip()
        try:
            with ComplianceLog() as log:
                entries = [e.to_dict() for e in log.all_entries()]
            reminder = build_quartal_reminder(entries, spec)
        except ValueError:
            QMessageBox.warning(self, S.APP_TITLE, S.REMINDER_ERROR)
            return
        except Exception as exc:  # pragma: no cover
            QMessageBox.critical(self, S.APP_TITLE, str(exc))
            return

        self.output.setPlainText(render_reminder(reminder))


__all__ = ["ReminderTab"]
