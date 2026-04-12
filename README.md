# VerordnungsAmpel

> Companion-Tool für niedergelassene Vertragsärzte zur Regress-Prävention
> im Moment der Verordnung.
>
> Companion tool for German physicians to prevent recoupment claims at the
> point of prescription.

> ⚠️ **Rechtlicher Hinweis / Legal Notice**
>
> VerordnungsAmpel ist ein **Informations- und Nachschlagewerk**.
> Kein Medizinprodukt. Nicht klinisch validiert. Nicht durch BfArM oder
> Benannte Stelle geprüft. Nicht zertifiziert. Kein Wartungsvertrag,
> kein Support-Versprechen, keine Verfügbarkeitszusage. Nutzung auf
> eigenes Risiko. Die ärztliche Verantwortung bleibt unverändert
> (§ 76 SGB V, § 630a BGB).
>
> Unentgeltliche Open-Source-Schenkung gemäß §§ 516 ff. BGB. Haftung
> auf Vorsatz und grobe Fahrlässigkeit beschränkt (§ 521 BGB, GPL-3.0
> §§ 15/16).

**Status:** Pre-Alpha v0.1.0 — CLI-MVP funktional, PySide6-Tray-GUI in Entwicklung
**Lizenz / License:** GPL-3.0-or-later
**Repository:** https://github.com/research-line/verordnungsampel

---

## Deutsch

### Was es ist

Ein Open-Source-Tool, das neben dem Praxisverwaltungssystem (PVS) läuft und bei jeder
ärztlichen Verordnung die Kombination aus **ICD-10-GM-Code** und **ATC-Code** gegen
öffentliche Regelwerke prüft. Ausgabe: eine Ampel (grün/gelb/rot) mit Begründung,
Quellenverweis und fälschungssicherem Audit-Trail.

**Was es nicht ist:** Kein Praxisverwaltungssystem. Kein Medical Device (im Sinne der
MDR). Keine Patientendatenverarbeitung. Nur Plausibilitätsprüfung gegen öffentliche
Regelwerke.

### Warum

- **47 %** der deutschen Hausärzte ändern ihr Verordnungsverhalten aus Regressangst
  (Ribbat et al. 2023, n ≈ 800)
- **75 %** der Praxen würden ihr aktuelles PVS *nicht* weiterempfehlen
  (Zi-Studie 2024, 10 245 Bewertungen)
- Drei kritische Funktionslücken in allen kommerziellen PVS:
  1. Strukturierte Begründungspflicht im Moment der Verordnung
  2. Bundesweite Praxisbesonderheiten-Erkennung
  3. Manipulationssicherer Compliance-Log mit Beweiskraft vor Sozialgericht

### Funktionen (alle 5 im MVP umgesetzt)

| # | Funktion | Status |
|---|---|---|
| 1 | Echtzeit-Plausibilitätsprüfung (Ampel gegen AM-RL III/V/VI, PRISCUS 2.0) | ✅ |
| 2 | Strukturierte Begründungspflicht als Hierarchical State Machine (BSG-konform) | ✅ |
| 3 | Vorab-Klärungs-Workflow container-sensitiv (Pflicht / Verboten / Stellungnahme) | ✅ |
| 4 | Praxisbesonderheiten-Erkennung + Quartalsreminder | ✅ |
| 5 | Manipulationssicherer Compliance-Log (Hash-Chain) | ✅ |

Test-Suite: **86 / 86 passed**.

### Schnellstart

```bash
# Installation (Source)
git clone https://github.com/research-line/verordnungsampel.git
cd verordnungsampel
pip install -r requirements.txt
pip install -e .

# Datenbank initialisieren (+ Seed-Daten laden)
python -m verordnungsampel.cli.main init

# Beispiele
python -m verordnungsampel.cli.main check --icd I10   --atc C09AA02              # GRÜN
python -m verordnungsampel.cli.main check --icd M54.5 --atc A02BC02              # GELB
python -m verordnungsampel.cli.main check --icd F41   --atc N05BA01  --alter 72  # ROT

# Strukturierte Begründung (HSM, interaktiv)
python -m verordnungsampel.cli.main justify --icd F41 --atc N05BA01 --alter 72

# Vorab-Antrag generieren
python -m verordnungsampel.cli.main workflow --icd R52.1 --atc QV12 \
    --kk "Musterkasse" --praxis "Musterpraxis" \
    --arzt "Dr. med. Musterarzt" --patient P-4711 --out antrag.txt

# Quartalsreminder
python -m verordnungsampel.cli.main remind --quartal 2026-Q2

# Compliance-Log
python -m verordnungsampel.cli.main log
python -m verordnungsampel.cli.main verify
```

Unter Windows: Doppelklick auf `start.bat` öffnet ein interaktives Demo-Menü.

### GUI (PySide6-Tray-Modus)

Das Tool kann als Tray-Anwendung neben dem PVS laufen (Companion-Modus):

```bash
pip install -e ".[gui]"
python -m verordnungsampel.cli.main gui
```

Das Hauptfenster ist kompakt, lässt sich per Klick auf „X“ ins System-Tray minimieren
und wird erst über **Rechtsklick auf das Tray-Icon → Beenden** wirklich geschlossen.
Always-on-top, Minimal-Modus und Transparenz-Optionen sind verfügbar.

### Architektur

| Komponente | Wahl |
|---|---|
| CLI-Kern | Python-Stdlib (sqlite3, hashlib, argparse) |
| GUI | PySide6 (LGPL, Qt Company) |
| Datenbank | SQLite, lokal in `%APPDATA%\VerordnungsAmpel\regelwerk.db` |
| Regelwerke | AM-RL Anlagen III / V / VI als JSON-Seed (`data/seed/`) |
| Compliance-Log | Hash-Chain, versiegelt Ampel-Ergebnis + Begründung + Workflow |

### Dokumentation

- [`KONZEPT.md`](KONZEPT.md) — Vollständiges Projektkonzept
- [`CHANGELOG.md`](CHANGELOG.md) — Versionshistorie
- [`docs/CODE_AUDIT.md`](docs/CODE_AUDIT.md) — Audit der Referenz-Codebases
- [`docs/RESOURCES_DIAGNOSTIC_PAPER.md`](docs/RESOURCES_DIAGNOSTIC_PAPER.md) — Pattern-Quellen (Geiger 2026)
- [`docs/legal/RECHTSGUTACHTEN_MDSW.md`](docs/legal/RECHTSGUTACHTEN_MDSW.md) — Erstgutachten „Informationswerk vs. MDSW"
- [`docs/legal/DSGVO_KONZEPT.md`](docs/legal/DSGVO_KONZEPT.md) — Datenschutz-Konzept

### Beziehung zu Um:bruch / Regress-Melder

- **PP-003** (Um:bruch) = anonyme Meldeplattform für bereits geschehene Regresse
- **ST-001** (Um:bruch) = wissenschaftliche Begleitstudie zum Regress-System
  https://github.com/research-line/regressangst
- **VerordnungsAmpel** (dieses Projekt) = Werkzeug zur Verhinderung künftiger Regresse
  VOR der Verordnung

### Mitwirken

Beiträge sind willkommen — insbesondere Aktualisierungen der AM-RL-Regelwerke und
neue Rechtsprechung. Siehe [`CONTRIBUTING.md`](CONTRIBUTING.md) (DCO-Signoff nötig).

### Haftungshinweis

Die VerordnungsAmpel ist ein **Informations- und Nachschlagewerk**. Sie ersetzt nicht
die ärztliche Prüfung im Einzelfall und stellt keine Rechtsberatung dar. Alle Entscheidungen
liegen bei der Ärztin / dem Arzt.

---

## English

### What it is

An open-source companion tool for German outpatient physicians that runs alongside the
practice-management system (PVS) and, at the moment of prescribing, checks the combination
of **ICD-10-GM code** and **ATC code** against public rule sets. Output: a traffic light
(green / yellow / red) with justification, source reference, and a tamper-proof audit trail.

**What it is not:** not a practice-management system, not a medical device, no patient
data processing. Pure plausibility checking against public rule sets.

### Why

- **47 %** of German GPs alter their prescribing behaviour out of fear of economic-efficiency
  review recoupments (Ribbat et al. 2023)
- **75 %** of practices would *not* recommend their current PVS (Zi 2024)
- Three critical functional gaps in all commercial PVS: structured rationale capture at
  time of prescription, nationwide practice-specifics detection, and a tamper-proof
  compliance log with evidentiary weight in social court proceedings.

### Features (all 5 MVP functions shipped)

1. Real-time plausibility check (traffic light against AM-RL annexes III / V / VI, PRISCUS 2.0)
2. Structured rationale capture as a Hierarchical State Machine (compliant with BSG case law)
3. Container-sensitive prior-clarification workflow (mandatory / forbidden / opinion-request)
4. Practice-specifics detection + quarterly reminder
5. Tamper-proof compliance log (hash chain)

Test suite: **86 / 86 passed**.

### Quick Start

```bash
git clone https://github.com/research-line/verordnungsampel.git
cd verordnungsampel
pip install -r requirements.txt
pip install -e .
python -m verordnungsampel.cli.main init
python -m verordnungsampel.cli.main check --icd I10 --atc C09AA02
```

### GUI (PySide6 tray mode)

```bash
pip install -e ".[gui]"
python -m verordnungsampel.cli.main gui
```

The main window is compact and, on clicking "X", minimises to the system tray. It is
only fully terminated by **right-clicking the tray icon → Quit**.

### Relationship to Um:bruch / Regress-Melder

- **PP-003** — anonymous reporting platform concept for past recoupments
- **ST-001** — scientific companion study — https://github.com/research-line/regressangst
- **VerordnungsAmpel** — this project — tool to prevent future recoupments before they happen

### Disclaimer

VerordnungsAmpel is an **information / reference tool**. It does not replace medical
judgement in individual cases and does not constitute legal advice. All decisions remain
with the practising physician.

---

*Project home: https://um-bruch.org*
