# VerordnungsAmpel — Benutzerhandbuch

> **Für niedergelassene Vertragsärzte, Praxisteams und technisch interessierte Anwender.**
>
> Stand: 2026-04-12 · Version 0.1.0 (Pre-Alpha) · Lizenz: GPL-3.0-or-later
> Repository: https://github.com/um-bruch/verordnungsampel

---

## Inhalt

1. [Überblick](#1-überblick)
2. [Installation](#2-installation)
3. [Erste Schritte — 5-Minuten-Tutorial](#3-erste-schritte--5-minuten-tutorial)
4. [Die fünf Funktionen im Detail](#4-die-fünf-funktionen-im-detail)
5. [GUI-Nutzung (Tray-Modus)](#5-gui-nutzung-tray-modus)
6. [Typische Workflows in der Praxis](#6-typische-workflows-in-der-praxis)
7. [Regelwerke und ihr Stand](#7-regelwerke-und-ihr-stand)
8. [Datenschutz und DSGVO](#8-datenschutz-und-dsgvo)
9. [Rechtlicher Rahmen](#9-rechtlicher-rahmen)
10. [Updates und Pflege](#10-updates-und-pflege)
11. [Häufige Fragen (FAQ)](#11-häufige-fragen-faq)
12. [Support und Mitwirken](#12-support-und-mitwirken)
13. [Glossar](#13-glossar)
14. [Anhänge](#14-anhänge)

---

## 1. Überblick

Die **VerordnungsAmpel** ist ein Open-Source-**Informationswerk**, das niedergelassene Vertragsärztinnen und Vertragsärzte im Moment der Verordnung gegen öffentliche Regelwerke abgleicht: **AM-RL Anlagen III / V / VI**, **PRISCUS 2.0** und eine Liste bundesweiter **Praxisbesonderheiten**. Sie schlägt nach, ob eine Kombination aus **ICD-10-GM-Code** und **ATC-Code** regressanfällig ist, und dokumentiert die Entscheidung in einem manipulationssicheren Compliance-Log.

### Was sie IST

- **Nachschlagewerk** für öffentliche Verordnungsregelwerke (AM-RL, PRISCUS, BMV-Ä, BSG-Rechtsprechung)
- **Dokumentationshilfe**, die eine strukturierte Begründung im Moment der Verordnung festhält
- **Compliance-Log** mit kryptografischer Hash-Chain für Beweiszwecke vor dem Sozialgericht
- **Companion-Tool**, das neben dem Praxisverwaltungssystem (PVS) läuft

### Was sie NICHT ist

- **Kein Medizinprodukt** im Sinne der MDR (keine CE-Kennzeichnung, keine Benannte Stelle)
- **Kein Praxisverwaltungssystem** (PVS-Ersatz) und kein DiGA
- **Keine medizinische Entscheidungshilfe**, keine Therapieempfehlung, keine Diagnosestellung
- **Kein Patientendatensystem** — es speichert keine Klarnamen, keine Befunde, keine Krankheitsverläufe
- **Keine Rechtsberatung** und kein Ersatz für anwaltlichen Rat im Regressfall

> **Haftungshinweis** (verbindlich)
>
> Die VerordnungsAmpel ist ein Informations- und Nachschlagewerk. Sie ist **nicht klinisch validiert**. Die ärztliche Verantwortung für jede Verordnung bleibt **vollumfänglich** bei der behandelnden Ärztin bzw. dem behandelnden Arzt. Das Tool ersetzt weder die eigenständige Prüfung der Indikation noch die Fachinformation. Nutzung erfolgt auf eigenes Risiko.

---

## 2. Installation

### 2.1 Voraussetzungen

| Komponente | Anforderung |
|---|---|
| Betriebssystem | Windows 10/11, macOS 12+, Linux (alle gängigen Distributionen) |
| Python | 3.10 oder neuer |
| Plattenplatz | ca. 50 MB (inkl. Datenbank und Seed-Daten) |
| Netzwerk | nur für Installation und Updates nötig — das Tool arbeitet offline |

Die Kernbibliothek kommt **ohne externe Python-Abhängigkeiten** aus (nur Standardbibliothek). Für die grafische Oberfläche (optional) wird **PySide6** verwendet.

### 2.2 Installation aus dem Quellcode

```bash
git clone https://github.com/um-bruch/verordnungsampel.git
cd verordnungsampel
pip install -r requirements.txt
pip install -e .
```

### 2.3 GUI zusätzlich installieren (optional)

```bash
pip install -e ".[gui]"
```

### 2.4 Erst-Initialisierung

Nach der Installation muss die lokale Datenbank angelegt und mit den Seed-Daten befüllt werden:

```bash
python -m verordnungsampel.cli.main init
```

Die Regelwerk-Datenbank wird angelegt unter:

- Windows: `%APPDATA%\VerordnungsAmpel\regelwerk.db`
- macOS: `~/Library/Application Support/VerordnungsAmpel/regelwerk.db`
- Linux: `~/.local/share/VerordnungsAmpel/regelwerk.db`

Der Compliance-Log liegt in **derselben Verzeichnisebene** in einer separaten Datei `compliance_log.db`.

### 2.5 Unter Windows: `start.bat`

Unter Windows genügt ein Doppelklick auf `start.bat` im Projektverzeichnis. Es öffnet ein interaktives Demo-Menü mit 15 Optionen, das die wichtigsten Funktionen ohne CLI-Kenntnisse zugänglich macht.

---

## 3. Erste Schritte — 5-Minuten-Tutorial

Ziel dieses Abschnitts: In fünf Minuten einmal GRÜN, GELB, ROT gesehen haben, eine Begründung erfasst und den Hash-Chain-Check ausgeführt zu haben.

### Schritt 1: `start.bat` ausführen

Doppelklick auf `start.bat` öffnet das Demo-Menü. Wer lieber die Kommandozeile nutzt, kann die Befehle in der rechten Spalte der Menüzeilen direkt ausführen.

### Schritt 2: GRÜN-Fall (Option 2)

**Fall:** ACE-Hemmer (Ramipril, ATC `C09AA02`) bei essentieller Hypertonie (ICD `I10`).

```bash
python -m verordnungsampel.cli.main check --icd I10 --atc C09AA02
```

Erwartete Ausgabe (gekürzt):

```
================================================================
VerordnungsAmpel  ICD=I10  ATC=C09AA02
----------------------------------------------------------------
Gesamtbewertung: [GRUEN]

Begruendungen:
  1. (GRUEN) [DEFAULT_GRUEN]
     Keine Regel der eingebetteten Regelwerke trifft auf diese
     Kombination zu. Das ersetzt NICHT die ärztliche Prüfung
     im Einzelfall.
================================================================
Hinweis: Dies ist ein Informationswerk. Es ersetzt NICHT die
ärztliche Prüfung im Einzelfall.
```

### Schritt 3: ROT-Fall (Option 4)

**Fall:** Diazepam (Benzodiazepin, ATC `N05BA01`) bei Angststörung (ICD `F41`), Patient 72 Jahre → PRISCUS 2.0 einschlägig.

```bash
python -m verordnungsampel.cli.main check --icd F41 --atc N05BA01 --alter 72
```

Die Ampel schlägt auf ROT, weil PRISCUS 2.0 Benzodiazepine bei Patienten ab 65 als potenziell inadäquat einstuft. Die Ausgabe enthält Quellenverweis und Container-Hinweis.

### Schritt 4: Compliance-Log ansehen (Option 11)

```bash
python -m verordnungsampel.cli.main log --tail 20
```

Ausgabe (Beispiel):

```
#00001 2026-04-12T09:14:03+00:00  ICD=I10      ATC=C09AA02  -> GRUEN  hash=a1b2c3d4e5f6...
#00002 2026-04-12T09:14:48+00:00  ICD=F41      ATC=N05BA01  -> ROT    hash=f6e5d4c3b2a1...
```

### Schritt 5: Hash-Chain prüfen (Option 12)

```bash
python -m verordnungsampel.cli.main verify
```

Erwartet: `Hash-Chain intakt. 2 Eintrag/Einträge geprüft.`

Damit ist das Setup getestet. Alle weiteren Kapitel gehen ins Detail.

### Was die Ampel bedeutet

| Farbe | Bedeutung | Typische Auslöser |
|---|---|---|
| **GRÜN** | Keine Regel der eingebetteten Regelwerke trifft zu. | Standardverordnung mit passender Indikation. |
| **GELB** | Eine Regel signalisiert eingeschränkte Erstattungsfähigkeit, einen Graubereich oder eine Dokumentationspflicht. | AM-RL-Einschränkung, dokumentationspflichtiger Off-Label-Pfad. |
| **ROT** | Eine Regel signalisiert hohes Regressrisiko, Verordnungsausschluss oder potenziell inadäquate Medikation. | Anlage III Ausschluss, PRISCUS-Treffer bei älteren Patienten, verbotene Vorabgenehmigung. |

**Container-Marker** sind zusätzliche Hinweise für den Vorab-Klärungs-Workflow:

- `pflicht_vorab` — Leistung benötigt vorab die Genehmigung der Krankenkasse (z.B. Cannabis).
- `verboten_vorab` — Vorabgenehmigung ist nicht zulässig (§ 29 BMV-Ä); stattdessen defensiv dokumentieren.
- `stellungnahme` — Graubereich, in dem eine Bitte um Stellungnahme an die Krankenkasse zulässig ist (BSG B 6 KA 27/12 R).
- `off_label` — Off-Label-Einsatz, für den die BSG-Kriterien geprüft werden müssen.

---

## 4. Die fünf Funktionen im Detail

### 4.1 Ampel-Check (Plausibilitätsprüfung)

**Wozu?** Nachschlagen, ob eine geplante Verordnung mit öffentlichen Regelwerken in Konflikt steht.

**Eingabe:** ICD-10-GM-Code, ATC-Code, optional Alter.

**Ausgabe:** Ampelfarbe GRÜN / GELB / ROT, alle zutreffenden Regelwerks-Treffer mit Begründung und Quellenverweis, optional Container-Hinweise und Praxisbesonderheiten-Treffer.

**CLI:**

```bash
python -m verordnungsampel.cli.main check --icd <ICD> --atc <ATC> [--alter <Jahre>] [--json] [--no-log] [--nutzer <Praxis-Account>]
```

**GUI-Tab:** *Check*

**Beispiele:**

```bash
# GRUEN — ACE-Hemmer bei Hypertonie
python -m verordnungsampel.cli.main check --icd I10 --atc C09AA02

# GELB — PPI ohne Refluxdiagnose
python -m verordnungsampel.cli.main check --icd M54.5 --atc A02BC02

# ROT — Benzodiazepin 72 J.
python -m verordnungsampel.cli.main check --icd F41 --atc N05BA01 --alter 72

# JSON-Ausgabe für Weiterverarbeitung
python -m verordnungsampel.cli.main check --icd I10 --atc C09AA02 --json
```

**Was im Compliance-Log gespeichert wird:** ICD, ATC, Alter, Ampelfarbe, zusammengefasste Begründung, Container-Hinweise, optionaler Nutzer-Bezeichner, Zeitstempel (UTC, ISO-8601), vorheriger Hash, aktueller Hash, bei Bedarf ein `extra`-Block mit Versionsnummer und Praxisbesonderheiten-Treffern.

### 4.2 Strukturierte Begründung (HSM)

**Wozu?** Wenn die Ampel GELB oder ROT anzeigt, ist im Regressverfahren eine strukturierte Begründung **im Moment der Verordnung** erforderlich — nachgereichte Dokumentation wird nach **BSG B 6 KA 26/13 R** nicht anerkannt.

**Ablauf** (als Hierarchical State Machine in `engine/justification_fsm.py`):

| Zustand | Pflicht bei | Mindest­länge |
|---|---|---|
| `diagnose` | GELB und ROT | 10 Zeichen |
| `vorbehandlung` | GELB und ROT | 10 Zeichen |
| `therapieversagen` | nur ROT | 15 Zeichen |
| `bsg_off_label` | ROT mit Container `off_label` — drei kumulative Kriterien | je 10 Zeichen |
| `praxisbesonderheit` | optional (ROT) | beliebig |
| `confirm` | immer zum Abschluss | Boolean `true` |

Die **drei BSG-Off-Label-Kriterien** (BVerfG 06.12.2005, 1 BvR 347/98 und Folgerechtsprechung):

1. **schwerwiegende_erkrankung** — Schwerwiegende Erkrankung ist belegt.
2. **keine_alternative** — Keine andere zugelassene Therapie verfügbar.
3. **begruendete_erfolgsaussicht** — Begründete Aussicht auf Erfolg besteht.

Alle drei müssen kumulativ dokumentiert sein.

**CLI — interaktiv:**

```bash
python -m verordnungsampel.cli.main justify --icd F41 --atc N05BA01 --alter 72
```

Das Tool stellt nacheinander die erforderlichen Fragen und liest die Antworten von der Tastatur.

**CLI — non-interaktiv (mit Antwort-JSON):**

```bash
python -m verordnungsampel.cli.main justify --icd F41 --atc N05BA01 --alter 72 --answers antworten.json
```

Format der `antworten.json` (siehe [Anhang B](#b-beispiel-antwortenjson-für-justify)):

```json
{
  "diagnose": "F41.1 generalisierte Angststoerung, mittelgradig.",
  "vorbehandlung": "SSRI (Sertralin 50 mg, 8 Wochen).",
  "therapieversagen": "Unvertraeglichkeit (Uebelkeit, Agitation), kein Ansprechen.",
  "praxisbesonderheit": "",
  "confirm": true
}
```

**GUI-Tab:** *Begruenden* — nur aktiv, wenn der Check-Tab zuvor ein GELB/ROT-Ergebnis geliefert hat.

**Was im Compliance-Log gespeichert wird:** Die vollständige Justification als `extra.justification`, inklusive Liste der erforderlichen Zustände, aller Antworten, Bestätigungs-Flag und Off-Label-Flag. Damit ist die Begründung Teil der Hash-Chain.

### 4.3 Vorab-Klärungs-Workflow (Container-sensitiv)

**Wozu?** Das deutsche GKV-Recht kennt drei disjunkte Vorab-Situationen. Der Workflow generiert den passenden Text.

| Container | Workflow-Typ | Rechtsgrundlage | Was wird erzeugt? |
|---|---|---|---|
| `pflicht_vorab` | `PFLICHT_ANTRAG` | § 31 Abs. 6 SGB V (Cannabis), § 37 SGB V (häusliche Krankenpflege), § 37a SGB V (Soziotherapie), § 40 SGB V (Reha) | Antragsschreiben an die Krankenkasse, Genehmigung abwarten |
| `verboten_vorab` | `VERBOTEN_HINWEIS` | § 29 BMV-Ä | Interner Doku-Hinweis: KEIN Antrag an die Kasse, stattdessen defensive Dokumentation |
| `stellungnahme` | `STELLUNGNAHME` | BSG B 6 KA 27/12 R | Bitte um Stellungnahme an die Krankenkasse, kein Antrag auf Vorabgenehmigung |
| (keiner) | `KEINE_AKTION` | — | Hinweis, dass kein Vorab-Schritt nötig ist |

**CLI:**

```bash
python -m verordnungsampel.cli.main workflow \
  --icd <ICD> --atc <ATC> [--alter <Jahre>] \
  --kk "<Krankenkasse>" \
  --praxis "<Praxisname>" --praxis-adresse "<Adresse>" \
  --arzt "<Arztname>" --bsnr <BSNR> --lanr <LANR> \
  --patient <Praxis-internes-Kürzel> \
  [--out <Pfad-zur-Textdatei>] [--json] [--no-log]
```

**GUI-Tab:** *Workflow* — nur aktiv, wenn der Check-Tab einen Container-Hinweis erkannt hat.

**Was im Compliance-Log gespeichert wird:** Workflow-Typ, Betreff, Empfänger und Rechtsgrundlage als `extra.workflow`. Damit ist nachweisbar, welcher Antragsweg gewählt wurde.

### 4.4 Praxisbesonderheiten und Quartalsreminder

**Wozu?** Nach **LSG Baden-Württemberg 15.11.2023** und **SG Marburg 31.01.2024** muss eine Praxisbesonderheit bereits im Verwaltungsverfahren substanziiert vorgetragen werden — wer sie erst im Klageverfahren nachreicht, verliert.

**Automatische Erkennung:** Bei jedem `check` und `justify` gleicht das Tool ICD und ATC gegen die Praxisbesonderheiten-Liste in der Datenbank ab. Treffer werden auf dem Bildschirm ausgegeben und als `extra.praxisbesonderheiten` im Compliance-Log versiegelt.

**Quartalsreminder:** Am Quartalsende kann die MFA oder die Ärztin alle Einträge des Quartals mit Praxisbesonderheits-Treffer listen lassen und prüfen, ob die entsprechende KV-Kennziffer auf dem Behandlungsschein markiert wurde.

**CLI:**

```bash
python -m verordnungsampel.cli.main remind --quartal 2026-Q2
```

Quartalsformat: `YYYY-Qn` (z.B. `2026-Q2` = 1. April bis 30. Juni 2026).

**GUI-Tab:** *Reminder*

### 4.5 Compliance-Log mit Hash-Chain

**Wozu?** Jede Verordnungsprüfung wird als Eintrag in einen Append-only-Log geschrieben. Jeder Eintrag enthält den SHA-256-Hash des vorherigen Eintrags (`prev_hash`) und seinen eigenen Hash über eine deterministisch serialisierte JSON-Darstellung. Eine nachträgliche Änderung irgendeines Eintrags bricht die Kette und kann jederzeit über `verify` nachgewiesen werden.

**Rechtsgrundlage:** § 371a ZPO (Beweiskraft elektronischer Dokumente). Das Tool bietet **keine qualifizierte elektronische Signatur**, aber es dokumentiert **Unverfälschbarkeit**: Eine Manipulation des Logs ist feststellbar. Damit entsteht eine Indizienkette, die im Sozialgerichtsverfahren gewürdigt werden kann.

**Was versiegelt wird:**

- Sequenznummer, Zeitstempel (UTC, ISO-8601)
- ICD, ATC, Alter
- Ampelfarbe, zusammengefasste Begründung, Container-Hinweis
- Optionaler Nutzerbezeichner
- `extra`-Block (z.B. Justification, Workflow-Metadaten, Praxisbesonderheiten)
- `prev_hash`, `hash`

**CLI:**

```bash
# Log anzeigen (letzte 20 Einträge, kompakt)
python -m verordnungsampel.cli.main log --tail 20

# Komplett als JSON für Export
python -m verordnungsampel.cli.main log --json > compliance_log.json

# Kette pruefen
python -m verordnungsampel.cli.main verify
```

**GUI-Tab:** *Compliance-Log*

**Exit-Code von `verify`:** `0` = Kette intakt, `2` = Kette gebrochen. Damit kann der Befehl in Wartungs-Skripten verwendet werden.

---

## 5. GUI-Nutzung (Tray-Modus)

Die grafische Oberfläche ist als **Companion-Fenster** gebaut: klein, andockbar, optional immer im Vordergrund, optional halbtransparent.

### 5.1 Starten

```bash
python -m verordnungsampel.cli.main gui
```

Ist PySide6 nicht installiert, gibt das Tool einen Hinweis mit Installationsbefehl aus.

### 5.2 Fensterverhalten

- **Klick auf „X"** → Fenster minimiert ins System-Tray. Das Programm läuft weiter.
- **Rechtsklick auf das Tray-Icon → Beenden** → Anwendung wird wirklich geschlossen.
- **Ansicht → Always-on-top** — hält das Fenster über allen anderen (für Nebenansicht neben dem PVS).
- **Ansicht → Minimal-Modus** — blendet alle Tabs außer *Check* aus und verkleinert das Fenster.
- **Ansicht → Transparenz** — setzt die Fenster-Opazität auf 92 %.

### 5.3 Die fünf Tabs

| Tab | Inhalt |
|---|---|
| **Check** | Eingabefelder für ICD, ATC, Alter. Button „Prüfen" führt die Ampel-Engine aus. Zeigt Farbe, Treffer, Container-Hinweise, Praxisbesonderheiten an. |
| **Begründen** | Nur aktiv, wenn der letzte Check GELB oder ROT war. Führt durch die HSM-Schritte. |
| **Workflow** | Nur aktiv, wenn der letzte Check einen Container-Hinweis hatte. Erzeugt den passenden Antrags-/Hinweistext. |
| **Compliance-Log** | Listet die letzten Einträge, ermöglicht Hash-Chain-Prüfung per Knopfdruck. |
| **Reminder** | Quartalsauswahl, Reminder-Report mit Praxisbesonderheits-Treffern. |

### 5.4 Screenshots

*(Screenshots werden in einem späteren Release ergänzt.)*

![Check-Tab](README/screenshots/check_tab.png)
![Begruenden-Tab](README/screenshots/justify_tab.png)
![Workflow-Tab](README/screenshots/workflow_tab.png)
![Compliance-Log-Tab](README/screenshots/log_tab.png)
![Reminder-Tab](README/screenshots/reminder_tab.png)

---

## 6. Typische Workflows in der Praxis

### Workflow A — Hausärztin, KHK, Statin (GRÜN)

1. In der Sprechstunde entsteht der Entschluss, Simvastatin (ATC `C10AA01`) bei KHK (ICD `I25.1`) zu verordnen.
2. Im Companion-Fenster oder per CLI: `check --icd I25.1 --atc C10AA01`.
3. Ampel zeigt GRÜN, keine Container-Hinweise, keine Praxisbesonderheit einschlägig.
4. Verordnung regulär im PVS ausstellen. Der Log-Eintrag ist automatisch versiegelt.

### Workflow B — Angststörung, Benzodiazepin, 72 Jahre (PRISCUS ROT)

1. Prüfung: `check --icd F41 --atc N05BA01 --alter 72` → ROT wegen PRISCUS 2.0.
2. Entscheidung: entweder **Alternative wählen** (SSRI, Pregabalin, Psychotherapie-Fokus) oder **Begründung erfassen**.
3. Bei Entscheidung für die Benzodiazepin-Verordnung: `justify --icd F41 --atc N05BA01 --alter 72` (interaktiv) oder mit `--answers`-JSON.
4. Die Begründung umfasst Diagnose, Vorbehandlung, Therapieversagen, optional Praxisbesonderheit.
5. Nach Bestätigung wird die Begründung als Teil der Hash-Chain versiegelt. Im Regressverfahren kann die Begründung bewiesen werden.

### Workflow C — Cannabis bei chronischen Schmerzen (PFLICHT_ANTRAG)

1. Prüfung: `check --icd R52.1 --atc QV12` → Container `pflicht_vorab` wird erkannt.
2. Antragstext erzeugen:

```bash
python -m verordnungsampel.cli.main workflow \
  --icd R52.1 --atc QV12 \
  --kk "Musterkasse" --praxis "Musterpraxis" \
  --arzt "Dr. med. Musterarzt" --bsnr 12345678 --lanr 123456789 \
  --patient P-4711 --out antrag_cannabis.txt
```

3. Die erzeugte Datei enthält den fertigen Antrag nach § 31 Abs. 6 SGB V. Vor dem Absenden:
   - Praxis- und Patientenfelder prüfen (vom Tool mit Platzhaltern befüllt, wenn nicht gesetzt).
   - Medizinische Begründung ergänzen oder per `justify` vorab erfassen und einbetten.
4. Antrag an die Krankenkasse senden, **Genehmigung oder Fristablauf abwarten**, erst dann verordnen.

### Workflow D — GLP-1-Agonist bei Adipositas (STELLUNGNAHME)

1. Prüfung: `check --icd E66.01 --atc A10BJ06` → Container `stellungnahme` (AM-RL Anlage III Nr. 32: GLP-1-Analoga nur bei Diabetes erstattungsfähig).
2. Stellungnahmetext erzeugen:

```bash
python -m verordnungsampel.cli.main workflow \
  --icd E66.01 --atc A10BJ06 \
  --kk "TK" --praxis "Hausarztpraxis" \
  --arzt "Dr. Schmidt" --patient P-0815 \
  --out stellungnahme_glp1.txt
```

3. Das Tool erzeugt eine **Bitte um Stellungnahme** nach **BSG B 6 KA 27/12 R** (nicht als Antrag auf Vorabgenehmigung, sondern als Bitte, die Rechtsauffassung der Kasse transparent zu machen).
4. Antwort der Kasse dokumentieren und in die Verordnungsentscheidung einbeziehen.

### Workflow E — Quartalsabschluss (MFA)

1. Am Quartalsende: `remind --quartal 2026-Q2`.
2. Der Reminder listet alle Einträge des Quartals mit Praxisbesonderheits-Treffer auf.
3. Für jeden Eintrag prüfen: Ist die KV-Kennziffer auf dem Behandlungsschein markiert?
4. Nicht markierte Kennziffern nachtragen, bevor die Quartalsabrechnung abgeschickt wird.

---

## 7. Regelwerke und ihr Stand

Alle Regelwerke sind als JSON-Dateien im Verzeichnis `data/seed/` eingebettet und werden beim `init` in die lokale SQLite-Datenbank geladen.

| Regelwerk | Kürzel | Stand (Stand-Datum im Seed) |
|---|---|---|
| AM-RL Anlage III — Verordnungseinschränkungen/-ausschlüsse | `AMRL_III` | 2025-10-09 |
| AM-RL Anlage V — verordnungsfähige Medizinprodukte | `AMRL_V` | 2026-03-24 |
| AM-RL Anlage VI — Off-Label (Teile A und B) | `AMRL_VI` | 2025-05-07 |
| PRISCUS 2.0 — potenziell inadäquate Medikation | `PRISCUS_2` | 2023 |
| GKV-SV bundesweite Praxisbesonderheiten (AMNOG) | `GKV_SV_PB` | 2025 |
| § 31 Abs. 6 SGB V (Cannabis-Genehmigung) | `SGB_V_31_6` | 2024 |
| § 29 BMV-Ä (Verbot Einzelfall-Vorabgenehmigung) | `BMV_AE_29` | 2024 |
| BSG B 6 KA 26/13 R (nachgereichte Doku) | `BSG_B6KA26_13` | 2014 |
| BSG B 6 KA 27/12 R (Stellungnahme-Bitte) | `BSG_B6KA27_12` | 2013 |
| AM-RL Anlage III Nr. 32 (GLP-1-Analoga) | `AMRL_III_GLP1` | 2025 |

> **Hinweis:** Das Stand-Datum pro Quelle wird in jeder Ausgabe mitgeführt und ist Teil des Compliance-Logs. Wer sich auf einen Eintrag beruft, sieht, von welcher Regelwerksversion er stammt.

Eine tiefere Versionierungs-Methodik (automatisiertes Versions-Tracking des Regelwerks über GitHub Actions) ist in Vorbereitung — siehe `data/seed/UPDATE_METHODE.md` *(in Erstellung)*.

### Einträge inspizieren

Der MVP bietet bislang keinen dedizierten `rules`- oder `sources`-Subcommand. Wer sich den aktuellen Regelwerksbestand ansehen möchte, kann entweder:

- das JSON im Seed-Verzeichnis `data/seed/` lesen, oder
- die SQLite-Datenbank mit `python -c "import sqlite3; ..."` öffnen und die Tabellen `regel`, `amrl_anlage`, `praxisbesonderheit`, `quelle` abfragen.

Ein komfortabler `rules`-Subcommand ist für eine spätere Version geplant.

---

## 8. Datenschutz und DSGVO

### 8.1 Was verarbeitet das Tool?

- **ICD-10-GM-Code** (Diagnose-Schlüssel, kein Klartext der Diagnose)
- **ATC-Code** (Wirkstoff-Schlüssel, keine PZN, kein Handelsname)
- **Alter in Jahren** (optional)
- **Praxis-internes Pseudonym** (optional, z.B. `P-4711`) — frei wählbar durch den Arzt, **kein Klarname**

### 8.2 Was verarbeitet das Tool NICHT?

- Keine Namen, Geburtsdaten, Adressen, Kontaktdaten von Patienten
- Keine Diagnosen im Klartext, keine Befunde, keine Laborwerte
- Keine PZN, keine Preise, keine Rabattverträge
- Keine Abrechnungsdaten

### 8.3 Wo werden Daten gespeichert?

Ausschließlich lokal auf dem Praxisrechner. **Keine Cloud, keine Telemetrie, kein Netzwerkzugriff** im Regelbetrieb.

- Regelwerk: `%APPDATA%\VerordnungsAmpel\regelwerk.db` (SQLite, read-only nach Init)
- Compliance-Log: `%APPDATA%\VerordnungsAmpel\compliance_log.db` (SQLite, append-only)

### 8.4 Betroffenenrechte

Da das Tool Pseudonyme (wie `P-4711`) verarbeitet, gelten die Betroffenenrechte aus Art. 12 – 22 DSGVO **vollumfänglich**. Die Verantwortung für die Auflösung des Pseudonyms liegt beim Arzt (die Zuordnungstabelle führt er außerhalb des Tools).

| Betroffenenrecht | Umsetzung |
|---|---|
| Auskunft (Art. 15) | CLI `export --patient <Pseudonym>` *(in Erstellung — als Empfehlung E1 im DSGVO-Konzept aufgeführt)* |
| Berichtigung (Art. 16) | Die Hash-Chain verhindert das In-Place-Ändern. Als Workaround wird ein neuer Log-Eintrag mit Korrekturverweis angehängt. |
| Löschung (Art. 17) | CLI `purge --all` und `purge --older-than <Datum>` *(in Erstellung — Empfehlungen E2/E3)* |
| Einschränkung (Art. 18) | `mark --restricted <seq>` *(in Erstellung — Empfehlung E4)* |
| Datenübertragbarkeit (Art. 20) | `export --patient <Pseudonym> --format json` *(in Erstellung — Empfehlung E5)* |
| Widerspruch (Art. 21) | analog Löschung |

**Hinweis zum Implementierungsstand:** Die Betroffenenrechte-CLI (Empfehlungen E1 bis E8 aus `docs/legal/DSGVO_KONZEPT.md`) ist im MVP **noch nicht umgesetzt**. Wer heute vollständig löschen will, kann die Datei `compliance_log.db` schließen und manuell löschen; damit ist der gesamte Log weg. Wer Einzel-Einträge exportieren will, kann mit `log --json` den vollen Log als JSON abrufen und manuell filtern.

Details: `docs/legal/DSGVO_KONZEPT.md`.

---

## 9. Rechtlicher Rahmen

### 9.1 Status als Informationswerk

Die VerordnungsAmpel ist rechtlich als **Informationswerk / Nachschlagewerk** konzipiert — vergleichbar mit einem gedruckten Praxishandbuch, der AM-RL-PDF-Datei oder einer statischen Web-Suche über Paragraphen. Sie ist **kein Medizinprodukt** im Sinne der MDR und **keine Medical Device Software** (MDSW).

Begründung der Einstufung (Kurzform):

- Es werden **keine patientenspezifischen Daten** verarbeitet (keine individuellen Messwerte, keine Befundhistorie).
- Jede Abfrage ist **stateless**: ICD + ATC [+ Alter], ohne Kontext des konkreten Patienten.
- Die Ausgabe ist **regelwerksbezogen**, nicht patientenbezogen.
- Keine Therapieempfehlung, keine Diagnose, keine Verlaufsprognose.
- Kein sozialrechtlicher Zweck, sondern Compliance-Hilfe nach § 106 SGB V.

Ausführliche Begründung: `docs/legal/RECHTSGUTACHTEN_MDSW.md`.

Abgrenzungs-Hinweis: Das erste KI-basierte Rechtsgutachten (MDSW) liegt vor. Ein zweites Gutachten zur produktsicherheits-/gewährleistungs-rechtlichen Haftung (**Haftungsgutachten**) ist *in Erstellung*. Ein **Research-Use-Only-Gutachten** (`RECHTSGUTACHTEN_RUO.md`) und ein **Publikations-/Lizenzgutachten** (`RECHTSGUTACHTEN_PUBLIKATION_LIZENZ.md`) liegen ebenfalls vor.

### 9.2 Haftung

- Die **ärztliche Verantwortung** für jede Verordnung bleibt unverändert. Das Tool ist ein Hilfsmittel, kein Entscheider.
- Eine fehlerhafte Regelwerks-Information (z.B. veraltete PRISCUS-Zuordnung) kann eine allgemeine Produkt- bzw. Deliktshaftung auslösen. Gegenmaßnahmen: sorgfältige redaktionelle Pflege, Versionierung, Quellenangaben, Disclaimer.
- GPL-3.0-Lizenz enthält den üblichen Haftungsausschluss in den Sections 15 und 16 (keine Garantie, kein Schadensersatz).

### 9.3 Was tun, wenn ein Regress trotz Tool-Nutzung kommt?

1. Prüfbescheid **fristgerecht** bearbeiten (Widerspruchsfristen!). Anwaltliche Beratung einholen.
2. Den relevanten Compliance-Log-Eintrag (`log --json`) als Anlage beifügen. Der Eintrag weist nach, **was zum Zeitpunkt der Verordnung dokumentiert wurde**.
3. Falls eine Praxisbesonderheit einschlägig ist: **substanziiert im Verwaltungsverfahren vortragen** (nicht erst im Klageverfahren — LSG BW 15.11.2023).
4. Hash-Chain-Integrität per `verify` dokumentieren (Bildschirmfoto oder Textausgabe der CLI).
5. Die juristische Bewertung des Einzelfalls bleibt dem Anwalt vorbehalten. Das Tool liefert Indizien, kein Urteil.

---

## 10. Updates und Pflege

### 10.1 Neue Version aus dem Repository ziehen

```bash
cd verordnungsampel
git pull
pip install -e .
```

### 10.2 Regelwerks-Updates

Das Regelwerk wächst und ändert sich laufend (neue AM-RL-Fassungen, neue G-BA-Entscheidungen, neue Rechtsprechung). Nach einem Update:

```bash
python -m verordnungsampel.cli.main init
```

Der Seed-Loader ist idempotent (DELETE vor INSERT für Praxisbesonderheiten und AM-RL-Anlagen), das heißt: alte Regelwerks-Versionen werden ersetzt, der Compliance-Log bleibt davon unberührt.

### 10.3 Compliance-Log bleibt erhalten

Updates berühren ausschließlich die Regelwerk-Datenbank (`regelwerk.db`). Der Compliance-Log (`compliance_log.db`) wird nicht angefasst. Die Hash-Chain bleibt über Versionsgrenzen hinweg intakt.

### 10.4 Methodik der Regelwerks-Pflege

Siehe `data/seed/UPDATE_METHODE.md` *(in Erstellung)*. Geplant sind vierteljährliche Seed-Updates per GitHub Actions, begleitet durch einen medizinischen Review-Partner.

---

## 11. Häufige Fragen (FAQ)

**Ist das ein Ersatz für meine ärztliche Prüfung?**
Nein. Die VerordnungsAmpel ist ein Nachschlagewerk für öffentliche Regelwerke. Die Prüfung der Indikation, der Kontraindikationen und der individuellen Patientensituation bleibt vollständig bei der behandelnden Ärztin bzw. dem behandelnden Arzt.

**Muss ich das Tool installieren, damit ich regresssicher bin?**
Nein. Das Tool ist ein Hilfsmittel. Regresssicherheit ergibt sich aus der ärztlichen Dokumentation, der Indikationsprüfung und der Kenntnis der Regelwerke — das Tool erleichtert den Zugriff darauf, übernimmt aber keine Verantwortung.

**Was passiert, wenn das Tool einen Fehler hat und ich deswegen einen Regress bekomme?**
Die Haftung bleibt beim verordnenden Arzt. Die GPL-3.0-Lizenz schließt Gewährleistung und Schadensersatz im zulässigen Rahmen aus. Das Tool zeigt zu jeder Regel das Stand-Datum der Quelle — eine veraltete Regelanzeige ist damit erkennbar. Im Zweifelsfall gilt: nicht blind auf das Tool verlassen, Primärquelle (z.B. G-BA-PDF) prüfen.

**Kann ich meine Daten exportieren oder löschen?**
Ja. Der vollständige Compliance-Log lässt sich mit `log --json` als JSON exportieren. Für die Löschung liegt die Datei `compliance_log.db` lokal auf dem Praxisrechner und kann einfach gelöscht werden; damit ist der Log komplett weg. Ein komfortabler `purge`/`export`-Subcommand (Empfehlungen E1–E8 aus dem DSGVO-Konzept) ist *in Erstellung*.

**Wer pflegt die Regelwerke?**
Aktuell die Open-Source-Community auf GitHub. Der Plan sieht einen medizinischen Review-Partner vor (Therapiefreiheit e.V. als erste Option), um die redaktionelle Pflege abzusichern. Bis dahin gilt: wer einen veralteten Eintrag findet, kann ihn per GitHub-Issue melden oder einen Pull Request stellen.

**Kann ich das Tool kommerziell einsetzen?**
Ja. Die GPL-3.0-Lizenz erlaubt kommerziellen Einsatz. Modifikationen und Ableitungen müssen unter derselben Lizenz veröffentlicht werden. Die bloße Nutzung in der Praxis ist keine „Verbreitung" im Lizenzsinn.

**Verarbeitet das Tool personenbezogene Daten?**
Nur in Form von ICD- und ATC-Codes und einem frei wählbaren Pseudonym. Keine Klarnamen, keine Befunde. Dennoch: weil der Arzt das Pseudonym auflösen kann, gelten die Betroffenenrechte aus Art. 12 – 22 DSGVO vollumfänglich. Details in `docs/legal/DSGVO_KONZEPT.md`.

**Kann ich das Tool offline betreiben?**
Ja, vollständig. Nach der Installation und dem `init` braucht es keine Netzwerkverbindung mehr. Keine Cloud, keine Telemetrie.

**Wie erkenne ich, ob das Regelwerk veraltet ist?**
Jeder Treffer zeigt das Stand-Datum der Quelle an. Wer einen neuen AM-RL-Stand sieht (z.B. auf g-ba.de), kann das Seed-Update per `git pull` + `init` einspielen.

**Läuft das auch auf dem Mac oder unter Linux?**
Ja. Python 3.10+ genügt. Die CLI funktioniert auf allen drei Plattformen. Die GUI erfordert PySide6, das ebenfalls plattformübergreifend verfügbar ist.

---

## 12. Support und Mitwirken

- **GitHub-Issues:** https://github.com/um-bruch/verordnungsampel/issues — für Fehlermeldungen, Regelwerks-Updates, Verbesserungsvorschläge.
- **E-Mail:** hallo@um-bruch.org
- **Pull Requests:** willkommen. Signoff via DCO (Developer Certificate of Origin) erforderlich — siehe `CONTRIBUTING.md`.
- **Sicherheits-Themen:** siehe `SECURITY.md` (verantwortliche Offenlegung).
- **Verhaltenskodex:** siehe `CODE_OF_CONDUCT.md`.

**Veraltete AM-RL-Regel melden:** GitHub-Issue mit folgenden Angaben: Regel-Kürzel (z.B. `AMRL_III_32`), neue Quell-URL (G-BA-PDF), geändertes Stand-Datum, kurze Beschreibung der Änderung.

---

## 13. Glossar

| Begriff | Erläuterung |
|---|---|
| **AM-RL** | Arzneimittel-Richtlinie des Gemeinsamen Bundesausschusses (G-BA). |
| **Anlage III** | Teil der AM-RL mit Verordnungseinschränkungen und -ausschlüssen. |
| **Anlage V** | Teil der AM-RL mit verordnungsfähigen Medizinprodukten. |
| **Anlage VI** | Teil der AM-RL zu Off-Label-Use (Teil A: anerkannt, Teil B: nicht anerkannt). |
| **ATC** | Anatomisch-Therapeutisch-Chemische Klassifikation (WHO). Kodiert Wirkstoffe, nicht Handelsnamen. |
| **BSG** | Bundessozialgericht. |
| **BSG B 6 KA 26/13 R** | Leitentscheidung: Nachgereichte Dokumentation reicht im Regressverfahren nicht. |
| **BSG B 6 KA 27/12 R** | Leitentscheidung: Bitte um Stellungnahme an die Krankenkasse ist zulässig. |
| **§ 29 BMV-Ä** | Bundesmantelvertrag Ärzte: Verbot der Einzelfall-Vorabgenehmigung normaler Arzneimittel. |
| **§ 31 Abs. 6 SGB V** | Cannabis als Medizin — Genehmigungspflicht bei Erstverordnung. |
| **§ 106 SGB V** | Rechtsgrundlage der Wirtschaftlichkeitsprüfung. |
| **§ 106b SGB V** | Rechtsgrundlage der Arzneimittel-Richtgrößenprüfung, inkl. Praxisbesonderheiten. |
| **§ 371a ZPO** | Beweiskraft elektronischer Dokumente im Zivil- und Sozialgerichtsverfahren. |
| **Container-Marker** | Interner Hinweis aus der Regelwerks-Logik, der den Vorab-Workflow auslöst (`pflicht_vorab`, `verboten_vorab`, `stellungnahme`, `off_label`). |
| **DSGVO** | Datenschutz-Grundverordnung (Verordnung (EU) 2016/679). |
| **G-BA** | Gemeinsamer Bundesausschuss. Gibt die AM-RL heraus. |
| **GKV-SV** | GKV-Spitzenverband. Führt die Liste bundesweiter Praxisbesonderheiten. |
| **Hash-Chain** | Kette aus SHA-256-Hashes, in der jeder Eintrag den Vorgänger-Hash enthält. Manipulation wird feststellbar. |
| **HSM** | Hierarchical State Machine. Muster zur Modellierung mehrstufiger Zustandsabläufe (hier: Begründungskette). |
| **ICD-10-GM** | Internationale Klassifikation der Krankheiten, 10. Revision, German Modification. |
| **MDSW** | Medical Device Software im Sinne der MDR (Medical Device Regulation, EU 2017/745). |
| **MDR** | Medical Device Regulation (EU 2017/745). |
| **PRISCUS 2.0** | Liste potenziell inadäquater Medikation bei älteren Menschen (Stand 2023). |
| **Praxisbesonderheit** | Anerkannter Grund für überdurchschnittliche Verordnungskosten (§ 106b Abs. 2 SGB V). |
| **PVS** | Praxisverwaltungssystem (z.B. TURBOMED, MEDISTAR, ALBIS, x.isynet). |
| **Pseudonym** | Kennzeichen, das ohne Zusatzwissen nicht auf eine Person zurückführt (Art. 4 Nr. 5 DSGVO). Nicht „anonym". |

---

## 14. Anhänge

### A. Vollständige CLI-Referenz

Alle Subcommands mit ihren Flags. Aufruf: `python -m verordnungsampel.cli.main <subcommand> [flags]`.

#### `init` — Datenbank initialisieren und Seed-Daten laden

Keine Flags.

#### `check` — Ampel-Check

| Flag | Pflicht | Beschreibung |
|---|---|---|
| `--icd <CODE>` | ja | ICD-10-GM-Code (z.B. `I10`) |
| `--atc <CODE>` | ja | ATC-Code (z.B. `C09AA02`) |
| `--alter <JAHRE>` | nein | Patientenalter in Jahren |
| `--justify` | nein | Bei GELB/ROT direkt strukturierte Begründung erfassen |
| `--answers <PFAD>` | nein | JSON-Datei mit vordefinierten Antworten für Non-Interactive-Modus |
| `--nutzer <NAME>` | nein | Optionaler Praxis-Account-Bezeichner für den Audit-Log |
| `--json` | nein | Ausgabe als JSON |
| `--no-log` | nein | Kein Eintrag im Compliance-Log |

Exit-Codes: `0` = OK, `3` = Begründung unvollständig (bei `--justify`).

#### `justify` — Check + strukturierte Begründung in einem Schritt

Flags identisch zu `check`, aber mit implizitem `--justify`.

#### `workflow` — Vorab-Klärungs-Workflow generieren

| Flag | Pflicht | Beschreibung |
|---|---|---|
| `--icd <CODE>` | ja | ICD-10-GM-Code |
| `--atc <CODE>` | ja | ATC-Code |
| `--alter <JAHRE>` | nein | Patientenalter |
| `--praxis <NAME>` | nein | Praxisname |
| `--praxis-adresse <ADR>` | nein | Praxisadresse |
| `--arzt <NAME>` | nein | Name des verordnenden Arztes |
| `--bsnr <BSNR>` | nein | Betriebsstättennummer |
| `--lanr <LANR>` | nein | Lebenslange Arztnummer |
| `--kk <NAME>` | nein | Krankenkasse |
| `--patient <KUERZEL>` | nein | Praxis-internes Pseudonym — **kein Klarname** |
| `--out <PFAD>` | nein | Dateipfad für den Workflow-Text |
| `--json` | nein | Metadaten als JSON ausgeben |
| `--no-log` | nein | Kein Eintrag im Compliance-Log |
| `--nutzer <NAME>` | nein | Audit-Log-Bezeichner |

Fehlende Felder werden im erzeugten Text mit lesbaren Platzhaltern (z.B. `[Praxisname einsetzen]`) ersetzt.

#### `log` — Compliance-Log anzeigen

| Flag | Pflicht | Beschreibung |
|---|---|---|
| `--tail <N>` | nein | Letzte N Einträge (Default: 20) |
| `--json` | nein | Ausgabe als JSON |

#### `verify` — Hash-Chain prüfen

Keine Flags. Exit-Code `0` = Kette intakt, `2` = Kette gebrochen.

#### `remind` — Quartals-Reminder für Praxisbesonderheiten

| Flag | Pflicht | Beschreibung |
|---|---|---|
| `--quartal <YYYY-Qn>` | ja | Quartalsbezeichner (z.B. `2026-Q2`) |
| `--json` | nein | Ausgabe als JSON |

#### `gui` — PySide6-Tray-Frontend starten

Keine Flags. Erfordert `pip install -e ".[gui]"`.

### B. Beispiel `antworten.json` für `justify`

**Für einen ROT-Fall ohne Off-Label-Container:**

```json
{
  "diagnose": "F41.1 generalisierte Angststoerung, mittelgradig, seit 9 Monaten.",
  "vorbehandlung": "Sertralin 50 mg taeglich ueber 8 Wochen.",
  "therapieversagen": "Unvertraeglichkeit (Uebelkeit, Agitation Woche 2 – 4), keine klinisch relevante Besserung.",
  "praxisbesonderheit": "",
  "confirm": true
}
```

**Für einen ROT-Fall mit Off-Label-Container (BSG-Kriterien):**

```json
{
  "diagnose": "<Beschreibung der schwerwiegenden Erkrankung>",
  "vorbehandlung": "<Substanzen, Dauer, Dosis>",
  "therapieversagen": "<Unvertraeglichkeit / Wirkungslosigkeit / Kontraindikation>",
  "bsg_off_label": {
    "schwerwiegende_erkrankung": "<Begruendung Schwere>",
    "keine_alternative": "<Begruendung Alternativlosigkeit>",
    "begruendete_erfolgsaussicht": "<Begruendung Erfolgsaussicht>"
  },
  "praxisbesonderheit": "",
  "confirm": true
}
```

Mindestlängen:
- `diagnose`, `vorbehandlung`: je 10 Zeichen
- `therapieversagen`: 15 Zeichen
- `bsg_off_label.*`: je 10 Zeichen
- `confirm`: Boolean `true`
- `praxisbesonderheit`: optional

### C. Abhängigkeiten

**Laufzeit (Kern):** nur Python-Standardbibliothek (`sqlite3`, `hashlib`, `argparse`, `json`, `datetime`, `pathlib`).

**Optional (GUI):** `PySide6 >= 6.6.0`.

**Entwicklung:** `pytest >= 7.0`, `pytest-cov >= 4.0`, `pytest-qt >= 4.4`.

Installation: `pip install -e ".[gui,dev]"`.

### D. Verweise auf weitere Dokumente

- `README.md` — Überblick, Quickstart (DE/EN)
- `KONZEPT.md` — Vollständiges Projektkonzept
- `CHANGELOG.md` — Versionshistorie
- `CONTRIBUTING.md` — Mitwirken (inkl. DCO-Signoff)
- `CODE_OF_CONDUCT.md` — Verhaltenskodex
- `SECURITY.md` — Sicherheitsmeldungen
- `docs/legal/RECHTSGUTACHTEN_MDSW.md` — Einstufung als Informationswerk (nicht MDSW)
- `docs/legal/DSGVO_KONZEPT.md` — Datenschutz, Betroffenenrechte, Löschkonzept
- `docs/legal/RECHTSGUTACHTEN_RUO.md` — Research-Use-Only-Gutachten
- `docs/legal/RECHTSGUTACHTEN_PUBLIKATION_LIZENZ.md` — Publikation und Lizenz
- `docs/CODE_AUDIT.md` — Audit der Referenz-Codebases
- `docs/RESOURCES_DIAGNOSTIC_PAPER.md` — Pattern-Quellen (Geiger 2026)
- `data/seed/UPDATE_METHODE.md` *(in Erstellung)* — Methodik der Regelwerks-Versionierung
- `docs/MARKTVERGLEICH.md` *(in Erstellung)* — Positionierung gegenüber kommerziellen PVS und vergleichbaren Tools

---

*Stand: 2026-04-12 · VerordnungsAmpel 0.1.0 (Pre-Alpha) · GPL-3.0-or-later · Lukas Geiger / Um:bruch · https://um-bruch.org*
