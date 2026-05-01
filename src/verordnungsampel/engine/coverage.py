"""Coverage-Analyse fuer Ampel-Entscheidungen.

Die Metrik folgt der einfachen Forschungsfrage: Fuer welchen Anteil einer
Fallmenge liefert das eingebettete Regelwerk einen expliziten Regeltreffer?

    C(S) = |erklaerte Faelle| / |alle Faelle|

Ein Fall gilt als erklaert, wenn mindestens ein echter Regel-Treffer vorliegt.
Das Default-Gruen ("keine Regel trifft zu") zaehlt bewusst nicht als erklaert.
Die Analyse ist damit eine Regelwerksabdeckung, keine medizinische Validierung.
"""

from __future__ import annotations

import sqlite3
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Optional, Sequence

from verordnungsampel.engine.evaluator import AmpelErgebnis, evaluate
from verordnungsampel.engine.rules import Regel

DEFAULT_GRUEN_RULE = "DEFAULT_GRUEN"


@dataclass(frozen=True)
class CoverageCase:
    """Ein pseudonymisierter Prueffall fuer die Coverage-Analyse."""

    icd: str
    atc: str
    alter: Optional[int] = None
    case_id: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "CoverageCase":
        """Erzeugt einen Fall aus JSON-/Dict-Daten.

        Akzeptierte ID-Felder sind ``id`` und ``case_id``. ``icd`` und ``atc``
        sind Pflichtfelder, weil ohne sie keine Ampel-Auswertung moeglich ist.
        """
        if not isinstance(data, Mapping):
            raise TypeError(
                "Coverage-Fall muss ein Objekt mit 'icd' und 'atc' sein."
            )
        icd = str(data.get("icd", "")).strip()
        atc = str(data.get("atc", "")).strip()
        if not icd or not atc:
            raise ValueError("Coverage-Fall braucht 'icd' und 'atc'.")
        alter_raw = data.get("alter")
        alter = int(alter_raw) if alter_raw not in (None, "") else None
        case_id = data.get("case_id", data.get("id"))
        return cls(
            icd=icd,
            atc=atc,
            alter=alter,
            case_id=str(case_id) if case_id not in (None, "") else None,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.case_id,
            "icd": self.icd,
            "atc": self.atc,
            "alter": self.alter,
        }


@dataclass(frozen=True)
class CoverageCaseResult:
    """Ampel-Auswertung eines einzelnen Coverage-Falls."""

    case: CoverageCase
    ergebnis: AmpelErgebnis

    @property
    def matching_rules(self) -> list[str]:
        return [
            treffer.regel_kuerzel
            for treffer in self.ergebnis.treffer
            if treffer.regel_kuerzel != DEFAULT_GRUEN_RULE
        ]

    @property
    def explained(self) -> bool:
        return bool(self.matching_rules)

    def to_dict(self) -> dict:
        return {
            "case": self.case.to_dict(),
            "gesamt": self.ergebnis.gesamt.value,
            "explained": self.explained,
            "matching_rules": self.matching_rules,
            "container": self.ergebnis.container_hinweise,
        }


@dataclass(frozen=True)
class CoverageReport:
    """Aggregierter Coverage-Bericht fuer eine Fallmenge."""

    results: list[CoverageCaseResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def explained_count(self) -> int:
        return sum(1 for result in self.results if result.explained)

    @property
    def unexplained_count(self) -> int:
        return self.total - self.explained_count

    @property
    def coverage_ratio(self) -> float:
        if self.total == 0:
            return 0.0
        return self.explained_count / self.total

    @property
    def by_ampel(self) -> dict[str, int]:
        counter = Counter(result.ergebnis.gesamt.value for result in self.results)
        return {farbe: counter.get(farbe, 0) for farbe in ("rot", "gelb", "gruen")}

    @property
    def rule_hits(self) -> dict[str, int]:
        counter: Counter[str] = Counter()
        for result in self.results:
            counter.update(result.matching_rules)
        return dict(sorted(counter.items()))

    @property
    def unexplained_cases(self) -> list[CoverageCase]:
        return [result.case for result in self.results if not result.explained]

    def to_dict(self) -> dict:
        return {
            "metric": "C(S)=explained/total",
            "total": self.total,
            "explained": self.explained_count,
            "unexplained": self.unexplained_count,
            "coverage_ratio": self.coverage_ratio,
            "coverage_percent": round(self.coverage_ratio * 100, 2),
            "by_ampel": self.by_ampel,
            "rule_hits": self.rule_hits,
            "unexplained_cases": [case.to_dict() for case in self.unexplained_cases],
            "results": [result.to_dict() for result in self.results],
        }


def normalize_cases(
    cases: Iterable[CoverageCase | Mapping[str, Any]],
) -> list[CoverageCase]:
    """Normalisiert Coverage-Faelle aus Dataclasses oder Mapping-Objekten."""
    normalized: list[CoverageCase] = []
    for case in cases:
        if isinstance(case, CoverageCase):
            normalized.append(case)
        elif isinstance(case, Mapping):
            normalized.append(CoverageCase.from_mapping(case))
        else:
            raise TypeError(
                "Coverage-Faelle muessen CoverageCase oder Mapping sein, "
                f"nicht {type(case).__name__}."
            )
    return normalized


def analyze_cases(
    cases: Iterable[CoverageCase | Mapping[str, Any]],
    *,
    regeln: Optional[Sequence[Regel]] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> CoverageReport:
    """Berechnet die Regelwerksabdeckung fuer eine Fallmenge.

    Args:
        cases: Iterable aus ``CoverageCase`` oder JSON-kompatiblen Dicts.
        regeln: Optionaler In-Memory-Regelsatz fuer Tests/Szenarien.
        conn: Optionale SQLite-Verbindung zur echten Regelwerksdatenbank.

    Returns:
        ``CoverageReport`` mit C(S), Ampel-Verteilung und unerklaerten Faellen.
    """
    normalized = normalize_cases(cases)
    results: list[CoverageCaseResult] = []
    for case in normalized:
        ergebnis = evaluate(
            case.icd,
            case.atc,
            alter=case.alter,
            regeln=regeln,
            conn=conn,
        )
        results.append(CoverageCaseResult(case=case, ergebnis=ergebnis))
    return CoverageReport(results=results)
