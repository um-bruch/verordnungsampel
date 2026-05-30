# Changelog / Änderungsprotokoll

Alle wesentlichen Änderungen an diesem Projekt werden hier dokumentiert.
Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

## [Unreleased]

### Hinzugefügt / Added
- `llms.txt` als maschinenlesbarer Projektkontext mit klarer Nicht-MDSW-,
  Nicht-CDS- und Research-Use-Only-Abgrenzung.
- Zusätzlicher README-Screenshot `README/screenshots/main-window.png` für das
  eigentliche Ampel-Hauptfenster; der vorhandene Disclaimer-Screenshot bleibt als
  Sicherheitshinweis sichtbar.
- GitHub Actions für Windows-Testläufe sowie Stale-/Welcome-Community-Workflows.
- `PORTIERUNGSPLAN.md` mit Usecase-basierter Plattformentscheidung: Windows und lokale Web/PWA bleiben primär, macOS/Linux werden als Source-Smokes geplant, Android/iOS nur als PWA-Smoke, Windows Store ist derzeit kein Ziel.
- `EXPORTFORMAT.md` als Planungsgrundlage für dateibasierte, pseudonymisierte Fallbündel und Regelwerks-Snapshots ohne Cloud-Synchronisierung.
- PySide6-basierte Tray-GUI (Companion-Modus neben Praxisverwaltungssystemen)
- Vollständiger AM-RL-Seed-Datensatz (Anlagen III, V, VI-A, VI-B)
- Coverage-Analyse für Ampel-Entscheidungen: `coverage --cases cases.json`
  berechnet C(S)=erklärte Fälle/alle Fälle mit Regel-Treffern und Default-Grün-Liste
- i18n-Infrastruktur (DE/EN): JSON-basierte Übersetzungen unter
  `data/translations/de.json` und `data/translations/en.json`, neues Modul
  `verordnungsampel.i18n` mit `t()`, `set_language()`, `get_language()`,
  `available_languages()`. Schema angelehnt an Geiger 2026 (DOI 10.5281/zenodo.18736725, MIT).
  Bestehender Code (`from gui import strings_de as S; S.APP_TITLE`) wird per
  PEP 562-Bridge weiterhin unterstützt und reagiert auf Sprachwechsel.
- Erstes KI-basiertes Rechtsgutachten: Status als Informationswerk vs. MDSW
- DSGVO-Konzept (Verarbeitungsverzeichnis, TOMs, Betroffenenrechte, Löschkonzept)
- GitHub-Pflichtdateien (CODE_OF_CONDUCT, SECURITY, CONTRIBUTING, FUNDING)
- Reproduzierbarer lokaler Windows-Build via `build_exe.bat` und `verordnungsampel_gui.py`
- Gitignore-Abdeckung für lokale Build-Artefakte, Secrets, Credentials und Test-Locks erweitert
- SQLite-Schema v2 mit Relationstabellen für AM-RL-, Praxisbesonderheits- und
  Regelwerks-Patterns zu bekannten ICD-/ATC-Codes
- Seed-Loader füllt diese Code-Relationen nach jedem `init` idempotent neu
- Test-Suite-Wachstum: 24 neue Tests in `tests/test_i18n.py`
  (Lazy-Load, Fallback DE↔EN, Format-Substitution, Bridge-Kompatibilität,
  Konsistenz DE/EN-Keysets)
- Test-Suite-Wachstum: 2 neue DB-Tests für Schema-v2-Relationen und
  idempotente Pattern-Expansion

### Geändert / Changed
- README-Discoverability für `VerordnungsAmpel`, AM-RL/G-BA, ICD-10-GM/ATC,
  PRISCUS 2.0, Praxisbesonderheiten und local-first Health-Policy-Research
  verbessert, ohne Wirk- oder Validierungsversprechen zu ergänzen.
- Paketbeschreibung, Keywords und Classifiers in `pyproject.toml` auf
  Research-Use-Only und Information-Analysis statt Medical-Software-Positionierung
  geschärft.
- Ordner-Lifecycle: DEV → PreGit → GO-PRI; GitHub-Sichtbarkeit ist inzwischen öffentlich.
- Repository-URL: github.com/research-line/verordnungsampel
- Der lokale `.SOFTWARE`-Ordnername bleibt bis zur nächsten Lifecycle-Bereinigung unverändert.
- Zweckbestimmung neu formuliert: **"Regress-Prävention"** als Vermarktungsbegriff fallengelassen (Risiko § 444 BGB Zusicherung, § 5 UWG irreführende Werbung, MDR-Zweckbestimmung). Neu: "Softwareentwurf zur Anzeige bekannter Regress-Risikoindikatoren aus öffentlichen Regelwerken — zu Forschungs- und Weiterentwicklungszwecken, ohne Gewähr." Betroffen: README, NOTICE, pyproject.toml, GUI-Strings, DSGVO-Konzept, Marktvergleich.
- Desktop-Packaging dokumentiert: lokaler PyInstaller-Onedir-Build mit Seed-Daten und Tray-Icons
- Öffentliche Konzept- und Ressourcen-Dokumentation um Hinweise auf lokale Referenzspiegel und interne Projektnamen bereinigt.
- README, User-Guide und Seed-Dokumentation auf den aktuellen Stand der 151 Tests, die Quellen-Ansicht und den manuellen AM-RL-Update-Check gebracht.
- README-Teststand auf 154 lokale Tests aktualisiert.
- Repo-Hygiene ergänzt: `.gitattributes` für stabile Zeilenenden und `.gitignore` für SQLite-Sidecars, Coverage-, Cache- und Zertifikatsartefakte.

### Behoben / Fixed
- Deutsche Nutzertexte im Regelwerke-Tab nutzen echte Umlaute für "angestoßen" und "Einträge".
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
