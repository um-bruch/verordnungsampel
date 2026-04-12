"""MainWindow mit Tabs und Tray-freundlichem Close-Verhalten.

Besonderheiten:
    * ``closeEvent`` minimiert in den Tray, statt die App zu beenden.
      Nur wenn ``allow_close == True`` (vom Tray-Controller gesetzt)
      akzeptiert das Fenster das Schließen wirklich.
    * Kompaktes Layout (ca. 540×620) — läuft gut neben anderen Fenstern.
    * Optionen für "Always on top", "Minimal-Modus" und leichte Transparenz.
    * Signale (``quit_requested``, ``ampel_changed``) kommunizieren mit
      dem TrayController und anderen Tabs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
)

from verordnungsampel import __version__
from verordnungsampel.engine.evaluator import AmpelErgebnis
from verordnungsampel.gui import strings_de as S
from verordnungsampel.gui.tabs.check_tab import CheckTab
from verordnungsampel.gui.tabs.justify_tab import JustifyTab
from verordnungsampel.gui.tabs.log_tab import LogTab
from verordnungsampel.gui.tabs.reminder_tab import ReminderTab
from verordnungsampel.gui.tabs.sources_tab import SourcesTab
from verordnungsampel.gui.tabs.workflow_tab import WorkflowTab


_ICONS_DIR = Path(__file__).resolve().parent / "icons"


class MainWindow(QMainWindow):
    """Hauptfenster mit Tabs (Check/Justify/Workflow/Log/Reminder)."""

    quit_requested = Signal()
    ampel_changed = Signal(str)  # "gruen" / "gelb" / "rot" / ""

    def __init__(self) -> None:
        super().__init__()
        self.allow_close = False
        self._current_ergebnis: Optional[AmpelErgebnis] = None

        self.setWindowTitle(S.APP_TITLE)
        self.setWindowIcon(QIcon(str(_ICONS_DIR / "ampel.svg")))
        self.resize(560, 640)
        self.setMinimumSize(440, 480)

        # Tabs
        self.tabs = QTabWidget()
        self.check_tab = CheckTab()
        self.justify_tab = JustifyTab()
        self.workflow_tab = WorkflowTab()
        self.log_tab = LogTab()
        self.reminder_tab = ReminderTab()
        self.sources_tab = SourcesTab()

        self.tabs.addTab(self.check_tab, S.TAB_CHECK)
        self.tabs.addTab(self.justify_tab, S.TAB_JUSTIFY)
        self.tabs.addTab(self.workflow_tab, S.TAB_WORKFLOW)
        self.tabs.addTab(self.log_tab, S.TAB_LOG)
        self.tabs.addTab(self.reminder_tab, S.TAB_REMINDER)
        self.tabs.addTab(self.sources_tab, S.TAB_SOURCES)

        self.setCentralWidget(self.tabs)

        # Statusleiste
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage(S.STATUS_READY)

        # Menüs
        self._build_menus()

        # Tabs verdrahten
        self.check_tab.result_ready.connect(self._on_result_ready)

        # Anfangszustand: Justify/Workflow deaktiviert (kein Ergebnis)
        self._set_dependent_tabs_enabled(False)
        self.justify_tab.set_ergebnis(None)
        self.workflow_tab.set_ergebnis(None)

    # ------------------------------------------------------------------
    # Menüs
    # ------------------------------------------------------------------

    def _build_menus(self) -> None:
        mbar = self.menuBar()

        file_menu = mbar.addMenu(S.MENU_FILE)
        quit_action = QAction(S.MENU_QUIT, self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(self.quit_requested.emit)
        file_menu.addAction(quit_action)

        view_menu = mbar.addMenu(S.MENU_VIEW)

        self.action_on_top = QAction(S.MENU_ALWAYS_ON_TOP, self, checkable=True)
        self.action_on_top.toggled.connect(self._toggle_always_on_top)
        view_menu.addAction(self.action_on_top)

        self.action_minimal = QAction(S.MENU_MINIMAL_MODE, self, checkable=True)
        self.action_minimal.toggled.connect(self._toggle_minimal_mode)
        view_menu.addAction(self.action_minimal)

        self.action_transparent = QAction(S.MENU_TRANSPARENCY, self, checkable=True)
        self.action_transparent.toggled.connect(self._toggle_transparency)
        view_menu.addAction(self.action_transparent)

        help_menu = mbar.addMenu(S.MENU_HELP)
        about_action = QAction(S.MENU_ABOUT, self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    # ------------------------------------------------------------------
    # View-Toggles
    # ------------------------------------------------------------------

    def _toggle_always_on_top(self, checked: bool) -> None:
        flags = self.windowFlags()
        if checked:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        # setWindowFlags versteckt das Fenster — wieder zeigen
        self.show()

    def _toggle_minimal_mode(self, checked: bool) -> None:
        """Im Minimal-Modus wird nur der Check-Tab sichtbar, andere verborgen."""
        for i in range(self.tabs.count()):
            if i == 0:
                continue
            self.tabs.setTabVisible(i, not checked)
        if checked:
            self.resize(440, 420)
        else:
            self.resize(560, 640)

    def _toggle_transparency(self, checked: bool) -> None:
        self.setWindowOpacity(0.92 if checked else 1.0)

    def _show_about(self) -> None:
        QMessageBox.information(
            self,
            S.MENU_ABOUT,
            S.ABOUT_TEXT.format(version=__version__),
        )

    # ------------------------------------------------------------------
    # Ergebnis-Routing
    # ------------------------------------------------------------------

    def _on_result_ready(self, ergebnis: AmpelErgebnis) -> None:
        """Check-Tab hat ein neues Ergebnis geliefert."""
        self._current_ergebnis = ergebnis
        farbe = ergebnis.gesamt.value if ergebnis else ""
        self.ampel_changed.emit(farbe)

        # Justify/Workflow-Tabs füttern
        self.justify_tab.set_ergebnis(ergebnis)
        self.workflow_tab.set_ergebnis(ergebnis)

        # Justify-Tab nur bei GELB/ROT aktivieren
        need_justify = farbe in ("gelb", "rot")
        self._set_justify_enabled(need_justify)

        # Workflow nur sichtbar wenn Container-Hinweis existiert
        has_container = bool(ergebnis.container_hinweise)
        self._set_workflow_enabled(has_container)

        self.statusBar().showMessage(f"Letzte Prüfung: {ergebnis.icd} + {ergebnis.atc} -> {farbe.upper()}")

    def _set_dependent_tabs_enabled(self, enabled: bool) -> None:
        self._set_justify_enabled(enabled)
        self._set_workflow_enabled(enabled)

    def _set_justify_enabled(self, enabled: bool) -> None:
        idx = self.tabs.indexOf(self.justify_tab)
        if idx >= 0:
            self.tabs.setTabEnabled(idx, enabled)

    def _set_workflow_enabled(self, enabled: bool) -> None:
        idx = self.tabs.indexOf(self.workflow_tab)
        if idx >= 0:
            self.tabs.setTabEnabled(idx, enabled)

    # ------------------------------------------------------------------
    # Close-Verhalten
    # ------------------------------------------------------------------

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802 - Qt-API
        """X im Fenster minimiert in den Tray.

        Nur wenn :attr:`allow_close` explizit gesetzt ist, akzeptiert das
        Fenster das Close-Event und beendet damit die App.
        """
        if self.allow_close:
            event.accept()
            return
        event.ignore()
        self.hide()


__all__ = ["MainWindow"]
