"""Check-Tab: ICD + ATC + Alter → Ampel-Bewertung.

Ruft die bestehende Engine (``engine.evaluator.evaluate``) auf und zeigt
das Ergebnis als farbige Ampel-Box mit allen Begründungen und Quellen.
"""

from __future__ import annotations

import html
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from verordnungsampel import __version__
from verordnungsampel.audit.compliance_log import ComplianceLog
from verordnungsampel.db.connection import open_database
from verordnungsampel.db.seed import ensure_seed_data
from verordnungsampel.engine.evaluator import Ampel, AmpelErgebnis, evaluate
from verordnungsampel.engine.praxisbesonderheit import find_matching
from verordnungsampel.gui import strings_de as S


AMPEL_STYLE = {
    Ampel.GRUEN: ("#2e7d32", "#a5d6a7", S.AMPEL_GRUEN),
    Ampel.GELB: ("#f9a825", "#fff59d", S.AMPEL_GELB),
    Ampel.ROT: ("#c62828", "#ef9a9a", S.AMPEL_ROT),
}


def _html(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


class CheckTab(QWidget):
    """Hauptbildschirm: Verordnung eingeben und bewerten."""

    #: ``AmpelErgebnis`` nach erfolgreicher Prüfung
    result_ready = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)

        form_box = QGroupBox("Eingabe")
        form = QFormLayout(form_box)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.icd_edit = QLineEdit()
        self.icd_edit.setPlaceholderText("z.B. I10")
        self.atc_edit = QLineEdit()
        self.atc_edit.setPlaceholderText("z.B. C09AA02")

        self.age_spin = QSpinBox()
        self.age_spin.setRange(-1, 120)
        self.age_spin.setSpecialValueText("—")
        self.age_spin.setValue(-1)  # "kein Alter angegeben"

        form.addRow(QLabel(S.CHECK_ICD_LABEL), self.icd_edit)
        form.addRow(QLabel(S.CHECK_ATC_LABEL), self.atc_edit)
        form.addRow(QLabel(S.CHECK_AGE_LABEL), self.age_spin)

        self.no_log_chk = QCheckBox(S.CHECK_NO_LOG)
        form.addRow(self.no_log_chk)

        self.check_btn = QPushButton(S.CHECK_BUTTON)
        self.check_btn.setDefault(True)
        self.check_btn.clicked.connect(self.on_check)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.check_btn)
        form.addRow(btn_row)

        root.addWidget(form_box)

        # Ampel-Box
        self.ampel_label = QLabel(S.AMPEL_NONE)
        self.ampel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ampel_label.setMinimumHeight(60)
        self.ampel_label.setFrameShape(QFrame.StyledPanel)
        f = QFont()
        f.setPointSize(20)
        f.setBold(True)
        self.ampel_label.setFont(f)
        self._set_ampel_display(None)
        root.addWidget(self.ampel_label)

        # Details
        self.details = QTextBrowser()
        self.details.setOpenExternalLinks(True)
        self.details.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.details.setPlainText(S.CHECK_HINT_EMPTY)
        root.addWidget(self.details, stretch=1)

        hint = QLabel(S.HINT_NOT_MEDICAL_DEVICE)
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #666; font-size: 10px;")
        root.addWidget(hint)

    # ------------------------------------------------------------------
    # Handler
    # ------------------------------------------------------------------

    def on_check(self) -> None:
        icd = self.icd_edit.text().strip()
        atc = self.atc_edit.text().strip()
        if not icd or not atc:
            QMessageBox.warning(self, S.APP_TITLE, S.CHECK_ERROR_MISSING)
            return

        alter_raw = self.age_spin.value()
        alter: Optional[int] = alter_raw if alter_raw >= 0 else None

        try:
            conn, _ = open_database()
            try:
                ensure_seed_data(conn)
                ergebnis = evaluate(icd, atc, alter=alter, conn=conn)
                pbs = find_matching(icd, atc, conn=conn)
            finally:
                conn.close()
        except Exception as exc:  # pragma: no cover - IO/DB robust
            QMessageBox.critical(
                self,
                S.APP_TITLE,
                S.CHECK_ERROR_GENERIC.format(msg=str(exc)),
            )
            return

        self._set_ampel_display(ergebnis.gesamt)
        self._render_details(ergebnis, pbs)

        if not self.no_log_chk.isChecked():
            self._write_log(ergebnis, pbs)

        # Signal für Justify/Workflow-Tabs + Tray-Icon
        self.result_ready.emit(ergebnis)

    # ------------------------------------------------------------------
    # Darstellung
    # ------------------------------------------------------------------

    def _set_ampel_display(self, ampel: Optional[Ampel]) -> None:
        if ampel is None:
            self.ampel_label.setText(S.AMPEL_NONE)
            self.ampel_label.setStyleSheet(
                "background:#eeeeee; color:#555; border:1px solid #bbb; border-radius:6px;"
            )
            return
        fg, bg, text = AMPEL_STYLE[ampel]
        self.ampel_label.setText(text)
        self.ampel_label.setStyleSheet(
            f"background:{bg}; color:{fg}; border:2px solid {fg}; border-radius:6px;"
        )

    def _render_details(self, ergebnis: AmpelErgebnis, pbs) -> None:
        lines = []
        # Alle variablen Inhalte laufen in setHtml; auch DB-Felder sind daher zu escapen.
        header = f"ICD={_html(ergebnis.icd)}  ATC={_html(ergebnis.atc)}"
        if ergebnis.alter is not None:
            header += f"  Alter={_html(ergebnis.alter)}"
        lines.append(f"<h3>{header}</h3>")

        # Hinweis bei DEFAULT_GRUEN (= kein Treffer)
        only_default = (
            len(ergebnis.treffer) == 1
            and ergebnis.treffer[0].regel_kuerzel == "DEFAULT_GRUEN"
        )
        if only_default:
            lines.append(f"<p><i>{S.CHECK_HINT_UNKNOWN}</i></p>")

        lines.append(f"<b>{S.CHECK_SOURCES_LABEL}</b><ul>")
        for t in ergebnis.treffer:
            color = AMPEL_STYLE[t.ampel][0]
            kuerzel = f"<span style='color:{color};'><b>[{t.ampel.value.upper()}]</b></span>"
            lines.append(f"<li>{kuerzel} <b>{_html(t.regel_kuerzel)}</b>: {_html(t.begruendung)}")
            if t.quelle:
                src = f"{_html(t.quelle.kuerzel)} — {_html(t.quelle.titel)}"
                if t.quelle.stand:
                    src += f", Stand {_html(t.quelle.stand)}"
                if t.quelle.url:
                    url = _html(t.quelle.url)
                    src = f"<a href='{url}'>{src}</a>"
                lines.append(f"<br/><small>Quelle: {src}</small>")
            if t.container:
                lines.append(f"<br/><small>Container: <code>{_html(t.container)}</code></small>")
            lines.append("</li>")
        lines.append("</ul>")

        if ergebnis.container_hinweise:
            lines.append(
                "<b>Container-Hinweise:</b> "
                + ", ".join(f"<code>{_html(c)}</code>" for c in ergebnis.container_hinweise)
            )

        if pbs:
            lines.append(f"<p><b>{S.CHECK_PB_LABEL}</b></p><ul>")
            for pb in pbs:
                q = f" ({_html(pb.quelle.kuerzel)})" if pb.quelle else ""
                lines.append(f"<li>{_html(pb.bezeichnung)}{q}</li>")
            lines.append("</ul>")
            lines.append(
                "<small>Nicht vergessen: KV-Kennziffer auf dem "
                "Behandlungsschein markieren (LSG BW 15.11.2023).</small>"
            )

        self.details.setHtml("\n".join(lines))

    def _write_log(self, ergebnis: AmpelErgebnis, pbs) -> None:
        extra = {"version": __version__, "source": "gui"}
        if pbs:
            extra["praxisbesonderheiten"] = [pb.to_dict() for pb in pbs]
        try:
            with ComplianceLog() as log:
                zusammenfassung = "; ".join(t.begruendung for t in ergebnis.treffer)
                log.append(
                    icd=ergebnis.icd,
                    atc=ergebnis.atc,
                    alter=ergebnis.alter,
                    ampel=ergebnis.gesamt.value,
                    begruendung=zusammenfassung,
                    container=";".join(ergebnis.container_hinweise) or None,
                    nutzer="gui",
                    extra=extra,
                )
        except Exception as exc:  # pragma: no cover - defensiv
            QMessageBox.warning(
                self,
                S.APP_TITLE,
                f"Eintrag konnte nicht in den Compliance-Log geschrieben werden: {exc}",
            )


__all__ = ["CheckTab"]
