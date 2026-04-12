# Rechtliche Prüfung — VerordnungsAmpel_SOCIAL als Medical Device Software (MDSW)?

**Datum:** 2026-04-12
**RB:** Claude (CL), Um:bruch Rechtsabteilung
**Typ:** Anlassprüfung / Gutachten auf Vorab-Anfrage
**Auftrag:** Lukas Geiger (Projekt-Initiator VerordnungsAmpel_SOCIAL), 2026-04-12
**Status:** KI-basierte Erstanalyse — kein Anwaltsersatz (siehe Abschnitt 4)

---

## 1. Gegenstand

Geprüft wird, ob das Software-Projekt **VerordnungsAmpel_SOCIAL** rechtlich als

- **(A) „Informationswerk" / Nachschlagewerk**
  (vergleichbar mit einem gedruckten Praxis-Handbuch, einem öffentlichen Wikipedia-Artikel, der AM-RL-Anlage als PDF oder einer statischen Web-Suche über AM-RL-Paragraphen),

ODER als

- **(B) Medical Device Software (MDSW)** im Sinne des Art. 2 Nr. 1 i. V. m. Erwägungsgrund 19 der Verordnung (EU) 2017/745 (Medical Device Regulation, MDR),

einzuordnen ist.

### 1.1 Prüfgegenstand (Sachverhalt)

Die VerordnungsAmpel (Stand MVP 2026-04-08, Referenz `KONZEPT.md` v1) ist als browserbasiertes Companion-Tool für niedergelassene Vertragsärztinnen und Vertragsärzte in Deutschland konzipiert. Die relevanten Features aus juristischer Sicht:

| Feature | Input | Verarbeitung | Output |
|---|---|---|---|
| **Ampel-Plausibilitätsprüfung** | ICD-10-GM-Code + ATC-Code, optional Alter | Abgleich gegen AM-RL Anlagen III/V/VI, PRISCUS 2.0 (bei Alter > 65), GKV-SV-Praxisbesonderheiten-Liste, § 31 Abs. 6 SGB V, § 29 BMV-Ä | Ampel GRÜN/GELB/ROT + Freitext-Begründung + Paragraphen-/Quellenverweis |
| **Strukturierte Begründungspflicht-Templates** | Dialog-Antworten des Arztes (FSM-Schritte: Diagnose → Vorbehandlung → Therapieversagen → ggf. BSG-Off-Label-Kriterien → ggf. Praxisbesonderheit) | Template-Ausfüllung, kein Algorithmus, kein KI-Modell | Strukturierter Begründungstext, dem Arzt zur freien Verwendung/Kopie bereitgestellt |
| **Vorab-Klärungs-Workflow** | Container-Marker der Ampel-Engine | Entscheidungsbaum (pflicht_vorab / verboten_vorab / stellungnahme / keine_aktion) nach öffentlichem Rechtsrahmen | Musterbrief an KK ODER Hinweistext „defensiv dokumentieren" |
| **Praxisbesonderheiten-Erkennung** | ATC+ICD + Stichtag | Pattern-Match gegen GKV-SV-Liste | Hinweistext „ggf. KV-Kennziffer setzen" |
| **Compliance-Log (Hash-Chain)** | Alle obigen Events | SHA-256-Kette über Einträge | lokal gespeicherte Log-Datei, nur lesend abrufbar |

### 1.2 Explizit ausgeschlossen

Nach aktueller Projektspezifikation verarbeitet die VerordnungsAmpel

- **KEINE** Patienten-Identifikationsdaten (Namen, Geburtsdaten, Versichertennummern),
- **KEINE** klinischen Messwerte (Labor, Vitalparameter, Bildgebung),
- **KEINE** vollständigen Medikationspläne einer realen Person,
- **KEINE** Therapieempfehlungen (weder Wirkstoff- noch Dosierungsvorschläge),
- **KEINE** Diagnosestellung (der ICD-Code wird vom Arzt eingegeben, nicht abgeleitet).

Das Tool liest nur **zwei anonyme Codes** pro Abfrage und vergleicht sie mit öffentlich publizierten Regelwerken des G-BA, des GKV-SV und der Fachgesellschaften.

### 1.3 Relevanz der Abgrenzung

| Einstufung | Folgen |
|---|---|
| **(A) Informationswerk** | Keine CE-Kennzeichnung, keine Benannte Stelle, keine klinische Bewertung nach Anhang XIV MDR, keine MPDG-Pflichten. Zulässige Marktbereitstellung ohne Konformitätsbewertung. |
| **(B) MDSW Klasse IIa nach Regel 11 MDR** | Konformitätsbewertung mit Beteiligung einer Benannten Stelle; ISO 13485-Qualitätsmanagement; IEC 62304-Softwarelebenszyklus; klinische Bewertung; technische Dokumentation nach Anhang II und III; EUDAMED-Registrierung; ca. 6–12 Monate Dauer, ca. 30.000–100.000 EUR Einmalkosten, laufende Pflege im fünfstelligen Bereich pro Jahr. Verstoß: Ordnungswidrigkeit bzw. Straftat nach §§ 92 ff. MPDG. |

Die Abgrenzung ist damit für die wirtschaftliche Machbarkeit und für die Förderfähigkeit im Prototype Fund **projektentscheidend**.

---

## 2. Rechtliche Einschätzung

### 2.1 Rechtsrahmen

| Norm / Dokument | Fundstelle |
|---|---|
| VO (EU) 2017/745 (MDR), insb. Art. 2 Nr. 1, Erwägungsgrund 19, Anhang VIII Regel 11 | EUR-Lex CELEX:32017R0745 |
| MDCG 2019-11 Rev. 1 (06/2025) — Leitfaden zu Qualifikation und Klassifikation von Software | [health.ec.europa.eu](https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en) |
| EuGH, Urt. v. 07.12.2017 — Rs. C-329/16 (Snitem und Philips France / Premier ministre) | [dejure.org/EuGH C-329/16](https://dejure.org/dienste/vernetzung/rechtsprechung?Text=C-329/16); curia.europa.eu Dok-ID 197527 |
| Medizinprodukterecht-Durchführungsgesetz (MPDG) v. 28.04.2020, zuletzt geändert 2023 | [gesetze-im-internet.de/mpdg](https://www.gesetze-im-internet.de/mpdg/) |
| BfArM-Leitlinie Abgrenzung/Klassifizierung (Medizinprodukte, Stand 2025) | [bfarm.de — FAQ Abgrenzung](https://www.bfarm.de/DE/Medizinprodukte/_FAQ/Klassifizierung-Abgrenzung/faq-liste.html) |
| ZVEI-Checkliste „Ist meine App ein Medizinprodukt?" (2017, weiter gültig) | [zvei.org](https://www.zvei.org/fileadmin/user_upload/Presse_und_Medien/Publikationen/2017/Juli/Checkliste__Medical_Apps_und_digitale_Gesundheitsanwendungen_als_Medizinprodukt/Checkliste-Ist-meine-App-ein-Medizinprodukt.PDF) |

### 2.2 Der Medizinproduktbegriff nach Art. 2 Nr. 1 MDR

Art. 2 Nr. 1 MDR definiert das Medizinprodukt als „Instrument, Apparat, Gerät, **Software**, Implantat, Reagenz, Material oder anderer Gegenstand, der dem Hersteller zufolge für Menschen bestimmt ist und allein oder in Kombination einen oder mehrere der folgenden spezifischen medizinischen Zwecke erfüllen soll:

- Diagnose, Verhütung, Überwachung, Vorhersage, Prognose, Behandlung oder Linderung von Krankheiten,
- Diagnose, Überwachung, Behandlung, Linderung von oder Kompensierung von Verletzungen oder Behinderungen,
- Untersuchung, Ersatz oder Veränderung der Anatomie oder eines physiologischen oder pathologischen Vorgangs oder Zustands,
- Gewinnung von Informationen durch In-vitro-Untersuchung von aus dem menschlichen Körper stammenden Proben […]"

Die MDR schließt Software ausdrücklich ein. Die Abgrenzung erfolgt **nicht** über die Technik, sondern über die **Zweckbestimmung** („intended purpose") des Herstellers (Art. 2 Nr. 12 MDR). Diese wird aus Etikettierung, Gebrauchsanweisung, Werbematerial und objektiver Produktgestaltung ermittelt ([MDCG 2019-11](https://health.ec.europa.eu/system/files/2020-09/md_mdcg_2019_11_guidance_en_0.pdf); Erwägungsgrund 19 MDR).

### 2.3 MDCG 2019-11 Rev. 1 — Entscheidungsbaum für Software

Die MDCG-Leitlinie (inhaltlich auch in Rev. 1 vom 17.06.2025 beibehalten) definiert Medical Device Software (MDSW) als

> „software that is intended to be used, alone or in combination, for a purpose as specified in the definition of a 'medical device' in the MDR […], regardless of whether the software is independent or driving/influencing the use of a device."

Der fünfstufige Entscheidungsbaum läuft vereinfacht so:

1. **Ist es Software im MDR-Sinn?** (≠ reines Datenspeichern, ≠ reine Kommunikation)
2. **Treibt oder beeinflusst sie ein Hardware-Medizinprodukt?** (Nein bei VerordnungsAmpel.)
3. **Führt sie eine Aktion an Daten durch, die über reine Speicherung, Archivierung, Kommunikation, einfache Suche oder verlustfreie Kompression hinausgeht?**
4. **Dient diese Aktion dem Nutzen einer individuellen Patientin / eines individuellen Patienten?**
5. **Hat die Aktion einen der in Art. 2 Nr. 1 MDR genannten medizinischen Zwecke (Diagnose, Therapie, Monitoring, Prognose, Prävention)?**

Nur wenn alle Stufen mit „Ja" beantwortet werden, ist die Software MDSW und unterliegt einer Klassifikation nach Regel 11.

Die Leitlinie hält auf S. 8 ff. ausdrücklich fest: Reine **„simple search"-Software**, die in öffentlich zugänglichen Bibliotheken oder Datenbanken Einträge zurückliefert, **ohne die Daten zu interpretieren oder patientenspezifisch zu verknüpfen**, ist **keine MDSW**. Entsprechendes gilt für Krankenhaus-Informationssysteme (HIS/PDMS/CIS), deren Zweck Administration, Abrechnung und Datenablage ist, **nicht** medizinische Entscheidungsunterstützung am individuellen Patienten.

### 2.4 EuGH, Rs. C-329/16 — Snitem/Philips France (07.12.2017)

Das für die vorliegende Frage zentrale Leiturteil betraf ebenfalls **Verordnungsunterstützungs-Software** (im Ausgangsfall: Module, die beim Rezeptieren aktiv wurden). Der Gerichtshof entschied zur damaligen Medizinprodukterichtlinie 93/42/EWG — deren Definitionen in der MDR wortgleich fortgeführt werden — Folgendes (Tenor, bestätigt u. a. in Fieldfisher-Analyse 2017 sowie MLL-News):

**Qualifizierend (= Medizinprodukt):**
Software ist Medizinprodukt, wenn mindestens eines ihrer Module

> „dazu bestimmt ist, Daten eines **individuellen Patienten** zu nutzen, um insbesondere Kontraindikationen, Wechselwirkungen von Arzneimitteln oder überhöhte Dosierungen **zu ermitteln**, […] weil sie einem der in der Richtlinie genannten medizinischen Zwecke (Verhütung, Überwachung, Behandlung oder Linderung von Krankheiten) dient."

Entscheidend war die **Kombination zweier Merkmale**:

(i) Verarbeitung **patientenspezifischer Daten** (nicht nur öffentlicher Katalogdaten),
(ii) **eigenständige Analyseleistung** (Auffinden von Interaktionen / Überdosierungen **für diesen einen Patienten**) mit medizinischer Zweckrichtung.

**Nicht qualifizierend (= kein Medizinprodukt):**
Der EuGH stellte zugleich klar — und das ist für unsere Frage zentral — dass Software

> „deren einziger Zweck das Speichern, Archivieren, Übermitteln oder die einfache Suche von Daten ist, ohne dass sie diese Daten verändert oder interpretiert,"

**kein Medizinprodukt** ist, selbst wenn sie in medizinischen Kontexten eingesetzt wird.

Dieses Differenzierungsmuster („patientenspezifische Interpretation" vs. „einfache Suche ohne Interpretation patientenspezifischer Daten") ist die tragende Abgrenzungsformel, nach der auch deutsche Gerichte und das BfArM die Klassifikation vornehmen.

### 2.5 Regel 11 MDR-Anhang VIII (im Falle einer Qualifikation als MDSW)

Für den Fall, dass eine Software als MDSW einzustufen wäre, greift Regel 11:

> „Software, die dazu bestimmt ist, Informationen zu liefern, die zu Entscheidungen für diagnostische oder therapeutische Zwecke herangezogen werden, gehört zur Klasse IIa, es sei denn, diese Entscheidungen haben Auswirkungen, die Folgendes verursachen können:
> — Tod oder irreversible Verschlechterung des Gesundheitszustands (Klasse III), oder
> — schwerwiegende Verschlechterung des Gesundheitszustands oder einen chirurgischen Eingriff (Klasse IIb). […]"

Im klinischen Umfeld einer Arzneiverordnung greift regelmäßig Klasse IIa, in Ausnahmefällen (z. B. Onkologika, Immunsuppressiva mit Letalitätsrisiko bei Fehldosierung) IIb oder III. Die Einstufung wäre also **nie** Klasse I für das hier skizzierte Feature-Set, **falls** MDSW-Eigenschaft bejaht würde.

MDCG 2019-11 Rev. 1 (06/2025) hat ausdrücklich klargestellt, dass die weit überwiegende Zahl von Decision-Support-Tools unter Regel 11 fällt und **nicht** mehr nach Klasse I klassifiziert werden kann, sofern die Software als MDSW qualifiziert.

### 2.6 Subsumtion — VerordnungsAmpel_SOCIAL

Die Prüfung erfolgt Stufe für Stufe an MDCG 2019-11 und EuGH C-329/16.

#### Schritt 1: Art. 2 Nr. 1 MDR — erfüllt die Zweckbestimmung einen der medizinischen Zwecke?

Hier liegt die eigentliche Steuerungsfrage. Die Zweckbestimmung des Herstellers ist **vom Um:bruch e. V. / den Projektträgern zu formulieren** — sie ist nicht objektiv gegeben, sondern projektpolitisch **gestaltbar**.

**Projektsprachliche Gestaltungsoptionen:**

| Formulierung | Risiko-Einstufung |
|---|---|
| „Werkzeug, das den Arzt bei der Diagnose und Therapieentscheidung unterstützt" | **hohes Risiko**: direkter therapeutischer Zweck wäre bejaht |
| „Software zur Erkennung kontraindizierter Arzneimittelgaben bei Patienten" | **hohes Risiko**: direkte Überwachung/Prävention einer Krankheit |
| „Nachschlagewerk für öffentliche Verordnungsregelwerke (AM-RL, PRISCUS, BMV-Ä), ohne patientenspezifische Verarbeitung und ohne Therapieempfehlung" | **niedriges Risiko**: vergleichbar mit einer elektronischen Ausgabe des gedruckten AM-RL-Katalogs |
| „Regress-Präventions-Tool zur strukturierten Dokumentationshilfe für vertragsärztliche Verordnungen nach § 106 SGB V" | **niedrigstes Risiko**: Zweck ist **sozialrechtliche Compliance**, nicht medizinische Entscheidung — ein eigener, MDR-fremder Zweck |

Die Zweckbestimmung muss der tatsächlichen Produktgestaltung standhalten (ZVEI-Checkliste Ziff. 1; BfArM-FAQ). Ein Disclaimer „kein Medizinprodukt" allein reicht **nicht** ([quickbirdmedical Leitfaden 2025](https://quickbirdmedical.com/medizinprodukt-app-software-mdr/)). Entscheidend ist das objektive Gesamtbild.

#### Schritt 2: Werden patientenspezifische Daten verarbeitet? (Snitem-Kernkriterium)

**Nein.** Das Produkt verarbeitet zwei anonyme Codes (ICD + ATC) ohne Bezug zu einer bestimmten oder bestimmbaren Person. Es liegt keine „Nutzung von Daten eines individuellen Patienten" im Sinne von Rn. 26 der Snitem-Entscheidung vor. Selbst Altersangaben werden als Zahlwert ohne Personenzuordnung entgegengenommen.

Dies ist das **entscheidendste Abgrenzungsmerkmal** gegenüber der Snitem-Software — deren Medizinprodukteigenschaft gerade aus der Verknüpfung mit Patientendaten des Praxis-EDV-Systems folgte.

#### Schritt 3: Handelt es sich um eine Analyse/Interpretation oder um einfache Suche?

**Eindeutig einfache Suche / Table-Lookup.** Der technische Ablauf ist:

1. Arzt gibt ICD + ATC ein.
2. System fragt eine SQLite-Tabelle ab: „Ist dieser ICD/ATC in AM-RL Anlage III gelistet? In PRISCUS? In § 31 Abs. 6 SGB V?"
3. System gibt den Tabelleneintrag mit Originaltext und Paragraphenverweis zurück.

Das ist funktional identisch mit einer CTRL+F-Suche in der PDF-Ausgabe der AM-RL. Es gibt **keine Algorithmen**, die Daten interpretieren; es gibt **keine KI-Modelle**; es gibt **keinen Score**; die Ampelfarbe ist die **direkte redaktionelle Beurteilung** des zugrundeliegenden Regelwerks (z. B.: „AM-RL Anlage III — verordnungseingeschränkt → ROT"), nicht ein vom System errechneter Risikoscore.

Der EuGH spricht in Snitem Rn. 33 exakt diesen Fall an: **Reine Datensuche ohne Veränderung oder Interpretation ist kein Medizinprodukt.**

#### Schritt 4: Dient die Aktion dem Nutzen eines individuellen Patienten?

**Primär nein.** Der unmittelbare Adressat des Outputs ist der **Vertragsarzt in seiner Rolle als Verwaltungsakteur gegenüber der GKV** — nicht der Patient. Der dokumentierte Zweck ist **Regressprävention** nach § 106 SGB V, also ein Schutzzweck gegen sozialrechtliche Nachforderungen der Krankenkasse. Das ist kein medizinischer, sondern ein **sozialrechtlich-wirtschaftlicher** Zweck.

Man kann argumentieren, dass mittelbar der Patient profitiert, weil ein entlasteter Arzt besser entscheidet. Dieser indirekte Nutzen reicht nach MDCG 2019-11 Decision Step 4 aber **nicht** aus; erforderlich ist der direkte patientenbezogene Nutzen („for the benefit of individual patients").

#### Schritt 5: Hat die Aktion einen der medizinischen Zwecke aus Art. 2 Nr. 1 MDR?

**Bei sauberer Zweckbestimmung nein.** Die „Plausibilitätsprüfung" ist eine **Rechtsprüfung** (passt diese Verordnung zu § 29 BMV-Ä / § 31 SGB V / AM-RL?), keine medizinische Prüfung (ist diese Verordnung für diesen Patienten medizinisch sinnvoll?). Das Tool prüft **Compliance**, nicht **klinische Indikation**.

Parallele: Ein Steuerberatungs-Programm, das beim Ausfüllen der Einkommensteuererklärung Warnungen gibt („Diese Ausgabe ist nach § 12 EStG nicht abzugsfähig"), ist kein Medizinprodukt, weil es rechtliche Regeln auf Eingaben des Nutzers anwendet, nicht medizinische.

#### Zwischenergebnis der Subsumtion

Bei **sorgfältiger Zweckbestimmungs-Formulierung** (Punkt 3.2) werden die Schritte 2, 3, 4 und 5 des MDCG-Entscheidungsbaums verneint. Damit greift die MDR nicht.

### 2.7 Vergleichbare Tools und ihre Einstufung

| Tool | Funktion | Tatsächliche Einstufung | Quelle |
|---|---|---|---|
| **UpToDate (Wolters Kluwer)** | Medizinisches Nachschlagewerk mit Therapieempfehlungen pro Krankheitsbild | In EU: als **medizinisches Informationsprodukt** vermarktet, **nicht CE-zertifiziert** als MDSW; Disclaimer „educational purposes only" | UpToDate-AGB; keine EUDAMED-Registrierung öffentlich auffindbar |
| **AMBOSS** | Digitales Lehrbuch + Entscheidungshilfen + Medikamentenlexikon | Als **Nachschlagewerk und Lernplattform**, **nicht** als MDSW vermarktet; keine CE-Kennzeichnung | amboss.com AGB |
| **Medscape Drug Interaction Checker** | Interaktionsprüfung zwischen bis zu 30 Wirkstoffen | In EU wird als **Referenzdatenbank** vermarktet; **nicht** patientenspezifisch (keine Anbindung an Praxis-EDV) → **kein** Medizinprodukt | [reference.medscape.com](https://reference.medscape.com/drug-interactionchecker) |
| **Medscape-Typ-Software in Praxissystemen integriert** | Gleiche Funktion, aber als Modul im PVS mit Patienten-Medikationsplan | Wird in Deutschland nach BfArM-Lesart und Snitem **als Medizinprodukt** eingestuft | EuGH C-329/16 |
| **Gelbe Liste Pharmindex Online** | ATC-/Fachinformations-Datenbank | Klassisches Nachschlagewerk → **kein** Medizinprodukt | gelbe-liste.de Impressum |
| **DrugSafe (verschiedene Anbieter)** | Interaktions- und Kontraindikationsprüfung auf Basis von Patienten-Medikationsplänen | In EU in der Regel **als MDSW Klasse IIa** zertifiziert, sobald Patienten-Medikationsplan verarbeitet wird | CE-Register-Stichproben |

**Kernmuster:** Die Schwelle zur MDSW wird **genau dann** überschritten, wenn das Tool **Daten eines konkreten Patienten verarbeitet** (auch wenn anonymisiert, aber als zusammenhängender Fall). Reine Katalog-Nachschlagewerke bleiben informativ.

Die VerordnungsAmpel_SOCIAL liegt architektonisch auf der **sicheren Seite** dieses Musters: jede Abfrage ist stateless, ICD+ATC-Paar ohne Kontext.

### 2.8 Rolle der Compliance-Log-Funktion (Hash-Chain)

Der manipulationssichere Compliance-Log ist rechtlich **nicht** als Medizinprodukt-Funktion einzuordnen. Er erfüllt zwei getrennte Zwecke:

1. **Prozessdokumentation für sozialrechtliche Verfahren.** Die Log-Datei mit SHA-256-Verkettung kann vor dem Sozialgericht als **privates elektronisches Dokument** im Sinne von § 371a Abs. 1 ZPO (analog anwendbar über § 202 SGG) in Augenschein genommen werden. Die Hash-Chain sichert die **Integrität** (nachträgliche Manipulation wird erkennbar), **nicht** aber die **Urheberschaft** — dafür bräuchte es qualifizierte elektronische Signaturen nach eIDAS. In der SG-Praxis wird die Hash-Chain regelmäßig als Indiz für die **frühzeitige Dokumentation** anerkannt, was nach BSG B 6 KA 26/13 und SG Marburg S 18 KA 96/23 ein Schlüsselkriterium ist.
2. **Keine medizinische Funktion.** Der Log speichert nur Metadaten über Tool-Nutzungen. Er enthält keine Patientendaten, er trifft keine medizinischen Aussagen, er greift nicht in Entscheidungen ein. MDR-Relevanz: **keine**.

Bewertung: Die Hash-Chain ist aus MDR-Sicht **neutral**, aus SG-Beweisrecht-Sicht **risikoarm vorteilhaft**. Eine Aufwertung zur qualifizierten elektronischen Signatur (§ 371a Abs. 2 ZPO: Urkundenbeweis-Ersatz) ist **nicht zwingend nötig**, aber langfristig ein Upgrade-Kandidat, falls das Tool im Pilotbetrieb in SG-Verfahren genutzt werden soll.

### 2.9 Randthemen

- **DiGA-Abgrenzung:** Eine DiGA (§ 33a SGB V) setzt zwingend die Medizinprodukte-Eigenschaft **mindestens** der Klasse I oder IIa voraus und ist **patientenbezogene** App. Da die VerordnungsAmpel weder patientenbezogen noch Medizinprodukt ist, ist eine DiGA-Einstufung ausgeschlossen — das ist aber auch gewollt (keine Erstattungsfähigkeit, keine BfArM-Registrierung).
- **Haftungsrecht (BGB/ProdHaftG):** Auch ohne MDR-Status greift die allgemeine Produkt- und Deliktshaftung. Fehlerhafte Regelwerks-Daten (z. B. falsche PRISCUS-Einordnung) können Schadensersatzansprüche auslösen, insbesondere wenn ein Arzt sich darauf verlässt und ein Regress entsteht. Gegenmaßnahme: Sorgfältige redaktionelle Pflege, Versionierung, Quellenangaben, Disclaimer mit klarem Hinweis „ersetzt keine eigenständige Prüfung durch den verordnenden Arzt".
- **Werberechtliche Grenzen (HWG):** Die Produktwerbung darf den nicht-medizinischen Charakter nicht verschleiern. Formulierungen wie „unterstützt therapeutische Entscheidungen" sind aus MDR-Sicht **gefährlich** und sollten vermieden werden.
- **Open-Source-Publikation / Prototype Fund:** Die OKFN-Förderung verlangt Open-Source-Publikation. Dies ist MDR-neutral; auch Open-Source-Code kann MDSW sein, wenn der Herausgeber des Produkts es als solches vermarktet. Umgekehrt bleibt es kein MDSW, wenn es als Bibliothek / Nachschlagewerk veröffentlicht wird und kein Anbieter es für medizinische Zwecke in Verkehr bringt.

### 2.10 Risikoeinschätzung

| Szenario | Wahrscheinlichkeit MDSW-Einstufung | Schadenspotenzial | Gesamt |
|---|---|---|---|
| Zweckbestimmung „Nachschlagewerk AM-RL" + strikte Disclaimer + keine Patientendaten | **niedrig** (≤ 15 %) | hoch (falls doch: Klasse IIa) | **niedrig-mittel** |
| Zweckbestimmung „Entscheidungsunterstützung" + Patientenbezug (auch pseudonym als Patienten-ID) | **hoch** (≥ 70 %) | hoch (Klasse IIa sicher) | **hoch** |
| Ungeschicktes Marketing („KI-Ampel für sichere Verordnung") | **sehr hoch** (≥ 90 %) | hoch | **kritisch** |
| Aktuelle MVP-Spezifikation (KONZEPT.md Stand 2026-04-08) | **niedrig** (ca. 15–20 %) | hoch | **mittel** |

Risikoeinschätzung insgesamt: **mittel**, mit deutlichem Handlungsspielraum für Risikominderung durch Formulierungs- und UI-Maßnahmen.

---

## 3. Empfehlung

### 3.1 Zusammenfassung

Die **VerordnungsAmpel_SOCIAL** ist bei **saubere Projektführung** rechtlich ein **Informationswerk / Nachschlagewerk** und **kein Medical Device Software** im Sinne der MDR. Das folgt aus:

- fehlendem patientenspezifischem Datenbezug (EuGH C-329/16, Rn. 26 negativ),
- reiner Lookup-Funktion ohne Dateninterpretation (EuGH C-329/16, Rn. 33; MDCG 2019-11 Step 3 negativ),
- sozialrechtlich-administrativer Zweckrichtung (nicht diagnostisch/therapeutisch).

Die Einschätzung ist **nicht selbstverständlich** — sie hängt von der disziplinierten Formulierung der Zweckbestimmung und der Gestaltung von UI, Marketing und Disclaimer ab. Bei Zweckbestimmungs-Drift (z. B. in Förderanträgen Formulierung „Entscheidungsunterstützung bei der Therapie") kann die Einstufung kippen.

**Empfehlung an die Redaktionssitzung und an LG:** Freigabe mit Auflagen (siehe 3.2).

### 3.2 Maßnahmen zur Risikominderung (verbindlich)

#### 3.2.1 Zweckbestimmung (Gebrauchsanweisung / README / Projektseite)

Verbindliche Mindest-Formulierung (verbindet beide zulässigen Profile):

> **„VerordnungsAmpel ist ein öffentliches Informations- und Nachschlagewerk zu sozialrechtlichen Verordnungsregelwerken (insbesondere AM-RL des G-BA, § 29 BMV-Ä, § 31 Abs. 6 SGB V, PRISCUS-Liste). Die Software dient der strukturierten Dokumentationshilfe zur Regress-Prävention nach § 106 SGB V. Sie trifft keine medizinischen Aussagen, stellt keine Diagnosen, spricht keine Therapieempfehlungen aus, bewertet keine konkreten Patienten und verarbeitet keine personenbezogenen Patientendaten. Sie ist kein Medizinprodukt im Sinne der Verordnung (EU) 2017/745 (MDR) und nicht CE-zertifiziert. Die medizinische Verantwortung für jede Verordnung liegt allein beim verordnenden Arzt."**

Diese Formulierung ist in README, pyproject.toml-Metadaten, Web-Impressum, Förderantrag und jeder öffentlichen Kommunikation **wortgleich** zu verwenden.

#### 3.2.2 UI-Maßnahmen

| Maßnahme | Begründung |
|---|---|
| **Kein Patienten-Identifier.** Keine Felder „Patient", „PID", „Name", „Geburtsdatum" in der UI. Auch Altersangabe nur als abstrakter Wert (nicht „Frau Müller, 72 J."). | Verhinderung des Snitem-Kernkriteriums (patientenspezifische Daten). |
| **Keine Speicherung von „Fällen".** Jede Abfrage ist stateless. Der Compliance-Log speichert Ereignisse (Zeitpunkt, ICD, ATC, Output), nicht „Patienten". | Kein kumulativer Patientenbezug. |
| **Keine Therapie-Vorschläge.** Die Ampel GELB/ROT darf **keine Alternativen vorschlagen** („Statt Wirkstoff A verwenden Sie Wirkstoff B"). Wenn Hinweistexte zu Alternativen gegeben werden, dann nur durch **Zitat aus der AM-RL** mit Quellenverweis, nicht als eigene Empfehlung. | Abgrenzung zu therapeutischem Zweck. |
| **Ampel-Label neutralisieren.** Statt „Verordnung riskant" besser „AM-RL Anlage III — verordnungseingeschränkt, Begründung erforderlich". Die Farbe ist **Status**, nicht **Urteil**. | Keine medizinische Wertung suggerieren. |
| **Begründungstexte = Zitate.** Jeder Ampel-Hinweis muss direkt mit dem Wortlaut der Quelle (§, AM-RL-Position, PRISCUS-Eintrag) belegt sein. | Unterstreicht „Nachschlagewerk" statt „Bewertung". |
| **Persistent sichtbarer Disclaimer.** Fußzeile in jeder Ansicht: „Informationswerk, kein Medizinprodukt, keine Therapieempfehlung. Medizinische Verantwortung beim Arzt." | Produkthaftungs- und HWG-Schutz. |
| **Eingangs-Disclaimer bei Erststart.** Einmalige Kenntnisnahme-Bestätigung durch den Nutzer (Checkbox) mit protokolliertem Akzept. | Nachweis, dass der Nutzer die Zweckbestimmung kennt. |
| **„Ersetzt keine eigene Prüfung"** als inline-Hinweis bei jedem Ampel-Ergebnis. | Produkthaftungsrechtliche Risikoreduktion. |

#### 3.2.3 Sprach- und Marketing-Regeln

**Zu vermeiden (triggert MDR-Einstufung):**

- „Klinische Entscheidungsunterstützung"
- „Therapiehilfe"
- „Entscheidet", „empfiehlt", „schlägt vor"
- „KI", „Algorithmus", „Machine Learning" (auch wenn technisch zutreffend, da es Interpretationsleistung suggeriert)
- „Sicherheit für den Patienten" als Primärnutzen
- „Diagnose", „Prognose", „Prädiktion" in jeglicher Form
- „CE" oder „zertifiziert" ohne echte Zertifizierung

**Empfohlen:**

- „Nachschlagewerk"
- „Informationswerkzeug"
- „Dokumentationshilfe"
- „Regress-Prävention"
- „Hinweis auf die Rechtslage"
- „Öffentliche Regelwerke strukturiert zugänglich"
- „Unterstützung der Compliance-Dokumentation"

#### 3.2.4 Organisatorische Maßnahmen

| Maßnahme | Wer | Frist |
|---|---|---|
| README und KONZEPT.md um o. g. Zweckbestimmung ergänzen | Projektleitung | vor Public Release |
| Disclaimer-Banner in CLI und später PWA implementieren | Dev-Team | vor Pilot |
| Redaktionelle QS für Regelwerks-Updates (Quartalscheck AM-RL) dokumentieren | Therapiefreiheit e. V. (Medical Reviewer) | vor Pilot |
| Versions- und Quellenangabe zu jedem ausgelieferten Datensatz (z. B. „AM-RL Stand 2026-Q2, Quelle: G-BA Beschluss vom …") | Dev-Team | vor Pilot |
| Fachanwalt Medizinrecht vor Public Release konsultieren (siehe 4.) | Projektleitung | vor Public Release, spätestens vor Prototype Fund-Einreichung |
| BfArM-Abgrenzungsantrag nach § 6 MPDG **optional** prüfen | Projektleitung | bei anhaltender Unsicherheit vor Skalierung |

Der **BfArM-Abgrenzungsantrag** (auch „Klassifizierungsentscheidung") nach § 6 Abs. 2 MPDG ist ein freiwilliges Instrument: Der Hersteller kann eine verbindliche Feststellung des BfArM einholen, ob sein Produkt Medizinprodukt ist. Dauer: 6–12 Monate, Kosten im vierstelligen Bereich. Empfehlung: **nicht im MVP-Stadium**, sondern erst wenn das Produkt im Markt etabliert ist und Klarheit wirtschaftlich wichtig wird.

### 3.3 Risikobewertung der Gesamtempfehlung

**Restrisiko nach Umsetzung aller Maßnahmen:** niedrig bis mittel.

Das verbleibende Risiko besteht darin, dass eine Marktaufsichtsbehörde (in Deutschland die Landesbehörden bzw. das BfArM) in einer späteren Überprüfung zu einer anderen Auffassung kommt. In diesem Fall wäre das Produkt entweder vom Markt zu nehmen oder nachzuzertifizieren. Das Risiko ist beherrschbar, weil a) die Zweckbestimmung eindeutig nicht-medizinisch ist, b) der EuGH in Snitem das Abgrenzungskriterium sauber herausgearbeitet hat, c) vergleichbare Nachschlagewerke (Medscape, Gelbe Liste, AMBOSS) seit Jahren ohne CE-Kennzeichnung in der EU vertrieben werden.

---

## 4. Grenzen dieser Einschätzung

Diese Einschätzung ist eine **KI-basierte Erstanalyse** der Um:bruch-Rechtsabteilung (Rolle RB, Besetzung Claude) auf Grundlage öffentlich zugänglicher Rechtsquellen und nach bestem Wissen. Sie **ersetzt keine anwaltliche Beratung**.

### 4.1 Was diese Einschätzung leistet

- Strukturierte Subsumtion unter die geltende Rechtslage (MDR 2017/745, MDCG 2019-11 Rev. 1, EuGH C-329/16, MPDG).
- Identifikation der entscheidungsrelevanten Unterscheidungsmerkmale.
- Konkrete, umsetzbare Risikominderungsmaßnahmen.
- Transparente Quellenangabe.

### 4.2 Was diese Einschätzung NICHT leistet

- Keine verbindliche Rechtsauskunft.
- Keine Garantie, dass eine Marktaufsichtsbehörde oder ein Gericht im Einzelfall dieselbe Einschätzung trifft.
- Keine Prüfung im konkreten UI-/Produkt-Stadium (dieses Gutachten bezieht sich auf die Spezifikation laut KONZEPT.md v1 Stand 2026-04-08; bei Feature-Änderungen ist erneut zu prüfen).
- Keine Prüfung der Datenschutzrechtslage (DSGVO) — separat.
- Keine Prüfung haftungsrechtlicher Fragen (BGB/ProdHaftG) — nur angerissen.

### 4.3 Empfohlene Eskalation

**Vor Public Release** und **vor Einreichung des Prototype Fund-Antrags** wird dringend empfohlen:

- Konsultation **eines Fachanwalts für Medizinrecht** mit MDR-/MDSW-Erfahrung (Kostenrahmen Erstberatung 190–400 EUR netto nach RVG).
- Fokusfragen für das Anwaltsgespräch:
  1. Prüfung der formulierten Zweckbestimmung (Punkt 3.2.1) auf Wasserfestigkeit.
  2. Risikoeinschätzung zur mittelbaren MDSW-Drift, falls das Tool später um patientenbezogene Features erweitert würde.
  3. Haftungsrisiko aus Fehlinformationen (ProdHaftG, § 823 BGB).
  4. Werberechtliche Grenzen (HWG) bei Ärzte-Kommunikation.
  5. Ob ein BfArM-Abgrenzungsantrag strategisch sinnvoll ist.

**Kandidaten** (nach Eigenrecherche zu kontaktieren; **diese Liste ist rein illustrativ und nicht geprüft**): Kanzleien mit ausgewiesener MDR-/Health-Tech-Praxis, z. B. Taylor Wessing (Medical Devices), CMS Hasche Sigle (Life Sciences), Fieldfisher (eHealth), Voelker & Partner (Medical Apps); ebenso Fachverbände mit Empfehlungslisten (bvitg, Spitzenverband Digitale Gesundheitsversorgung).

---

## 5. Recherchequellen

### 5.1 Primärrecht und Leitfäden (EU)

- Verordnung (EU) 2017/745 des Europäischen Parlaments und des Rates v. 05.04.2017 (Medical Device Regulation, MDR), insb. Art. 2 Nr. 1 und Nr. 12, Erwägungsgrund 19, Anhang VIII Regel 11 — [EUR-Lex 32017R0745](https://eur-lex.europa.eu/eli/reg/2017/745/oj).
- MDCG 2019-11 Rev. 1 „Guidance on Qualification and Classification of Software in Regulation (EU) 2017/745 – MDR and Regulation (EU) 2017/746 – IVDR", Stand Juni 2025 — [health.ec.europa.eu — Update Juni 2025](https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en); Ursprungsdokument als [PDF](https://health.ec.europa.eu/system/files/2020-09/md_mdcg_2019_11_guidance_en_0.pdf).

### 5.2 Rechtsprechung (EU)

- EuGH, Urt. v. 07.12.2017, Rs. C-329/16 „Snitem und Philips France / Premier ministre u. a." — [curia.europa.eu Dok-ID 197527](https://curia.europa.eu/juris/liste.jsf?language=de&td=ALL&num=C-329/16); Fundstellen- und Kommentar-Register [dejure.org](https://dejure.org/dienste/vernetzung/rechtsprechung?Text=C-329/16); deutsche PDF-Fassung auf [Johner-Institut-Blog](https://www.johner-institut.de/blog/wp-content/uploads/2017/12/EuGH-Software-Medizinprodukt-Module.pdf); Kommentar [MLL News](https://www.mll-news.com/eugh-wann-gilt-eine-software-als-medizinprodukt/).

### 5.3 Deutsches Umsetzungsrecht

- Medizinprodukterecht-Durchführungsgesetz (MPDG) v. 28.04.2020 — [gesetze-im-internet.de/mpdg](https://www.gesetze-im-internet.de/mpdg/).
- BfArM-FAQ „Klassifizierung und Abgrenzung" — [bfarm.de](https://www.bfarm.de/DE/Medizinprodukte/_FAQ/Klassifizierung-Abgrenzung/faq-liste.html).
- BfArM-Verfahren nach § 6 Abs. 2 MPDG (Feststellung rechtlicher Status und Klassifizierung) — [bfarm.de](https://www.bfarm.de/DE/Medizinprodukte/Aufgaben/Festellung-rechtlicher-Status-und-Klassifizierung/_artikel.html).
- BfArM-DiGA-Leitfaden v. 3.6 (10.12.2025) — [bfarm.de/SharedDocs](https://www.bfarm.de/SharedDocs/Downloads/DE/Medizinprodukte/diga_leitfaden.html).

### 5.4 Fachkommentare und Leitfäden

- Johner Institut, „MDR Regel 11: Der Klassifizierungs-Albtraum?" — [blog.johner-institute.com](https://blog.johner-institute.com/regulatory-affairs/mdr-rule-11/).
- VDE, „Klassifizierung von Medizinprodukten nach MDR: Regel 11 für Software" — [vde.com](https://www.vde.com/topics-de/health/beratung/regel-11).
- Emergo by UL, „European Revision of Primary Software Guidance (MDCG 2019-11 Rev. 1)" — [emergobyul.com](https://www.emergobyul.com/news/european-revision-primary-software-guidance-mdcg-2019-11-revision-1-small-changes-meaningful).
- ZVEI, „Checkliste: Ist meine App ein Medizinprodukt?" (2017) — [zvei.org](https://www.zvei.org/fileadmin/user_upload/Presse_und_Medien/Publikationen/2017/Juli/Checkliste__Medical_Apps_und_digitale_Gesundheitsanwendungen_als_Medizinprodukt/Checkliste-Ist-meine-App-ein-Medizinprodukt.PDF).
- Quickbird Medical, „Leitfaden: Ist Ihre Software ein Medizinprodukt?" — [quickbirdmedical.com](https://quickbirdmedical.com/medizinprodukt-app-software-mdr/).
- Fieldfisher Life Sciences Blog, „Drug prescription assistance software is classed as a medical device (C-329/16)" — [fieldfisher.com](https://www.fieldfisher.com/en/sectors/life-sciences/life-sciences-law-blog/update-on-e-health-drug-prescription-assistance-software-is-classed-as-a-medical-device-snitem-c-32916).

### 5.5 Beweisrecht / Sozialgerichtsverfahren

- § 371a ZPO — Beweiskraft elektronischer Dokumente — [dejure.org](https://dejure.org/gesetze/ZPO/371a.html).
- § 202 SGG — Verweis auf die ZPO im Sozialgerichtsverfahren.
- Beitrag „Audit-Log als Beweismittel: Was bei Rechtsstreitigkeiten zählt", docurex (Praxiskommentar, illustrativ) — [docurex.com](https://www.docurex.com/audit-log-als-beweismittel/).

### 5.6 Hintergrund Projekt

- VerordnungsAmpel_SOCIAL KONZEPT.md v1 (Stand 2026-04-08, lokal).
- VerordnungsAmpel_SOCIAL README.md (Stand 2026-04-08, lokal).
- Um:bruch-Politik zum Projekt: `.UMBRUCH/Policies/RECHTSABTEILUNG.md` Stand 02.04.2026.

---

**Disclaimer (nochmals, gesetzt als Schlussklausel):**
Diese Einschätzung ist eine KI-basierte Erstanalyse und ersetzt keine anwaltliche Beratung. Bei Risikoeinschätzung „Hoch" oder „Kritisch" wird die Einschaltung eines Fachanwalts empfohlen. Die vorliegende Bewertung hat Risikoeinschätzung **mittel** ergeben — vor Public Release wird zu einem Termin bei einem Fachanwalt für Medizinrecht (MDR-/MDSW-Schwerpunkt) geraten.

**Prüfende Stelle:** Um:bruch e. V. (i. Gr.) — Rechtsabteilung RB
**Bearbeiter:** Claude (CL), als KI-Rolle
**Bericht ablegen unter:** `_editorial/recht_2026-04-12_VerordnungsAmpel_MDSW.md` (zusätzliche Referenzkopie für die Um:bruch-Redaktionssitzung)

*Ende des Gutachtens.*
