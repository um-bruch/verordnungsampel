"""PySide6-basiertes Tray-Frontend für die VerordnungsAmpel-CLI-Engine.

Die GUI ruft die bestehenden Engine-/Output-/Audit-Module direkt auf
(keine Logik-Duplikation). Sie startet als QSystemTrayIcon mit einem
kompakten, nicht-intrusiven Hauptfenster.

Entry-Points:
    * ``python -m verordnungsampel.cli.main gui``
    * :func:`verordnungsampel.gui.app.run_gui` (programmatisch)
"""

from __future__ import annotations

__all__ = ["run_gui"]


def run_gui(*args, **kwargs) -> int:
    """Lazy-Re-Export für ``gui.app.run_gui``.

    Vermeidet, dass ``import verordnungsampel.gui`` bereits PySide6 lädt.
    """
    from verordnungsampel.gui.app import run_gui as _run

    return _run(*args, **kwargs)
