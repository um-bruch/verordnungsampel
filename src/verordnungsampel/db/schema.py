"""SQLite-Schema fuer VerordnungsAmpel.

Tabellen:
    - icd10               Diagnose-Codes (ICD-10-GM)
    - atc                 Wirkstoff-Codes (ATC, WHO)
    - amrl_anlage         AM-RL Anlagen III/V/VI als generische Eintraege
    - praxisbesonderheit  GKV-SV-Liste der bundesweiten Praxisbesonderheiten
    - regel               Generische Ampel-Regeln (atc_pattern + Bedingung -> Ampel)
    - quelle              Quellen-Referenzen (z.B. AM-RL Anlage III, BSG-Urteile)
    - settings            Key-Value Konfiguration

Hash-Chain-Tabellen liegen in audit/compliance_log.py (separater DB-Pfad,
damit Read-only-Regelwerk und User-Audit nicht vermischt werden).
"""

from __future__ import annotations

import sqlite3

SCHEMA_VERSION = 1


def schema_version() -> int:
    """Liefert die aktuelle Schemaversion."""
    return SCHEMA_VERSION


def create_schema(conn: sqlite3.Connection) -> None:
    """Legt alle Tabellen idempotent an und fuehrt Mini-Migrationen aus.

    Args:
        conn: Aktive SQLite-Verbindung. ``foreign_keys`` muss bereits aktiv sein.
    """
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            key   TEXT PRIMARY KEY,
            value TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS icd10 (
            code        TEXT PRIMARY KEY,
            bezeichnung TEXT NOT NULL,
            kapitel     TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS atc (
            code        TEXT PRIMARY KEY,
            bezeichnung TEXT NOT NULL,
            wirkstoff   TEXT,
            ddd         REAL,
            ddd_einheit TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS quelle (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            kuerzel       TEXT NOT NULL UNIQUE,
            titel         TEXT NOT NULL,
            url           TEXT,
            stand         TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS amrl_anlage (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            anlage        TEXT NOT NULL,        -- 'III', 'V', 'VI'
            atc_pattern   TEXT NOT NULL,        -- z.B. 'A02BC%' fuer PPI
            bedingung     TEXT,                 -- Klartext (Indikationen, Ausschluesse)
            ampel         TEXT NOT NULL,        -- 'gruen' | 'gelb' | 'rot'
            begruendung   TEXT NOT NULL,
            quelle_id     INTEGER,
            FOREIGN KEY (quelle_id) REFERENCES quelle(id) ON DELETE SET NULL
        )
        """
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_amrl_atc_pattern ON amrl_anlage(atc_pattern)"
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS praxisbesonderheit (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            atc_pattern   TEXT NOT NULL,
            icd_pattern   TEXT,
            bezeichnung   TEXT NOT NULL,
            gueltig_ab    TEXT,
            gueltig_bis   TEXT,
            quelle_id     INTEGER,
            FOREIGN KEY (quelle_id) REFERENCES quelle(id) ON DELETE SET NULL
        )
        """
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_pb_atc_pattern ON praxisbesonderheit(atc_pattern)"
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS regel (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            kuerzel       TEXT NOT NULL UNIQUE,
            atc_pattern   TEXT,
            icd_pattern   TEXT,
            altersgrenze  INTEGER,             -- Schwellenwert (z.B. 65 fuer PRISCUS)
            ampel         TEXT NOT NULL,
            begruendung   TEXT NOT NULL,
            container     TEXT,                -- 'pflicht_vorab' | 'verboten_vorab' | 'stellungnahme' | NULL
            quelle_id     INTEGER,
            FOREIGN KEY (quelle_id) REFERENCES quelle(id) ON DELETE SET NULL
        )
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_regel_atc ON regel(atc_pattern)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_regel_icd ON regel(icd_pattern)")

    cur.execute(
        "INSERT OR REPLACE INTO settings(key, value) VALUES (?, ?)",
        ("schema_version", str(SCHEMA_VERSION)),
    )

    conn.commit()


def get_setting(conn: sqlite3.Connection, key: str, default: str | None = None) -> str | None:
    """Liest einen Wert aus der ``settings``-Tabelle.

    Args:
        conn: Aktive Verbindung.
        key: Schluessel.
        default: Rueckgabewert wenn der Schluessel fehlt.

    Returns:
        Persistierter Wert oder ``default``.
    """
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    if row is None:
        return default
    return row[0]


def save_setting(conn: sqlite3.Connection, key: str, value: str) -> None:
    """Persistiert einen Wert in der ``settings``-Tabelle (Upsert)."""
    conn.execute(
        "INSERT OR REPLACE INTO settings(key, value) VALUES (?, ?)",
        (key, str(value)),
    )
    conn.commit()
