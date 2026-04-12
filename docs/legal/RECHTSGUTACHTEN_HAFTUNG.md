# Rechtliche Prüfung — VerordnungsAmpel_SOCIAL: Haftung gegenüber Nutzern (Ärzten) bei Regress-Schaden

**Datum:** 2026-04-12
**RB:** Claude (CL), Um:bruch Rechtsabteilung
**Typ:** Anlassprüfung / Folgegutachten zu `RECHTSGUTACHTEN_MDSW.md` (2026-04-12)
**Auftrag:** Lukas Geiger (Projekt-Initiator VerordnungsAmpel_SOCIAL), 2026-04-12
**Status:** KI-basierte Erstanalyse — kein Anwaltsersatz (siehe Abschnitt 12)

---

## 1. Gegenstand und Bezug zu anderen Gutachten

Dieses Gutachten ist das **dritte Folgegutachten** zum Projekt VerordnungsAmpel_SOCIAL und behandelt die Frage der **zivilrechtlichen Haftung des Projektträgers (Um:bruch) gegenüber dem Nutzer (Arzt)**, wenn dieser sich auf das Tool verlässt und dennoch einen Regress erleidet.

### Bezug zu bisherigen Gutachten

| Gutachten | Gegenstand | Kernergebnis |
|---|---|---|
| **RECHTSGUTACHTEN_MDSW.md** (2026-04-12) | Abgrenzung Informationswerk vs. Medical Device Software nach MDR | Bei sauberer Zweckbestimmung kein MDSW. Kein CE, keine Klasse IIa. |
| **DSGVO_KONZEPT.md** (Projektintern) | Datenschutz-Architektur | Keine Personendaten, nur ICD/ATC-Codes. DSGVO formal nicht anwendbar. |
| **RECHTSGUTACHTEN_RUO.md** (Folge-1) | Research Use Only — Status vor Pilot | noch nicht erstellt |
| **RECHTSGUTACHTEN_PUBLIKATION_LIZENZ.md** (Folge-2) | Publikations- und Lizenzstrategie (GPL-3.0) | noch nicht erstellt |
| **RECHTSGUTACHTEN_HAFTUNG.md** (Folge-3, hier) | Haftung gegenüber dem Arzt bei Regress-Schaden | Siehe Abschnitt 9 |

### Die konkrete Frage des Mandanten

> "Wer haftet, wenn ein Arzt sich auf die VerordnungsAmpel verlässt, und aufgrund eines Fehlers oder einer veralteten Regel dennoch ein Regress gegen ihn läuft?"

### Die zu prüfende Position des Mandanten

> "Nicht getestet. Ärzte sind — wie immer — selbst verantwortlich. Wir streben externe Prüfungen an, können sie aber nicht garantieren. Nutzung auf eigenes Risiko."

---

## 2. Die zu prüfende Position des Mandanten

Die Mandanten-Position besteht aus vier Teilen:

| Teilaussage | Rechtliche Stoßrichtung |
|---|---|
| „Nicht getestet" | Offenlegung fehlender Validierung → Ausschluss von Zusicherungen (§ 444 BGB) |
| „Ärzte sind selbst verantwortlich" | Verweis auf die ärztliche Letztverantwortung nach § 630a BGB, § 76 SGB V |
| „Externe Prüfungen angestrebt, aber nicht garantiert" | Ehrlicher Projektstatus, keine Vorspiegelung von Geprüftheit |
| „Nutzung auf eigenes Risiko" | Klassischer Risikoübernahme-Disclaimer (AS IS, NO WARRANTY) |

Diese Position ist **im Kern tragfähig**, muss aber **operationalisiert** werden: Disclaimer müssen rechtlich wirksam formuliert, an den richtigen Stellen platziert und technisch verpflichtend (Erststart-Acknowledgement) gemacht werden. Zugleich darf nichts beworben werden, was diese Position unterläuft (z. B. „geprüft", „zertifiziert", „sicher"). Vgl. dazu die Subsumtion in Abschnitt 9.

---

## 3. Rechtsgrundlagen der Haftung im Überblick

### 3.1 Deliktische Haftung — § 823 Abs. 1 BGB

§ 823 Abs. 1 BGB verpflichtet zum Schadensersatz bei rechtswidriger, schuldhafter Verletzung eines absolut geschützten Rechtsguts. Für die VerordnungsAmpel relevant:

- **Geschütztes Rechtsgut:** Das Vermögen des Arztes ist von § 823 Abs. 1 BGB **nicht** erfasst — reine Vermögensschäden (etwa ein Regressbetrag von 50.000 EUR) sind keine Rechtsgutsverletzung im Sinne dieser Norm. Das ist das Haupttor, durch das die Mandanten-Position gehen kann.
- **Ausnahme:** Bei Körperverletzung (z. B. wenn eine falsche Regelangabe mittelbar zu einem Behandlungsfehler führt) wäre § 823 Abs. 1 BGB anwendbar — hier liegt aber keine direkte Kausalität vor, weil der Arzt Letztentscheider bleibt.

**Folgerung:** § 823 Abs. 1 BGB ist für reine Regress-Vermögensschäden regelmäßig nicht einschlägig.

### 3.2 § 823 Abs. 2 BGB i. V. m. Schutzgesetz

Schadensersatz wegen Verletzung eines Schutzgesetzes (z. B. MPDG-Vorschriften bei unterlassener CE-Kennzeichnung eines MDSW). Da das Tool nach RECHTSGUTACHTEN_MDSW.md **kein** MDSW ist, liegt kein Verstoß gegen MDR/MPDG vor, also auch keine Schutzgesetzverletzung.

### 3.3 Vertragliche Haftung — § 280 BGB i. V. m. Vertragstyp

Ein Schadensersatzanspruch aus § 280 Abs. 1 BGB setzt ein **Schuldverhältnis** voraus. Bei kostenloser Open-Source-Software auf GPL-3.0 wird nach herrschender Meinung ein **Schenkungsvertrag mit lizenzrechtlichen Elementen** konstruiert (ifrOSS; Spindler 2003; Brennecke-Kommentar 2022).

Damit greift die Sonderregel der **Schenkungshaftung nach § 521 BGB** (siehe Abschnitt 5).

### 3.4 Produkthaftung — ProdHaftG (alte Fassung)

Das deutsche Produkthaftungsgesetz in seiner derzeitigen Fassung (ProdHaftG) erfasst nach herrschender Meinung **Standardsoftware** zwar als „Produkt", aber:

- Der persönliche Anwendungsbereich greift nur bei **gewerblicher Inverkehrbringung** (§ 1 Abs. 1 ProdHaftG).
- Nach § 1 Abs. 2 Nr. 3 ProdHaftG ist Haftung ausgeschlossen, wenn der Hersteller das Produkt **nicht zum Zweck des Verkaufs oder einer anderen Form des wirtschaftlichen Vertriebs** hergestellt hat.
- **Reine Vermögensschäden** (ohne Personen- oder Sachschaden) sind nach § 1 Abs. 1 S. 1 ProdHaftG ohnehin **nicht** erfasst (vgl. Ferner-Alsdorf zur Produkthaftung und OSS).

**Folgerung für Regress-Schaden:** Das ProdHaftG (alt) greift nicht, weil (i) reiner Vermögensschaden vorliegt und (ii) Um:bruch die Software nicht wirtschaftlich vertreibt.

### 3.5 Produkthaftungs-Richtlinie (EU) 2024/2853 — neu ab 09.12.2026

Die am 18.11.2024 im Amtsblatt veröffentlichte **Richtlinie (EU) 2024/2853** (kurz „PLD 2024") erweitert den Produktbegriff ausdrücklich auf Software und KI-Systeme (Art. 4 Nr. 1 PLD 2024). Umsetzungsfrist: **09.12.2026** (Art. 22).

**Zentraler Punkt für Open Source:** Erwägungsgrund 14 und die Definition in Art. 2 nehmen **„Free and Open Source Software, die außerhalb einer gewerblichen Tätigkeit entwickelt oder bereitgestellt wird"**, aus dem Anwendungsbereich heraus. Wenn jedoch ein gewerblicher Hersteller OSS in ein gewerbliches Produkt integriert, haftet dieser zweite Hersteller weiter (Buse-Blog 2024; FPS Law 2024; Bird & Bird Update 2024; Wikipedia zu RL 2024/2853).

**Die entscheidende Frage für Um:bruch** ist daher: Wird die Bereitstellung der VerordnungsAmpel durch Um:bruch e. V. als **„gewerbliche Tätigkeit"** eingestuft?

Abschnitt 6 widmet sich dieser Frage ausführlich. Ergebnis vorweg: Bei sauberer Gestaltung (Vereinsstruktur, nicht-kommerzielle Bereitstellung, kein Verkauf, kein Service-Abo) bleibt Um:bruch in der Ausnahme. Der Prototype-Fund-Zuschuss ist keine „gewerbliche Tätigkeit" im Sinne der PLD (vgl. Knowledge Base Prototype Fund — „Verantwortung für Software und Inhalte").

### 3.6 Überblicks-Ergebnis

| Haftungsgrundlage | Greift bei Regress-Schaden? | Begründung |
|---|---|---|
| § 823 Abs. 1 BGB | **Nein** | Vermögensschaden nicht geschützt |
| § 823 Abs. 2 BGB | **Nein** | Kein Schutzgesetz verletzt (kein MDSW) |
| § 280 BGB (Vertrag) | **Eingeschränkt** | Nur Schenkung → § 521 BGB-Privileg |
| ProdHaftG (alt) | **Nein** | Kein Vertrieb, kein Personen-/Sachschaden |
| PLD 2024 (ab 09.12.2026) | **Nein, bei sauberer Gestaltung** | OSS-Ausnahme für nicht-gewerbliche Bereitstellung |

---

## 4. Haftungsausschluss in GPL-3.0 — Wirksamkeit in Deutschland

### 4.1 Die GPL-3.0-Klauseln

GPL-3.0 **Section 15 (Disclaimer of Warranty):**

> "THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. […] THE PROGRAM IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE."

GPL-3.0 **Section 16 (Limitation of Liability):**

> "IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES […]"

### 4.2 Durchsetzbarkeit der GPL in Deutschland

Die GPL als solche ist in Deutschland als Lizenzvertrag **anerkannt und durchsetzbar** (siehe Rechtsprechung seit LG München I v. 19.05.2004 — Az. 21 O 6123/04 — dem weltweit ersten GPL-Urteil; bestätigt durch LG Berlin v. 21.02.2006 — Az. 16 O 134/06; LG Hamburg 2013; LG München I v. 08.11.2021 — Az. 21 O 9576/19 zu GPL-2.0; ifrOSS-Rechtsprechungssammlung).

**Aber:** Die Durchsetzbarkeit der GPL als Ganzes impliziert **nicht** die Durchsetzbarkeit ihrer Haftungsausschluss-Klauseln.

### 4.3 Einordnung als AGB — §§ 305 ff. BGB

Die GPL-Klauseln sind **für eine Vielzahl von Verträgen vorformulierte Bedingungen** und werden damit als **Allgemeine Geschäftsbedingungen** im Sinne des § 305 Abs. 1 BGB qualifiziert (herrschende Meinung; ifrOSS „Ist der in Open Source-Lizenzen übliche Haftungs- und Gewährleistungsausschluss in Deutschland wirksam?"; Brennecke 2022; Spindler-Gutachten 2003).

Das bedeutet: Die Klauseln unterliegen der **AGB-Inhaltskontrolle** nach §§ 307–309 BGB.

### 4.4 Unwirksamkeit des pauschalen Ausschlusses

Der **pauschale Ausschluss jeglicher Haftung** in GPL Section 15/16 ist nach herrschender Meinung **unwirksam**, weil:

- **§ 309 Nr. 7 Buchst. a BGB:** Haftung für Vorsatz und grobe Fahrlässigkeit kann in AGB niemals ausgeschlossen werden.
- **§ 309 Nr. 7 Buchst. b BGB:** Haftung für Körper-, Gesundheits- und Lebensschäden kann in AGB ebenfalls nicht ausgeschlossen werden.
- **§ 307 Abs. 2 Nr. 2 BGB:** Kardinalpflichten (wesentliche Vertragspflichten) können auch bei einfacher Fahrlässigkeit nicht vollständig ausgeschlossen werden.

**Konsequenz:** Die GPL-Haftungsausschluss-Klauseln gelten in Deutschland **nur insoweit**, als sie sich innerhalb dieser AGB-rechtlichen Grenzen bewegen. Der Rest fällt weg; anstelle des unwirksamen Ausschlusses tritt das **dispositive Gesetzesrecht** (§ 306 Abs. 2 BGB).

### 4.5 Rettungsanker: Das dispositive Recht ist das Schenkungsrecht

Und genau hier liegt der **entscheidende Glückstreffer** für Open-Source-Projekte:

Das dispositive Recht für kostenlose Software ist nach herrschender Meinung das **Schenkungsrecht** — und dieses sieht in § 521 BGB ohnehin eine **Haftungsbegrenzung auf Vorsatz und grobe Fahrlässigkeit** vor. Damit kommt der GPL-Nutzer praktisch zum selben Ergebnis wie mit dem (unwirksamen) AGB-Ausschluss.

Siehe Abschnitt 5.

---

## 5. Schenkungshaftung als tragende Konstruktion — § 521 BGB

### 5.1 OSS als Schenkung

Nach nahezu einhelliger juristischer Literatur (Spindler 2003; Jaeger/Metzger „Open Source Software", 4. Aufl. 2020; ifrOSS; Brennecke 2022) ist die kostenlose Bereitstellung von Open-Source-Software rechtlich als **Schenkung** im Sinne der §§ 516 ff. BGB zu qualifizieren. Der Schenker verspricht dem Beschenkten eine unentgeltliche Zuwendung (hier: ein Nutzungsrecht an der Software).

### 5.2 § 521 BGB — Die Haftungsprivilegierung

> § 521 BGB — Haftung des Schenkers:
> „Der Schenker hat nur Vorsatz und grobe Fahrlässigkeit zu vertreten."

Das heißt für die VerordnungsAmpel:

- **Einfache Fahrlässigkeit** (z. B. versehentliche Übernahme eines veralteten AM-RL-Datensatzes) → **keine Haftung**.
- **Grobe Fahrlässigkeit** (z. B. bewusstes Ignorieren bekannter Datenfehler, Nichtausliefern eines wichtigen Sicherheits-Updates über Monate trotz Kenntnis) → **Haftung**.
- **Vorsatz** (z. B. wissentliches Falschanzeigen einer Regel) → **Haftung**.

### 5.3 § 524 BGB — Rechts- und Sachmängel

§ 524 Abs. 1 BGB geht noch weiter: Für Sach- und Rechtsmängel haftet der Schenker **nur bei Arglist** (Verschweigen eines bekannten Mangels). Eine veraltete Regel, die Um:bruch nicht kannte, ist kein Arglist-Fall.

### 5.4 Zwingende Haftungsgrenzen

Auch § 521 BGB kann aber die gesetzlich zwingenden Haftungsgrenzen nicht unterschreiten:

- **Verletzung von Leben, Körper, Gesundheit** (§ 309 Nr. 7 BGB — zwingend auch bei Schenkung)
- **Vorsatz und grobe Fahrlässigkeit** (nie ausschließbar)
- **Produkthaftung** (soweit anwendbar — aber hier nach Abschnitt 3.4/3.5 ohnehin nicht)

**Folgerung:** Um:bruch haftet gegenüber einem Nutzer, der sich auf die VerordnungsAmpel verlassen hat, regelmäßig **nur bei Vorsatz und grober Fahrlässigkeit** — weder bei einfacher Nachlässigkeit, noch bei einem fehlerhaften AM-RL-Datensatz, den das Regelwerk selbst falsch publiziert hat, noch bei einer veralteten Regel, solange man die Aktualisierungsbemühungen dokumentiert.

### 5.5 Worauf Um:bruch achten muss, um das Privileg nicht zu verlieren

- **Keine Zusicherungen geben** („zuverlässig", „umfassend geprüft", „regressfest", „garantiert aktuell") — das wäre eine Zusicherung i. S. d. § 442 BGB oder ein Übernahmeverschulden.
- **Keine Arglist:** Bekannte Datenfehler müssen öffentlich dokumentiert werden (z. B. im Bug-Tracker und im Changelog).
- **Keine grobe Fahrlässigkeit:** Update-Prozess dokumentieren (Quartals-Build aus GitHub Actions, Stand-Datum prominent angezeigt, bekannte offene Issues gelistet).
- **Keine versteckten Mängel:** Funktionale Grenzen müssen **vor der Nutzung** klar benannt werden (Disclaimer, Erststart-Acknowledgement).

---

## 6. Die neue PLD 2024/2853 — was ändert sich ab 09.12.2026?

### 6.1 Kernneuerungen

Die Richtlinie (EU) 2024/2853 (PLD 2024) ersetzt die alte Produkthaftungsrichtlinie 85/374/EWG. Zentrale Änderungen ([EUR-Lex 32024L2853](https://eur-lex.europa.eu/eli/dir/2024/2853/oj?locale=de); Wikipedia; Bird & Bird 2024; Buse-Blog 2024; FPS Law 2024):

1. **Produktbegriff erweitert** (Art. 4 Nr. 1): „Software" und „KI-Systeme" sind ausdrücklich erfasst.
2. **Komponenten** (Art. 4 Nr. 4): Auch Software-Komponenten (Bibliotheken, SaaS-Module) sind Produkte.
3. **Fehlerbegriff erweitert** (Art. 7): Cybersicherheits-Risiken, fehlende Updates und Lernverhalten von KI-Systemen können Fehler begründen.
4. **Erleichterte Beweislast** (Art. 10): Umkehrung in bestimmten Konstellationen.
5. **Umsetzungsfrist:** 09.12.2026 (Art. 22).

### 6.2 Die Open-Source-Ausnahme

**Erwägungsgrund 14 PLD 2024** und die Betrachtung in Art. 2:

> Die Richtlinie gilt **nicht** für „freie und quelloffene Software, die **außerhalb einer gewerblichen Tätigkeit** entwickelt oder bereitgestellt wird".

Das Ziel: Innovation und Forschung nicht zu behindern.

### 6.3 Was ist „gewerbliche Tätigkeit"?

Erwägungsgrund 14 präzisiert: Eine gewerbliche Tätigkeit liegt vor, wenn:

- **Entgelt verlangt wird** (Kaufpreis, Abonnement, Wartungsgebühr),
- **persönliche Daten für andere Zwecke als Sicherheit/Interoperabilität** verwendet werden (z. B. Werbung),
- **die Software als Teil eines gewerblichen Dienstes bereitgestellt wird** (z. B. SaaS mit Verkaufscharakter).

**Nicht** gewerblich ist dagegen:

- Bereitstellung durch eine gemeinnützige Organisation (Verein, Stiftung, Universität),
- rein spendenfinanzierte oder öffentlich geförderte Projekte (Prototype Fund, EU-Förderprogramme),
- hobbyistische / forschende Entwicklung,
- Bereitstellung als reine Quellcode-Veröffentlichung auf GitHub ohne Vertriebskanal.

### 6.4 Anwendung auf Um:bruch / VerordnungsAmpel

| Merkmal | Projekt-Status | Ergebnis |
|---|---|---|
| Rechtsform | Um:bruch e. V. (gemeinnützig, geplant) | Nicht-gewerblich |
| Preis | Kostenlos (GPL-3.0) | Nicht-gewerblich |
| Finanzierung | Prototype Fund (Zuschuss) + Spenden | Nicht-gewerblich (vgl. Erwägungsgrund 14) |
| Datenverarbeitung | Nur ICD/ATC-Codes, keine Personendaten | Nicht-gewerblich |
| Vertriebsweg | GitHub, eigene Website | Nicht-gewerblich |
| Service / Wartung | Rein freiwillig, keine SLA | Nicht-gewerblich |

**Folgerung:** Die VerordnungsAmpel fällt bei aktueller Projektgestaltung **in die OSS-Ausnahme der PLD 2024**. Die Haftung nach nationalem Umsetzungsrecht bleibt auf das Schenkungsrecht (§ 521 BGB) beschränkt.

### 6.5 Risiken die beibehalten werden müssen

Die OSS-Ausnahme würde **entfallen**, wenn Um:bruch (oder ein Kooperationspartner):

- ein **kommerzielles Service-Angebot** um die Software baut (SaaS-Hosting gegen Entgelt, Support-Abo),
- das Tool in ein **kommerzielles PVS** integriert (dann haftet der PVS-Hersteller),
- **personenbezogene Daten zu Werbezwecken** verarbeitet (aktuell nicht der Fall),
- den Status e. V./gUG aufgibt und zur gewerblichen GmbH mutiert.

### 6.6 Zwischenergebnis zur PLD 2024

Die PLD 2024 ist **gut** für nicht-gewerbliche Open-Source-Projekte — sie **bestätigt** sogar deren Sonderstellung auf EU-Ebene. Voraussetzung: Um:bruch bewahrt seinen nicht-gewerblichen Status.

Siehe Abschnitt 11 für die Empfehlung, bei der Vereinsgründung (e. V. oder gUG) diesen Status bewusst zu wählen.

---

## 7. Instruktionspflichten — Stand-Datum, Update-Hinweise, Disclaimer

### 7.1 Rechtsgrundlage

Auch der Schenker einer Software ist nach der allgemeinen Verkehrssicherungspflicht und nach § 241 Abs. 2 BGB (Rücksichtnahmepflicht) verpflichtet, den Beschenkten auf **offensichtliche Gefahren** hinzuweisen. Bei medizinnaher Software sind das:

- **Stand der Datenbasis** (AM-RL-Anlagen, PRISCUS, Praxisbesonderheiten-Liste) — Datum und Version
- **Abdeckungsgrenzen** (welche Regeln werden abgebildet, welche nicht?)
- **Bekannte Fehler** (offene Bug-Reports)
- **Aktualisierungshinweis** (wie oft wird aktualisiert? Wer haftet für Verzögerungen?)

### 7.2 Wo müssen die Hinweise stehen?

Die Hinweise müssen **so platziert sein, dass ein verständiger Nutzer sie nicht übersehen kann**. Nach § 305 Abs. 2 BGB gilt das auch für die Einbeziehung der GPL-Klauseln. Für die Haftungslage bedeutet das:

| Kanal | Mindestinhalt |
|---|---|
| **README.md** | Großer Disclaimer-Block, Stand-Datum, Quellenliste, GPL-Verweis |
| **LICENSE-Datei** | Originale GPL-3.0 + deutschsprachiger Zusatz („Hinweis zum deutschen Recht") |
| **GUI-Startscreen (Erstnutzung)** | Modaler Dialog mit Disclaimer, Button „Ich habe gelesen und verstanden", Pflicht-Checkbox |
| **GUI-Dauerhaft sichtbar** | Statuszeile mit Stand-Datum der Regelwerke und Versionsnummer |
| **Jede Ampel-Ausgabe** | Fußzeile „Stand der Regelwerke: YYYY-MM-DD. Ärztliche Letztverantwortung unverändert." |
| **Compliance-Log-Eintrag** | Automatisch: Stand-Datum + Disclaimer-Bestätigung beim Erststart versiegelt |
| **Impressum (Website)** | Kontakt Um:bruch, Hinweis auf Nicht-Kommerzialität, GPL-Verweis |

Siehe Abschnitt 10 für konkrete Textbausteine.

### 7.3 Veraltete Regelwerke — Haftungsfrage

**Szenario:** Der Arzt verlässt sich am 15.09.2026 auf eine Ampel-Auskunft, die auf AM-RL-Anlage III Stand 01.06.2026 basiert. Zwischen 01.06. und 15.09. hat der G-BA die Regel geändert. Regress läuft.

| Bedingung | Haftung Um:bruch? |
|---|---|
| Stand-Datum war prominent sichtbar, Arzt ignoriert es | **Keine Haftung** — Eigenverantwortung |
| Stand-Datum versteckt, Tool suggeriert Aktualität | **Haftung möglich** (Arglist/Zusicherung) |
| Quartalsbuild-Prozess dokumentiert, Verzögerung dokumentiert | **Keine Haftung** — kein grober Fahrlässigkeitsvorwurf |
| Um:bruch wusste von der Änderung und hat sie verschwiegen | **Haftung** (§ 524 BGB Arglist) |

**Faustregel:** Das Tool muss den **Zustand seiner Wissensbasis** so transparent kommunizieren, dass der Arzt eine **eigenverantwortliche Entscheidung** treffen kann, ob er sich darauf verlässt.

### 7.4 Konkrete Anforderungen

1. **Stand-Datum** pro Regelwerk, nicht nur global. Beispiel: „AM-RL Anlage III: 01.06.2026. PRISCUS 2.0: 2023. GKV-SV Praxisbesonderheiten: Q2/2026."
2. **Änderungshistorie** öffentlich (GitHub Releases + CHANGELOG.md).
3. **Bekannte offene Issues** sichtbar verlinkt (GitHub Issues, Label „data-quality").
4. **Update-Benachrichtigung:** Wenn Tool > 90 Tage ohne Update läuft, prominenter Hinweis „Datenbasis möglicherweise veraltet, bitte Update durchführen".
5. **Keine Push-Automatik** — der Arzt entscheidet, ob er ein Update einspielt.

---

## 8. Restverantwortung des Arztes — Facharztstandard und § 76 SGB V

### 8.1 § 630a Abs. 2 BGB — Behandlungsvertrag

> „Die Behandlung hat nach den zum Zeitpunkt der Behandlung bestehenden, allgemein anerkannten fachlichen Standards zu erfolgen, soweit nicht etwas anderes vereinbart ist."

Der Facharztstandard ist **objektiv** zu bestimmen (BGH ständige Rechtsprechung; zuletzt BGH v. 06.05.2008 — Az. VI ZR 64/07 für Allgemeinmediziner; BGH v. 15.06.1993 — Az. VI ZR 175/92). Der Arzt kann sich nicht auf subjektive Gründe, auf Zeitdruck oder auf fremde Informationsquellen berufen, um von diesem Standard abzuweichen.

### 8.2 § 76 SGB V — Freie Arztwahl und Verordnungsverantwortung

§ 76 SGB V regelt formell die freie Arztwahl des Versicherten. In der Sozialrechtsprechung ist daraus aber auch die **eigenverantwortliche Verordnung** des Vertragsarztes abgeleitet. Der Vertragsarzt ist **persönlich** für jede Verordnung verantwortlich (zuletzt BSG v. 11.05.2011 — Az. B 6 KA 13/10 R zum Stempel-statt-Unterschrift-Regress; bestätigt in der aktuellen Rechtsprechung zu § 106 SGB V-Verfahren).

**Zentrale Aussage:** Der Arzt kann sich im Regressprozess **nicht auf fremde Software** berufen, um einer Regressforderung zu entgehen. Das BSG hat in ständiger Rechtsprechung klargestellt, dass der Vertragsarzt **persönlich** die Verordnung zu prüfen und zu verantworten hat (vgl. auch SG Marburg v. 14.02.2024 — Az. S 18 KA 96/23 zur Dokumentationspflicht zum Zeitpunkt der Verordnung).

### 8.3 Einsatz medizinischer Software — neue Rechtsprechung

Die aufkommende KI-in-der-Medizin-Rechtsprechung (vgl. BMC-Primary-Care-Literatur 2024; BDI-Positionspapier „Medizinischer Fortschritt versus haftungsrechtliche Fragen", 2024) formuliert den Grundsatz:

> „Der Fehler eines KI- oder Software-Systems führt nicht automatisch zu einer Haftung des Arztes. Eine Pflichtverletzung liegt nur vor, wenn das System unsachgemäß ausgewählt, bedient oder überwacht wurde."

Spiegelbildlich gilt: Die Nutzung einer Software **entlässt den Arzt nicht aus seiner Pflicht zur eigenen Prüfung**. Die Software ist **Werkzeug**, nicht **Entscheider**.

### 8.4 Folgerung für Um:bruch

Der Arzt bleibt in jedem Regressprozess **Letztverantwortlicher**:

1. Er gibt ICD und ATC selbst ein (keine automatische Codierung durch das Tool).
2. Er entscheidet, ob er der Ampel-Auskunft folgt oder nicht.
3. Er ist für das Einholen aktueller Informationen (KV-Rundschreiben, G-BA-Bekanntmachungen, Fachinformationen) zuständig.
4. Er ist für die Vollständigkeit seiner Dokumentation verantwortlich.

Die VerordnungsAmpel ist ausdrücklich als **Companion-Tool** konzipiert (siehe KONZEPT.md Abschnitt „Worum geht es?"). Sie **ersetzt** kein ärztliches Urteil, sie unterstützt es.

**Für die Haftungsabwehr ist genau diese Rollenklarheit das stärkste Argument.**

---

## 9. Analyse: Ist die Mandanten-Position tragfähig?

### 9.1 Die Position im Check

> „Nicht getestet. Ärzte sind selbst verantwortlich. Externe Prüfungen werden angestrebt. Nutzung auf eigenes Risiko."

| Teilaussage | Tragfähig? | Caveat |
|---|---|---|
| „Nicht getestet" | **Ja, entlastend.** Ausschluss von Zusicherungen (§ 442, § 444 BGB). | Muss überall sichtbar sein, nicht nur im Impressum. |
| „Ärzte sind selbst verantwortlich" | **Ja, gesetzlich gestützt.** § 630a BGB, § 76 SGB V, BSG-Rspr. | Darf nicht so formuliert werden, dass der Disclaimer „überrascht" (§ 305c BGB). |
| „Externe Prüfungen angestrebt" | **Ja, ehrlich.** Keine Zusicherung, keine Irreführung. | „Angestrebt" ≠ „in Vorbereitung" ≠ „abgeschlossen". Wording genau halten. |
| „Nutzung auf eigenes Risiko" | **Ja, als Klarstellung.** In Verbindung mit § 521 BGB tragend. | Pauschaler Haftungsausschluss in AGB unwirksam — Privileg kommt aus dem Schenkungsrecht, nicht aus der Klausel. |

### 9.2 Gesamturteil

Die Mandanten-Position ist **rechtlich tragfähig**, **unter vier Voraussetzungen**:

1. **Die nicht-gewerbliche Struktur wird gewahrt** (e. V., kein Verkauf, kein SaaS-Abo, kein Werbe-Daten-Geschäft). → Schützt § 521 BGB und die PLD-2024-Ausnahme.
2. **Die Zweckbestimmung bleibt ein Nachschlagewerk** (siehe RECHTSGUTACHTEN_MDSW.md, Abschnitt 2.6, 3.2). → Keine MDSW, kein MPDG-Verstoß.
3. **Die Disclaimer werden an allen relevanten Stellen sichtbar und technisch verpflichtend** platziert (Erststart-Acknowledgement, Dauerhafte GUI-Statuszeile, README, LICENSE-Zusatz, Impressum). → Beweisbarkeit im Streitfall.
4. **Keine werbliche Übersteigerung** — Um:bruch vermeidet jegliche Formulierung, die eine Zusicherung begründen könnte (z. B. „zuverlässig", „regressfest", „geprüft", „zertifiziert", „sicher"). → Kein § 444 BGB (Zusicherung), keine Arglist.

### 9.3 Wo die Position **nicht** trägt

- **Vorsatz und grobe Fahrlässigkeit** sind nie ausschließbar. Beispiele:
  - Um:bruch weiß von einem schwerwiegenden Datenfehler und veröffentlicht kein Hotfix über 60 Tage → grobe Fahrlässigkeit.
  - Ein Mitarbeiter manipuliert bewusst die Ampel-Ausgabe (intern oder per PR) → Vorsatz.
- **Verletzung von Leben/Körper/Gesundheit** ist zwingend haftbar. → Nicht im Regress-Szenario relevant, aber theoretisch: Wenn eine Falschangabe zur Therapieentscheidung führte und Patient geschädigt würde.
- **Schutzgesetzverletzungen** (z. B. wenn Tool gegen den eigenen Willen in den MDSW-Bereich rutscht und ungeahndet in Verkehr gebracht wird → § 823 Abs. 2 BGB i. V. m. MDR/MPDG).

### 9.4 Restrisiko-Einschätzung

| Szenario | Risiko | Abhilfe |
|---|---|---|
| Arzt verliert Regress, klagt gegen Um:bruch auf Schadensersatz | **Gering**, bei korrekten Disclaimern | Abschnitt 10 umsetzen |
| Arzt klagt, behauptet Zusicherung durch Werbematerial | **Mittel**, wenn Werbung zu offensiv | Wording-Check durch RB vor jedem Release |
| Patient geschädigt durch falsche Ampel-Auskunft | **Sehr gering** (Tool gibt keine Therapie-Empfehlung) | MDSW-Ausschluss behalten (RECHTSGUTACHTEN_MDSW.md) |
| BSG sieht in Zukunft erhöhte Sorgfaltspflicht für Software-Nutzer | **Offen**, abhängig von Rechtsprechung | Rechtsprechungsmonitoring in Policies verankern |
| Konkurrent-PVS verklagt Um:bruch wegen „Irreführung" | **Gering** (UWG) | Werbung bleibt sachlich |

**Gesamtrisiko bei sauberer Umsetzung: Gering.**

---

## 10. Konkrete Textbausteine

### 10.1 README.md — Hauptbaustein

```markdown
## ⚠️ Wichtiger Hinweis (Disclaimer)

Die VerordnungsAmpel ist ein **nicht getestetes, nicht zertifiziertes,
nicht klinisch validiertes** Informationswerkzeug. Externe Prüfungen
sind angestrebt, aber nicht abgeschlossen.

**Das Tool ersetzt keinesfalls:**
- die ärztliche Prüfung der Indikation,
- die Dokumentationspflicht nach § 630f BGB,
- die Verordnungsverantwortung nach § 76 SGB V,
- die Kenntnis aktueller G-BA-Beschlüsse, KV-Rundschreiben und
  Fachinformationen.

**Nutzung auf eigenes Risiko.** Die ärztliche Letztverantwortung
bleibt uneingeschränkt bestehen. Für Regress-Schäden, die aus der
Nutzung des Tools entstehen, haftet Um:bruch e. V. gemäß § 521 BGB
nur bei Vorsatz und grober Fahrlässigkeit.

**Stand der Regelwerke:** siehe GUI-Statuszeile und CHANGELOG.md.

**Lizenz:** GNU General Public License Version 3.0 (GPL-3.0).
Haftungsausschluss gemäß Sections 15 und 16 GPL-3.0, in Deutschland
ergänzt durch § 521 BGB.
```

### 10.2 GUI — Startscreen (Erstnutzung)

```
┌────────────────────────────────────────────────────┐
│ WILLKOMMEN BEI DER VERORDNUNGSAMPEL                │
│                                                    │
│ Bevor Sie das Tool benutzen, bestätigen Sie bitte: │
│                                                    │
│ ☐ Ich verstehe, dass dieses Tool NICHT klinisch    │
│   getestet oder zertifiziert ist.                  │
│                                                    │
│ ☐ Ich verstehe, dass die ärztliche Letzt-          │
│   verantwortung bei mir liegt.                     │
│                                                    │
│ ☐ Ich verstehe, dass dieses Tool KEINE Therapie-   │
│   empfehlung gibt, sondern nur öffentlich verfüg-  │
│   bare Regelwerke abbildet.                        │
│                                                    │
│ ☐ Ich nutze das Tool auf eigenes Risiko.           │
│                                                    │
│            [ Abbrechen ]   [ Bestätigen ]          │
└────────────────────────────────────────────────────┘
```

Nach Bestätigung: Compliance-Log-Eintrag mit Timestamp, Benutzerkennzeichen, Disclaimer-Version-Hash.

### 10.3 GUI — Dauerhafte Statuszeile

```
┌─────────────────────────────────────────────────────────────┐
│ Stand der Regelwerke: 2026-04-08  |  Version 0.5.0          │
│ ⚠ Nicht getestet. Nutzung auf eigenes Risiko.               │
│ [ Regelwerke prüfen ] [ Update suchen ] [ Disclaimer ]      │
└─────────────────────────────────────────────────────────────┘
```

### 10.4 GUI — Ampel-Ausgabe-Fußzeile

```
─────────────────────────────────────────────────────────
Diese Ausgabe ist eine strukturierte Suche in öffent-
lichen Regelwerken (AM-RL, PRISCUS, BMV-Ä, § 31 SGB V).
Sie ist KEINE Therapieempfehlung und ersetzt NICHT die
ärztliche Entscheidung.
Stand: 2026-04-08. Nutzung auf eigenes Risiko.
─────────────────────────────────────────────────────────
```

### 10.5 LICENSE-Zusatz (NOTICE.md oder LICENSE_DE.md)

```markdown
## Hinweis zum deutschen Recht (in Ergänzung zur GPL-3.0)

Diese Software wird gemäß GNU General Public License Version 3.0
(GPL-3.0) bereitgestellt. Die in Section 15 („Disclaimer of Warranty")
und Section 16 („Limitation of Liability") vorgesehenen pauschalen
Haftungsausschlüsse sind nach deutschem AGB-Recht (§§ 305 ff. BGB)
in Teilen unwirksam.

An ihre Stelle tritt das dispositive Schenkungsrecht der §§ 516 ff.
BGB. Gemäß § 521 BGB haftet der Schenker dem Empfänger gegenüber
NUR für Vorsatz und grobe Fahrlässigkeit. Für Sach- und Rechtsmängel
haftet der Schenker gemäß § 524 BGB nur, wenn er einen Mangel arglistig
verschweigt.

Die ärztliche Letztverantwortung nach § 630a Abs. 2 BGB und § 76 SGB V
bleibt durch die Nutzung dieser Software unberührt. Die Software ist
kein Medizinprodukt im Sinne der Verordnung (EU) 2017/745 und keine
Therapieempfehlung.

Um:bruch e. V., Stand: 2026-04-12
```

### 10.6 Impressum (Website)

```markdown
Anbieter:
Um:bruch e. V. (i. G.)
[Adresse einsetzen]

Kontakt: hallo@um-bruch.org

Die VerordnungsAmpel wird ohne Gewinnerzielungsabsicht entwickelt und
kostenfrei bereitgestellt. Die Software ist Open Source (GPL-3.0) und
wird als nicht-gewerbliches Forschungs- und Dokumentationswerkzeug
bereitgestellt.

Die Software ist kein Medizinprodukt (vgl. Rechtsgutachten vom
12.04.2026, verfügbar unter [Link]). Sie ersetzt keine ärztliche
Entscheidung. Die Nutzung erfolgt auf eigenes Risiko.
Haftung nur bei Vorsatz und grober Fahrlässigkeit (§ 521 BGB).
```

### 10.7 Compliance-Log — Erststart-Eintrag

```json
{
  "event": "first_start_acknowledgement",
  "timestamp": "2026-04-12T15:23:41Z",
  "user_hash": "sha256:<...>",
  "disclaimer_version": "1.0",
  "disclaimer_hash": "sha256:<...>",
  "acknowledgements": [
    "not_tested",
    "not_certified",
    "doctor_responsibility",
    "no_therapy_recommendation",
    "use_at_own_risk"
  ],
  "tool_version": "0.5.0",
  "rule_data_stand": {
    "amrl_anlage_iii": "2026-04-01",
    "amrl_anlage_v": "2026-04-01",
    "amrl_anlage_vi": "2026-04-01",
    "priscus_2": "2023",
    "gkv_sv_praxisbesonderheiten": "2026-Q1"
  }
}
```

Dieser Eintrag ist Teil der Hash-Chain und beweisbar. Im Streitfall zeigt er, dass der Nutzer die Disclaimer gesehen und bestätigt hat.

---

## 11. Versicherungsempfehlung und Organisationsform

### 11.1 Haftpflichtversicherung

Auch wenn die Rechtslage für Um:bruch günstig ist, bleibt ein **Restrisiko**:

- Prozesskosten bei (erfolgreicher) Abwehr einer Klage
- Individualisiertes Kulanzrisiko
- Reputationsverluste bei öffentlichem Verfahren

**Empfehlung:** Abschluss einer **Betriebs- und Berufshaftpflichtversicherung für gemeinnützige Organisationen** mit expliziter Einschlussklausel für „Software- und Datenrisiken" (IT-Haftpflicht-Baustein).

**Marktanbieter (Stand 2026):** Hiscox Vereinshaftpflicht, Gothaer NPO-Schutz, exali IT-Haftpflicht (für Open-Source-Projekte verfügbar). Kostenrahmen: ca. 300–900 EUR / Jahr für eine Grunddeckung von 1 Mio. EUR.

**Wichtig beim Abschluss:** Im Fragebogen explizit angeben:
- Open-Source-Bereitstellung
- Nicht-gewerblich, Verein
- Zielgruppe Mediziner (Risikoerhöhung kann zu Aufschlag führen)
- Keine klinische Anwendung / kein CE-Kennzeichen

### 11.2 Rechtsform — eingetragener Verein (e. V.) vs. gUG

**Empfehlung:** Gründung als **eingetragener Verein (e. V.) mit Gemeinnützigkeitsanerkennung** (§§ 51 ff. AO).

**Vorteile:**
- Vereinshaftung (§ 31 BGB) statt persönlicher Haftung der Mitglieder
- OSS-Ausnahme der PLD 2024 greift klar (nicht-gewerbliche Organisation)
- Prototype Fund und andere Förderer bevorzugen gemeinnützige Träger
- Spendenquittungen möglich

**Alternative: gemeinnützige Unternehmergesellschaft (gUG)**:
- Haftungsbeschränkung auf das Vereinsvermögen
- Flexibler als e. V.
- Aber: Kann unter Umständen als „gewerblich" interpretiert werden — juristische Klärung nötig vor Wahl

**Persönliche Haftung des Vorstandes** bleibt in beiden Fällen bei grober Sorgfaltspflichtverletzung bestehen. Deshalb zusätzlich:

**D&O-Versicherung** (Directors and Officers Liability) für Vorstandsmitglieder bei Vereinsgründung. Ca. 200–500 EUR / Jahr für kleine Vereine.

### 11.3 Was Um:bruch NICHT tun sollte

- **GmbH-Gründung:** Wird als gewerblich eingestuft → PLD-2024-Ausnahme entfällt, § 521 BGB-Privileg ggf. ebenfalls (Schenkungscharakter schwieriger zu begründen).
- **SaaS-Angebot:** Macht Um:bruch zum gewerblichen Dienstleister.
- **Support-Abos:** Macht Um:bruch zum gewerblichen Dienstleister.
- **Werbefinanzierung:** Gleiches Risiko, außerdem DSGVO-sensitiv.

---

## 12. Grenzen dieser Einschätzung und Anwaltsempfehlung

### 12.1 KI-basierte Erstanalyse

Dieses Gutachten wurde von Claude (KI) als Rechtsbeauftragter (RB) der Um:bruch-Rechtsabteilung erstellt. Es ist eine **strukturierte Erstanalyse** auf Basis öffentlich zugänglicher Rechtsquellen, einschließlich Gesetzestexten, Rechtsprechung und Fachliteratur.

**Dieses Gutachten ersetzt keine anwaltliche Beratung.**

### 12.2 Wann ein Anwalt einzuschalten ist

Gemäß `C:\Users\User\OneDrive\.UMBRUCH\Policies\RECHTSABTEILUNG.md` ist ein Fachanwalt zwingend hinzuzuziehen bei:

| Auslöser | Fachgebiet |
|---|---|
| **Vor der Vereinsgründung** | Vereins-/Gemeinnützigkeitsrecht |
| **Vor erster öffentlicher Release / Pilot** (2. Halbjahr 2026) | Medizinprodukt-/Softwarerecht, IT-Haftung |
| **Vor Abschluss der Haftpflichtversicherung** (Fragebogen-Check) | Versicherungsrecht (optional) |
| **Bei Umsetzung der PLD 2024 ins deutsche Recht** (vor 09.12.2026) | Produkthaftungsrecht |
| **Bei jeder Abmahnung oder Klage** | Je nach Art (Eskalationsverfahren siehe Policies/RECHTSABTEILUNG.md) |

**Empfohlene Anwaltskanzleien für Open-Source/IT:**
- JBB Rechtsanwälte (spezialisiert auf OSS; vertreten Welte et al.)
- Jaeger/Metzger (GRUR-Experten, OSS-Recht)
- ifrOSS (Institut für Rechtsfragen der Freien und Open Source Software) — Gutachten und Beratung

### 12.3 Unsicherheiten in dieser Einschätzung

- **PLD 2024 ist noch nicht in nationales Recht umgesetzt.** Die exakte Fassung des deutschen Umsetzungsgesetzes (voraussichtlich Änderung des ProdHaftG) liegt zum Stand 12.04.2026 noch nicht vor. Erste Referentenentwürfe werden für H2/2026 erwartet.
- **Rechtsprechung zu Decision-Support-Tools außerhalb von MDSW** ist in Deutschland noch dünn. Der Facharztstandard-Anker ist solide, aber Details zur Nutzer-Sorgfalt beim Software-Einsatz werden in den nächsten 3–5 Jahren durch neue Urteile präzisiert werden.
- **„Commercial activity" im PLD-Sinne** ist ein neuer Rechtsbegriff — seine Abgrenzung wird durch den EuGH in den kommenden Jahren präzisiert werden.

### 12.4 Diese Einschätzung ist eine KI-basierte Erstanalyse

> „Diese Einschätzung ist eine KI-basierte Erstanalyse und ersetzt
>   keine anwaltliche Beratung. Die Risikoeinschätzung für das
>   Szenario (Regress-Schaden beim Arzt) ist: **GERING** bei
>   korrekter Umsetzung der Empfehlungen in Abschnitten 10 und 11.
>   Bei nächstem Release / Pilot-Phase wird die Einschaltung eines
>   Fachanwalts für Medizinprodukt-/IT-Recht empfohlen."

---

## 13. Quellenverzeichnis

### Gesetze und Richtlinien

- **BGB** — Bürgerliches Gesetzbuch, insbesondere §§ 241, 280, 305–310, 442, 444, 516–524 (Schenkung), 521 (Haftung des Schenkers), 630a–630h (Behandlungsvertrag), 823
  Fundstelle: [gesetze-im-internet.de/bgb](https://www.gesetze-im-internet.de/bgb/)
- **SGB V** — Sozialgesetzbuch Fünftes Buch, insbesondere §§ 31, 73, 76, 106
  Fundstelle: [gesetze-im-internet.de/sgb_5](https://www.gesetze-im-internet.de/sgb_5/)
- **ProdHaftG** — Produkthaftungsgesetz
  Fundstelle: [gesetze-im-internet.de/prodhaftg](https://www.gesetze-im-internet.de/prodhaftg/)
- **Richtlinie (EU) 2024/2853** — EU-Produkthaftungsrichtlinie (PLD 2024), Amtsblatt L 2024/2853 v. 18.11.2024, Umsetzungsfrist 09.12.2026
  Fundstelle: [eur-lex.europa.eu/eli/dir/2024/2853](https://eur-lex.europa.eu/eli/dir/2024/2853/oj?locale=de)
- **MDR** — Verordnung (EU) 2017/745
- **GPL-3.0** — GNU General Public License Version 3.0
  Fundstelle: [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

### Rechtsprechung

- **LG München I v. 19.05.2004 — Az. 21 O 6123/04** (GPL-Durchsetzbarkeit — weltweit erstes GPL-Urteil)
  Fundstelle: [dejure.org](https://dejure.org/dienste/vernetzung/rechtsprechung?Gericht=LG+M%C3%BCnchen+I&Datum=2004-05-19&Aktenzeichen=21+O+6123/04); [medienrecht-urheberrecht.de](https://www.medienrecht-urheberrecht.de/19-it-softwarerecht/181-lg-muenchen-gpl-lizenz-wirksam.html)
- **LG Berlin Beschl. v. 21.02.2006 — Az. 16 O 134/06** (GPL-Durchsetzbarkeit)
  Fundstelle: [ifross.org](https://www.ifross.org/artikel/entscheidung-des-lg-berlin-bestaetigt-durchsetzbarkeit-gpl)
- **EuGH Urt. v. 07.12.2017 — Rs. C-329/16 (Snitem/Philips France)** (Softwareabgrenzung Medizinprodukt)
- **BGH Urt. v. 28.05.2021 — V ZR 24/20** (§ 444 BGB, Haftungsausschluss und Arglist)
  Fundstelle: [lorenz.userweb.mwn.de](https://lorenz.userweb.mwn.de/urteile/vzr24_20.htm)
- **BGH Urt. v. 06.05.2008 — VI ZR 64/07** (Facharztstandard Allgemeinmediziner)
- **BGH Urt. v. 15.06.1993 — VI ZR 175/92** (Objektiver Facharztstandard)
- **BSG Urt. v. 11.05.2011 — B 6 KA 13/10 R** (Stempel-statt-Unterschrift, Vertragsarzt-Verantwortung)
  Fundstelle: [jura.cc Rechtstipps](https://www.jura.cc/rechtstipps/stempel-statt-unterschrift-bsg-bestaetigt-490-000-e-regress-fuer-vertragsarzt/)
- **SG Marburg Urt. v. 14.02.2024 — S 18 KA 96/23** (Dokumentation zum Zeitpunkt der Verordnung)
- **LSG BW 15.11.2023** (Praxisbesonderheiten im Verwaltungsverfahren)

### Fachliteratur

- **ifrOSS (Institut für Rechtsfragen der Freien und Open Source Software):** „Ist der in Open Source-Lizenzen übliche Haftungs- und Gewährleistungsausschluss in Deutschland wirksam?"
  Fundstelle: [ifross.org](https://ifross.org/open-source-lizenzen-uebliche-haftungs-und-gewaehrleistungsausschluss-deutschland-wirksam)
- **Spindler, G.:** „Rechtsfragen der Open Source Software" (Studie für VSI, 2003)
  Fundstelle: [uni-goettingen.de](https://www.uni-goettingen.de/de/document/download/035cb3109455169625e840892422916e.pdf/studie_final.pdf)
- **Jaeger/Metzger:** „Open Source Software", 4. Auflage 2020, C. H. Beck
- **Brennecke Rechtsanwälte:** „Open Source Einführung Teil 3 — Haftungsrisiken und Lizenz"
  Fundstelle: [brennecke-rechtsanwaelte.de](https://www.brennecke-rechtsanwaelte.de/Open-Source-Einfuehrung-Teil-3-Haftungsrisiken-und-Lizenzmodelle_13829)
- **Bird & Bird:** „Update: Reform der Produkthaftung beschlossen — Neue Haftungs- und Prozessrisiken für Unternehmen!" (2024)
  Fundstelle: [twobirds.com](https://www.twobirds.com/de/insights/2024/germany/update-reform-der-produkthaftung-beschlossen)
- **Buse Heberer Fromm:** „Was sich durch die neue EU Produkthaftungsrichtlinie (EU) 2024/2853 ändert" (2024)
  Fundstelle: [buse.de](https://buse.de/blog/handelsrecht/aenderung-eu-produkthaftungsrichtlinie-eu-2024-2853/)
- **FPS Law:** „Die neue EU-Produkthaftungsrichtlinie — Risiken (auch) für Softwarehersteller" (2024)
  Fundstelle: [fps-law.de](https://fps-law.de/de/fps-blog/die-neue-eu-produkthaftungsrichtlinie-risiken-auch-fuer-softwarehersteller)
- **Loschelder Leisenberg:** „Neue EU-Produkthaftungsrichtlinie (EG) 2024/2853: Alles, was Sie wissen müssen"
  Fundstelle: [ll-ip.com](https://ll-ip.com/aktuelles/eu-produkthaftungsrichtlinie-2024-2853-anwalt-de/)
- **Ferner, J.:** „Produkthaftung und Open-Source-Software"
  Fundstelle: [ferner-alsdorf.de](https://www.ferner-alsdorf.de/produkthaftung-und-open-source-software/)
- **Prototype Fund Knowledge Base:** „Verantwortung für Software und Inhalte"
  Fundstelle: [kb.prototypefund.de](https://kb.prototypefund.de/books/rechtliche-grundlagen/page/verantwortung-fur-software-und-inhalte)
- **Exali:** „Open Source Software: Wann haften Entwickler?"
  Fundstelle: [exali.de](https://www.exali.de/Info-Base/open-source-sicherheitsrisiken)
- **BDI:** „Medizinischer Fortschritt versus haftungsrechtliche Fragen für Ärztinnen und Ärzte" (2024)
  Fundstelle: [bdi.de](https://www.bdi.de/politik-und-presse/nachrichten/meldung/medizinischer-fortschritt-versus-haftungsrechtliche-fragen-fuer-aerztinnen-und-aerzte/)
- **Deutsche Ärzteversicherung:** „Berufshaftpflicht mit Regress-Schutz für angestellte Ärzte"
  Fundstelle: [aerzteversicherung.de](https://www.aerzteversicherung.de/Produkte/Berufshaftpflicht/Regress-Schutz)
- **Therapiefreiheit für Ärzte e. V.:** „BSG-Entscheidung zu Differenzkosten: Steigende Regressgefahr"
  Fundstelle: [therapiefreiheit.org](https://therapiefreiheit.org/bsg-entscheidung-zu-differenzkosten-steigende-regressgefahr-wie-schuetzen-sie-ihre-praxis/)

### Interne Dokumente

- `RECHTSGUTACHTEN_MDSW.md` (2026-04-12) — Hauptgutachten
- `DSGVO_KONZEPT.md` (Projektintern)
- `KONZEPT.md` (v1, 2026-04-08)
- `C:\Users\User\OneDrive\.UMBRUCH\Policies\RECHTSABTEILUNG.md`

---

**Abgelegt unter:** `docs/legal/RECHTSGUTACHTEN_HAFTUNG.md`
**Version:** 1.0
**Autor:** Claude (CL), Um:bruch Rechtsabteilung
**Datum:** 2026-04-12
