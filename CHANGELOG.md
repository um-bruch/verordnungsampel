# Changelog / Änderungsprotokoll

Alle wesentlichen Änderungen an diesem Projekt werden hier dokumentiert.
Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

## [Unreleased]

### Hinzugefügt / Added
- PySide6-basierte Tray-GUI (Companion-Modus neben Praxisverwaltungssystemen)
- Vollständiger AM-RL-Seed-Datensatz (Anlagen III, V, VI-A, VI-B)
- Coverage-Analyse für Ampel-Entscheidungen: `coverage --cases cases.json`
  berechnet C(S)=erklärte Fälle/alle Fälle mit Regel-Treffern und Default-Grün-Liste
- Erstes KI-basiertes Rechtsgutachten: Status als Informationswerk vs. MDSW
- DSGVO-Konzept (Verarbeitungsverzeichnis, TOMs, Betroffenenrechte, Löschkonzept)
- GitHub-Pflichtdateien (CODE_OF_CONDUCT, SECURITY, CONTRIBUTING, FUNDING)
- Reproduzierbarer lokaler Windows-Build via `build_exe.bat` und `verordnungsampel_gui.py`
- Gitignore-Abdeckung für lokale Build-Artefakte, Secrets, Credentials und Test-Locks erweitert

### Geändert / Changed
- Ordner-Lifecycle: DEV → PreGit → GO-PRI; GitHub-Sichtbarkeit ist inzwischen öffentlich.
- Repository-URL: github.com/research-line/verordnungsampel
- Der lokale `.SOFTWARE`-Ordnername bleibt bis zur nächsten Lifecycle-Bereinigung unverändert.
- Zweckbestimmung neu formuliert: **"Regress-Prävention"** als Vermarktungsbegriff fallengelassen (Risiko § 444 BGB Zusicherung, § 5 UWG irreführende Werbung, MDR-Zweckbestimmung). Neu: "Softwareentwurf zur Anzeige bekannter Regress-Risikoindikatoren aus öffentlichen Regelwerken — zu Forschungs- und Weiterentwicklungszwecken, ohne Gewähr." Betroffen: README, NOTICE, pyproject.toml, GUI-Strings, DSGVO-Konzept, Marktvergleich.
- Desktop-Packaging dokumentiert: lokaler PyInstaller-Onedir-Build mit Seed-Daten und Tray-Icons

### Behoben / Fixed
- Marketing-Blacklist: "KI" als interne Abkürzung für Kontraindikation ersetzt (Verwechslungsgefahr mit AI/KI); "KI-gestützt" → "KI-basiert" in USER-GUIDE

## [0.1.0] - 2026-04-08

### Hinzugefügt / Added
- MVP-Kern mit allen 5 KONZEPT-Funktionen
- SQLite-Regelwerk (`db/schema.py`, `db/seed.py`, `db/connection.py`)
- Ampel-Engine GRÜN/GELB/ROT mit Container-Logik (`engine/evaluator.py`, `engine/rules.py`)
- Kryptografische Hash-Chain als Compliance-Log (`audit/compliance_log.py`)
- Strukturierte Begründungspflicht als Hierarchical State Machine (`engine/justification_fsm.py`)
  Pattern adaptiert aus Geiger (2026) *"An Integrated Multiaxial Model for Computer-Assisted Psychiatric Diagnosis"*, Section 9 (DOI 10.5281/zenodo.18736725)
- Vorab-Klärungs-Workflow container-sensitiv (`output/vorab_workflow.py`):
  PFLICHT_ANTRAG / VERBOTEN_HINWEIS / STELLUNGNAHME / KEINE_AKTION
- Praxisbesonderheiten-Erkennung + Quartalsreminder (`engine/praxisbesonderheit.py`)
- CLI-Frontend mit 7 Subcommands: `init`, `check`, `log`, `verify`, `justify`, `workflow`, `remind`
- Interaktives Demo-Menü (`start.bat` mit 14 Optionen)
- Seed-Daten MVP-Umfang: 10 Quellen, 13 ICD-10, 16 ATC, 4 AM-RL-Anlagen, 2 Praxisbesonderheiten, 10 Regeln
- Test-Suite: 86/86 tests passed
- Projekt-Dokumentation: KONZEPT.md, README.md, CODE_AUDIT.md, RESOURCES_DIAGNOSTIC_PAPER.md

### Architekturentscheidungen
- Python-Stdlib-only für MVP-Kern (sqlite3, json, hashlib, argparse, datetime)
- GPL-3.0-Lizenz
- Kein PVS, kein Medical Device, keine Patientendaten (nur ICD- und ATC-Codes)
- Lokale Speicherung in SQLite (`%APPDATA%\VerordnungsAmpel\regelwerk.db`)
