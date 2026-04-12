# VerordnungsAmpel_SOCIAL — DSGVO-Konzept

> Datenschutzkonzept für das Projekt "VerordnungsAmpel" (Softwareentwurf: Abgleich ärztlicher Verordnungen mit öffentlichen Regelwerken; Regress-Risikoindikatoren-Anzeige zu Forschungszwecken).
> Erstellt: 2026-04-12 | Status: Erstversion | Version: 1.0
> Verfasser: Rechtsabteilung (RB) des Um:bruch Think Tanks (CL / Claude)
> Prüfintervall: Halbjährlich oder bei funktionalen Erweiterungen, die neue Datenflüsse einführen.
> Grundlage: Verordnung (EU) 2016/679 (DSGVO), BDSG-neu, § 203 StGB (ärztliche Schweigepflicht), SGB V.

---

## 1. Einleitung und Geltungsbereich

### 1.1 Zweck dieses Dokuments

Dieses Konzept beschreibt den datenschutzrechtlichen Status und die technisch-organisatorische
Ausgestaltung des Open-Source-Tools **VerordnungsAmpel_SOCIAL**. Es adressiert sowohl die Frage,
*welche* Daten das Tool verarbeitet, als auch die Frage, *wer* nach DSGVO dafür verantwortlich ist.
Das Dokument wendet sich an drei Adressatenkreise:

1. **Urheber des Quellcodes** (Lukas Geiger, c/o Um:bruch Think Tank — **nicht** als eingetragener Verein) und künftige Forks/Dritte-Entwickler — als
   Nachweis, dass das Tool "data protection by design" (Art. 25 DSGVO) umsetzt.
2. **Nutzer (niedergelassene Vertragsärzte)** — als Orientierungshilfe, unter welchen Bedingungen sie
   das Tool DSGVO-konform in ihrer Praxis einsetzen können.
3. **Aufsichtsbehörden und Datenschutzbeauftragte** der Praxen — als prüfbare Grundlage.

### 1.2 Was tut das Tool?

**VerordnungsAmpel** ist ein Companion-Tool für niedergelassene Vertragsärzte in Deutschland. Es
läuft **lokal auf dem Arztrechner** (CLI-Programm, später PWA) und prüft Arzneimittel-Verordnungen
im Moment der Eingabe gegen öffentliche Regelwerke (AM-RL Anlagen III/V/VI, PRISCUS 2.0, GKV-SV-Liste
der Praxisbesonderheiten). Ausgabe: Ampel (grün/gelb/rot), strukturierte Begründung, manipulations-
sicherer Compliance-Log als Beweismittel vor dem Sozialgericht.

### 1.3 Architektur-Grundsatz "Keine Patientendaten"

Das Tool ist so konzipiert, dass es **keine identifizierenden Patientendaten** verarbeitet:

- **Eingabe je Fall:** ICD-10-GM-Code (z. B. `I10`), ATC-Code (z. B. `C09AA02`), optional Alter.
- **Keine Eingabe:** Name, Geburtsdatum, Anschrift, Krankenversichertennummer, eGK-Daten.
- **Optional:** Ein frei gewähltes **Patienten-Pseudonym** (z. B. `P-4711`), das der Arzt selbst
  vergibt und nur er auflösen kann.

**Keine Cloud, keine Backend-Server, keine Telemetrie.** Alle Daten bleiben auf dem Rechner des
Nutzers in `%APPDATA%\VerordnungsAmpel\regelwerk.db` (Windows) bzw. `~/.local/share/verordnungsampel/`
(Linux/macOS).

### 1.4 Geltungsbereich

Dieses Konzept gilt für:

- Die **Software-Distribution** (GitHub-Repository, Installer, Dokumentation).
- Die **Referenzinstallation** auf Entwicklungsrechnern der Um:bruch/Therapiefreiheit-Entwickler.
- Den **Pilot-Einsatz** in zehn Praxen (geplant).

Es gilt **nicht** für:

- Die individuelle Konfiguration einer Praxis-Installation (dafür ist die jeweilige Praxis
  verantwortlich, siehe Abschnitt 13).
- Integrationen mit Praxisverwaltungssystemen (aktuell nicht geplant; würde eigenes Konzept
  erfordern).

---

## 2. Rollenverteilung nach DSGVO

| Akteur | DSGVO-Rolle | Begründung |
|---|---|---|
| **Niedergelassener Vertragsarzt / Praxis** | **Verantwortlicher** (Art. 4 Nr. 7 DSGVO) | Entscheidet über Zweck und Mittel der Datenverarbeitung; das Tool ist Mittel zur Erfüllung seiner Dokumentations- und Plausibilitätsprüfungspflichten. |
| **VerordnungsAmpel (Software)** | **Hilfsmittel / Werkzeug** | Kein eigenes Rechtssubjekt. Die Software verarbeitet Daten rein lokal auf der Infrastruktur des Verantwortlichen. |
| **Um:bruch e.V. / Therapiefreiheit e.V. (Entwickler/Herausgeber)** | **Weder Auftragsverarbeiter noch Verantwortlicher** | Stellt die Software als Open-Source-Werkzeug bereit. Kein Zugriff auf die Daten, keine Weisungsbefugnis bei der Verarbeitung. Analog zu Herstellern von Office-Software oder Editoren. |
| **Prototype Fund / OKFN Deutschland (Förderer)** | **Kein DSGVO-Akteur** | Fördert die Entwicklung, verarbeitet keine Daten aus dem Tool. |

### 2.1 Warum der Entwickler nicht Verantwortlicher ist

Gemäß EuGH C-25/17 (Zeugen Jehovas) und EDSA-Leitlinien 07/2020 zu Verantwortlichkeit ist
Verantwortlicher, wer **"über Zwecke und Mittel der Verarbeitung entscheidet"**. Die Entwickler
von VerordnungsAmpel entscheiden weder über den Zweck der Verarbeitung (Risikoindikatoren-Sichtung
und sozialrechtliche Dokumentation in der konkreten Praxis) noch über die Mittel im
entscheidungsrelevanten Sinne (welche Patientenfälle
verordnet werden). Die Festlegung der Software-Funktionen ist mit der Festlegung des Zwecks einer
allgemeinen Software (z. B. LibreOffice, Thunderbird) vergleichbar und begründet keine Verantwort-
lichkeit.

### 2.2 Warum der Entwickler nicht Auftragsverarbeiter ist

Auftragsverarbeiter (Art. 4 Nr. 8, Art. 28 DSGVO) ist, wer **weisungsgebunden für den
Verantwortlichen** Daten verarbeitet. VerordnungsAmpel-Entwickler verarbeiten keine Nutzerdaten
(keine Telemetrie, kein Cloud-Sync, kein Support-Zugriff). Damit entfällt die Pflicht zum
Abschluss eines Auftragsverarbeitungsvertrags (AVV).

### 2.3 Konsequenz für den Nutzer (Arzt)

Der Arzt / die Praxis muss:

- Das Tool ins eigene **Verarbeitungsverzeichnis** (Art. 30 DSGVO) aufnehmen — auch dann, wenn
  nur ICD- und ATC-Codes verarbeitet werden. Siehe Mustereintrag in Abschnitt 13.3.
- Prüfen, ob der **eigene Datenschutzbeauftragte** (sofern bestellt) informiert werden muss.
- Bei Nutzung von Patienten-Pseudonymen: **die Zuordnung Pseudonym ↔ Patient** getrennt und
  sicher aufbewahren (siehe Abschnitt 13.2).

---

## 3. Verarbeitungsverzeichnis (Art. 30 DSGVO)

### 3.1 Angaben zum Verantwortlichen (vom Arzt zu ergänzen)

| Feld | Angabe |
|---|---|
| Verantwortlicher | <Praxisinhaber / Gemeinschaftspraxis> |
| Kontakt | <Praxisadresse, E-Mail> |
| Datenschutzbeauftragter | <sofern bestellt — Pflicht ab 20 Personen, die regelmäßig personenbezogene Daten verarbeiten, oder bei umfangreicher Verarbeitung besonderer Kategorien nach Art. 9, Art. 37 Abs. 1 lit. c DSGVO> |
| Tool-Version | <Version, z. B. 0.1.0> |
| Installationsdatum | <Datum> |

### 3.2 Verarbeitungstätigkeiten im Tool

| Nr. | Tätigkeit | Betroffene | Datenarten | Rechtsgrundlage | Speicherdauer | Empfänger | Drittland? |
|---|---|---|---|---|---|---|---|
| **V1** | **Plausibilitätsprüfung Verordnung** | Arzt (als Nutzer); ggf. Patient (pseudonymisiert) | ICD-10-GM-Code, ATC-Code, Alter (Jahre), optional Patienten-Pseudonym | Art. 6(1)(f) DSGVO (berechtigtes Interesse Arzt: Regress-Risiko-Dokumentation, Dokumentation nach § 630f BGB) | Dauerhaft im Compliance-Log, bis aktive Löschung durch Arzt | Keine (lokal) | Nein |
| **V2** | **Strukturierte Begründung (HSM)** | Arzt; ggf. Patient (pseudonymisiert) | Freitext-Begründung, Vorbehandlung, Therapieversagen, Diagnose-Kontext | Art. 6(1)(c) i.V.m. § 630f BGB (Dokumentationspflicht), Art. 6(1)(f) (Beweisvorsorge) | Dauerhaft im Compliance-Log | Keine | Nein |
| **V3** | **Compliance-Log mit Hash-Chain** | Arzt; Praxis | Zeitstempel, Hash-Kette, versiegelter Eintrag (enthält V1+V2-Daten) | Art. 6(1)(c) i.V.m. § 630f BGB, Art. 6(1)(f) (Regress-Risiko-Dokumentation, Beweisvorsorge) | 10 Jahre (Analogie zu § 630f Abs. 3 BGB, ärztliche Dokumentationspflicht); danach löschbar | Keine | Nein |
| **V4** | **Praxis-Kontextdaten** | Arzt, Praxis | Praxisname, Arztname, ggf. LANR, BSNR (in Workflow-Briefen) | Art. 6(1)(c) (Pflichtangaben in KK-Antrag), Art. 6(1)(f) | Bis Deinstallation / aktive Löschung | Keine | Nein |
| **V5** | **Workflow-Brief-Generierung** (Antrag an KK, Stellungnahme) | Arzt, Patient (pseudonymisiert), Krankenkasse (Empfänger) | Praxisdaten (V4) + Patienten-Pseudonym + medizinische Begründung (V2) | Art. 6(1)(c) i.V.m. § 31 Abs. 6 SGB V (Cannabis), § 37 SGB V etc. | Briefausgabe dauerhaft im Compliance-Log; Textdatei-Export liegt in Nutzerhand | Krankenkasse (bei Versand durch Arzt) | Nein |
| **V6** | **Quartalsreminder Praxisbesonderheiten** | Arzt | Aggregation aus V1-V3-Einträgen eines Quartals | Art. 6(1)(f) (LSG BW 15.11.2023: substanziierter Vortrag PB) | Report-Ausgabe transient; Rohdaten siehe V3 | Keine | Nein |
| **V7** | **SQLite-Datenbank auf Arztrechner** | (alle obigen) | regelwerk.db in %APPDATA% | Technische Umsetzung von V1-V6 | Siehe V1-V6; Datei als Ganzes löschbar | Keine | Nein |

**Keine weiteren Verarbeitungen.** Keine Telemetrie, keine Absturzberichte, keine Online-Updates
personenbezogener Daten, keine eingebettete Analytics.

### 3.3 TOM-Verweis

Siehe Abschnitt 8 (Technisch-organisatorische Maßnahmen).

---

## 4. Rechtsgrundlagen je Verarbeitung (Art. 6 DSGVO)

### 4.1 Übersicht

| Verarbeitung | Primäre Rechtsgrundlage | Sekundäre/Flankierende | Erwägung |
|---|---|---|---|
| V1 Plausibilitätsprüfung | **Art. 6(1)(f)** berechtigtes Interesse | Art. 6(1)(b) wenn Patient Arztvertrag hat | Regress-Risiko-Dokumentation ist berechtigtes Interesse des Arztes; Patient profitiert mittelbar (qualitätsgesicherte Verordnung). |
| V2 Begründungsdokumentation | **Art. 6(1)(c)** rechtliche Pflicht | Art. 6(1)(f) | § 630f BGB (Patientenakte), § 57 BMV-Ä, SGB V. |
| V3 Compliance-Log | **Art. 6(1)(c)** + **Art. 6(1)(f)** | — | Doppelter Grund: Dokumentationspflicht + Beweisvorsorge Sozialgericht (BSG B 6 KA 26/13). |
| V4 Praxis-Kontextdaten | **Art. 6(1)(c)** | Art. 6(1)(f) | Pflichtangaben bei Anträgen; eigene Daten des Arztes (Art. 6(1)(a) nicht erforderlich, da keine Drittperson). |
| V5 Workflow-Briefe | **Art. 6(1)(c)** | — | SGB V-Antragspflichten; Übermittlung an KK erfolgt durch Arzt eigenverantwortlich. |
| V6 Quartalsreminder | **Art. 6(1)(f)** | — | Organisatorisches Hilfsmittel, rein intern. |

### 4.2 Besondere Kategorien (Art. 9 DSGVO) — Abgrenzung

ICD-10-GM-Codes sind **Gesundheitsdaten im Sinne von Art. 4 Nr. 15 DSGVO** und damit besondere
Kategorien nach Art. 9 Abs. 1 DSGVO — **sobald sie einer bestimmten Person zugeordnet werden
können**. Im Tool liegen ICD-Codes isoliert vor (ohne Namen); sobald sie jedoch mit einem
Patienten-Pseudonym verknüpft werden, das der Arzt re-identifizieren kann, handelt es sich um
**pseudonymisierte Gesundheitsdaten** (Art. 4 Nr. 5) und damit weiterhin um besondere Kategorien
beim Arzt.

**Rechtsgrundlage nach Art. 9 Abs. 2 DSGVO:**

- **Art. 9 Abs. 2 lit. h DSGVO** i.V.m. **§ 22 Abs. 1 Nr. 1 lit. b BDSG**: Verarbeitung zum Zweck
  der Gesundheitsvorsorge, medizinischen Diagnostik, Versorgung oder Behandlung im
  Gesundheitsbereich durch Berufsgeheimnisträger.

Der Arzt als Berufsgeheimnisträger (§ 203 StGB) ist privilegierter Verarbeiter. Das Tool unterstützt
ihn bei einer Verarbeitung, die er in diesem Rahmen ohnehin durchführen dürfte.

### 4.3 § 203 StGB — Ärztliche Schweigepflicht

Das Tool verarbeitet **keine Klartext-Patientendaten** und löst daher für sich genommen keine
Offenbarung nach § 203 StGB aus. Da die Daten das lokale System nicht verlassen, tritt auch kein
mitwirkender Dritter in Erscheinung, der nach § 203 Abs. 4 StGB verpflichtet werden müsste. Die
Pseudonym-Zuordnungstabelle (siehe 13.2) ist vom Arzt selbst zu führen und unterliegt dort
derselben Schweigepflicht.

---

## 5. Datenkategorien und Schutzstufen

| Kategorie | DSGVO-Artikel | Konkret im Tool | Schutzstufe |
|---|---|---|---|
| ICD-10-GM-Code (isoliert) | — (Fachcode) | Eingabefeld `icd` | Normal |
| ICD-10-GM-Code + Pseudonym | Art. 4 Nr. 5, Art. 9 (über Pseudonym) | `justify --patient P-4711 --icd F41` | **Hoch** (Gesundheitsdaten, pseudonymisiert) |
| ATC-Code (Wirkstoff, isoliert) | — (Fachcode) | Eingabefeld `atc` | Normal |
| ATC-Code + Pseudonym | Art. 4 Nr. 5, Art. 9 | analog | **Hoch** |
| Freitext-Begründung | Art. 4 Nr. 1, Art. 9 (inhaltlich) | HSM-Step "Therapieversagen" etc. | **Hoch** |
| Zeitstempel | Art. 4 Nr. 1 (bezogen auf Arzt) | Compliance-Log `ts` | Normal |
| Praxisname, Arztname | Art. 4 Nr. 1 (Arztdaten) | Config / Workflow-Briefe | Normal |
| Patienten-Pseudonym (isoliert) | Art. 4 Nr. 5 | `--patient P-4711` | Normal (pseudonymisiert, nicht anonym) |
| Hash-Kette | nicht personenbezogen | `chain_hash` in DB | Nicht DSGVO-relevant |
| Regelwerks-Daten (AM-RL, PRISCUS) | nicht personenbezogen | seed data | Nicht DSGVO-relevant (öffentliche Daten) |

**Besondere Kategorien nach Art. 9** fallen nur in Kombination mit einem Pseudonym oder einer
Zuordnungsmöglichkeit an. Im reinen Modus ohne Pseudonym entstehen sie nicht.

---

## 6. Speicherung und Löschfristen

### 6.1 Speicherorte

| Artefakt | Ort | Format |
|---|---|---|
| Regelwerk + Compliance-Log | `%APPDATA%\VerordnungsAmpel\regelwerk.db` (Windows) bzw. `~/.local/share/verordnungsampel/regelwerk.db` | SQLite |
| Workflow-Briefe (Export) | Vom Nutzer gewählter Pfad (`--out antrag.txt`) | Plain Text |
| Konfiguration (Praxisname etc.) | `%APPDATA%\VerordnungsAmpel\config.json` | JSON |
| Logfiles (technisch) | `%APPDATA%\VerordnungsAmpel\logs\` (sofern aktiviert) | Text |

**Keine Speicherung ausserhalb des lokalen Systems.**

### 6.2 Löschfristen

| Datenart | Regelfrist | Begründung |
|---|---|---|
| Compliance-Log-Einträge (V3) | **10 Jahre** | Analogie zu § 630f Abs. 3 BGB (ärztliche Dokumentationspflicht); Regressprüfungen laufen teils mehrjährig, Sozialgerichtsverfahren können lange dauern. |
| Workflow-Brief-Exporte | In Nutzerhand | Arzt entscheidet — analog zu anderen Praxis-Dokumenten. |
| Config/Praxisdaten | Bis Deinstallation | Reine Installations-Metadaten. |
| Technische Logs | 30 Tage (sofern aktiviert; Default: deaktiviert) | Fehleranalyse. |

**Empfehlung an den Arzt:** Jährlich prüfen, welche Einträge älter als 10 Jahre sind und aus dem
Compliance-Log entfernt werden können (siehe Abschnitt 9 zum Konflikt mit der Hash-Chain).

### 6.3 Löschmechanismen

Das Tool stellt bereit (bzw. soll bereitstellen, siehe Abschnitt 14):

- **`purge --older-than <Datum>`** — Bulk-Löschung von Compliance-Log-Einträgen älter als Datum.
  Erzeugt neuen Genesis-Block (Hash-Chain-Neustart), mit Protokolleintrag "Teil-Purge am ...".
- **`purge --all`** — Komplett-Reset der Datenbank.
- **`export --patient P-4711 --format json`** — Export aller Einträge zu einem Pseudonym
  (zur Umsetzung des Auskunftsrechts, wenn der Patient Auskunft verlangt und der Arzt das
  Pseudonym auflösen kann).
- **`export --all --format json`** — Voll-Export (Datenportabilität Art. 20 im Verhältnis Arzt
  zu einem evtl. Nachfolgesystem).

---

## 7. Betroffenenrechte (Art. 12-22 DSGVO)

Hier ist strikt zu unterscheiden: Die Rechte richten sich gegen den **Arzt als Verantwortlichen**,
nicht gegen das Tool/die Entwickler. Das Tool bietet aber die **technischen Funktionen**, die der
Arzt zur Erfüllung seiner Pflichten benötigt.

### 7.1 Umsetzungsmatrix

| Recht | Artikel | Wer erfüllt? | Wie im Tool? |
|---|---|---|---|
| **Informationspflicht** | Art. 13/14 | Arzt (in seinen Datenschutzinformationen) | Arzt kann auf dieses Konzept verweisen. |
| **Auskunft** | Art. 15 | Arzt | `export --patient <Pseudonym> --format json`; Arzt löst Pseudonym auf, liefert Inhalt. |
| **Berichtigung** | Art. 16 | Arzt | Tool verhindert Änderung wegen Hash-Chain. **Workaround:** Nachtrag als neuer Log-Eintrag mit Verweis auf korrigierten Eintrag (Korrekturvermerk); altes Ergebnis bleibt als Historie sichtbar. |
| **Löschung** | Art. 17 | Arzt | Voll-Löschung über `purge --all`; selektive Löschung über `purge --older-than` oder (nach Implementierung) `purge --patient <Pseudonym>` mit Chain-Neustart. |
| **Einschränkung** | Art. 18 | Arzt | Eintrag kann in externer Notiz als "gesperrt" markiert werden; Tool selbst kennt keinen Einschränkungs-Status. **Empfehlung:** Feature `mark --restricted <id>` in Tool aufnehmen. |
| **Datenübertragbarkeit** | Art. 20 | Arzt | `export --patient <Pseudonym> --format json` (strukturiert, maschinenlesbar). |
| **Widerspruch** | Art. 21 | Arzt | Bei Widerspruch gegen Art. 6(1)(f)-Verarbeitungen: Löschung wie Art. 17. |
| **Automatisierte Einzelentscheidung** | Art. 22 | Arzt | Tool trifft **keine Einzelentscheidung**: Ampel ist Entscheidungshilfe, der Arzt entscheidet. Art. 22 greift daher nicht (entspricht Erwägungsgrund 71). |

### 7.2 Fristen

- Auskunft (Art. 15), Datenübertragbarkeit (Art. 20): **1 Monat** (Art. 12 Abs. 3), verlängerbar
  um 2 Monate.
- Löschung (Art. 17), Berichtigung (Art. 16): **unverzüglich**.

### 7.3 Sonderfall Patienten-Pseudonym

Patientenpseudonyme wie `P-4711` sind **nicht anonym**, sondern pseudonymisiert (Art. 4 Nr. 5).
Der Arzt kann sie über seine eigene Zuordnungstabelle auflösen. Damit gelten Betroffenenrechte
**vollumfänglich**. Für den Arzt bedeutet das:

1. Zuordnungstabelle Pseudonym ↔ Patient sauber führen (siehe 13.2).
2. Bei Auskunftsersuchen Pseudonym im Tool nachschlagen, Inhalt exportieren, dem Patienten
   aushändigen.
3. Bei Löschersuchen: Einträge zum Pseudonym löschen (Bulk-Purge mit Chain-Neustart oder
   selektive Löschfunktion).

---

## 8. Technisch-organisatorische Maßnahmen (Art. 32 DSGVO)

### 8.1 Technische Maßnahmen (bereits umgesetzt oder vorgesehen)

| Maßnahme | Status | Umsetzung |
|---|---|---|
| **Lokale Datenhaltung** | ✅ Umgesetzt | SQLite im Nutzerprofil; keine Cloud-Synchronisation. |
| **Keine Telemetrie** | ✅ Umgesetzt | Kein Netzwerk-Call aus dem Tool, außer optional Update-Check (gegen GitHub-Release-API, ohne personenbezogene Daten). |
| **Pseudonymisierung (Art. 32 Abs. 1 lit. a)** | ✅ Umgesetzt (strukturell) | Pseudonym statt Name; Zuordnung außerhalb des Tools. |
| **Integritätsschutz (Art. 32 Abs. 1 lit. b)** | ✅ Umgesetzt | Hash-Chain über Compliance-Log; `verify` erkennt Manipulation. |
| **Verschlüsselung at rest** | ⚠️ Empfohlen | Empfehlung an Arzt: BitLocker (Windows Pro/Enterprise) oder FileVault (macOS) auf System-/Datenpartition. Optional: SQLCipher-Variante der Datenbank (Roadmap). |
| **Verschlüsselung in transit** | — | Entfällt: kein Netzwerktransport personenbezogener Daten. |
| **Zugriffskontrolle** | ⚠️ Systemebene | Tool selbst hat keine Authentifizierung (analog Desktop-Office). Schutz erfolgt über Windows-Login / Bildschirmsperre. |
| **Backup** | ⚠️ Empfohlen | Empfehlung: Tägliches Backup der Praxis-IT, inklusive `%APPDATA%\VerordnungsAmpel\`. |
| **Logging und Nachvollziehbarkeit** | ✅ Umgesetzt | Alle Verordnungsprüfungen im Compliance-Log mit Zeitstempel. |
| **Löschbarkeit (Art. 17-konform)** | ⚠️ Teilweise | Voll-Löschung möglich; selektive Einzellöschung konfliktbehaftet (siehe 9). Empfehlung: `purge`-CLI + Chain-Neustart. |

### 8.2 Organisatorische Maßnahmen (Empfehlungen an die Praxis)

- Schulung der Mitarbeiter, dass keine Klartext-Patientendaten im Tool eingegeben werden.
- Dokumentierte Verfahren zur Pseudonym-Vergabe und -Auflösung.
- Aufnahme in Verarbeitungsverzeichnis der Praxis (Mustereintrag 13.3).
- Zuständigkeit im Team benennen (wer pflegt das Tool, wer beantwortet Betroffenenanfragen dazu).

### 8.3 Risikoanalyse nach Art. 32 Abs. 2

| Risiko | Eintrittswahrscheinlichkeit | Schadensschwere | Bewertung |
|---|---|---|---|
| Verlust der lokalen DB (Festplattenausfall) | Mittel | Gering für Datenschutz (keine Leak-Wirkung), hoch für Beweismittelfunktion | Backup erforderlich |
| Unbefugter Zugriff am Arztrechner | Gering (gesicherte Praxis-IT vorausgesetzt) | Hoch (Art. 9-Daten lesbar) | Betriebssystem-Verschlüsselung + Bildschirmsperre |
| Diebstahl des Rechners | Gering | Hoch | Festplattenverschlüsselung Pflicht |
| Manipulation der DB (z. B. durch Mitarbeiter) | Gering | Hoch für Beweismittelfunktion | Hash-Chain + `verify` |
| Fehlerhafte Pseudonym-Eingabe | Mittel | Gering (Konsistenzverlust, kein Leak) | Eingabevalidierung |
| Exfiltration durch Malware | Gering-mittel | Hoch | Standard-Anti-Malware der Praxis |

Ergebnis: Die Maßnahmen sind **angemessen im Sinne von Art. 32 DSGVO**, sofern die Empfehlungen
an den Arzt (Verschlüsselung, Backup) umgesetzt werden.

---

## 9. Sonderfrage: Hash-Chain vs. Recht auf Löschung (Art. 17)

### 9.1 Der Konflikt

Der Compliance-Log ist als **Hash-Chain** konzipiert: Jeder Eintrag enthält den Hash des
Vorgängereintrags. Das dient der **Manipulationssicherheit** — ein nachträgliches Ändern oder
Entfernen eines einzelnen Eintrags wird durch `verify` erkannt. Genau diese Eigenschaft kollidiert
prima facie mit Art. 17 DSGVO: Wenn ein Patient Löschung verlangt, soll sein Eintrag entfernt
werden — aber dadurch bricht die Kette.

### 9.2 Lösung: Bulk-Löschung + Chain-Neustart

Das Tool folgt dem Grundsatz: **Einzelne Einträge sind nicht löschbar, aber der gesamte Log (oder
ein Bereich davon) ist es.** Umgesetzt über:

1. **`purge --all`**: Löscht die gesamte DB und erzeugt einen neuen Genesis-Block. Alle Daten sind
   weg, Art. 17 ist vollumfänglich erfüllt.
2. **`purge --older-than <Datum>`**: Löscht alle Einträge bis zum Datum, erzeugt neuen Genesis-Block
   mit Zeitstempel und Protokolleintrag ("Teil-Purge am YYYY-MM-DD aus DSGVO-Gründen"). Nachfolgende
   Einträge werden neu verkettet. Verify-Ergebnis zeigt: Chain gültig ab Genesis-Block X.
3. **`purge --patient <Pseudonym>`** (empfohlen, noch zu implementieren): Exportiert alle nicht-
   betroffenen Einträge, löscht die alte DB, reimportiert in neue Chain. Langsam, aber Art.-17-konform.

### 9.3 Rechtliche Würdigung

- **Art. 17 Abs. 1 DSGVO** verlangt "unverzügliche Löschung" — wird durch `purge`-Funktionen
  erfüllt, auch wenn dabei unbetroffene Einträge ebenfalls verschwinden oder neu verkettet werden.
- **Art. 17 Abs. 3 lit. b DSGVO** erlaubt Ausnahmen bei "Erfüllung einer rechtlichen
  Verpflichtung" — die zehnjährige Aufbewahrung nach § 630f BGB kann im Einzelfall einen
  Löschanspruch verdrängen. In diesem Fall wird **nicht** gelöscht, sondern nur **eingeschränkt**
  (Art. 18 Abs. 1 lit. b), etwa durch Export + Vermerk.
- **Beweismittelfunktion vs. Löschrecht:** Wenn ein laufendes Regressverfahren den Log als
  Beweismittel benötigt, überwiegt in aller Regel das berechtigte Interesse des Arztes an der
  Integritätssicherung (Art. 17 Abs. 3 lit. e — Verteidigung von Rechtsansprüchen). Der Arzt muss
  dies dokumentieren und dem Betroffenen begründet mitteilen.

### 9.4 Empfehlung

- In der Praxis wird der Löschanspruch für einzelne Patientenfälle **selten** eintreten, da die
  ärztliche 10-Jahres-Aufbewahrung greift.
- Wenn er nach Ablauf der Aufbewahrungsfrist eintritt: `purge --older-than` oder
  `purge --patient` nutzen, Chain-Neustart dokumentieren.
- Der Neustart-Event **selbst** ist kein Integritätsverlust: Verify gibt ab Genesis-Block
  wieder volle Sicherheit.

---

## 10. Weitergabe an Dritte / Auftragsverarbeiter (Art. 28)

**Keine.** Das Tool verarbeitet Daten ausschließlich lokal. Es gibt:

- keine Auftragsverarbeiter,
- keine Empfänger im Regelbetrieb,
- keine Schnittstellen zu Dritten,
- keine automatisierte Übermittlung.

**Ausnahme 1 — nutzergetriggert:** Wenn der Arzt mit `workflow --out antrag.txt` einen Brief an
die Krankenkasse generiert und diesen versendet, ist das eine vom Arzt aktiv veranlasste
**Übermittlung an einen Empfänger** (die Krankenkasse). Rechtsgrundlage: § 31 Abs. 6 SGB V bzw.
analog. Diese Übermittlung fällt in die Sphäre des Arztes; das Tool liefert nur das Dokument.

**Ausnahme 2 — geplant, optional:** Update-Check gegen GitHub-Release-API. Dabei wird nur die
aktuelle Tool-Version gesendet, keine personenbezogenen Daten. Sollte diese Funktion kommen, wird
sie hier ergänzt und erhält Opt-out.

---

## 11. Datenübermittlung in Drittländer (Art. 44-49)

**Keine.** Alle Daten bleiben lokal im Nutzersystem. Kein Cloud-Backend, kein CDN, keine
US-Dienstleister im Datenfluss.

**Ausnahme (hypothetisch):** GitHub-Release-API-Updatecheck (falls implementiert) würde Metadaten
an GitHub Inc. (USA) senden. Da keine personenbezogenen Daten übermittelt würden, läge keine
Übermittlung im Sinne von Art. 44 vor.

---

## 12. Meldepflichten bei Datenpannen (Art. 33/34)

### 12.1 Zuständigkeit

Eine Datenpanne im Zusammenhang mit dem Tool ist **eine Datenpanne des Arztes**, nicht der
Entwickler. Der Arzt muss:

- Binnen **72 Stunden** nach Kenntnis der Aufsichtsbehörde melden (Art. 33 DSGVO), sofern ein
  Risiko für Betroffene besteht.
- Bei hohem Risiko die Betroffenen informieren (Art. 34 DSGVO).

### 12.2 Typische Szenarien

| Szenario | Meldepflicht? | Bemerkung |
|---|---|---|
| Diebstahl des Arztrechners mit unverschlüsselter Platte | **Ja** (Art. 33 + 34) | Gesundheitsdaten (Art. 9) betroffen. |
| Malware-Infektion mit Exfiltrationsverdacht | **Ja** | Wie oben. |
| Versehentliche Weitergabe der DB-Datei | **Ja** | Siehe oben. |
| Fehlerhafte Ampel-Entscheidung ohne Datenleak | **Nein** | Keine Datenpanne i.S.d. Art. 33. |
| Hash-Chain-Bruch (technisch) | **Nein** (Art. 33), aber Dokumentationsfehler | Integritätsverlust ohne Offenlegung. |

### 12.3 Pflicht der Entwickler

Die Entwickler sind nicht Meldeverpflichtete. **Sie werden jedoch** sicherheitsrelevante Defekte
(z. B. SQL-Injection, Pfadtraversal) binnen 30 Tagen nach Bekanntwerden öffentlich im
GitHub-Security-Advisory dokumentieren (Coordinated Disclosure). Kontakt: `security@um-bruch.org`
(einzurichten).

---

## 13. Pflichten für den Nutzer (Arzt)

### 13.1 Vor Inbetriebnahme

- [ ] Dieses Konzept einmal vollständig lesen.
- [ ] Prüfen, ob der eigene Datenschutzbeauftragte zu beteiligen ist.
- [ ] Festplattenverschlüsselung aktivieren (BitLocker/FileVault).
- [ ] Aufnahme in Verarbeitungsverzeichnis der Praxis (Mustereintrag 13.3).
- [ ] Backup-Strategie bestätigen.
- [ ] Datenschutzinformation für Patienten (Art. 13 DSGVO) ggf. aktualisieren, falls Pseudonyme
      verwendet werden.

### 13.2 Pseudonym-Verfahren (empfohlenes Setup)

- **Separate Zuordnungstabelle** (z. B. verschlüsseltes Excel, Tresor im PVS) führen:
  `P-4711 → Max Mustermann, geb. 01.01.1970`
- Zugriff nur für autorisiertes Personal.
- Pseudonyme **nicht** aus sensiblen Daten ableiten (keine Initialen + Geburtsjahr), sondern
  fortlaufend nummerieren.
- Bei Praxisübergabe: Tabelle dem Nachfolger nur mit Patienteneinwilligung übergeben, sonst löschen.

### 13.3 Mustereintrag Verarbeitungsverzeichnis

```
Bezeichnung: Regressprüfung mit VerordnungsAmpel
Zweck: Plausibilitätsprüfung von Verordnungen, strukturierte Begründung,
       Compliance-Dokumentation zur Abwehr von Wirtschaftlichkeitsprüfungen.
Rechtsgrundlage: Art. 6 Abs. 1 lit. c DSGVO i.V.m. § 630f BGB;
                 Art. 9 Abs. 2 lit. h DSGVO i.V.m. § 22 BDSG.
Betroffene: Patienten (pseudonymisiert), Arzt/Praxis.
Datenkategorien: ICD-10-GM, ATC, Alter, optional Patientenpseudonym,
                 Begründungstexte, Zeitstempel.
Empfänger: Keine (lokal); Krankenkasse nur bei aktiv durch Arzt versendeten Anträgen.
Drittlandübermittlung: Keine.
Löschfrist: Compliance-Log 10 Jahre analog § 630f Abs. 3 BGB;
            unverzügliche Löschung bei berechtigtem Antrag nach Art. 17.
TOMs: Festplattenverschlüsselung, Backup, Hash-Chain-Integritätsschutz,
      Pseudonymisierung, Bildschirmsperre, Zugriffsschutz auf Praxis-IT.
Verantwortlicher: <Praxisinhaber>
Letzte Prüfung: <Datum>
```

### 13.4 Im laufenden Betrieb

- Bei Betroffenenanfragen: Pseudonym auflösen, Export durchführen, binnen Frist reagieren.
- Hash-Chain-Integrität mindestens quartalsweise prüfen (`verify`-Befehl).
- Softwareaktualisierungen zeitnah einspielen (Patchpflicht aus Art. 32).

---

## 14. Empfehlungen an die Entwickler

Die folgenden Punkte sind teils umgesetzt, teils noch offen. Sie dienen dazu, "privacy by design"
und die Erfüllbarkeit von Betroffenenrechten im Tool zu gewährleisten.

### 14.1 Umgesetzt (Stand 2026-04-08)

- ✅ Keine Telemetrie, keine Cloud.
- ✅ Hash-Chain-Compliance-Log mit `verify`.
- ✅ Pseudonym-Feld (optional, nicht verpflichtend).
- ✅ Lokale SQLite in `%APPDATA%`.

### 14.2 Empfohlene Ergänzungen (Priorität 1 — vor Pilot)

| # | Feature | Begründung | Aufwand |
|---|---|---|---|
| E1 | **`export --patient <Pseudonym> [--format json|pdf]`** | Art. 15 + Art. 20: Auskunft und Datenportabilität. | Mittel |
| E2 | **`export --all --format json`** | Datenportabilität insgesamt; auch für Praxisübergabe. | Gering |
| E3 | **`purge --all`** (Chain-Reset) | Art. 17: Vollständige Löschung. | Gering |
| E4 | **`purge --older-than <Datum>`** (Chain-Neustart) | Art. 17 + Routinelöschung nach 10 Jahren. | Mittel |
| E5 | **`purge --patient <Pseudonym>`** (selektiv + Re-Chain) | Art. 17 bei Betroffenenanfrage vor Fristablauf. | Hoch (Chain-Rebuild) |
| E6 | **`config set praxis.name ...`** statt Hardcode | Saubere Trennung Code/Konfiguration; vereinfacht DSGVO-Auskunft. | Gering |
| E7 | **Startup-Banner mit Hinweis:** "Dieses Tool verarbeitet keine Klartext-Patientendaten. Verwenden Sie Pseudonyme." | User-Education, Art. 25 (Voreinstellung). | Trivial |
| E8 | **SECURITY.md im Repo** mit Coordinated-Disclosure-Adresse | Art. 32: Responsible Disclosure. | Gering |

### 14.3 Empfohlene Ergänzungen (Priorität 2 — vor Public Release)

| # | Feature | Begründung |
|---|---|---|
| E9 | **Optional: SQLCipher-Variante** der DB (Passphrase beim Start) | Defense in Depth, wenn Festplattenverschlüsselung aus irgendeinem Grund ausfällt. |
| E10 | **`mark --restricted <id> --reason ...`** | Art. 18: Einschränkung der Verarbeitung. |
| E11 | **Automatischer Reminder:** Einträge älter als 10 Jahre vorhanden — Purge anbieten | Datenminimierung, Speicherbegrenzung. |
| E12 | **Verify auf Abruf + einmal pro Monat automatisch** | Art. 32 Integritätsschutz. |
| E13 | **Signierte Releases** (GPG oder Sigstore) | Schutz vor Supply-Chain-Manipulation. |

### 14.4 Empfohlene Ergänzungen (Priorität 3 — PWA-Phase)

| # | Feature | Begründung |
|---|---|---|
| E14 | **Lokaler Storage + Service Worker offline-first** | Weiterhin keine Serverdaten. |
| E15 | **Keine Third-Party-Fonts, keine CDN-Ressourcen** | Schrems-II-frei. |
| E16 | **CSP-Header streng** (self, no external) | Exfiltrations-Schutz. |
| E17 | **Bei PVS-Integration (langfristig): eigenes DSGVO-Konzept** | Neuer Datenfluss → neues Konzept. |

---

## 15. Grenzen dieser Einschätzung

### 15.1 Disclaimer

Dieses Konzept wurde durch die **KI-basierte Rechtsabteilung (RB) des Um:bruch Think Tanks** (CL /
Claude) erstellt. Es ersetzt **keine anwaltliche Beratung** und **keine Prüfung durch einen
zertifizierten Datenschutzbeauftragten**.

- Gesetzes- und Rechtsprechungsstand: April 2026. Relevante Urteile (BSG, SG Marburg, LSG BW) sind
  bis zum Erstellungsdatum berücksichtigt, können sich aber ändern.
- Formulierungen zu Art. 9 Abs. 2 lit. h DSGVO i.V.m. § 22 BDSG stützen sich auf die herrschende
  Literaturmeinung zur Verarbeitung durch Berufsgeheimnisträger. Im Einzelfall können
  Landesaufsichtsbehörden abweichende Auffassungen vertreten.
- Der Konflikt Hash-Chain ↔ Art. 17 (Abschnitt 9) ist in Literatur und Rechtsprechung bislang nicht
  abschließend geklärt. Die hier vertretene Lösung (Bulk-Purge + Chain-Neustart) ist eine
  pragmatische, vertretbare Auslegung, nicht die einzig mögliche.

### 15.2 Empfehlungen vor Produktivbetrieb in einer Praxis

1. **Anwaltliche Gegenprüfung** dieses Konzepts durch eine auf Medizinrecht + Datenschutz
   spezialisierte Kanzlei.
2. **Rückkopplung mit der zuständigen Landesaufsichtsbehörde** (Vorab-Anfrage nach Art. 36 DSGVO ist
   nicht zwingend, kann aber Rechtssicherheit schaffen).
3. **Datenschutzfolgenabschätzung (DSFA, Art. 35 DSGVO)** durch die einsetzende Praxis — ist bei
   Gesundheitsdatenverarbeitung im größeren Umfang empfohlen, auch wenn sie beim einzelnen
   Arzt oft unter der Schwelle bleibt.
4. **Einbindung eines Datenschutzbeauftragten**, sofern in der Praxis vorhanden oder erforderlich
   (Art. 37 DSGVO).
5. **Konsultation des ärztlichen Berufsrechts** (Landesärztekammer) zur Frage, ob die
   Dokumentation in einer separaten Software neben dem PVS standesrechtliche Fragen aufwirft.

### 15.3 Aktualisierung dieses Konzepts

Das Konzept ist bei jeder der folgenden Änderungen zu aktualisieren:

- Neue Features, die Datenverarbeitung einführen oder verändern.
- Einführung von Netzwerkkommunikation jeglicher Art.
- Integration mit Dritt-Systemen (PVS, KV-SafeNet, TI).
- Änderung der Trägerschaft.
- Neue einschlägige Rechtsprechung oder Gesetzgebung.

**Verantwortlich:** RB (Rechtsabteilung Um:bruch Think Tank) in Abstimmung mit den Projektträgern.

---

## 16. Verwandte Dokumente

| Dokument | Inhalt |
|---|---|
| [KONZEPT.md](../../KONZEPT.md) | Projektkonzept, Funktionen, Architektur |
| [README.md](../../README.md) | Kurzüberblick, CLI-Befehle |
| [docs/CODE_AUDIT.md](../CODE_AUDIT.md) | Audit der Referenz-Codebases |
| `C:\Users\User\OneDrive\.UMBRUCH\Wiki\DSGVO-KONZEPT.md` | Um:bruch-eigenes DSGVO-Konzept (Vorbild) |
| `C:\Users\User\OneDrive\.UMBRUCH\Wiki\MERKBLATT-DSGVO.md` | Begriffs-Leitfaden |

---

*Erstellt: 2026-04-12 — RB: CL (Claude) | Nächste Pflichtprüfung: Oktober 2026 | Version 1.0*
