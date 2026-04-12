"""Maintainer-Tool: Diff-Check fuer AM-RL-Anlagen gegen neue G-BA-PDFs.

NUR FUER MAINTAINER!
====================

Dieses Skript laedt optional eine neue AM-RL-PDF vom G-BA, extrahiert
Rohtext (PyMuPDF) und vergleicht mit der bereits vorhandenen Kopie in
``data/seed/_raw/``. Es meldet, welche Nummern neu / geloescht / geaendert
sind — nimmt aber **keine automatische Uebernahme** in die JSON-Seeds
vor. Die Uebernahme muss manuell erfolgen (Haftungsrisiko, siehe
``data/seed/UPDATE_METHODE.md``).

Abhaengigkeiten (optional):
    - pymupdf   (PDF-Text)
    - requests  (Download von URLs)

Beispiele:
    # Download + Diff gegen aktuelle Raw-Kopie
    python scripts/update_amrl.py --anlage III \
        --url https://www.g-ba.de/downloads/83-691-1036/AM-RL-III-...pdf

    # Diff einer lokal bereits vorliegenden PDF/TXT
    python scripts/update_amrl.py --anlage V \
        --new data/seed/_raw/amrl_V_candidate.pdf

    # Nur Archiv-Kopie aus aktuellem Stand anlegen (ohne Download)
    python scripts/update_amrl.py --archive
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
SEED_DIR = ROOT / "data" / "seed"
RAW_DIR = SEED_DIR / "_raw"
ARCHIV_DIR = SEED_DIR / "_archiv"

ANLAGE_MAP = {
    "III": {"json": "amrl_anlage_III.json", "raw_prefix": "amrl_III_"},
    "V":   {"json": "amrl_anlage_V.json",   "raw_prefix": "amrl_V_"},
    "VI":  {"json": None,                   "raw_prefix": "amrl_VI_"},   # Teil A+B
    "VI_A": {"json": "amrl_anlage_VI_A.json", "raw_prefix": "amrl_VI_"},
    "VI_B": {"json": "amrl_anlage_VI_B.json", "raw_prefix": "amrl_VI_"},
}


def _latest_raw(prefix: str) -> Optional[Path]:
    """Findet die neueste _raw/-Datei fuer die Anlage (lexikalisch groesste)."""
    if not RAW_DIR.exists():
        return None
    candidates = sorted(
        (p for p in RAW_DIR.glob(prefix + "*.txt") if "candidate" not in p.name),
        reverse=True,
    )
    return candidates[0] if candidates else None


def _extract_text(pdf_path: Path) -> str:
    """Extrahiert Text aus einer PDF mittels PyMuPDF.

    Wirft ImportError wenn pymupdf nicht installiert ist.
    """
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "pymupdf fehlt. Installation: pip install pymupdf"
        ) from exc
    doc = fitz.open(str(pdf_path))
    try:
        return "\n".join(page.get_text() for page in doc)
    finally:
        doc.close()


def _download(url: str, target: Path) -> None:
    """Laedt eine URL herunter. Nutzt requests, Fallback urllib."""
    try:
        import requests  # type: ignore
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        target.write_bytes(resp.content)
        return
    except ImportError:
        pass
    from urllib.request import urlopen
    with urlopen(url, timeout=60) as r:
        target.write_bytes(r.read())


def _normalize_lines(text: str) -> List[str]:
    """Entfernt Whitespace und leere Zeilen fuer Diff-Zwecke."""
    return [
        re.sub(r"\s+", " ", line.strip())
        for line in text.splitlines()
        if line.strip()
    ]


def _extract_numbers(text: str) -> Dict[str, str]:
    """Sehr grobe Heuristik: findet 'Nr. <n>' Abschnitte.

    Liefert dict {nummer: erste_zeile}.
    """
    result: Dict[str, str] = {}
    pattern = re.compile(r"^\s*(\d{1,3})\.\s+([^\n]+)", re.MULTILINE)
    for m in pattern.finditer(text):
        nr = m.group(1)
        if nr not in result:
            result[nr] = m.group(2).strip()
    return result


def _load_current_eintraege(anlage: str) -> Tuple[List[Dict], Dict]:
    """Laedt die aktuellen JSON-Eintraege einer Anlage (neu + Legacy-Format)."""
    spec = ANLAGE_MAP.get(anlage)
    if not spec or not spec["json"]:
        return [], {}
    path = SEED_DIR / spec["json"]
    if not path.exists():
        return [], {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        return data.get("eintraege", []), data.get("_meta", {})
    if isinstance(data, list):
        return data, {}
    return [], {}


def cmd_diff(args: argparse.Namespace) -> int:
    """Diff: neue PDF/TXT vs. alte Raw-Kopie + JSON-Nummernliste."""
    anlage = args.anlage
    spec = ANLAGE_MAP.get(anlage)
    if not spec:
        print(f"FEHLER: unbekannte Anlage: {anlage}", file=sys.stderr)
        return 2

    # 1. Neuer Rohtext besorgen
    new_path = Path(args.new) if args.new else None
    if args.url:
        if not new_path:
            target_name = f"{spec['raw_prefix']}{date.today().isoformat()}.pdf"
            new_path = RAW_DIR / target_name
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Lade {args.url} -> {new_path}")
        _download(args.url, new_path)

    if not new_path or not new_path.exists():
        print("FEHLER: --new <pdf_oder_txt> oder --url angeben", file=sys.stderr)
        return 2

    # Text extrahieren
    if new_path.suffix.lower() == ".pdf":
        new_text = _extract_text(new_path)
    else:
        new_text = new_path.read_text(encoding="utf-8", errors="replace")

    # 2. Alte Raw-Kopie finden
    old_path = _latest_raw(spec["raw_prefix"])
    if not old_path:
        print(f"WARNUNG: Keine alte _raw/-Kopie fuer {anlage} gefunden.")
        old_text = ""
    else:
        print(f"Vergleich mit: {old_path}")
        old_text = old_path.read_text(encoding="utf-8", errors="replace")

    # 3. Textzeilen-Diff
    old_lines = _normalize_lines(old_text)
    new_lines = _normalize_lines(new_text)
    diff = list(difflib.unified_diff(
        old_lines, new_lines,
        fromfile=str(old_path) if old_path else "(leer)",
        tofile=str(new_path),
        lineterm="",
        n=1,
    ))
    added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))

    # 4. Nummern-Diff
    old_nrs = _extract_numbers(old_text)
    new_nrs = _extract_numbers(new_text)
    only_old = sorted(set(old_nrs) - set(new_nrs), key=lambda x: int(x))
    only_new = sorted(set(new_nrs) - set(old_nrs), key=lambda x: int(x))

    # 5. JSON-Eintraege: welche Nummern sind aktuell gepflegt?
    eintraege, meta = _load_current_eintraege(anlage)
    json_nrs = {e.get("nr") for e in eintraege if e.get("nr")}

    print()
    print("=" * 70)
    print(f"Diff-Report Anlage {anlage}")
    print("=" * 70)
    print(f"Zeilen hinzugefuegt: {added}")
    print(f"Zeilen entfernt:     {removed}")
    print()
    if only_new:
        print("NEUE Nummern im PDF (nicht im alten Stand):")
        for n in only_new:
            in_json = " [nicht in JSON]" if n not in json_nrs else ""
            print(f"  + Nr. {n}: {new_nrs[n][:80]}{in_json}")
    if only_old:
        print("ENTFERNTE Nummern (im alten Stand, fehlen im neuen):")
        for n in only_old:
            print(f"  - Nr. {n}: {old_nrs[n][:80]}")
    if not only_new and not only_old:
        print("Keine Nummern-Aenderungen erkannt.")

    if args.show_diff and diff:
        print()
        print("-" * 70)
        print("Unified Diff (gekuerzt auf 80 Zeilen):")
        for line in diff[:80]:
            print(line)
        if len(diff) > 80:
            print(f"... ({len(diff)-80} weitere Zeilen ausgelassen)")

    print()
    print("HINWEIS: Keine automatische Uebernahme! Manuelle Pflege noetig.")
    print("Siehe data/seed/UPDATE_METHODE.md Abschnitt 4.")
    return 0


def cmd_archive(args: argparse.Namespace) -> int:
    """Kopiert den aktuellen Seed-Stand nach _archiv/<DATUM>/."""
    target = ARCHIV_DIR / (args.datum or date.today().isoformat())
    target.mkdir(parents=True, exist_ok=True)
    import shutil
    copied = 0
    for spec in ANLAGE_MAP.values():
        if not spec["json"]:
            continue
        src = SEED_DIR / spec["json"]
        if src.exists():
            shutil.copy2(src, target / spec["json"])
            copied += 1
    print(f"{copied} Seed-Dateien archiviert nach: {target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="update_amrl",
        description="Maintainer-Tool: Diff-Check fuer AM-RL-Anlagen.",
    )
    sub = p.add_subparsers(dest="cmd", required=False)

    p_diff = sub.add_parser("diff", help="Neue PDF/TXT vs. alten Stand vergleichen")
    p_diff.add_argument("--anlage", required=True, choices=list(ANLAGE_MAP.keys()))
    p_diff.add_argument("--new", default=None, help="Pfad zu neuer PDF oder TXT")
    p_diff.add_argument("--url", default=None, help="G-BA-Download-URL (optional)")
    p_diff.add_argument("--show-diff", action="store_true", help="Unified-Diff anzeigen")
    p_diff.set_defaults(func=cmd_diff)

    p_arch = sub.add_parser("archive", help="Aktuellen Seed-Stand ins Archiv kopieren")
    p_arch.add_argument("--datum", default=None, help="YYYY-MM-DD (default: heute)")
    p_arch.set_defaults(func=cmd_archive)

    # Kompatibilitaet: wenn kein Subcommand -> diff
    p.add_argument("--anlage", help=argparse.SUPPRESS)
    p.add_argument("--new", help=argparse.SUPPRESS)
    p.add_argument("--url", help=argparse.SUPPRESS)
    p.add_argument("--archive", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--show-diff", action="store_true", help=argparse.SUPPRESS)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "func", None):
        return args.func(args)
    # Kein Subcommand: --archive oder --anlage
    if getattr(args, "archive", False):
        return cmd_archive(args)
    if getattr(args, "anlage", None):
        return cmd_diff(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
