"""Log-Tab: Compliance-Log anzeigen + Hash-Chain prüfen.

Zeigt alle Einträge des :class:`ComplianceLog` als Tabelle und bietet
einen Button für die Hash-Chain-Verifikation (``verify_chain``).
"""

from __future__ import annotations

from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from verordnungsampel.audit.compliance_log import ComplianceLog, LogEintrag
from verordnungsampel.gui import strings_de as S


class LogTab(QWidget):
    """Tabellen-Ansicht des Compliance-Logs."""

    COLUMNS = ["Seq", "Timestamp", "ICD", "ATC", "Ampel", "Container", "Hash", "Marker"]

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        btn_row = QHBoxLayout()
        self.refresh_btn = QPushButton(S.LOG_REFRESH)
        self.refresh_btn.clicked.connect(self.refresh)
        btn_row.addWidget(self.refresh_btn)

        self.verify_btn = QPushButton(S.LOG_VERIFY)
        self.verify_btn.clicked.connect(self.on_verify)
        btn_row.addWidget(self.verify_btn)

        btn_row.addStretch()
        self.count_label = QLabel("")
        btn_row.addWidget(self.count_label)

        root.addLayout(btn_row)

        self.table = QTableWidget(0, len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        root.addWidget(self.table, stretch=1)

    # ------------------------------------------------------------------
    # Handler
    # ------------------------------------------------------------------

    def refresh(self) -> None:
        try:
            with ComplianceLog() as log:
                entries: List[LogEintrag] = log.all_entries()
        except Exception as exc:  # pragma: no cover - defensiv
            QMessageBox.warning(self, S.APP_TITLE, str(exc))
            return

        self.table.setRowCount(0)
        if not entries:
            self.count_label.setText(S.LOG_EMPTY)
            return

        self.count_label.setText(f"{len(entries)} Eintrag/Einträge")
        self.table.setRowCount(len(entries))
        for row, e in enumerate(entries):
            markers = []
            if isinstance(e.extra, dict):
                if e.extra.get("justification", {}).get("required_states"):
                    markers.append("+begruendung")
                if "workflow" in e.extra:
                    wf_type = e.extra["workflow"].get("workflow_type", "?")
                    markers.append(f"+wf:{wf_type}")
                pbs = e.extra.get("praxisbesonderheiten") or []
                if pbs:
                    markers.append(f"+pb:{len(pbs)}")
            values = [
                str(e.seq),
                e.timestamp,
                e.icd,
                e.atc,
                e.ampel.upper(),
                e.container or "",
                (e.hash or "")[:12] + "…" if e.hash else "",
                ", ".join(markers),
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                if col == 4:  # Ampel farbig
                    color_map = {
                        "GRUEN": "#2e7d32",
                        "GELB": "#f9a825",
                        "ROT": "#c62828",
                    }
                    color = color_map.get(val, "#333")
                    item.setForeground(Qt.GlobalColor.black)
                    item.setData(Qt.ForegroundRole, None)
                    from PySide6.QtGui import QBrush, QColor
                    item.setForeground(QBrush(QColor(color)))
                self.table.setItem(row, col, item)

    def on_verify(self) -> None:
        try:
            with ComplianceLog() as log:
                ok = log.verify_chain()
                n = len(log)
        except Exception as exc:  # pragma: no cover
            QMessageBox.critical(self, S.APP_TITLE, str(exc))
            return
        if ok:
            QMessageBox.information(
                self, S.APP_TITLE, S.LOG_VERIFY_OK.format(n=n)
            )
        else:
            QMessageBox.critical(self, S.APP_TITLE, S.LOG_VERIFY_FAIL)


__all__ = ["LogTab"]
