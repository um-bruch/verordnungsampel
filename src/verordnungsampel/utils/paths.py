"""Pfad-Aufloesung fuer Daten- und User-Verzeichnisse."""

from __future__ import annotations

import os
from pathlib import Path


def project_data_dir() -> Path:
    """Pfad zum mitgelieferten Daten-Verzeichnis (Read-only Regelwerke).

    Wird sowohl im Source-Layout (`src/verordnungsampel/...`) als auch in
    einem installierten Paket aufgeloest. Die Seed-JSON-Dateien liegen in
    ``data/seed/`` im Projektroot.
    """
    here = Path(__file__).resolve()
    # Projektroot = src/verordnungsampel/utils/paths.py -> 4 Stufen hoch
    project_root = here.parents[3]
    return project_root / "data"


def user_data_dir() -> Path:
    """Pfad zum nutzerspezifischen Daten-Verzeichnis (Compliance-Log, User-DB).

    - Windows: ``%APPDATA%/VerordnungsAmpel``
    - sonst:   ``~/.verordnungsampel``
    """
    appdata = os.environ.get("APPDATA")
    if appdata:
        path = Path(appdata) / "VerordnungsAmpel"
    else:
        path = Path.home() / ".verordnungsampel"
    path.mkdir(parents=True, exist_ok=True)
    return path
