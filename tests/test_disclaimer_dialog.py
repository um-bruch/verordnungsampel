"""Tests fuer den Erststart-Acknowledgement-Dialog.

Deckt ab:
    1. Dialog ist modal und ohne X schliessbar
    2. Alle vier Pflicht-Checkboxen sind erforderlich, sonst kein Akzeptieren
    3. Akzeptieren-Flow persistiert Timestamp + Hash + Log-Eintrag
    4. Ablehnen-Flow persistiert NICHTS
    5. Persistenz: zweiter Start zeigt Dialog nicht erneut an
    6. Hash-Aenderung erzwingt erneute Bestaetigung
    7. compute_disclaimer_hash ist deterministisch
"""

from __future__ import annotations

import os
import sys

import pytest

pytest.importorskip("PySide6")

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from verordnungsampel.audit.compliance_log import ComplianceLog  # noqa: E402
from verordnungsampel.db.connection import open_database  # noqa: E402
from verordnungsampel.gui import disclaimer_dialog as DD  # noqa: E402


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication(sys.argv)
    yield app


@pytest.fixture
def isolated_env(tmp_path, monkeypatch):
    """Isoliert Regelwerks-DB und Compliance-Log pro Test."""
    from verordnungsampel.utils import paths as path_utils
    from verordnungsampel.db import connection as conn_mod
    from verordnungsampel.audit import compliance_log as log_mod

    monkeypatch.setattr(path_utils, "user_data_dir", lambda: tmp_path)
    monkeypatch.setattr(conn_mod, "user_data_dir", lambda: tmp_path)
    monkeypatch.setattr(log_mod, "user_data_dir", lambda: tmp_path)
    yield tmp_path


# ---------------------------------------------------------------------------
# 1. Dialog-Eigenschaften: modal, kein X
# ---------------------------------------------------------------------------


def test_dialog_ist_modal_und_ohne_x_button(qapp):
    dlg, _state = DD.build_dialog()
    try:
        assert dlg.isModal() is True
        # Close-Button ist entfernt aus WindowFlags
        assert not (dlg.windowFlags() & Qt.WindowCloseButtonHint)
        # Vier Checkboxen vorhanden
        assert len(dlg._checkboxes) == 4
        # Alle zu Beginn unchecked
        assert all(not cb.isChecked() for cb in dlg._checkboxes)
    finally:
        dlg.deleteLater()


# ---------------------------------------------------------------------------
# 2. Alle 4 Checkboxen sind Pflicht
# ---------------------------------------------------------------------------


def test_akzeptieren_ist_erst_aktiv_wenn_alle_vier_gecheckt(qapp):
    dlg, _state = DD.build_dialog()
    try:
        assert dlg._btn_accept.isEnabled() is False
        # Eine nach der anderen aktivieren
        for i, cb in enumerate(dlg._checkboxes):
            cb.setChecked(True)
            qapp.processEvents()
            if i < len(dlg._checkboxes) - 1:
                assert dlg._btn_accept.isEnabled() is False, (
                    f"Button darf noch nicht aktiv sein nach {i+1}/4 Checkboxen"
                )
        # Nach der vierten muss er aktiv sein
        assert dlg._btn_accept.isEnabled() is True
        # Und wieder ausmachen -> inaktiv
        dlg._checkboxes[0].setChecked(False)
        qapp.processEvents()
        assert dlg._btn_accept.isEnabled() is False
    finally:
        dlg.deleteLater()


# ---------------------------------------------------------------------------
# 3. Akzeptieren-Flow: persistiert Timestamp + Hash + Compliance-Log-Eintrag
# ---------------------------------------------------------------------------


def test_akzeptieren_persistiert_und_versiegelt_im_log(qapp, isolated_env):
    conn, _ = open_database()
    log = ComplianceLog()
    try:
        # Mock-Dialog-Fabrik: akzeptiert sofort mit allen 4 Labels
        def factory(parent=None):
            class _Fake:
                def exec(self):
                    return 1

            fake = _Fake()
            st = {
                "accepted": True,
                "labels": [
                    "Label 1",
                    "Label 2",
                    "Label 3",
                    "Label 4",
                ],
            }
            return fake, st

        log_len_before = len(log)
        result = DD.ensure_disclaimer_accepted(
            conn, log, dialog_factory=factory
        )
        assert result is True
        # Settings persistiert
        from verordnungsampel.db.schema import get_setting

        assert get_setting(conn, DD.DISCLAIMER_SETTINGS_KEY) is not None
        stored_hash = get_setting(conn, DD.DISCLAIMER_HASH_KEY)
        expected_hash = DD.compute_disclaimer_hash(DD.load_disclaimer_text())
        assert stored_hash == expected_hash
        # Compliance-Log um 1 groesser
        assert len(log) == log_len_before + 1
        # Letzter Eintrag enthaelt event=first_start_acknowledgement
        last = log.all_entries()[-1]
        assert last.extra.get("event") == "first_start_acknowledgement"
        assert last.extra.get("disclaimer_hash") == expected_hash
        assert last.extra.get("acknowledgements") == [
            "Label 1",
            "Label 2",
            "Label 3",
            "Label 4",
        ]
        # Hash-Chain ist intakt
        assert log.verify_chain() is True
    finally:
        log.close()
        conn.close()


# ---------------------------------------------------------------------------
# 4. Ablehnen-Flow: nichts persistiert, return False
# ---------------------------------------------------------------------------


def test_ablehnen_persistiert_nichts(qapp, isolated_env):
    conn, _ = open_database()
    log = ComplianceLog()
    try:

        def factory(parent=None):
            class _Fake:
                def exec(self):
                    return 0

            fake = _Fake()
            st = {"accepted": False, "labels": []}
            return fake, st

        log_len_before = len(log)
        result = DD.ensure_disclaimer_accepted(
            conn, log, dialog_factory=factory
        )
        assert result is False
        from verordnungsampel.db.schema import get_setting

        assert get_setting(conn, DD.DISCLAIMER_SETTINGS_KEY) is None
        assert get_setting(conn, DD.DISCLAIMER_HASH_KEY) is None
        # Kein Log-Eintrag
        assert len(log) == log_len_before
    finally:
        log.close()
        conn.close()


# ---------------------------------------------------------------------------
# 5. Persistenz: nach Akzeptieren erscheint der Dialog beim zweiten Start nicht
# ---------------------------------------------------------------------------


def test_zweiter_start_zeigt_dialog_nicht_mehr(qapp, isolated_env):
    conn, _ = open_database()
    log = ComplianceLog()
    try:
        # Erste Runde: akzeptieren
        def accept_factory(parent=None):
            class _Fake:
                def exec(self):
                    return 1

            return _Fake(), {
                "accepted": True,
                "labels": ["a", "b", "c", "d"],
            }

        assert DD.ensure_disclaimer_accepted(
            conn, log, dialog_factory=accept_factory
        ) is True
        log_len_after_first = len(log)

        # Zweite Runde: Factory darf NICHT aufgerufen werden
        call_counter = {"n": 0}

        def forbidden_factory(parent=None):
            call_counter["n"] += 1
            raise AssertionError(
                "Dialog wurde erneut aufgerufen, obwohl schon akzeptiert!"
            )

        assert DD.ensure_disclaimer_accepted(
            conn, log, dialog_factory=forbidden_factory
        ) is True
        assert call_counter["n"] == 0
        # Kein neuer Log-Eintrag
        assert len(log) == log_len_after_first
    finally:
        log.close()
        conn.close()


# ---------------------------------------------------------------------------
# 6. Hash-Aenderung erzwingt erneute Bestaetigung
# ---------------------------------------------------------------------------


def test_hash_aenderung_erzwingt_neues_acknowledgement(
    qapp, isolated_env, monkeypatch
):
    conn, _ = open_database()
    log = ComplianceLog()
    try:

        def accept_factory(parent=None):
            class _Fake:
                def exec(self):
                    return 1

            return _Fake(), {
                "accepted": True,
                "labels": ["a", "b", "c", "d"],
            }

        assert DD.ensure_disclaimer_accepted(
            conn, log, dialog_factory=accept_factory
        ) is True

        # NOTICE-Text "aendern" -> anderer Hash
        monkeypatch.setattr(
            DD,
            "load_disclaimer_text",
            lambda: "EIN VOELLIG ANDERER DISCLAIMER-TEXT",
        )

        call_counter = {"n": 0}

        def factory(parent=None):
            call_counter["n"] += 1

            class _Fake:
                def exec(self):
                    return 1

            return _Fake(), {
                "accepted": True,
                "labels": ["x", "y", "z", "w"],
            }

        assert DD.ensure_disclaimer_accepted(
            conn, log, dialog_factory=factory
        ) is True
        # Dialog MUSS erneut gezeigt werden
        assert call_counter["n"] == 1
    finally:
        log.close()
        conn.close()


# ---------------------------------------------------------------------------
# 7. Hash ist deterministisch
# ---------------------------------------------------------------------------


def test_compute_disclaimer_hash_ist_deterministisch():
    text = "Hello Disclaimer"
    h1 = DD.compute_disclaimer_hash(text)
    h2 = DD.compute_disclaimer_hash(text)
    assert h1 == h2
    # Andere Eingabe -> anderer Hash
    assert DD.compute_disclaimer_hash(text + " !") != h1
    # 64 Hex-Zeichen (SHA-256)
    assert len(h1) == 64
