"""Logger-Setup fuer VerordnungsAmpel.

Auf Windows muss PYTHONIOENCODING=utf-8 gesetzt sein, sonst gibt es bei
deutschen Umlauten in Logmeldungen einen UnicodeEncodeError (cp1252).
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Optional

_DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"

_configured = False


def _ensure_utf8_streams() -> None:
    """Forciert UTF-8 fuer stdout/stderr (Windows-cp1252-Workaround)."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


def _configure_root() -> None:
    global _configured
    if _configured:
        return
    _ensure_utf8_streams()
    level_name = os.environ.get("VERORDNUNGSAMPEL_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format=_DEFAULT_FORMAT,
        datefmt=_DEFAULT_DATEFMT,
    )
    _configured = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Gibt einen konfigurierten Logger zurueck.

    Args:
        name: Logger-Name. Default ``verordnungsampel``.

    Returns:
        Konfigurierter ``logging.Logger``.
    """
    _configure_root()
    return logging.getLogger(name or "verordnungsampel")
