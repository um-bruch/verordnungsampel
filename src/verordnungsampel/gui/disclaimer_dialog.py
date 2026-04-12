"""Erststart-Acknowledgement-Dialog.

Umsetzung der Empfehlung 10.2 aus ``docs/legal/RECHTSGUTACHTEN_HAFTUNG.md``.

Beim ersten GUI-Start wird ein modaler Dialog gezeigt, der den Nutzer
zwingt, vier Pflicht-Checkboxen anzuhaken, bevor die Anwendung weiter
genutzt werden kann:

1. Tool nicht klinisch validiert
2. Kein Medizinprodukt, nicht zertifiziert
3. Ärztliche Verantwortung liegt beim Arzt
4. Nutzung auf eigenes Risiko (§ 521 BGB)

Bestätigung wird:

- Im Compliance-Log (Hash-Chain) versiegelt --> Beweisbarkeit
- In der Regelwerks-DB (``settings``-Tabelle) als ``disclaimer_accepted_at``
  und ``disclaimer_hash`` persistiert --> schneller Lookup beim nächsten
  Start

Erneute Anzeige ist nötig, wenn:

- ``disclaimer_accepted_at`` fehlt, ODER
- ``disclaimer_hash`` nicht mehr mit dem aktuellen NOTICE-Text übereinstimmt
  (Version wurde aktualisiert --> neues Acknowledgement), ODER
- die Hash-Kette des Compliance-Logs gebrochen ist (Manipulation).

Der Dialog ist bewusst so robust gebaut, dass er ohne PySide6 importierbar
bleibt. PySide6-Imports erfolgen erst innerhalb der Funktionen.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from verordnungsampel.gui import strings_de as S


# NOTICE-Datei: liegt im Repo-Root (parent x 4 vom Modul-Pfad).
# Wir laden sie zur Laufzeit, um den Hash aktuell zu halten.
_MODULE_DIR = Path(__file__).resolve().parent
_REPO_ROOT_CANDIDATES = [
    _MODULE_DIR.parent.parent.parent,  # src/verordnungsampel/gui -> repo root
    _MODULE_DIR.parent.parent.parent.parent,  # zur Sicherheit
]

DISCLAIMER_SETTINGS_KEY = "disclaimer_accepted_at"
DISCLAIMER_HASH_KEY = "disclaimer_hash"
DISCLAIMER_VERSION = "1.0"

# Fallback-Text, falls NOTICE nicht gefunden wird. Inhaltlich identisch
# mit den vier Pflicht-Checkboxen + NOTICE-Kernpunkten.
_FALLBACK_DISCLAIMER_TEXT = (
    "VerordnungsAmpel ist ein Informations- und Nachschlagewerk.\n"
    "- Kein Medizinprodukt im Sinne der MDR (EU) 2017/745\n"
    "- Nicht klinisch validiert\n"
    "- Nicht durch BfArM oder Benannte Stelle geprüft oder zertifiziert\n"
    "- Kein Wartungsvertrag, kein Support-Versprechen\n"
    "Die ärztliche Verantwortung bleibt beim Arzt (§ 76 SGB V, § 630a BGB).\n"
    "Haftung auf Vorsatz und grobe Fahrlässigkeit beschränkt (§ 521 BGB)."
)


def load_disclaimer_text() -> str:
    """Liest den Haftungstext aus der NOTICE-Datei.

    Fällt auf einen statischen Fallback zurück, wenn NOTICE nicht gefunden
    werden kann (z.B. in installierten Wheels ohne Repo-Layout).
    """
    for candidate in _REPO_ROOT_CANDIDATES:
        notice_path = candidate / "NOTICE"
        if notice_path.is_file():
            try:
                return notice_path.read_text(encoding="utf-8")
            except OSError:
                continue
    return _FALLBACK_DISCLAIMER_TEXT


def compute_disclaimer_hash(text: str) -> str:
    """SHA-256 des Disclaimer-Textes (hex)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def disclaimer_is_accepted(
    conn,
    compliance_log,
    *,
    current_hash: Optional[str] = None,
) -> bool:
    """Prüft, ob der aktuelle Disclaimer bereits akzeptiert wurde.

    Args:
        conn: Geöffnete Regelwerks-DB-Connection (mit ``settings``-Tabelle).
        compliance_log: :class:`ComplianceLog`-Instanz (oder Mock).
        current_hash: Aktueller Hash des Disclaimer-Textes. Wird berechnet,
            wenn ``None``.

    Returns:
        ``True`` nur dann, wenn
        (a) ein Timestamp in ``settings`` hinterlegt ist,
        (b) der gespeicherte Hash == aktueller Hash, und
        (c) die Compliance-Log-Hash-Chain intakt ist.
    """
    if current_hash is None:
        current_hash = compute_disclaimer_hash(load_disclaimer_text())

    try:
        from verordnungsampel.db.schema import get_setting

        accepted_at = get_setting(conn, DISCLAIMER_SETTINGS_KEY)
        stored_hash = get_setting(conn, DISCLAIMER_HASH_KEY)
    except Exception:  # pragma: no cover - defensive
        return False

    if not accepted_at or not stored_hash:
        return False
    if stored_hash != current_hash:
        return False

    # Hash-Chain muss intakt sein. Wenn nicht, erneut bestätigen lassen.
    try:
        if not compliance_log.verify_chain():
            return False
    except Exception:  # pragma: no cover - defensive
        return False
    return True


def record_acceptance(
    conn,
    compliance_log,
    *,
    text: str,
    acknowledged_labels: list[str],
    timestamp: Optional[str] = None,
) -> str:
    """Persistiert die Bestätigung.

    Args:
        conn: Regelwerks-DB-Connection.
        compliance_log: :class:`ComplianceLog`.
        text: Der exakte Disclaimer-Text, den der Nutzer gesehen hat.
        acknowledged_labels: Die vier angezeigten Checkbox-Labels.
        timestamp: Optional (für Tests). Default: aktueller UTC-Zeitpunkt.

    Returns:
        Der Hash des Disclaimer-Textes (für Logging/Tests).
    """
    from verordnungsampel.db.schema import save_setting

    if timestamp is None:
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    disclaimer_hash = compute_disclaimer_hash(text)

    save_setting(conn, DISCLAIMER_SETTINGS_KEY, timestamp)
    save_setting(conn, DISCLAIMER_HASH_KEY, disclaimer_hash)

    # Zusätzlich im Compliance-Log versiegeln (Hash-Chain).
    extra = {
        "event": "first_start_acknowledgement",
        "disclaimer_version": DISCLAIMER_VERSION,
        "disclaimer_hash": disclaimer_hash,
        "acknowledgements": acknowledged_labels,
    }
    compliance_log.append(
        icd="-",
        atc="-",
        ampel="-",
        begruendung="Erststart-Acknowledgement: Nutzer hat alle 4 Pflicht-Checkboxen bestätigt.",
        timestamp=timestamp,
        extra=extra,
    )
    return disclaimer_hash


# ---------------------------------------------------------------------------
# PySide6-Dialog
# ---------------------------------------------------------------------------


def build_dialog(parent=None):
    """Baut einen :class:`QDialog` mit den vier Pflicht-Checkboxen.

    PySide6 wird erst hier importiert, damit das Modul in headless-Tests
    (Compliance-Logik) ohne PySide6 lauffähig bleibt.

    Returns:
        Tuple ``(dialog, state)`` wobei ``state`` ein Dict mit
        ``{"accepted": bool, "labels": list[str]}`` ist, das nach Dialog-
        Ende ausgewertet werden kann.
    """
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QCheckBox,
        QDialog,
        QDialogButtonBox,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QTextEdit,
        QVBoxLayout,
    )

    state = {"accepted": False, "labels": []}

    dlg = QDialog(parent)
    dlg.setWindowTitle(S.DISCLAIMER_DIALOG_TITLE)
    dlg.setModal(True)
    # X-Button deaktivieren (nur Akzeptieren/Ablehnen erlaubt)
    dlg.setWindowFlags(
        (dlg.windowFlags() | Qt.CustomizeWindowHint)
        & ~Qt.WindowCloseButtonHint
    )
    dlg.resize(620, 620)

    layout = QVBoxLayout(dlg)

    headline = QLabel(S.DISCLAIMER_DIALOG_HEADLINE)
    headline.setWordWrap(True)
    headline_font = headline.font()
    headline_font.setBold(True)
    headline.setFont(headline_font)
    layout.addWidget(headline)

    # Disclaimer-Text (aus NOTICE)
    text_view = QTextEdit()
    text_view.setReadOnly(True)
    text_view.setPlainText(load_disclaimer_text())
    text_view.setObjectName("disclaimer_text_view")
    layout.addWidget(text_view, 1)

    # Pflicht-Checkboxen (Reihenfolge = Haftungsgutachten 10.2)
    labels = [
        S.DISCLAIMER_CHECK_NOT_VALIDATED,
        S.DISCLAIMER_CHECK_NOT_CERTIFIED,
        S.DISCLAIMER_CHECK_DOCTOR_RESPONSIBILITY,
        S.DISCLAIMER_CHECK_OWN_RISK,
    ]
    checkboxes: list[QCheckBox] = []
    for label in labels:
        cb = QCheckBox(label)
        cb.setChecked(False)
        layout.addWidget(cb)
        checkboxes.append(cb)

    info = QLabel(S.DISCLAIMER_INFO_BUTTONS)
    info.setWordWrap(True)
    info.setStyleSheet("color: gray; font-size: 10pt;")
    layout.addWidget(info)

    # Buttons
    button_row = QHBoxLayout()
    btn_reject = QPushButton(S.DISCLAIMER_BTN_REJECT)
    btn_accept = QPushButton(S.DISCLAIMER_BTN_ACCEPT)
    btn_accept.setEnabled(False)
    btn_accept.setDefault(True)
    button_row.addWidget(btn_reject)
    button_row.addStretch(1)
    button_row.addWidget(btn_accept)
    layout.addLayout(button_row)

    def _update_accept_enabled() -> None:
        btn_accept.setEnabled(all(cb.isChecked() for cb in checkboxes))

    for cb in checkboxes:
        cb.toggled.connect(_update_accept_enabled)

    def _on_accept() -> None:
        state["accepted"] = True
        state["labels"] = [cb.text() for cb in checkboxes]
        dlg.accept()

    def _on_reject() -> None:
        state["accepted"] = False
        state["labels"] = []
        dlg.reject()

    btn_accept.clicked.connect(_on_accept)
    btn_reject.clicked.connect(_on_reject)

    # Für Tests: Referenzen auf Kinderwidgets ankoppeln
    dlg._checkboxes = checkboxes  # type: ignore[attr-defined]
    dlg._btn_accept = btn_accept  # type: ignore[attr-defined]
    dlg._btn_reject = btn_reject  # type: ignore[attr-defined]
    dlg._text_view = text_view  # type: ignore[attr-defined]

    return dlg, state


def ensure_disclaimer_accepted(
    conn,
    compliance_log,
    *,
    parent=None,
    dialog_factory: Optional[Callable] = None,
) -> bool:
    """Prüft Persistenz und zeigt den Dialog nur bei Bedarf.

    Args:
        conn: Regelwerks-DB-Connection (mit ``settings``-Tabelle).
        compliance_log: :class:`ComplianceLog`-Instanz.
        parent: Qt-Parent (optional).
        dialog_factory: Für Tests: alternative Dialog-Fabrik, die statt
            :func:`build_dialog` einen Mock-Dialog liefert.

    Returns:
        ``True`` wenn bereits akzeptiert war oder der Nutzer jetzt akzeptiert,
        ``False`` wenn abgelehnt.
    """
    text = load_disclaimer_text()
    current_hash = compute_disclaimer_hash(text)

    if disclaimer_is_accepted(
        conn, compliance_log, current_hash=current_hash
    ):
        return True

    factory = dialog_factory or build_dialog
    dlg, state = factory(parent)
    dlg.exec()
    if not state["accepted"]:
        return False

    record_acceptance(
        conn,
        compliance_log,
        text=text,
        acknowledged_labels=state["labels"],
    )
    return True


__all__ = [
    "DISCLAIMER_HASH_KEY",
    "DISCLAIMER_SETTINGS_KEY",
    "DISCLAIMER_VERSION",
    "build_dialog",
    "compute_disclaimer_hash",
    "disclaimer_is_accepted",
    "ensure_disclaimer_accepted",
    "load_disclaimer_text",
    "record_acceptance",
]
