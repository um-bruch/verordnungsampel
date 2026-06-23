"""Manipulationssicherer Compliance-Log mit kryptografischer Hash-Chain.

Idee:
    Jeder Log-Eintrag enthaelt ``prev_hash`` (SHA-256 des vorherigen Eintrags)
    und ``hash`` (SHA-256 des aktuellen, kanonisch serialisierten Eintrags).
    Eine nachtraegliche Aenderung eines beliebigen Eintrags bricht die Kette
    und kann durch :meth:`ComplianceLog.verify_chain` jederzeit nachgewiesen
    werden.

Nicht geheim, nur unverfaelschbar:
    Das Ziel ist Beweiskraft vor Sozialgericht (BSG B 6 KA 26/13: nachgereichte
    Doku reicht NICHT). Es geht NICHT um Verschluesselung — die Eintraege
    sollen offen lesbar sein, aber nicht nachtraeglich aenderbar.

Persistierung:
    SQLite-Tabelle ``compliance_log`` in einer separaten DB-Datei
    (Default: ``user_data_dir()/compliance_log.db``), damit das User-Audit
    und das Read-only-Regelwerk getrennt bleiben.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from verordnungsampel.utils.logger import get_logger
from verordnungsampel.utils.paths import user_data_dir

logger = get_logger(__name__)

GENESIS_HASH = "0" * 64


@dataclass
class LogEintrag:
    """Ein einzelner Audit-Eintrag im Compliance-Log."""

    seq: int
    timestamp: str
    icd: str
    atc: str
    alter: Optional[int]
    ampel: str
    begruendung: str
    container: Optional[str]
    nutzer: Optional[str]
    prev_hash: str
    hash: str
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "seq": self.seq,
            "timestamp": self.timestamp,
            "icd": self.icd,
            "atc": self.atc,
            "alter": self.alter,
            "ampel": self.ampel,
            "begruendung": self.begruendung,
            "container": self.container,
            "nutzer": self.nutzer,
            "prev_hash": self.prev_hash,
            "hash": self.hash,
            "extra": self.extra,
        }


def _canonical_payload(
    *,
    seq: int,
    timestamp: str,
    icd: str,
    atc: str,
    alter: Optional[int],
    ampel: str,
    begruendung: str,
    container: Optional[str],
    nutzer: Optional[str],
    prev_hash: str,
    extra: Dict[str, Any],
) -> bytes:
    """Erzeugt eine kanonische, deterministische JSON-Darstellung fuer den Hash."""
    payload = {
        "seq": seq,
        "timestamp": timestamp,
        "icd": icd,
        "atc": atc,
        "alter": alter,
        "ampel": ampel,
        "begruendung": begruendung,
        "container": container,
        "nutzer": nutzer,
        "prev_hash": prev_hash,
        "extra": extra,
    }
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode(
        "utf-8"
    )


def _compute_hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


class ComplianceLog:
    """Append-only Log mit Hash-Chain auf SQLite-Basis."""

    def __init__(self, db_path: Path | str | None = None) -> None:
        if db_path is None:
            db_path = user_data_dir() / "compliance_log.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path))
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._create_table()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS compliance_log (
                seq         INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp   TEXT NOT NULL,
                icd         TEXT NOT NULL,
                atc         TEXT NOT NULL,
                alter_jahre INTEGER,
                ampel       TEXT NOT NULL,
                begruendung TEXT NOT NULL,
                container   TEXT,
                nutzer      TEXT,
                extra_json  TEXT NOT NULL DEFAULT '{}',
                prev_hash   TEXT NOT NULL,
                hash        TEXT NOT NULL UNIQUE
            )
            """
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Append
    # ------------------------------------------------------------------

    def append(
        self,
        *,
        icd: str,
        atc: str,
        ampel: str,
        begruendung: str,
        alter: Optional[int] = None,
        container: Optional[str] = None,
        nutzer: Optional[str] = None,
        timestamp: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> LogEintrag:
        """Fuegt einen neuen Eintrag an, berechnet ``prev_hash`` und ``hash``.

        Args:
            icd: ICD-10-GM-Code.
            atc: ATC-Code.
            ampel: Ergebnis-Ampel (``gruen|gelb|rot``).
            begruendung: Strukturierte Begruendung (zusammengefasst).
            alter: Optionales Patientenalter (oder ``None``).
            container: Container-Hinweis (z.B. ``pflicht_vorab``) oder ``None``.
            nutzer: Optionaler Nutzerbezeichner (Praxis-Account, kein Patient).
            timestamp: ISO-8601-String (Default: aktueller UTC-Zeitpunkt).
            extra: Beliebige zusaetzliche Felder (werden mitversiegelt).

        Returns:
            Den persistierten :class:`LogEintrag`.
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        extra = extra or {}

        prev_hash = self._tail_hash()
        cur = self._conn.execute(
            """
            INSERT INTO compliance_log
                (timestamp, icd, atc, alter_jahre, ampel, begruendung,
                 container, nutzer, extra_json, prev_hash, hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                icd,
                atc,
                alter,
                ampel,
                begruendung,
                container,
                nutzer,
                json.dumps(extra, sort_keys=True, ensure_ascii=False),
                prev_hash,
                "",  # Platzhalter, gleich aktualisieren
            ),
        )
        seq = cur.lastrowid

        payload = _canonical_payload(
            seq=seq,
            timestamp=timestamp,
            icd=icd,
            atc=atc,
            alter=alter,
            ampel=ampel,
            begruendung=begruendung,
            container=container,
            nutzer=nutzer,
            prev_hash=prev_hash,
            extra=extra,
        )
        new_hash = _compute_hash(payload)
        self._conn.execute(
            "UPDATE compliance_log SET hash=? WHERE seq=?",
            (new_hash, seq),
        )
        self._conn.commit()

        return LogEintrag(
            seq=seq,
            timestamp=timestamp,
            icd=icd,
            atc=atc,
            alter=alter,
            ampel=ampel,
            begruendung=begruendung,
            container=container,
            nutzer=nutzer,
            prev_hash=prev_hash,
            hash=new_hash,
            extra=extra,
        )

    def _tail_hash(self) -> str:
        row = self._conn.execute(
            "SELECT hash FROM compliance_log ORDER BY seq DESC LIMIT 1"
        ).fetchone()
        return row[0] if row else GENESIS_HASH

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) FROM compliance_log").fetchone()
        return row[0] if row else 0

    def __iter__(self) -> Iterator[LogEintrag]:
        cur = self._conn.execute(
            """
            SELECT seq, timestamp, icd, atc, alter_jahre, ampel, begruendung,
                   container, nutzer, extra_json, prev_hash, hash
            FROM compliance_log
            ORDER BY seq ASC
            """
        )
        for row in cur:
            try:
                _extra = json.loads(row[9]) if row[9] else {}
            except json.JSONDecodeError:
                _extra = {}
            yield LogEintrag(
                seq=row[0],
                timestamp=row[1],
                icd=row[2],
                atc=row[3],
                alter=row[4],
                ampel=row[5],
                begruendung=row[6],
                container=row[7],
                nutzer=row[8],
                prev_hash=row[10],
                hash=row[11],
                extra=_extra,
            )

    def all_entries(self) -> List[LogEintrag]:
        return list(self)

    # ------------------------------------------------------------------
    # Verify
    # ------------------------------------------------------------------

    def verify_chain(self) -> bool:
        """Prueft die gesamte Hash-Kette von vorne nach hinten.

        Returns:
            ``True`` wenn die Kette intakt ist, sonst ``False``.
        """
        prev_hash = GENESIS_HASH
        for entry in self:
            if entry.prev_hash != prev_hash:
                logger.error(
                    "Hash-Chain gebrochen bei seq=%s: prev_hash=%s erwartet=%s",
                    entry.seq,
                    entry.prev_hash,
                    prev_hash,
                )
                return False
            payload = _canonical_payload(
                seq=entry.seq,
                timestamp=entry.timestamp,
                icd=entry.icd,
                atc=entry.atc,
                alter=entry.alter,
                ampel=entry.ampel,
                begruendung=entry.begruendung,
                container=entry.container,
                nutzer=entry.nutzer,
                prev_hash=entry.prev_hash,
                extra=entry.extra,
            )
            recomputed = _compute_hash(payload)
            if recomputed != entry.hash:
                logger.error(
                    "Hash-Mismatch bei seq=%s: berechnet=%s gespeichert=%s",
                    entry.seq,
                    recomputed,
                    entry.hash,
                )
                return False
            prev_hash = entry.hash
        return True

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        try:
            self._conn.close()
        except sqlite3.Error:
            pass

    def __enter__(self) -> "ComplianceLog":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
