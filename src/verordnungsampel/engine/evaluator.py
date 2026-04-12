"""Ampel-Engine: Auswertung einer Verordnung gegen die Regelmenge.

Der Evaluator nimmt eine Verordnung (ICD-10 + ATC + optional Alter)
und produziert ein :class:`AmpelErgebnis` mit Gesamtfarbe, allen
Treffer-Begruendungen und Quellenverweisen.

Logik:
    - Alle anwendbaren Regeln werden gesammelt
    - Die "schaerfste" Ampel gewinnt: rot > gelb > gruen
    - Wenn keine Regel greift -> gruen mit Standard-Begruendung
    - Container-sensitive Hinweise (Vorab-Klaerung) werden separat ausgegeben
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, List, Optional, Sequence

from verordnungsampel.engine.rules import Quelle, Regel, pattern_matches


class Ampel(str, Enum):
    """Drei Ampelfarben mit Vergleichsordnung (rot > gelb > gruen)."""

    GRUEN = "gruen"
    GELB = "gelb"
    ROT = "rot"

    @property
    def schaerfe(self) -> int:
        return {"gruen": 0, "gelb": 1, "rot": 2}[self.value]

    @classmethod
    def aus_str(cls, wert: str) -> "Ampel":
        wert_l = (wert or "").strip().lower()
        for ampel in cls:
            if ampel.value == wert_l:
                return ampel
        raise ValueError(f"Unbekannte Ampelfarbe: {wert!r}")


@dataclass
class Treffer:
    """Ein einzelner Regeltreffer waehrend der Auswertung."""

    regel_kuerzel: str
    ampel: Ampel
    begruendung: str
    quelle: Optional[Quelle] = None
    container: Optional[str] = None


@dataclass
class AmpelErgebnis:
    """Gesamtergebnis einer Verordnungspruefung."""

    icd: str
    atc: str
    alter: Optional[int]
    gesamt: Ampel
    treffer: List[Treffer] = field(default_factory=list)

    @property
    def begruendungen(self) -> List[str]:
        return [t.begruendung for t in self.treffer]

    @property
    def quellen(self) -> List[Quelle]:
        return [t.quelle for t in self.treffer if t.quelle is not None]

    @property
    def container_hinweise(self) -> List[str]:
        return sorted({t.container for t in self.treffer if t.container})

    def to_dict(self) -> dict:
        return {
            "icd": self.icd,
            "atc": self.atc,
            "alter": self.alter,
            "gesamt": self.gesamt.value,
            "treffer": [
                {
                    "regel": t.regel_kuerzel,
                    "ampel": t.ampel.value,
                    "begruendung": t.begruendung,
                    "container": t.container,
                    "quelle": (
                        {
                            "kuerzel": t.quelle.kuerzel,
                            "titel": t.quelle.titel,
                            "url": t.quelle.url,
                            "stand": t.quelle.stand,
                        }
                        if t.quelle
                        else None
                    ),
                }
                for t in self.treffer
            ],
        }


_DEFAULT_GRUEN_BEGRUENDUNG = (
    "Keine Regel der eingebetteten Regelwerke trifft auf diese Kombination zu. "
    "Das ersetzt NICHT die aerztliche Pruefung im Einzelfall."
)


def evaluate(
    icd: str,
    atc: str,
    alter: Optional[int] = None,
    *,
    regeln: Optional[Sequence[Regel]] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> AmpelErgebnis:
    """Wertet eine Verordnung gegen alle anwendbaren Regeln aus.

    Args:
        icd: ICD-10-GM-Code (z.B. ``"I10"``).
        atc: ATC-Code (z.B. ``"C09AA02"``).
        alter: Optionales Alter des Patienten in Jahren.
        regeln: Optionale explizite Regelmenge. Wenn ``None`` und ``conn``
            gegeben, werden Regeln aus der DB gelesen.
        conn: Optionale SQLite-Verbindung. Wenn weder ``regeln`` noch ``conn``
            angegeben sind, gilt ein leerer Regelsatz (Ergebnis = gruen).

    Returns:
        :class:`AmpelErgebnis`.
    """
    icd_norm = (icd or "").strip().upper()
    atc_norm = (atc or "").strip().upper()

    if regeln is None and conn is not None:
        regeln = _load_regeln_from_db(conn)
    if regeln is None:
        regeln = []

    treffer: List[Treffer] = []
    for regel in regeln:
        if not pattern_matches(regel.atc_pattern, atc_norm):
            continue
        if not pattern_matches(regel.icd_pattern, icd_norm):
            continue
        if regel.altersgrenze is not None:
            if alter is None or alter < regel.altersgrenze:
                continue
        treffer.append(
            Treffer(
                regel_kuerzel=regel.kuerzel,
                ampel=Ampel.aus_str(regel.ampel),
                begruendung=regel.begruendung,
                quelle=regel.quelle,
                container=regel.container,
            )
        )

    if not treffer:
        gesamt = Ampel.GRUEN
        treffer = [
            Treffer(
                regel_kuerzel="DEFAULT_GRUEN",
                ampel=Ampel.GRUEN,
                begruendung=_DEFAULT_GRUEN_BEGRUENDUNG,
            )
        ]
    else:
        gesamt = max((t.ampel for t in treffer), key=lambda a: a.schaerfe)

    return AmpelErgebnis(
        icd=icd_norm,
        atc=atc_norm,
        alter=alter,
        gesamt=gesamt,
        treffer=treffer,
    )


def _load_regeln_from_db(conn: sqlite3.Connection) -> List[Regel]:
    """Liest die Regeln aus der DB-Tabelle ``regel`` und ``amrl_anlage``.

    Beide Tabellen werden zu :class:`Regel`-Objekten gemappt; AM-RL-Eintraege
    bekommen das Praefix ``AMRL_<Anlage>_`` als Kuerzel.
    """
    regeln: List[Regel] = []

    rows = conn.execute(
        """
        SELECT r.kuerzel, r.atc_pattern, r.icd_pattern, r.altersgrenze,
               r.ampel, r.begruendung, r.container,
               q.kuerzel, q.titel, q.url, q.stand
        FROM regel r
        LEFT JOIN quelle q ON q.id = r.quelle_id
        """
    ).fetchall()
    for row in rows:
        quelle = None
        if row[7]:
            quelle = Quelle(kuerzel=row[7], titel=row[8], url=row[9], stand=row[10])
        regeln.append(
            Regel(
                kuerzel=row[0],
                atc_pattern=row[1],
                icd_pattern=row[2],
                altersgrenze=row[3],
                ampel=row[4],
                begruendung=row[5],
                container=row[6],
                quelle=quelle,
            )
        )

    rows = conn.execute(
        """
        SELECT a.id, a.anlage, a.atc_pattern, a.bedingung, a.ampel, a.begruendung,
               q.kuerzel, q.titel, q.url, q.stand
        FROM amrl_anlage a
        LEFT JOIN quelle q ON q.id = a.quelle_id
        """
    ).fetchall()
    for row in rows:
        quelle = None
        if row[6]:
            quelle = Quelle(kuerzel=row[6], titel=row[7], url=row[8], stand=row[9])
        bezeichnung = row[3] or ""
        kuerzel = f"AMRL_{row[1]}_{row[0]}"
        begruendung = row[5]
        if bezeichnung:
            begruendung = f"{begruendung} (Bedingung: {bezeichnung})"
        regeln.append(
            Regel(
                kuerzel=kuerzel,
                atc_pattern=row[2],
                ampel=row[4],
                begruendung=begruendung,
                quelle=quelle,
            )
        )

    return regeln
