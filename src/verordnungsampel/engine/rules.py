"""Datentypen fuer die Ampel-Engine: Quelle, Regel, Treffer.

Reines Python-Modul ohne Datenbank-Abhaengigkeit, damit der Evaluator
sowohl gegen die DB als auch gegen rein In-Memory-Regelsaetze laufen kann
(wichtig fuer Tests und Property-basierte Verifikation).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Quelle:
    """Eine Quelle (Gesetz, Anlage, Urteil) hinter einer Regel."""

    kuerzel: str
    titel: str
    url: Optional[str] = None
    stand: Optional[str] = None


@dataclass(frozen=True)
class Regel:
    """Eine generische Ampel-Regel.

    Felder:
        kuerzel: Eindeutiger Bezeichner (z.B. ``AMRL_III_PPI_LANGZEIT``).
        atc_pattern: SQL-LIKE-Muster auf den ATC-Code (z.B. ``A02BC%``).
            ``None`` bedeutet "trifft auf jeden ATC".
        icd_pattern: SQL-LIKE-Muster auf den ICD-10-Code. ``None`` = beliebig.
        altersgrenze: Wenn gesetzt, greift die Regel nur, wenn ``alter >= altersgrenze``
            (z.B. ``65`` fuer PRISCUS-Liste).
        ampel: ``"gruen"``, ``"gelb"`` oder ``"rot"``.
        begruendung: Klartext, der der Aerztin angezeigt wird.
        container: Optional einer von ``pflicht_vorab``, ``verboten_vorab``,
            ``stellungnahme`` (Container-sensitive Vorab-Klaerungs-Logik).
        quelle: Quellenverweis fuer Audit-Trail.
    """

    kuerzel: str
    ampel: str
    begruendung: str
    atc_pattern: Optional[str] = None
    icd_pattern: Optional[str] = None
    altersgrenze: Optional[int] = None
    container: Optional[str] = None
    quelle: Optional[Quelle] = None


def pattern_matches(pattern: Optional[str], wert: Optional[str]) -> bool:
    """Prueft ob ein SQL-LIKE-Muster auf einen Wert passt.

    Unterstuetzt nur ``%`` (beliebige Zeichenfolge) und ``_`` (genau ein Zeichen).
    Eckige Klammern u.ae. werden NICHT interpretiert (Sicherheits-default).

    Args:
        pattern: Muster mit ``%``/``_`` oder ``None``.
        wert: Zu pruefender Wert oder ``None``.

    Returns:
        ``True`` wenn pattern ``None`` ist (=keine Einschraenkung) oder wenn
        der Wert auf das Muster passt. ``False`` wenn pattern gesetzt ist und
        der Wert ``None`` oder leer.
    """
    if pattern is None or pattern == "":
        return True
    if not wert:
        return False
    pat = pattern.upper()
    val = wert.upper()
    return _match(pat, val)


def _match(pattern: str, wert: str) -> bool:
    """Rekursiver Matcher fuer ``%`` (greedy any) und ``_`` (single char)."""
    if not pattern:
        return not wert
    head = pattern[0]
    rest = pattern[1:]
    if head == "%":
        if not rest:
            return True
        for i in range(len(wert) + 1):
            if _match(rest, wert[i:]):
                return True
        return False
    if head == "_":
        if not wert:
            return False
        return _match(rest, wert[1:])
    if not wert:
        return False
    if wert[0] != head:
        return False
    return _match(rest, wert[1:])
