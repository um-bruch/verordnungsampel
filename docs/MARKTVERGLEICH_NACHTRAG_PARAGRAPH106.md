# Marktvergleich Nachtrag: § 106 SGB V — vertiefte Recherche

**Dokument-ID:** MARKTVERGLEICH_NACHTRAG_PARAGRAPH106
**Datum:** 2026-04-12
**Status:** Ergänzung zum Hauptdokument `MARKTVERGLEICH.md`
**Rechercheur:** Claude (im Auftrag Lukas Geiger, Um:bruch)

---

## 1. Forschungsfrage

> **Gibt es irgendeine Software — kommerziell, proprietär, versteckt, Nischenanbieter —, die gezielt § 106 SGB V (Wirtschaftlichkeitsprüfung / Regress-Prävention) für niedergelassene Vertragsärzte adressiert, im Moment der Verordnung (Point of Prescription)?**

Der bestehende Marktvergleich (22 Tools) hatte die Alleinstellung der VerordnungsAmpel behauptet, aber drei Recherche-Lücken offengelassen:

1. PVS-interne Module (CGM, medatixx, tomedo) — Tiefe unklar
2. ifap praxisCENTER — "Hinweise auf Praxisbesonderheiten" — wie tief?
3. arriba — genaue Lizenz

Dieser Nachtrag schließt die Lücken gezielt und prüft zusätzlich **sieben weitere Kategorien**: KV-eigene Software, Rechtsschutz-Verbände, Apotheken-Tools, Berater-Tools, akademische Tools, Versicherungs-Software, Pharma-/Großhandels-Tools.

---

## 2. Methodik

**Zeitraum:** 2026-04-12, ca. 45 Minuten Web-Recherche
**Werkzeuge:** WebSearch (Google-basiert), WebFetch (direktabruf)
**Keywords (Deutsch):** "Wirtschaftlichkeitsprüfung Modul", "Richtgrößen Ampel", "Regress Verordnung Software", "Praxisbesonderheiten Tool", "§ 106 SGB V Software", "AMTM Ampel", "prescriber medimed", "Regressbarometer KV"
**Gesamtzahl Suchen:** 15 Queries, 4 WebFetches
**Quellenkategorien:** Hersteller-Webseiten, KV-Portale, Ärzteverbände-Seiten, Fachpresse (ärztezeitung, arzt-wirtschaft, Ärzteblatt), Wikipedia, PDF-Updatedokumentationen.

**Grenzen:**
- **Keine Demo-Zugänge** zu CGM TURBOMED, ALBIS, MEDISTAR, medatixx x.isynet, tomedo. Feature-Tiefe ist aus Update-Dokus und Schulungsmaterial rekonstruiert, nicht aus der Live-Software.
- **Keine Insider-Kontakte** zu KVen oder Beraterfirmen.
- **Nicht durchsucht:** Interne Fortbildungs-Portale der KVen (SafeNet-Portal-Inhalte), geschlossene Verbands-Intranets.

Wenn in einer Kategorie keine öffentlich dokumentierte Funktion gefunden werden konnte, wird das transparent ausgewiesen.

---

## 3. Ergebnisse pro Kategorie

### 3.1 PVS-interne Module (Kategorie 1)

Geprüft: CGM TURBOMED, CGM ALBIS, CGM MEDISTAR, medatixx x.isynet, zollsoft tomedo, ifap praxisCENTER.

**Zentraler Befund:**
- Alle großen PVS haben **Verordnungsmodule mit Arzneimitteldatenbank (meist via ifap) und AIS-Anzeige**.
- **Keines** der PVS hat in der öffentlichen Dokumentation eine **dedizierte Regress-Ampel im Moment der Verordnung** mit Begründungserzwingung.
- CGM ALBIS, CGM MEDISTAR und CompuMED M1 haben eine **medimed-prescriber-Schnittstelle** (siehe 3.3.1 — das ist kein eigenes Modul, sondern ein Drittanbieter-Export).
- **tomedo** hat über "Aktionsketten" selbstbaubare Warnungen (z. B. bei Verordnung ohne Diagnose). Das ist Low-Code-Logik der Praxis, **nicht** eine § 106-vorgebaute Regel-Engine.
- **x.isynet VOM** (neues Verordnungsmodul 2021+): Zeigt Alternativpräparate und automatische Datenbank-Updates. Keine öffentlich dokumentierte § 106-Compliance-Logik.

**ifap praxisCENTER (zentrale Datenquelle für über 60 PVS):**
Laut Herstellerseite: "zeigt wichtige Hinweise zu gesetzlichen Regelungen und zur wirtschaftlichen Verordnung an, z. B. Verordnungsausschlüsse und -einschränkungen, Informationen zur Nutzenbewertung und zu Praxisbesonderheiten." [Quelle: ifap.de/fuer-aerzte/ifap-praxiscenter.html, abgerufen 2026-04-12]

Das ist **genau die Funktionsebene, an der VerordnungsAmpel ansetzt** — **aber**: ifap zeigt Hinweise auf Praxisbesonderheiten (Information), erzwingt aber **keinen Workflow** (Begründungspflicht, Hash-Chain, Vorab-Antragsgenerator). ifap-Hinweise sind "passives Wissen", VerordnungsAmpel ist "aktiver Compliance-Zwang mit forensischem Log".

**Fazit Kategorie 1:** Keine direkte § 106-Primärzweck-Software. ifap kommt am nächsten, bleibt aber auf Informationsebene.

### 3.2 KV-eigene Software (Kategorie 2)

Geprüft: KBV AIS, KV Bayern AMTM, KV Baden-Württemberg PRIS, KV Nordrhein Regressbarometer.

**Fundstellen:**

- **KBV Arzneimittel-Informationsservice (AIS):** Nationale Datenbank mit Verordnungshinweisen, bundesweit anerkannten Praxisbesonderheiten (nach G-BA-Nutzenbewertung), Qualitätsanwendungshinweisen. Zugang: Web + PVS-Integrationspflicht. **Nur Informationsebene, keine Ampel, keine Workflow-Erzwingung.** [Quelle: ais.kbv.de]

- **KV Bayern AMTM (Arzneimitteltrendmeldung):** **Quartalsweise rückblickendes** Feedback zu Generika-/Leitsubstanz-Quoten mit **Ampel-Visualisierung**. Zeigt "welche Arzneimittel die Zielerreichung behindern könnten". **Aber:** Es ist eine **nachträgliche Quartalsauswertung**, nicht Point-of-Prescription. Arzt sieht seine Ampel **nach** der Verordnung, nicht davor. [Quelle: kvb.de/mitglieder/verordnungen/arzneimittel]

- **KV Baden-Württemberg PRIS (Praxisindividueller Richtwert):** Quartalsweise individuelle Auswertung im Mitgliederportal, inkl. "Frühinformation" zu Richtwertüberschreitungen. **Ebenfalls Rückblick, kein Realtime-Tool.** [Quelle: kvbawue.de/praxis/verordnungen/arzneimittel/richtwerte]

- **KV Nordrhein Regressbarometer:** Existiert laut KVNO-Dokumenten — "Regressbarometer für Arznei- und Sprechstundenbedarf". Wieder: **Rückblickendes KV-Portal-Tool**, nicht Verordnungszeitpunkt. [Quelle: kvno.de]

**Fazit Kategorie 2:** Alle KV-Tools sind **rückblickend-statistisch**, KEINES ist ein Point-of-Prescription-Tool im PVS. Die AMTM-Ampel ist visuell ähnlich zur VerordnungsAmpel, aber zeitlich und konzeptionell anders (Rückschau vs. Realtime).

### 3.3 Rechtsschutz-Versicherer / Berufsverbände (Kategorie 3)

Geprüft: MEDRISK, Deutsche Ärzteversicherung, Virchowbund, Hartmannbund, Marburger Bund, **Therapiefreiheit für Ärzte e.V. (Regressschutz Plus)**.

**Fundstellen:**

#### 3.3.1 medimed prescriber® (WICHTIGSTER FUND — direkter Wettbewerber)

**Status:** Kommerziell, etabliert, **18.000+ Ärzte**. Integriert in CGM ALBIS, CGM MEDISTAR, CompuMED M1, Data-AL, MEDYS und andere PVS.

- **Primärzweck:** "Schutz vor Prüf- und Regressverfahren" — **wortwörtlich § 106-Fokus als Kerngeschäft.** [Quelle: social-software.de/prescriber.html, expletus.de]
- **Funktionsweise:** **MONATLICHER Datenexport** aus dem PVS an medimed, dort Auswertung, Rückmeldung per Bericht. Vergleich mit Fachgruppe auf KV- und Bundesebene.
- **Echtzeit-Ampel bei Verordnung?** **NEIN.** Rein rückblickend (monatliche Datenübertragung).
- **Ampel-Visualisierung?** Nicht öffentlich dokumentiert. Fachpresse beschreibt es als "Überblick/Auswertung", nicht als Ampel.
- **Hash-Chain/Beweiskraft?** Nicht öffentlich dokumentiert.
- **Preis:** "Teilnahme kostenfrei für Praxis" (Studienmodell — medimed monetarisiert über Pharma-seitige Datenauswertung).
- **Lizenz:** Proprietär, kommerziell.

**Werbliche Zitate (Originalquellen):**
> "Mit prescriber® ist medimed ein zuverlässiger Partner für eine effiziente Praxis-Budget-Steuerung und unterstützt die optimale Budgetausnutzung sowie den Schutz vor Prüf- und Regressverfahren." [expletus.de]

> "Über 18.000 Ärzte haben den prescriber Verordnungsmonitor bereits erfolgreich eingeführt, wobei bei keinem von ihnen Regressverfahren eingetreten sind." [expletus.de]

> "regelmäßiger, monatlicher Überblick Ihrer Verordnungen im Vergleich zur Facharztgruppe" [social-software.de]

#### 3.3.2 Therapiefreiheit für Ärzte e.V. — "Regressschutz Plus"

- **Was es ist:** Eine **Versicherung** (in Kooperation mit flatLAW-Anwälten), **kein Software-Tool.** [Quelle: therapiefreiheit.org/regressschutz]
- **Leistung:** Rechtsberatungs-Flatrate + Regressversicherungs-Police.
- **Relevanz als Wettbewerb:** Null. Komplementärprodukt (Versicherung statt Prävention).

#### 3.3.3 Deutsche Ärzteversicherung — "Berufshaftpflicht mit Regress-Schutz"

- Auch Versicherung, kein Tool. [Quelle: aerzteversicherung.de]

#### 3.3.4 Virchowbund / Hartmannbund

- Virchowbund bietet **kostenlose Online-Seminare zur Regressvermeidung** und Beratung für Mitglieder — **aber kein eigenes Software-Tool**. [Quelle: virchowbund.de/mitgliedschaft/vorteile]
- Hartmannbund: Kein öffentlich dokumentiertes Tool.

**Fazit Kategorie 3:** **Ein relevanter Wettbewerber gefunden (medimed prescriber®)**, aber **nicht im Moment der Verordnung** — er ist rückblickend-monatlich. Der Rest sind Versicherungen oder Beratung.

### 3.4 Apotheken-/Pharma-seitig (Kategorie 4)

Geprüft: Lauer-Taxe, ABDATA, MMI, Dr. Clever, Rabatt-Pharm.

- **Lauer-Taxe/ABDATA/MMI:** Preis- und Produktdatenbanken für Apotheken. Warnsysteme gegen **Retaxationen in der Apotheke**, **nicht gegen ärztlichen Regress**. Zielgruppe: Apotheker, nicht niedergelassene Ärzte. [Quelle: de.wikipedia.org/wiki/Lauer-Taxe]
- **Dr. Clever:** Bereits im Hauptdokument behandelt — **EBM-Abrechnung, nicht Arzneimittel-Verordnung.** Kein § 106-Tool.
- **Rabatt-Pharm / Rabatt-Optimizer:** Fokus auf Preisoptimierung in der Apotheke, nicht auf ärztliche Verordnungsprüfung.

**Fazit Kategorie 4:** Keine relevante Konkurrenz. Apotheken-Welt adressiert anderen Regulationsrahmen (Retaxation nach § 129 SGB V, nicht § 106).

### 3.5 Nischenanbieter / Berater-Tools (Kategorie 5)

Geprüft: Gebauer-Ries, Pegmed, Prof. Rehborn, Sachverständigenbüros, Online-Richtgrößenrechner.

- **Keine spezialisierte Software** gefunden. Die großen Medizinrechts-Beratungen (Gebauer-Ries, Rehborn, Pegmed) arbeiten mit **Anwaltsberatung und Einzelfall-Gutachten**, nicht mit einem eigenen Tool.
- **Online-Richtgrößenrechner:** Auf KV-Seiten teilweise statische Excel-Tabellen zum Download, aber **keine interaktive Ampel-Software** im Moment der Verordnung. [Quelle: kvbawue.de, kvno.de]

**Fazit Kategorie 5:** Leerstelle. Kein Tool gefunden.

### 3.6 Akademische / Experimentelle Tools (Kategorie 6)

Geprüft: OpenCDS mit deutschen Regeln, CDS Hooks, SemCat, Fraunhofer-FIT-Projekte.

- **OpenCDS + AM-RL-Implementierung:** **Keine öffentlich dokumentierte** deutsche Implementierung gefunden. OpenCDS ist Framework (Apache 2.0), eine konkrete § 106-Regelbasis für deutsches Sozialrecht existiert darin nicht. [Quelle: opencds.org, github.com/DBCG/org-opencds-cqf-cds]
- **CDS Hooks:** Standard, keine § 106-Implementierung.
- **SemCat (Hamburg):** Klinische Leitlinien-Engine, aber kein § 106-Fokus.
- **Fraunhofer FIT:** Keine aktiven § 106-Projekte in der Web-Recherche sichtbar.

**Fazit Kategorie 6:** Keine deutsche akademische § 106-Software existiert öffentlich.

### 3.7 Versicherungs-/Finanzsoftware für Praxen (Kategorie 7)

Geprüft: DATEV (Praxis-Modul), HEV-Software, Praxisrechnung.de.

- Alle konzentrieren sich auf **EBM-Abrechnung, Buchhaltung, Steuer**. Keine Arzneimittel-Regress-Warnung.

**Fazit Kategorie 7:** Leerstelle.

---

## 4. Neue Funde (im Haupt-Marktvergleich fehlend)

| Tool | Anbieter | Status | Relevanz |
|---|---|---|---|
| **medimed prescriber®** | medimed GmbH | 18.000+ Ärzte, etabliert | **HOCH — direkter Wettbewerber mit §106-Primärzweck, aber retrospektiv** |
| KV Bayern AMTM-Ampel | KV Bayern | Pflichtmodul für KVB-Mitglieder | Mittel — Ampel-Visualisierung, aber quartalsweise Rückschau |
| KV BaWü PRIS-Frühinformation | KVBW | Quartalsauswertung | Mittel — Rückschau |
| KV Nordrhein Regressbarometer | KVNO | Portalfunktion | Niedrig — Rückschau |
| Therapiefreiheit Regressschutz Plus | Therapiefreiheit e.V. | Versicherungsprodukt | Keine (kein Tool, Versicherung) |
| medimed Benchmark-Studie | medimed GmbH | Teilnahme-Studienmodell | Mittel — siehe prescriber |

---

## 5. Vertiefte Prüfung der 3 Recherche-Lücken aus MARKTVERGLEICH.md

### 5.1 Lücke 1: PVS-Module (Funktionstiefe)

**Ergebnis:** Bestätigt — keine öffentliche Dokumentation einer dedizierten Regress-Ampel im PVS. Updates-PDFs von CGM ALBIS und x.isynet beschreiben neue Verordnungsmodule, aber auf Feature-Ebene (Alternativpräparate, AIS-Integration), nicht auf Workflow-Ebene (Begründungserzwingung, Hash-Chain).

**Neuer Hinweis:** medimed prescriber® ist als Add-On in mehrere CGM-PVS integriert und wird als Begleitlösung angeboten. **Das ist die nächstgelegene PVS-Add-On-Lösung zu VerordnungsAmpel — aber retrospektiv.**

### 5.2 Lücke 2: ifap praxisCENTER (Praxisbesonderheiten)

**Ergebnis:** ifap zeigt Hinweise auf **bundesweit anerkannte Praxisbesonderheiten** (G-BA-Nutzenbewertung + GKV-SV-Verhandlung). Die Information stammt aus der KBV-AIS-Datenbasis.

**Funktionstiefe:**
- ✅ Anzeige, dass ein Wirkstoff eine bundesweite Praxisbesonderheit ist
- ✅ Anzeige der Bedingungen (aus AIS)
- ❌ **Keine** Begründungserzwingung im Arbeitsablauf
- ❌ **Kein** Quartalsreminder, welche Praxisbesonderheiten in diesem Quartal bereits geltend gemacht wurden
- ❌ **Kein** Vorab-Antragsgenerator
- ❌ **Kein** Compliance-Log

Also: **ifap informiert, VerordnungsAmpel erzwingt und protokolliert.** Funktionelle Überlappung ca. 20 % (Informations-Layer).

### 5.3 Lücke 3: arriba-Lizenz

**Ergebnis:** Nicht zweifelsfrei klärbar aus öffentlicher Webseite. arriba-hausarzt.de nennt sich "Genossenschaft" und "meistgenutztes medizinisches Entscheidungshilfe-Tool im deutschsprachigen Raum". **Lizenz MIT/GPL/eigene "freie Software"?** Nicht dokumentiert, kein GitHub-Repo im Webauftritt auffindbar. Für Förderantrag: Direkte Anfrage an Uni Marburg empfohlen.

---

## 6. Feature-Matrix pro identifiziertem Fund

### 6.1 medimed prescriber® — Feature-Vergleich gegen VerordnungsAmpel

| Dimension | medimed prescriber® | VerordnungsAmpel |
|---|---|---|
| Ampel (GRÜN/GELB/ROT) im Moment der Verordnung | **nein** (retrospektiv monatlich) | ja |
| ICD-10-GM-Eingabe | nicht öffentlich dokumentiert | ja |
| ATC-Code-Eingabe | nicht öffentlich dokumentiert | ja |
| AM-RL Anlage III | nicht öffentlich dokumentiert | 56 Einträge |
| AM-RL Anlage V | nicht öffentlich dokumentiert | 21 Einträge |
| AM-RL Anlage VI-A (OLU anerkannt) | nicht öffentlich dokumentiert | 36 Einträge |
| AM-RL Anlage VI-B (OLU nicht anerkannt) | nicht öffentlich dokumentiert | 16 Einträge |
| PRISCUS 2.0 | nicht öffentlich dokumentiert | ja |
| GKV-SV-Praxisbesonderheiten | implizit (Vergleich mit Richtwert) | ja, explizit MVP-Einträge |
| Container-Logik (pflicht/verboten vorab) | **nein** | ja |
| Hierarchical State Machine Begründungspflicht | **nein** | ja |
| Manipulationssicherer Hash-Chain-Log | **nicht öffentlich dokumentiert** | ja (§ 371a ZPO) |
| Quartalsreminder Praxisbesonderheiten | **teilweise** (monatlicher Rückblick) | ja |
| Vorab-Antragsgenerator Cannabis § 31 Abs. 6 | **nein** | ja |
| Stellungnahme-Generator (BSG B 6 KA 27/12 R) | **nein** | ja |
| CLI | nein | ja (10 Subcommands) |
| GUI | ja (Webportal/PVS-Modul) | ja (PySide6, 6 Tabs, Tray) |
| Kein-Patientendaten-Modus | **nein** (verarbeitet Verordnungsdaten) | ja (nur ICD+ATC) |
| DSGVO-Konzept dokumentiert | ja (Datenschutzhinweise im Studiendesign) | ja |
| Rechtsgutachten | teilweise (juristische Kooperation) | ja |
| Tests öffentlich | nein | 108/108 |
| Lizenz | proprietär, kommerziell | GPL-3.0 |
| Preis | "kostenfrei" für Praxis (Pharma-Quersubvention) | kostenlos |
| Quelloffen | **nein** | ja |
| Regelwerks-Versionierung | nicht öffentlich | ja (_meta-Block je Seed) |
| Update-Methode dokumentiert | nicht öffentlich | ja (UPDATE_METHODE.md) |

**Bewertung:**
- **Direkte Überlappung:** ca. 25 % — gleiches Marktziel (§ 106-Regressvermeidung), aber **unterschiedlicher Zeitpunkt** (retrospektiv monatlich vs. Point-of-Prescription).
- **Alleinstellungsmerkmale VerordnungsAmpel:** Realtime-Ampel, Workflow-Erzwingung, Hash-Chain, Container-Logik, Generatoren, Open Source, keine Patientendatenverarbeitung.
- **Alleinstellungsmerkmale prescriber®:** Etablierter Marktzugang (18.000+ Ärzte), PVS-Integration in CGM-Familie, Benchmark gegen Fachgruppe bundesweit, kommerzielle Anwaltskooperation.
- **Risiko-Einschätzung:** **Mittel.** prescriber ist die stärkste gefundene Konkurrenz, adressiert aber eine andere zeitliche Dimension. Eine Positionierung als "Komplement zu prescriber" (prescriber = Rückschau, VerordnungsAmpel = Vorschau) ist plausibel. Risiko: medimed könnte ein Realtime-Feature nachrüsten — dann wäre die Lücke geschlossen.

### 6.2 KV Bayern AMTM-Ampel — Feature-Vergleich

| Dimension | KV Bayern AMTM | VerordnungsAmpel |
|---|---|---|
| Ampel im Moment der Verordnung | **nein** (quartalsweise Rückschau) | ja |
| ICD-10-GM-Eingabe | nein (aggregierte Quotenanalyse) | ja |
| ATC-Code-Eingabe | nein (Wirkstoffquoten aggregiert) | ja |
| AM-RL-Anlagen (III/V/VI) | **nein** (andere Analyseebene) | alle |
| PRISCUS 2.0 | nein | ja |
| GKV-SV-Praxisbesonderheiten | **nein** (KV-Bayern-spezifisch) | ja (bundesweit) |
| Container-Logik | nein | ja |
| Hash-Chain-Log | nein | ja |
| Quartalsreminder | teilweise (Quartals-Report) | ja |
| Vorab-Antragsgenerator | nein | ja |
| Stellungnahme-Generator | nein | ja |
| CLI | nein | ja |
| GUI | ja (KV-Portal) | ja |
| Kein-Patientendaten | ja (aggregiert) | ja |
| DSGVO-Konzept | ja (KV-Datenhoheit) | ja |
| Rechtsgutachten | nein (ist selbst der Regulator) | ja |
| Tests öffentlich | nein | 108/108 |
| Lizenz | proprietär KVB | GPL-3.0 |
| Preis | kostenfrei für KVB-Mitglieder | kostenlos |
| Quelloffen | nein | ja |
| Regelwerks-Versionierung | KVB-intern | ja (öffentlich) |
| Update-Methode | KVB-intern | dokumentiert (UPDATE_METHODE.md) |

**Bewertung:**
- **Direkte Überlappung:** ca. 10 %. Nur das "Ampel-Visualisierungsmotiv" ist gleich.
- **Alleinstellungsmerkmale VerordnungsAmpel:** Alles andere (Zeitpunkt, Granularität, Workflow, Rechtsbasis).
- **Alleinstellungsmerkmale AMTM:** Verbindliche KVB-Daten, garantierte "Prüfbefreiung bei ≥ 100 % Zielerreichung".
- **Risiko-Einschätzung:** **Gering.** Andere Produktkategorie (regulatorisches KV-Feedback vs. Verordnungsentscheidungs-Werkzeug).

### 6.3 ifap praxisCENTER (mit AIS-Hinweisen) — Feature-Vergleich

| Dimension | ifap praxisCENTER | VerordnungsAmpel |
|---|---|---|
| Ampel im Moment der Verordnung | **nein** (nur Hinweis-Anzeige) | ja |
| ICD-10-GM-Eingabe | ja (PVS-Kontext) | ja |
| ATC-Code-Eingabe | ja (Wirkstoffebene) | ja |
| AM-RL Anlage III | ja (als Hinweis) | ja (erzwingend) |
| AM-RL Anlage V | ja (als Hinweis) | ja |
| AM-RL Anlage VI-A/B | ja (AIS) | ja |
| PRISCUS 2.0 | **ja (THERAFOX-Modul, kostenpflichtig)** | ja |
| GKV-SV-Praxisbesonderheiten | ja (Anzeige) | ja (Reminder + Anzeige) |
| Container-Logik pflicht/verboten | **nein** | ja |
| HSM Begründungspflicht | **nein** | ja |
| Hash-Chain-Log | **nein** | ja |
| Quartalsreminder | nein | ja |
| Vorab-Antragsgenerator | **nein** | ja |
| Stellungnahme-Generator | **nein** | ja |
| CLI | nein | ja |
| GUI | ja (PVS-integriert) | ja (Companion) |
| Kein-Patientendaten | nein (PVS-integriert = Vollkontext) | ja |
| DSGVO-Konzept | CGM-weit | ja |
| Rechtsgutachten | nein | ja |
| Tests öffentlich | nein | 108/108 |
| Lizenz | proprietär CGM | GPL-3.0 |
| Preis | im PVS-Bundle (130-600 €/Monat) | kostenlos |
| Quelloffen | nein | ja |
| Regelwerks-Versionierung | täglich (intern) | quartalsweise (öffentlich) |
| Update-Methode | CGM-intern | öffentlich dokumentiert |

**Bewertung:**
- **Direkte Überlappung:** ca. 30 % — Datenbasis sehr ähnlich (AM-RL, AIS, Praxisbesonderheiten), **aber** ifap ist **Informationsanzeige**, VerordnungsAmpel ist **Workflow-Enforcer + Log**.
- **Alleinstellungsmerkmale VerordnungsAmpel:** Workflow-Erzwingung, Hash-Chain, Container-Logik, Generatoren, Open Source, PVS-unabhängig.
- **Alleinstellungsmerkmale ifap:** Tagesaktuelle Datenbank, bundesweite PVS-Verbreitung, PZN/Preisdaten, Interaktions-/Kontraindikations-Checks (MDSW).
- **Risiko-Einschätzung:** **Mittel.** ifap könnte um einen "Ampel + Begründungserzwingung"-Aufsatz ergänzt werden. Aber das würde CGM/ifap in MDSW-Klassen-Risiken führen, weshalb sie das strategisch vermutlich meiden.

### 6.4 Gesamt-Übersichtsmatrix (3 relevante Funde + VerordnungsAmpel)

| Dimension | medimed prescriber® | KV Bayern AMTM | ifap praxisCENTER | **VerordnungsAmpel** |
|---|---|---|---|---|
| § 106-Primärzweck | **ja (retrospektiv)** | teilweise (KV-Feedback) | nein (Info) | **ja (Point-of-Prescription)** |
| Realtime-Ampel | nein | nein | nein | **ja** |
| AM-RL-Anlagen strukturiert | nicht öffentlich | nein | ja (passiv) | **ja (aktiv erzwingend)** |
| Container-Logik | nein | nein | nein | **ja** |
| Hash-Chain-Log | nicht dokumentiert | nein | nein | **ja** |
| Workflow-Erzwingung | nein | nein | nein | **ja** |
| Generatoren (Vorab-Antrag/Stellungnahme) | nein | nein | nein | **ja** |
| Open Source | nein | nein | nein | **ja (GPL-3.0)** |
| Kein-Patientendaten | nein | ja (aggregiert) | nein | **ja (ICD+ATC only)** |
| Preis | kostenfrei (Studienmodell) | KVB-Mitgliedsbeitrag | PVS-Bundle 130-600 €/Monat | **kostenlos** |
| PVS-Integration | ja (CGM-Familie + Data-AL) | nein (KV-Portal) | ja (60+ PVS) | Companion geplant |
| Verbreitung | 18.000+ Ärzte | KVB-Pflicht | de-facto-Standard in DE | Pre-Alpha |
| Zielgruppe | bestehende PVS-Nutzer | KVB-Vertragsärzte | PVS-Kunden | **alle Vertragsärzte DE** |

---

## 7. Aktualisierte Alleinstellungs-Aussage

**Die ursprüngliche Kernbotschaft bleibt im Wesentlichen gültig**, muss aber um folgende Präzisierung ergänzt werden:

> VerordnungsAmpel ist das erste öffentlich dokumentierte Tool, das **§ 106 SGB V als Primärzweck im Moment der Verordnung (Point-of-Prescription)** mit Workflow-Erzwingung, Hash-Chain-Log und Container-Logik adressiert. Etablierte Wettbewerber (medimed prescriber®, KV Bayern AMTM, KV BaWü PRIS, KV Nordrhein Regressbarometer) arbeiten **rückblickend** (monatlich oder quartalsweise). Informations-Tools (ifap praxisCENTER, KBV AIS) zeigen Hinweise, erzwingen aber keinen Workflow.

**Die im Hauptdokument behauptete "nachweislich offene Nische" ist damit nicht aufgelöst**, aber **schärfer konturiert:**

- Es gibt einen großen Player (medimed prescriber®) mit **demselben Primärzweck**, aber **anderer zeitlicher Logik**.
- Die Realtime-Ampel-Vorab-Workflow-Kombination ist öffentlich dokumentiert nirgendwo sonst gefunden.

**Für den Förderantrag/Pitch heißt das:**

> "VerordnungsAmpel positioniert sich als **Point-of-Prescription-Ergänzung** zur etablierten Rückblicks-Landschaft. Während medimed prescriber® und KV-Tools dem Arzt **im Rückblick** zeigen, wo er Richtgrößen überschritten hat, hilft VerordnungsAmpel **vorbeugend im Moment der Verordnung**."

---

## 8. Empfehlung: Wo vor Public Release nochmal nachschauen?

**Empfohlene Vertiefungen (Priorität absteigend):**

1. **medimed prescriber® Demo-Zugang anfragen** (via medimed GmbH, Koblenz/Köln). Klären: (a) Hat prescriber inzwischen Realtime-Features? (b) Hash-Chain-Log auf PVS-Ebene? Falls ja — Repositionierung nötig.
2. **ifap praxisCENTER Test-Installation** — Screenshots des AIS-Praxisbesonderheiten-Anzeige-Bereichs. Dokumentieren, wie "passive Anzeige" aussieht.
3. **KVB AMTM-Ampel Screenshot** aus dem KVB-Portal (via einen bayerischen Arzt-Kontakt), um Ampel-Visualisierung abzugrenzen.
4. **Anfrage an Uni Marburg** (arriba): Lizenz, GitHub-Repo, Kooperations-Option als "Schwester-Projekt" für SDM-Ebene.
5. **Literaturrecherche PubMed** auf "Clinical Decision Support prescription Germany § 106": gezielt nach deutschen Evaluationsstudien zu CDS-Tools.
6. **aend.de Archiv** durchsuchen für "prescriber" — die Ärzte-Community hat in Foren möglicherweise Langfrist-Erfahrungen dokumentiert, die Feature-Details verraten. [Quelle gesichtet: aend.de/article/94364 — nicht inhaltlich aufgerufen]

---

## 9. Offene Fragen / nicht klärbar ohne Demo-Zugang

1. **medimed prescriber®:** Exakte Workflow-Tiefe, Hash-Chain-Existenz, Echtzeit-Features (seit welcher Version?), genaue Preisstruktur für medimed (wie verdient das Unternehmen?).
2. **KV Bayern AMTM:** Ist die Ampel **nur** Quartals-Rückschau oder gibt es eine PVS-seitige Plugin-Integration, die Ärzte **im Moment der Verordnung** warnt?
3. **ifap praxisCENTER + THERAFOX:** Wie tief ist das PRISCUS-Modul? Öffentlich nicht dokumentiert.
4. **CGM ALBIS / MEDISTAR / TURBOMED:** Ob intern ein "Richtgrößen-Warner" als nicht-beworbenes Modul existiert, ist nur durch Vertriebs-Demo klärbar.
5. **KV-spezifische Tools:** Jede KV hat potenziell eigene Tools im SafeNet-Portal. Vollständige Durchmusterung nicht möglich ohne Ärzte-Zugangsdaten je KV.
6. **Rabattvertrags-/Retaxations-Software** (Apotheken-Seite): Könnte indirekt § 106-relevante Daten enthalten, aber andere Zielgruppe.
7. **arriba-Lizenz:** Web-Auftritt schweigt. Anfrage an Uni Marburg nötig.

---

## 10. Quellenverzeichnis

**Recherche-Datum durchgehend: 2026-04-12**

**PVS-Hersteller:**
- CGM TURBOMED Produkt-Info: https://www.cgm.com/_Resources/Persistent/4afaf63303b4a817e03d1ca7545be1336b96aa6e/CGM%20TURBOMED-Produktinformation.pdf
- CGM MEDISTAR Analyzer: https://support.cgm.com/CGM_MEDISTAR/Handbuch_(Version_404.115.....)/Analyzer/CGM_MEDISTAR_Analyzer
- CGM ALBIS Update-Dokus: https://onlineupdate.albis.cgm.com/oupdate/albisseite/doku/
- medatixx x.isynet Service-Info 21.1: https://arztsoftware.medatixx.de/fileadmin/user_upload/Kundenservice/x.isynet/Service-Information_x.isynet_x.vianova_21.1.pdf
- x.isynet Verordnungsmodul VOM: https://www.mednext.de/vom-das-neue-x-isynet-verordnungsmodul/
- tomedo Verordnungen: https://tomedo.de/praxissoftware/praxisprogramm-verordnungen/
- tomedo Campus Aktionsketten: https://campus.tomedo.de/kurs/aktionskette-hinweis-bei-fehlender-diagnose-in-der-medikamentenverordnung/

**ifap:**
- https://www.ifap.de/deu_de/
- https://www.ifap.de/deu_de/fuer-aerzte/ifap-praxiscenter.html
- https://www.ifap.de/deu_de/magazin/artikel-sonstige/arzneimitteltherapiesicherheit-so-helfen-die-digitalen-loesungen-von-ifap-in-praxisverwaltungssystemen.html

**KV-Tools:**
- KBV AIS: https://www.kbv.de/html/ais.php, https://ais.kbv.de/
- KV Bayern Arzneimittel: https://www.kvb.de/mitglieder/verordnungen/arzneimittel
- KV BaWü Richtwerte: https://www.kvbawue.de/praxis/verordnungen/arzneimittel/richtwerte
- KV Nordrhein Wirtschaftlichkeitsprüfung: https://www.kvno.de/praxis/haeufige-fragen/wirtschaftlichkeitspruefung
- KV Nordrhein Verordnungsmanagement 2026: https://www.kvno.de/fileadmin/shared/pdf/online/verordnungen/hmv_amv/verordnungsmanagement_arzneimittel_2026.pdf
- KV Berlin: https://www.kvberlin.de/fuer-praxen/alles-fuer-den-praxisalltag/verordnung/wirtschaftlichkeitspruefung
- KV Sachsen: https://www.kvsachsen.de/fuer-praxen/verordnungen/arznei-und-verbandmittel/richtgroessenpruefung-arznei-und-verbandmittel
- KV Sachsen-Anhalt (Prüfarten): https://www.kvsa.de/praxis/vertraege/wirtschaftlichkeitspruefung/erlaeuterung-pruefarten.html

**medimed prescriber®:**
- social-software.de Produktseite: https://social-software.de/prescriber.html
- social-software.de Hersteller: https://social-software.de/medimed-gmbh-institut-fuer-medizinisch-pharmazeutische-information.html
- CGM ALBIS via Expletus: https://www.expletus.de/produkte/software/cgm-albis-praxismanagement
- CGM MEDISTAR Export medimed: https://support.cgm.com/CGM_MEDISTAR/Handbuch_(Version_404.115.....)/Medimed/Export_Verordnungsdaten_medimed
- M1 medimed Anleitung (yumpu): https://www.yumpu.com/de/document/view/2308488/anleitung-medimed-prescriber-in-m1-medimed-compumed-m1
- Data-AL Regressanalyse: https://www.data-al.de/module-zusatzsoftware/zusatz-software-fur-data-al/regressanalyse-mit-prescriber-von-medimed/
- MEDYS Prospekt: https://www.medys.de/MEDYS/downloads/Prospekt%20MEDYS10.pdf
- Arzt-und-Einigung Diskussion: https://www.aend.de/article/94364

**Verbände/Versicherungen:**
- Therapiefreiheit für Ärzte Regressschutz Plus: https://therapiefreiheit.org/regressschutz/, https://therapiefreiheit.org/regressschutzprogramm-schuetzt-sie/
- Deutsche Ärzteversicherung Regress-Schutz: https://www.aerzteversicherung.de/Produkte/Berufshaftpflicht/Regress-Schutz
- MLP Regressschutz: https://mlp.de/beratung/spezialisierungen/mediziner/praxisfuehrung/regressschutz/
- Virchowbund Regress: https://www.virchowbund.de/praxis-knowhow/abrechnung-finanzen/regress
- Virchowbund Medikamente richtig verordnen: https://www.virchowbund.de/praxisaerzte-blog/medikamente-richtig-verordnen-so-vermeiden-sie-als-arzt-regresse

**Akademisch/Standards:**
- OpenCDS: https://opencds.org/
- OpenCDS CDS Hooks GitHub: https://github.com/DBCG/org-opencds-cqf-cds
- arriba-hausarzt.de: https://arriba-hausarzt.de/

**Hintergrund (Rechtsrahmen):**
- BMG Richtgrößen: https://www.bundesgesundheitsministerium.de/service/begriffe-von-a-z/r/richtgroessen-und-wirtschaftlichkeitspruefung.html
- arzt-wirtschaft Arzneimittelregress: https://www.arzt-wirtschaft.de/lexikon/arzneimittelregress
- ärztezeitung Systemwechsel: https://www.aerztezeitung.de/praxis_wirtschaft/regress/article/933307/voll-gange-systemwechsel-wirtschaftlichkeitspruefung.html
- Lauer-Taxe Wikipedia: https://de.wikipedia.org/wiki/Lauer-Taxe
- draco.de Richtgrößen: https://www.draco.de/richtgroessen-und-regress/

---

## Dokumenthistorie

- **2026-04-12 v1.0:** Erstellung Nachtrag durch Claude im Auftrag Lukas Geiger. Ergänzt MARKTVERGLEICH.md v1 um 15 gezielte Web-Recherchen + 4 WebFetches in sieben Kategorien. Wichtigster neuer Fund: medimed prescriber® (18.000+ Ärzte, §106-Primärzweck, aber retrospektiv).

---

*Dieses Dokument ist Arbeitsgrundlage. Vor Förderantrag oder Public Release sollten die in Abschnitt 8 benannten Demo-Zugänge und Kontaktaufnahmen (medimed, ifap, Uni Marburg) erfolgen. Die in Abschnitt 9 benannten offenen Fragen sind kein Blocker, aber sollten im Pilot-Phase-Plan adressiert werden. Änderungsvorschläge via Pull Request gegen das VerordnungsAmpel-Repository.*
