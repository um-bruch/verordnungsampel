# VerordnungsAmpel — Konzeptdokument

> Erstellt: 2026-04-08 | Aktualisiert: 2026-04-12 | Status: CLI-MVP + GUI lauffähig
> Rechtsform: keine eigene. Urheber: Lukas Geiger (c/o Um:bruch Think Tank, nicht als e.V. eingetragen)
> Veröffentlichung: reines Open-Source-Projekt, GPL-3.0-or-later
> Betreuung und Testung: werden ausdrücklich NICHT durch den Urheber übernommen. Dritte (Ärzteverbände, Forschungsgruppen, Vereine) sind eingeladen, das Tool aufzugreifen, zu evaluieren und weiterzuentwickeln.

> **Hinweis (Revision 2026-04-12):** Die ursprüngliche Annahme "Trägerschaft durch Um:bruch e.V. + Therapiefreiheit e.V." (Stand 2026-04-08) wurde verworfen. Es gibt keinen eingetragenen Verein Um:bruch, und der Kontakt zu Therapiefreiheit e.V. wurde nicht hergestellt. Die Software wird als reine OSS veröffentlicht, **ohne** Trägerkonstellation, **ohne** Förderantrag, **ohne** Pilot-Praxen, **ohne** Kooperationsankündigung. Frühere Abschnitte sind historisch und werden als solche kenntlich gemacht.

---

## Worum geht es?

**VerordnungsAmpel** ist ein Companion-Tool für niedergelassene Vertragsärzte in Deutschland, das im Moment der Verordnung Regress-Risiken sichtbar macht und juristisch belastbare Begründungen erzeugt. Es ist **kein Praxisverwaltungssystem** und ersetzt keines — es arbeitet daneben als Browser-Tool oder Companion-App.

**Kernfunktion in einem Satz:** Eingabe = ICD-Code + Wirkstoff/ATC. Verarbeitung = Plausibilitätsprüfung gegen öffentliche Regelwerke + erzwungene strukturierte Begründung. Ausgabe = Ampel (grün/gelb/rot) mit Begründung, Quellenverweis und Direkt-Eintrag in die Patientenakte.

---

## Warum dieses Projekt?

### Die Daten

Aus der Recherche im April 2026 (siehe Um:bruch / Regress-Melder):

- **47% der deutschen Hausärzte / 55% der Orthopäden** ändern ihr Verordnungsverhalten aus Regressangst (Ribbat et al. 2023, n≈800, bundesweit)
- **51% der Hausärzte** überweisen Patienten an Spezialisten, obwohl sie selbst behandeln könnten (Ribbat 2023)
- **75% der Praxen würden ihr aktuelles PVS NICHT weiterempfehlen** (Zi-Studie 2024, 10.245 Bewertungen)
- **27% der Hausärzte** haben "starke Rechtsangst", **54%** ordnen wöchentlich unnötige Labortests an (Goetz et al. 2024, BMC Primary Care)
- **155.678 Vertragsärzte** in Deutschland (KBV 2025, ohne Psychotherapeuten)

### Der Markt

- **Marktversager:** CompuGroup Medical (TURBOMED, MEDISTAR, ALBIS) und medatixx (x.isynet) dominieren mit ca. 78% Marktanteil
- **Keine Listenpreise** veröffentlicht
- **Gesamtbelastung Hausarztpraxis:** 130-600 EUR/Monat netto durch PVS, bei Vollausstattung über 10.000 EUR/Jahr
- **Drei kritische Funktionslücken** in allen kommerziellen PVS:
  1. Strukturierte Begründungspflicht im Moment der Verordnung
  2. Bundesweite Praxisbesonderheiten-Erkennung
  3. Manipulationssicherer Compliance-Log mit Beweiskraft vor Sozialgericht

### Die juristische Lage

Die juristisch belegten TOP-3-Schutzmaßnahmen sind alle softwaregestützt umsetzbar:

1. **Lückenlose Dokumentation ZUM ZEITPUNKT der Verordnung** (SG Marburg 14.02.2024, S 18 KA 96/23; BSG B 6 KA 26/13: nachgereichte Doku reicht NICHT)
2. **Vorab-Klärung in den expliziten Ausnahmefällen** (Cannabis nach § 31 Abs. 6 SGB V, häusliche Krankenpflege § 37, Soziotherapie § 37a, stationäre Reha § 40, bestimmte Heil-/Hilfsmittel) — NICHT bei normalen Arzneimitteln mit Indikation (§ 29 BMV-Ä verbietet Vorabprüfung)
3. **Substanziierter Vortrag von Praxisbesonderheiten BEREITS im Verwaltungsverfahren** (LSG BW 15.11.2023, SG Marburg 31.01.2024)

---

## Funktionen (MUST-Have MVP)

### 1. Echtzeit-Plausibilitätsprüfung

Eingabe: ICD-10-GM-Code + Wirkstoff/ATC-Code
Verarbeitung: Abgleich gegen
- AM-RL Anlage III (Verordnungseinschränkungen)
- AM-RL Anlage V (Off-Label-Empfehlungen)
- AM-RL Anlage VI (Off-Label-Entscheidungen des G-BA)
- PRISCUS 2.0 bei Altersangabe >65
- GKV-SV-Liste bundesweiter Praxisbesonderheiten

Ausgabe: Ampel grün / gelb / rot mit Begründungstext und Quellenverweis

### 2. Strukturierte Begründungspflicht-Templates ✅ implementiert (2026-04-08)

Bei jeder regressanfälligen Verordnung erzwingt das Tool eine strukturierte Begründung:
- Diagnose
- Vorbehandlung (was wurde versucht?)
- Therapieversagen (warum nicht ausreichend?)
- BSG-Off-Label-Kriterien-Checkliste (wenn relevant, 3 kumulative Kriterien)
- Praxisbesonderheit (wenn vorhanden, optional)
- Bestätigung

**Umgesetzt als Hierarchical State Machine** (`src/verordnungsampel/engine/justification_fsm.py`), Pattern adaptiert aus Geiger (2026) Section 9. Die FSM bestimmt die erforderlichen Schritte abhängig von Ampelfarbe und Container (siehe `required_steps_for`), validiert Pflichtfelder und versiegelt das Ergebnis im `extra`-Feld des Compliance-Logs als Teil der Hash-Chain.

Ausgabe: Direkt-Eintrag in den Compliance-Log (mit Audit-Trail + Hash-Chain-Schutz). CLI: `justify --icd ... --atc ...` interaktiv oder mit `--answers antworten.json` non-interactive.

### 3. Vorab-Klärungs-Workflow (Container-sensitiv) ✅ implementiert (2026-04-08)

Das Tool unterscheidet sauber zwischen:
- **Pflicht-Vorabgenehmigung** (Cannabis, Soziotherapie, häusliche Krankenpflege, Reha, bestimmte Heil-/Hilfsmittel) → automatische Antragsgenerierung an die KK
- **Verbotene Vorabgenehmigung** (normale Arzneimittel mit Indikation, § 29 BMV-Ä) → Hinweis: "Kasse darf hier nicht genehmigen, dokumentiere defensiv"
- **Stellungnahme-Möglichkeit** (Grauzonen wie GLP-1, vertraulicher Erstattungsbetrag) → Hilfe beim Verfassen einer Bitte um Stellungnahme nach BSG B 6 KA 27/12 R

**Umgesetzt als pure function** (`src/verordnungsampel/output/vorab_workflow.py`). Die Funktion `determine_workflow(ergebnis)` leitet den Typ aus Container-Hinweisen der Ampel-Engine ab, `build_workflow(ergebnis, context, justification)` rendert einen vollständigen Brief/Hinweis-Text mit Praxisdaten, Rechtsgrundlage und nächstem Schritt. Optional wird eine bereits erfasste Justification in den Antragstext eingebettet. CLI: `workflow --icd ... --atc ... --kk ... --patient P-4711 --out antrag.txt`. Workflow-Typ wird als `extra.workflow` im Compliance-Log versiegelt.

### 4. Praxisbesonderheiten-Erkennung mit Quartalsmarkierung ✅ implementiert (2026-04-08)

- AMNOG-Liste der anerkannten Praxisbesonderheiten
- Erinnerung am Quartalsende: "Hast du KV-Kennziffer auf dem Behandlungsschein markiert?"
- Pattern-Erkennung: Welche Patientenstrukturen rechtfertigen Praxisbesonderheit-Antrag?

**Umgesetzt** in `src/verordnungsampel/engine/praxisbesonderheit.py`:
- `find_matching(icd, atc, conn, stichtag)` — Pattern-Match auf ATC + ICD mit Gültigkeitsprüfung
- `parse_quartal("2026-Q2")` / `build_quartal_reminder(log_entries, quartal)` — Reminder geht durch den Compliance-Log und listet alle Verordnungen mit PB-Treffer eines Quartals auf
- `render_reminder()` — druckfertige Textausgabe mit Rechtshinweis (LSG BW 15.11.2023)

CLI: `check`/`justify` zeigen PB-Hinweise automatisch an und versiegeln sie als `extra.praxisbesonderheiten` im Compliance-Log. Neuer Subcommand `remind --quartal 2026-Q2` erzeugt den Quartalsreport.

### 5. Manipulationssicherer Compliance-Log

- Alle Verordnungen mit Zeitstempel
- Erzeugte Begründung
- Abgelaufene Warnungen
- **Beweiskraft im Sozialgerichtsverfahren** (kryptographisch versiegelt, nicht nachträglich änderbar)

---

## Was es NICHT ist

- ❌ Kein Praxisverwaltungssystem (PVS)
- ❌ Keine Patientendatenverarbeitung (nur ICD-Codes + Wirkstoffe, keine Personendaten)
- ❌ Keine Medical Device Software (rechtlich: Informations-/Nachschlagewerk, nicht MDSW — vermeidet MDR Klasse IIa)
- ❌ Keine KBV-Zertifizierung nötig
- ❌ Kein Konkurrent zu CGM/medatixx — sondern Companion-Tool

---

## Architektur

| Komponente | Wahl | Begründung |
|---|---|---|
| Frontend | PWA / Browser-App | Kein Installations-Stress, plattformunabhängig |
| Backend | Lokal (PWA) oder leichtes Hetzner Webhosting | Keine Patientendaten = einfache Architektur |
| Datenbank | SQLite mit eingebetteten Regelwerken | Portabel, keine Cloud-DB nötig |
| Daten-Updates | GitHub Actions Quartalsbuild | Versioniert, transparent |
| Wirkstoff-Stammdaten | ATC-Codes (WHO, kostenfrei) | Kein ABDATA/MMI-Lizenzbedarf |
| Regelwerke | AM-RL Anlagen III/V/VI als JSON (manuell extrahiert) | Öffentlich, frei |
| Hosting | Hetzner Webhosting S | <20 €/Monat |

**Bewusste Einschränkung:** Keine PZN, keine Preise, keine Rabattverträge — diese Daten sind im ABDATA/MMI-Oligopol gefangen und für ein offenes Tool nicht zugänglich. Das ist ein Trade-off, kein Bug.

---

## Aufwand und Zeitrahmen

**Schätzung:** 28-52 Personenmonate, **12-24 Monate mit 1-2-Personen-Team** (oder 6-9 Monate radikal fokussiert auf einen MVP).

**Hauptkostenfaktor:** Medizinischer Reviewer für laufende Regelpflege (kein Code-Aufwand, sondern Domänen-Wissen).

---

## Trägermodell (historisch — siehe Revisionshinweis oben)

> Die folgende Tabelle stand im ursprünglichen Konzept vom 2026-04-08 und ist am 2026-04-12 **verworfen** worden. Das Projekt wird als reine OSS ohne Träger veröffentlicht. Dritte Organisationen können das Tool aufgreifen und eigene Trägerkonstellationen aufbauen.

| Rolle (historisch, ~~nicht umgesetzt~~) | ~~Träger~~ |
|---|---|
| ~~Projektheimat~~ | ~~Um:bruch e.V.~~ (nicht eingetragener Verein) |
| ~~Medizinischer Review-Partner~~ | ~~Therapiefreiheit e.V.~~ (Kontakt nicht hergestellt) |
| ~~Förderung~~ | ~~Prototype Fund der Open Knowledge Foundation Deutschland~~ (nicht beantragt) |
| ~~Pilot~~ | ~~10 Praxen~~ (nicht rekrutiert) |
| Bauträger ❌ | NICHT die KV (struktureller Interessenkonflikt) — diese Aussage gilt weiterhin |

**Aktueller Stand:** Keine Trägerschaft. Das Tool ist lauffähiger OSS-Code auf GitHub, dokumentiert als Informationswerk. Interessierte Träger können es forken, evaluieren und unter GPL-3.0 weiterverbreiten.

---

## Beziehung zu PP-003 / ST-001

Dieses Projekt ist die **technische Schwester** des Konzeptpapiers PP-003 (Regress-Transparenzportal) und der Begleitstudie ST-001 (Systemtheoretische Aufarbeitung der Regressangst).

- **PP-003** = Datensammlung über bereits geschehene Regresse (anonyme Meldeplattform)
- **ST-001** = Wissenschaftliche Tiefenanalyse warum das nötig ist
- **VerordnungsAmpel** = Softwareentwurf zur Anzeige bekannter Regress-Risikoindikatoren vor der Verordnung

Die drei Bausteine ergänzen sich:
- PP-003 schließt die Daten-Lücke (was passiert ist)
- VerordnungsAmpel schließt die Informations-Lücke am Verordnungspunkt
- ST-001 liefert die Begründung für beides

---

## Codebases zum Ausschlachten

Im Ordner `_codebases/` liegen zwei bestehende Um:bruch/Lukisch-Projekte als Referenzen, deren Architektur und Komponenten wiederverwendet werden können:

### REF_MediPlaner_CASHCOW

**Pfad:** `_codebases/REF_MediPlaner_CASHCOW/`

**Was da brauchbar ist:**
- Datenbankarchitektur (`database.py`) — SQLite-Setup, Migration, Schema-Verwaltung
- PDF-Export (`pdf_export.py`) — könnte für Compliance-Log-Export genutzt werden
- Inventory-System (`inventory.py`) — Pattern für Wirkstoff-Stammdaten-Verwaltung
- i18n / locales — falls Mehrsprachigkeit benötigt
- Test-Suite (`tests/`) — Patterns für strukturiertes Testing
- Releases-Pipeline (`releases/`) — Build- und Distribution-Pattern

**Was NICHT übernommen wird:**
- Lizenz (CASHCOW-Lizenz, nicht passend für SOCIAL-Projekt)
- Medikamenten-/Patientendatenverwaltung (zu spezifisch)
- UI (PySide6-Desktop-App, wir wollen PWA)

### REF_Diagnostic_Paper (Geiger 2026, DOI 10.5281/zenodo.18736725)

**Pfad:** `_codebases/REF_Diagnostic_Paper/` — ausführliche Einordnung in [`docs/RESOURCES_DIAGNOSTIC_PAPER.md`](docs/RESOURCES_DIAGNOSTIC_PAPER.md).

**Was da brauchbar ist:**
- `build_code_database.py` (801 Zeilen) — Schema-Vorlage für die ICD-10-GM-Datenbank (bilinguale Titel, Cross-System-Mapping mit Qualitätsbewertung)
- `translations.json` (584 Keys DE/EN) — i18n-Infrastruktur direkt portabel
- `testcenter/app.py` — Flask-Backend mit `before_request` Auto-DB-Init, Session-Management, Token-URLs, REST-API, Critical-Item-Alerts. Direkte Vorlage für PWA-Erweiterung
- `paper/*.tex` — Struktur-Vorbild für ST-001 (Sections 7 Coverage-Analysis, 9 HSM, 12 DSGVO/Liability/Bias, 13 Validation, 14 Interoperabilität)
- **Hierarchical State Machine als Decision-Engine** (Section 9) — Pattern für strukturierte Begründungspflicht

**Was NICHT übernommen wird:**
- Psychiatrie-spezifische 6-Achsen-Logik (`multiaxial_diagnostic_system.py`)
- ICD-11/DSM-5/ICF-Datenbank (`diagnostic_codes.db`) — wir nutzen ICD-10-GM
- Test-Instrument-JSONs (PHQ-9, GAD-7, ...) — domänenfremd

### REF_Foerderplaner_Autismo_pro

**Pfad:** `_codebases/REF_Foerderplaner_Autismo_pro/`

**Was da brauchbar ist:**
- Klienten-Datenverwaltung (`klienten_data/`) — Pattern für DSGVO-konforme lokale Datenhaltung
- ICF-Strukturen (`icf_struktur_treeview.json`) — Pattern für hierarchische Datenstrukturen (analog zu ICD-10-GM-Hierarchie)
- Backups (`backups/`) — Backup-Pattern
- Multi-User (`users.json`) — Falls später Mehrbenutzer-Modus
- Locks (`locks/`) — Concurrency-Pattern
- Build-System (`build_installer.bat`, `foerderplaner.spec`) — PyInstaller-Pattern wenn lokale App nötig
- Research-Subordner (`research/`) — Pattern für eingebettete Quellen

**Was NICHT übernommen wird:**
- Inhaltlicher Fokus (Autismus-Förderplanung)
- ICF-Spezifika (wir nutzen ICD-10-GM)
- Desktop-UI (siehe oben)

---

## Nächste Schritte (historisch — siehe Revisionshinweis oben)

> Die folgende Liste stand im ursprünglichen Konzept. Stand 2026-04-12 sind Punkte 1, 2 und 5 **gestrichen** (keine Partner-/Förderaktivitäten durch den Urheber); Punkte 3, 4, 6, 7 sind **umgesetzt**.

1. ~~Konzept finalisieren mit Therapiefreiheit e.V.~~ (gestrichen 2026-04-12: kein Partnerkontakt geplant)
2. ~~Förderantrag Prototype Fund vorbereiten~~ (gestrichen 2026-04-12)
3. **Datenmodell skizzieren** — erledigt (SQLite-Schema + AM-RL-Seeds III/V/VI)
4. **Prototype aus Codebases zusammenstellen** — erledigt (CLI-MVP + PySide6-Tray-GUI, 108/108 Tests)
5. ~~Pilot-Praxen identifizieren~~ (gestrichen 2026-04-12)
6. **Rechtsgutachten einholen** — erledigt (MDSW, DSGVO, RUO, Publikation/Lizenz, Haftung; alle in `docs/legal/`)
7. **DSGVO-Konzept** — erledigt (`docs/legal/DSGVO_KONZEPT.md`)

**Offene Punkte (2026-04-12+):**
- AM-RL-Seeds durch externe medizinische Prüfung validieren — **nicht durch den Urheber**, sondern durch Dritte die das Projekt aufgreifen
- DPMA-Markenrecherche "VerordnungsAmpel" — bei Bedarf
- Implementierung der DSGVO-CLI-Empfehlungen E1-E8 (`export`, `purge`) — offen

---

## Status-Tracking

| Meilenstein | Status | Datum |
|---|---|---|
| Konzept skizziert | ✅ erledigt | 2026-04-08 |
| Codebases als Referenz übernommen | ✅ erledigt | 2026-04-08 |
| Code-Audit der Referenz-Codebases | ✅ erledigt | 2026-04-08 |
| Projektgerüst (pyproject, LICENSE GPL-3.0, start.bat) | ✅ erledigt | 2026-04-08 |
| SQLite-Datenmodell + Seed-Daten | ✅ erledigt | 2026-04-08 |
| Ampel-Engine (GRÜN/GELB/ROT) | ✅ erledigt | 2026-04-08 |
| Compliance-Log mit Hash-Chain | ✅ erledigt | 2026-04-08 |
| CLI-Frontend (init/check/log/verify/justify/workflow/remind) | ✅ erledigt | 2026-04-08 |
| **Funktion 2: Strukturierte Begründungspflicht (HSM)** | ✅ erledigt | 2026-04-08 |
| **Funktion 3: Vorab-Klärungs-Workflow (Container-sensitiv)** | ✅ erledigt | 2026-04-08 |
| **Funktion 4: Praxisbesonderheiten-Erkennung + Quartalsreminder** | ✅ erledigt | 2026-04-08 |
| **Alle 5 KONZEPT-Funktionen implementiert** | ✅ erledigt | 2026-04-08 |
| Seed-Daten um `stellungnahme`-Pfad erweitert (GLP-1/Soziotherapie) | ✅ erledigt | 2026-04-08 |
| Seed-Loader idempotent (DELETE vor Insert für PB/AMRL) | ✅ erledigt | 2026-04-08 |
| Test-Suite (86/86 passed) | ✅ erledigt | 2026-04-08 |
| **MVP-Kern lauffähig** | ✅ erledigt | 2026-04-08 |
| Diagnostic-Paper als Ressource dokumentiert | ✅ erledigt | 2026-04-08 |
| Förderantrag Prototype Fund | ⬜ offen | — |
| Rechtsgutachten (Informationswerk, nicht MDSW) | ⬜ offen | — |
| ~~Therapiefreiheit-Erstkontakt~~ | 🚫 gestrichen | 2026-04-12 (keine Partnerschaft geplant) |
| Pilot-Praxen identifiziert | ⬜ offen | — |
| Flask-Backend + PWA-Frontend (vollständiger MVP) | ⬜ offen | — |
| Pilot-Phase | ⬜ offen | — |
| Public Release | ⬜ offen | — |
