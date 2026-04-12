"""Praxisbesonderheiten-Erkennung (KONZEPT Funktion 4).

Praxisbesonderheiten sind gemaess § 106b Abs. 2 SGB V und der
Rahmenvereinbarung nach § 106b Abs. 2 SGB V anerkannte Gruende fuer
ueberdurchschnittliche Verordnungskosten. Der GKV-Spitzenverband fuehrt
eine Liste bundesweit anerkannter Praxisbesonderheiten (AMNOG-Praeparate
und weitere).

Zweck dieses Moduls:
    1. **Erkennung** — bei einer Verordnung pruefen, ob eine bundesweite
       oder lokale Praxisbesonderheit einschlaegig ist.
    2. **Quartalsreminder** — am Quartalsende den Compliance-Log
       durchgehen und alle Verordnungen auflisten, bei denen eine
       Praxisbesonderheit eingriff. Der Arzt muss dann sicherstellen,
       dass die entsprechende KV-Kennziffer auf dem Behandlungsschein
       markiert wurde.

Juristischer Hintergrund (Substanziierter Vortrag):
    - LSG Baden-Wuerttemberg 15.11.2023: Praxisbesonderheiten muessen
      **bereits im Verwaltungsverfahren** substanziiert vorgetragen
      werden — wer sie erst im Klageverfahren nachreicht, verliert.
    - SG Marburg 31.01.2024: Substanziierter Vortrag setzt konkrete
      Patientenstrukturdaten voraus.

Design-Prinzipien:
    - Pure functions ohne I/O (DB-Verbindung wird injiziert)
    - Pattern-Matching via :func:`engine.rules.pattern_matches`
    - Gueltigkeitszeitraum streng (None-Grenzen offen)
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, Iterable, List, Optional

from verordnungsampel.engine.rules import Quelle, pattern_matches


@dataclass(frozen=True)
class Praxisbesonderheit:
    """Ein einzelner Praxisbesonderheit-Eintrag."""

    id: int
    atc_pattern: str
    icd_pattern: Optional[str]
    bezeichnung: str
    gueltig_ab: Optional[str]  # ISO-Datum
    gueltig_bis: Optional[str]  # ISO-Datum
    quelle: Optional[Quelle] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "atc_pattern": self.atc_pattern,
            "icd_pattern": self.icd_pattern,
            "bezeichnung": self.bezeichnung,
            "gueltig_ab": self.gueltig_ab,
            "gueltig_bis": self.gueltig_bis,
            "quelle": (
                {
                    "kuerzel": self.quelle.kuerzel,
                    "titel": self.quelle.titel,
                }
                if self.quelle
                else None
            ),
        }


# ---------------------------------------------------------------------------
# Datum-Helpers
# ---------------------------------------------------------------------------


def _parse_iso(value: Optional[str]) -> Optional[date]:
    """Konvertiert einen ISO-Datumsstring (YYYY-MM-DD) in ein ``date``.

    ``None`` und Leerstring werden zu ``None``.
    """
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None


def is_valid_at(pb: Praxisbesonderheit, stichtag: date) -> bool:
    """Prueft, ob eine Praxisbesonderheit zu einem Stichtag aktiv ist.

    Args:
        pb: Die Praxisbesonderheit.
        stichtag: Pruefdatum.

    Returns:
        ``True`` wenn ``gueltig_ab <= stichtag <= gueltig_bis`` (None-Grenzen
        werden als offen interpretiert).
    """
    ab = _parse_iso(pb.gueltig_ab)
    bis = _parse_iso(pb.gueltig_bis)
    if ab is not None and stichtag < ab:
        return False
    if bis is not None and stichtag > bis:
        return False
    return True


# ---------------------------------------------------------------------------
# DB-Lookup
# ---------------------------------------------------------------------------


def load_from_db(conn: sqlite3.Connection) -> List[Praxisbesonderheit]:
    """Laedt alle Praxisbesonderheiten inklusive Quellen aus der DB."""
    rows = conn.execute(
        """
        SELECT p.id, p.atc_pattern, p.icd_pattern, p.bezeichnung,
               p.gueltig_ab, p.gueltig_bis,
               q.kuerzel, q.titel, q.url, q.stand
        FROM praxisbesonderheit p
        LEFT JOIN quelle q ON q.id = p.quelle_id
        ORDER BY p.id
        """
    ).fetchall()
    result: List[Praxisbesonderheit] = []
    for row in rows:
        quelle: Optional[Quelle] = None
        if row[6]:
            quelle = Quelle(kuerzel=row[6], titel=row[7], url=row[8], stand=row[9])
        result.append(
            Praxisbesonderheit(
                id=row[0],
                atc_pattern=row[1],
                icd_pattern=row[2],
                bezeichnung=row[3],
                gueltig_ab=row[4],
                gueltig_bis=row[5],
                quelle=quelle,
            )
        )
    return result


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------


def find_matching(
    icd: str,
    atc: str,
    *,
    conn: Optional[sqlite3.Connection] = None,
    pbs: Optional[Iterable[Praxisbesonderheit]] = None,
    stichtag: Optional[date] = None,
) -> List[Praxisbesonderheit]:
    """Findet alle einschlaegigen Praxisbesonderheiten fuer eine Verordnung.

    Args:
        icd: ICD-10-GM-Code der Diagnose.
        atc: ATC-Code des Wirkstoffs.
        conn: DB-Verbindung (wenn ``pbs`` nicht gegeben).
        pbs: Explizite Liste (fuer Tests).
        stichtag: Pruefdatum fuer den Gueltigkeitszeitraum. Default: heute.

    Returns:
        Liste aller Treffer in DB-Reihenfolge.
    """
    if pbs is None:
        if conn is None:
            return []
        pbs = load_from_db(conn)
    icd_norm = (icd or "").strip().upper()
    atc_norm = (atc or "").strip().upper()
    stichtag = stichtag or date.today()

    matches: List[Praxisbesonderheit] = []
    for pb in pbs:
        if not pattern_matches(pb.atc_pattern, atc_norm):
            continue
        if pb.icd_pattern and not pattern_matches(pb.icd_pattern, icd_norm):
            continue
        if not is_valid_at(pb, stichtag):
            continue
        matches.append(pb)
    return matches


# ---------------------------------------------------------------------------
# Quartals-Reminder
# ---------------------------------------------------------------------------


@dataclass
class QuartalReminder:
    """Ergebnis des Quartals-Reminders."""

    quartal: str  # z.B. "2026-Q2"
    start: date
    ende: date
    eintraege: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def anzahl(self) -> int:
        return len(self.eintraege)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "quartal": self.quartal,
            "start": self.start.isoformat(),
            "ende": self.ende.isoformat(),
            "anzahl": self.anzahl,
            "eintraege": list(self.eintraege),
        }


def parse_quartal(spec: str) -> tuple[date, date, str]:
    """Parst einen Quartalsbezeichner wie ``2026-Q2`` in Start/Ende/Label.

    Raises:
        ValueError: Bei fehlerhaftem Format.
    """
    spec = (spec or "").strip().upper()
    if len(spec) != 7 or spec[4:6] != "-Q" or not spec[:4].isdigit() or not spec[6].isdigit():
        raise ValueError(f"Erwarte Format YYYY-Qn (z.B. 2026-Q2), erhalten: {spec!r}")
    jahr = int(spec[:4])
    q = int(spec[6])
    if q < 1 or q > 4:
        raise ValueError(f"Quartal muss 1-4 sein, erhalten: {q}")
    start_monat = (q - 1) * 3 + 1
    ende_monat = start_monat + 2
    start = date(jahr, start_monat, 1)
    if ende_monat == 12:
        ende = date(jahr, 12, 31)
    else:
        # Letzter Tag des Ende-Monats
        next_start = date(jahr, ende_monat + 1, 1)
        ende = date.fromordinal(next_start.toordinal() - 1)
    return start, ende, f"{jahr}-Q{q}"


def build_quartal_reminder(
    log_entries: Iterable[Dict[str, Any]],
    quartal: str,
) -> QuartalReminder:
    """Filtert Compliance-Log-Eintraege auf ein Quartal und extrahiert
    Eintraege mit Praxisbesonderheit-Treffer.

    Erwartet ``log_entries`` im Format von :meth:`ComplianceLog.all_entries`
    (bzw. der ``to_dict()``-Ausgabe der ``LogEintrag``-Dataclass).

    Args:
        log_entries: Iterable der Compliance-Log-Eintraege.
        quartal: Quartalsbezeichner (``"2026-Q2"``).

    Returns:
        :class:`QuartalReminder` mit gefilterten Eintraegen.
    """
    start, ende, label = parse_quartal(quartal)
    treffer: List[Dict[str, Any]] = []
    for entry in log_entries:
        ts_raw = entry.get("timestamp")
        if not ts_raw:
            continue
        try:
            dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            entry_date = dt.date()
        except ValueError:
            continue
        if entry_date < start or entry_date > ende:
            continue
        extra = entry.get("extra") or {}
        pbs = extra.get("praxisbesonderheiten") or []
        if not pbs:
            continue
        treffer.append(
            {
                "seq": entry.get("seq"),
                "datum": entry_date.isoformat(),
                "icd": entry.get("icd"),
                "atc": entry.get("atc"),
                "ampel": entry.get("ampel"),
                "praxisbesonderheiten": pbs,
            }
        )
    return QuartalReminder(
        quartal=label,
        start=start,
        ende=ende,
        eintraege=treffer,
    )


def render_reminder(reminder: QuartalReminder) -> str:
    """Erzeugt eine druckfertige Textausgabe fuer das Quartal."""
    lines: List[str] = []
    lines.append("=" * 72)
    lines.append(
        f"QUARTALS-REMINDER PRAXISBESONDERHEITEN  {reminder.quartal}"
        f"  ({reminder.start.strftime('%d.%m.%Y')} – {reminder.ende.strftime('%d.%m.%Y')})"
    )
    lines.append("=" * 72)
    if reminder.anzahl == 0:
        lines.append("Keine Verordnungen mit Praxisbesonderheit-Treffer im Quartal.")
        lines.append("=" * 72)
        return "\n".join(lines)
    lines.append(
        f"{reminder.anzahl} Verordnung(en) mit Praxisbesonderheit. Bitte pruefen, "
        f"ob die KV-Kennziffer auf dem Behandlungsschein markiert wurde."
    )
    lines.append("-" * 72)
    for item in reminder.eintraege:
        pbs = item["praxisbesonderheiten"]
        pbs_names = ", ".join(
            pb.get("bezeichnung", f"PB#{pb.get('id')}") for pb in pbs
        )
        lines.append(
            f"#{item['seq']:05d} {item['datum']} ICD={item['icd']} "
            f"ATC={item['atc']} [{item['ampel'].upper()}]"
        )
        lines.append(f"   -> {pbs_names}")
    lines.append("-" * 72)
    lines.append(
        "Hinweis: Nicht markierte Praxisbesonderheiten fuehren im Regressverfahren "
        "zum Ausschluss substanziierten Vortrags (LSG BW 15.11.2023)."
    )
    lines.append("=" * 72)
    return "\n".join(lines)
