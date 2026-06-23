"""Regressionstests — bugfix-library-transfer Batch #20 (2026-06-21).

Geprüfte Patterns:
  D2 — deprecated PySide6-Enums (7 Dateien + log_tab QHeaderView/QTableWidget)
  U2 — json.load/json.loads ohne JSONDecodeError-Handler (3 Dateien)
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC = ROOT / "src" / "verordnungsampel"

DISCLAIMER    = SRC / "gui" / "disclaimer_dialog.py"
APP           = SRC / "gui" / "app.py"
MAIN_WIN      = SRC / "gui" / "main_window.py"
CHECK_TAB     = SRC / "gui" / "tabs" / "check_tab.py"
LOG_TAB       = SRC / "gui" / "tabs" / "log_tab.py"
SOURCES_TAB   = SRC / "gui" / "tabs" / "sources_tab.py"
JUSTIFY_TAB   = SRC / "gui" / "tabs" / "justify_tab.py"
I18N          = SRC / "i18n.py"
CLI_MAIN      = SRC / "cli" / "main.py"
COMPLIANCE    = SRC / "audit" / "compliance_log.py"


# ── D2: disclaimer_dialog.py ────────────────────────────────────────────────

class TestD2DisclaimerDialog(unittest.TestCase):
    def _src(self):
        return DISCLAIMER.read_text(encoding="utf-8")

    def test_customize_window_hint_migrated(self):
        src = self._src()
        self.assertIn("Qt.WindowType.CustomizeWindowHint", src,
                      "disclaimer_dialog: Qt.CustomizeWindowHint nicht migriert — BUG-D2")
        self.assertNotIn("Qt.CustomizeWindowHint", src,
                         "disclaimer_dialog: deprecated Qt.CustomizeWindowHint noch vorhanden — BUG-D2")

    def test_window_close_button_hint_migrated(self):
        src = self._src()
        self.assertIn("Qt.WindowType.WindowCloseButtonHint", src,
                      "disclaimer_dialog: Qt.WindowCloseButtonHint nicht migriert — BUG-D2")
        self.assertNotIn("Qt.WindowCloseButtonHint", src,
                         "disclaimer_dialog: deprecated Qt.WindowCloseButtonHint noch vorhanden — BUG-D2")


# ── D2: app.py ──────────────────────────────────────────────────────────────

class TestD2App(unittest.TestCase):
    def _src(self):
        return APP.read_text(encoding="utf-8")

    def test_tray_trigger_migrated(self):
        src = self._src()
        self.assertIn("QSystemTrayIcon.ActivationReason.Trigger", src,
                      "app: QSystemTrayIcon.Trigger nicht migriert — BUG-D2")
        self.assertNotIn("QSystemTrayIcon.Trigger", src,
                         "app: deprecated QSystemTrayIcon.Trigger noch vorhanden — BUG-D2")

    def test_tray_doubleclick_migrated(self):
        src = self._src()
        self.assertIn("QSystemTrayIcon.ActivationReason.DoubleClick", src,
                      "app: QSystemTrayIcon.DoubleClick nicht migriert — BUG-D2")
        self.assertNotIn("QSystemTrayIcon.DoubleClick", src,
                         "app: deprecated QSystemTrayIcon.DoubleClick noch vorhanden — BUG-D2")


# ── D2: main_window.py ──────────────────────────────────────────────────────

class TestD2MainWindow(unittest.TestCase):
    def _src(self):
        return MAIN_WIN.read_text(encoding="utf-8")

    def test_window_stays_on_top_hint_migrated(self):
        src = self._src()
        self.assertIn("Qt.WindowType.WindowStaysOnTopHint", src,
                      "main_window: Qt.WindowStaysOnTopHint nicht migriert — BUG-D2")
        self.assertNotIn("Qt.WindowStaysOnTopHint", src,
                         "main_window: deprecated Qt.WindowStaysOnTopHint noch vorhanden — BUG-D2")


# ── D2: check_tab.py ────────────────────────────────────────────────────────

class TestD2CheckTab(unittest.TestCase):
    def _src(self):
        return CHECK_TAB.read_text(encoding="utf-8")

    def test_align_right_migrated(self):
        src = self._src()
        self.assertIn("Qt.AlignmentFlag.AlignRight", src,
                      "check_tab: Qt.AlignRight nicht migriert — BUG-D2")
        self.assertNotIn("Qt.AlignRight", src,
                         "check_tab: deprecated Qt.AlignRight noch vorhanden — BUG-D2")

    def test_align_center_migrated(self):
        src = self._src()
        self.assertIn("Qt.AlignmentFlag.AlignCenter", src,
                      "check_tab: Qt.AlignCenter nicht migriert — BUG-D2")
        self.assertNotIn("Qt.AlignCenter", src,
                         "check_tab: deprecated Qt.AlignCenter noch vorhanden — BUG-D2")

    def test_size_policy_expanding_migrated(self):
        src = self._src()
        self.assertIn("QSizePolicy.Policy.Expanding", src,
                      "check_tab: QSizePolicy.Expanding nicht migriert — BUG-D2")
        self.assertNotIn("QSizePolicy.Expanding", src,
                         "check_tab: deprecated QSizePolicy.Expanding noch vorhanden — BUG-D2")


# ── D2: log_tab.py ──────────────────────────────────────────────────────────

class TestD2LogTab(unittest.TestCase):
    def _src(self):
        return LOG_TAB.read_text(encoding="utf-8")

    def test_foreground_role_migrated(self):
        src = self._src()
        self.assertIn("Qt.ItemDataRole.ForegroundRole", src,
                      "log_tab: Qt.ForegroundRole nicht migriert — BUG-D2")
        self.assertNotIn("Qt.ForegroundRole", src,
                         "log_tab: deprecated Qt.ForegroundRole noch vorhanden — BUG-D2")

    def test_header_resize_to_contents_migrated(self):
        src = self._src()
        self.assertIn("QHeaderView.ResizeMode.ResizeToContents", src,
                      "log_tab: QHeaderView.ResizeToContents nicht migriert — BUG-D2")
        self.assertNotIn("QHeaderView.ResizeToContents\n", src,
                         "log_tab: deprecated QHeaderView.ResizeToContents noch vorhanden — BUG-D2")

    def test_select_rows_migrated(self):
        src = self._src()
        self.assertIn("QAbstractItemView.SelectionBehavior.SelectRows", src,
                      "log_tab: QTableWidget.SelectRows nicht migriert — BUG-D2")
        self.assertNotIn("QTableWidget.SelectRows", src,
                         "log_tab: deprecated QTableWidget.SelectRows noch vorhanden — BUG-D2")

    def test_no_edit_triggers_migrated(self):
        src = self._src()
        self.assertIn("QAbstractItemView.EditTrigger.NoEditTriggers", src,
                      "log_tab: QTableWidget.NoEditTriggers nicht migriert — BUG-D2")
        self.assertNotIn("QTableWidget.NoEditTriggers", src,
                         "log_tab: deprecated QTableWidget.NoEditTriggers noch vorhanden — BUG-D2")


# ── D2: sources_tab.py ──────────────────────────────────────────────────────

class TestD2SourcesTab(unittest.TestCase):
    def _src(self):
        return SOURCES_TAB.read_text(encoding="utf-8")

    def test_rich_text_migrated(self):
        src = self._src()
        self.assertIn("Qt.TextFormat.RichText", src,
                      "sources_tab: Qt.RichText nicht migriert — BUG-D2")
        self.assertNotIn("Qt.RichText", src,
                         "sources_tab: deprecated Qt.RichText noch vorhanden — BUG-D2")

    def test_align_top_migrated(self):
        src = self._src()
        self.assertIn("Qt.AlignmentFlag.AlignTop", src,
                      "sources_tab: Qt.AlignTop nicht migriert — BUG-D2")
        self.assertNotIn("Qt.AlignTop", src,
                         "sources_tab: deprecated Qt.AlignTop noch vorhanden — BUG-D2")


# ── D2: justify_tab.py ──────────────────────────────────────────────────────

class TestD2JustifyTab(unittest.TestCase):
    def _src(self):
        return JUSTIFY_TAB.read_text(encoding="utf-8")

    def test_align_top_migrated(self):
        src = self._src()
        self.assertIn("Qt.AlignmentFlag.AlignTop", src,
                      "justify_tab: Qt.AlignTop nicht migriert — BUG-D2")
        self.assertNotIn("Qt.AlignTop", src,
                         "justify_tab: deprecated Qt.AlignTop noch vorhanden — BUG-D2")


# ── U2: i18n.py ─────────────────────────────────────────────────────────────

class TestU2I18n(unittest.TestCase):
    def _src(self):
        return I18N.read_text(encoding="utf-8")

    def test_load_language_file_has_json_decode_error_handler(self):
        src = self._src()
        self.assertIn("except json.JSONDecodeError", src,
                      "i18n: _load_language_file ohne JSONDecodeError-Handler — BUG-U2")

    def test_load_language_file_raises_value_error(self):
        src = self._src()
        self.assertIn("raise ValueError", src,
                      "i18n: ValueError-Weitergabe fehlt — BUG-U2")


# ── U2: cli/main.py ─────────────────────────────────────────────────────────

class TestU2CliMain(unittest.TestCase):
    def _src(self):
        return CLI_MAIN.read_text(encoding="utf-8")

    def test_load_answers_file_has_json_decode_error_handler(self):
        src = self._src()
        self.assertIn("Ungültige Antwortdatei", src,
                      "cli/main: _load_answers_file ohne JSONDecodeError-Handler — BUG-U2")

    def test_load_coverage_cases_has_json_decode_error_handler(self):
        src = self._src()
        self.assertIn("Ungültige Coverage-Datei", src,
                      "cli/main: _load_coverage_cases ohne JSONDecodeError-Handler — BUG-U2")


# ── U2: audit/compliance_log.py ─────────────────────────────────────────────

class TestU2ComplianceLog(unittest.TestCase):
    def _src(self):
        return COMPLIANCE.read_text(encoding="utf-8")

    def test_extra_json_loads_has_json_decode_error_handler(self):
        src = self._src()
        self.assertIn("except json.JSONDecodeError", src,
                      "compliance_log: json.loads(row[9]) ohne JSONDecodeError-Handler — BUG-U2")

    def test_extra_bare_inline_absent(self):
        src = self._src()
        self.assertNotIn("extra=json.loads(row[9])", src,
                         "compliance_log: bare inline json.loads ohne Handler noch vorhanden — BUG-U2")


if __name__ == "__main__":
    unittest.main()
