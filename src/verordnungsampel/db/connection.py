"""Connection-Management fuer die VerordnungsAmpel-SQLite-Datenbank.

Pattern aus REF_MediPlaner_CASHCOW/database.py adaptiert:
- Foreign Keys aktiv
- Integritaetscheck mit Auto-Backup bei Korruption
- Schema-Bootstrapping bei jedem Open
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Tuple

from verordnungsampel.db.schema import create_schema
from verordnungsampel.utils.logger import get_logger
from verordnungsampel.utils.paths import user_data_dir

logger = get_logger(__name__)


def _safe_connect(db_path: Path) -> sqlite3.Connection:
    """Verbindet zur DB mit Integritaetscheck und Auto-Backup bei Korruption.

    Args:
        db_path: Pfad zur SQLite-Datei.

    Returns:
        Verbundene Connection mit aktivem Foreign-Key-Check und initialisiertem Schema.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        result = conn.execute("PRAGMA integrity_check").fetchone()
        if result is None or result[0] != "ok":
            raise sqlite3.DatabaseError(f"Integritaetspruefung fehlgeschlagen: {result}")
    except sqlite3.DatabaseError as exc:
        conn.close()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = db_path.with_suffix(db_path.suffix + f".corrupt_{ts}.bak")
        logger.warning("DB %s korrupt (%s) -> Backup nach %s", db_path, exc, backup_path)
        try:
            os.replace(db_path, backup_path)
        except (OSError, PermissionError):
            logger.error("Backup-Verschiebung fehlgeschlagen", exc_info=True)
        conn = sqlite3.connect(str(db_path))
        conn.execute("PRAGMA foreign_keys = ON")
    create_schema(conn)
    return conn


def open_database(db_path: Path | str | None = None) -> Tuple[sqlite3.Connection, Path]:
    """Oeffnet die Regelwerk-Datenbank, legt sie ggf. an.

    Args:
        db_path: Optionaler Pfad. Default: ``user_data_dir()/regelwerk.db``.

    Returns:
        Tupel ``(connection, path)``.
    """
    if db_path is None:
        db_path = user_data_dir() / "regelwerk.db"
    db_path = Path(db_path)
    conn = _safe_connect(db_path)
    logger.debug("Datenbank geoeffnet: %s", db_path)
    return conn, db_path


def open_in_memory() -> sqlite3.Connection:
    """Oeffnet eine reine In-Memory-Datenbank fuer Tests.

    Returns:
        Verbundene Connection mit aktivem Schema.
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    create_schema(conn)
    return conn
