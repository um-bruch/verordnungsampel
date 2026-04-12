# Marktvergleich — VerordnungsAmpel_SOCIAL

**Datum:** 2026-04-12
**Autor:** Claude (CL), Um:bruch Research-Line
**Auftrag:** Lukas Geiger, Projekt-Initiator DEV_VerordnungsAmpel_SOCIAL
**Status:** Erstanalyse; WebSearch-basiert, keine Produkt-Demos durchgeführt
**Geltungsdauer:** Preise/Features veränderlich — bei Förderantrag erneut verifizieren

---

## 1. Einleitung und Methodik

### 1.1 Zweck

Diese Marktübersicht ordnet das Projekt **VerordnungsAmpel_SOCIAL** in die Landschaft bestehender Werkzeuge ein, die im ärztlichen Verordnungs-Workflow Entscheidungshilfen, Arzneimittel-Informationen, Interaktions-Checks oder Regress-Prävention liefern. Ziel ist kein Marketing-Vergleich, sondern eine belastbare Grundlage für:

- die Positionierung in `README.md` und Förderantrag (Prototype Fund),
- die Abgrenzung in der Rechtsprüfung (`docs/legal/RECHTSGUTACHTEN_MDSW.md`),
- ehrliche Transparenz gegenüber Pilot-Praxen und Fachöffentlichkeit,
- die Formulierung von Feature-Roadmap und Kollaborations-Schnittstellen.

### 1.2 Methodik

- **Quellen:** WebSearch über die offiziellen Hersteller-Seiten, Fachartikel (Deutsches Ärzteblatt, Medical Tribune), KBV-/KV-Veröffentlichungen, Wikipedia (zur Orientierung), regulatorische Dokumente (G-BA, GKV-SV).
- **Keine Produkt-Tests.** Alle Aussagen zu Funktionen stützen sich auf öffentliche Marketing- und Support-Seiten der jeweiligen Anbieter oder auf wissenschaftliche Publikationen. Features, die nicht öffentlich dokumentiert sind, sind als "n/a" oder "nicht öffentlich dokumentiert" markiert.
- **Bewusst ausgelassen:** Interne technische Spezifikationen der PVS-Hersteller (CGM, medatixx), die ohne Vertragsvereinbarung nicht zugänglich sind. Wo dennoch Bewertungen vorgenommen werden, sind sie als "Schätzung auf Basis öffentlicher Dokumentation" gekennzeichnet.
- **Disclaimer-Blacklist:** Formulierungen wie "Entscheidungsunterstützung", "KI-Diagnose" oder "Therapieempfehlung" werden im VerordnungsAmpel-Kontext bewusst gemieden, um die im MDSW-Gutachten getroffene Einstufung als "Informations- und Nachschlagewerk" nicht durch Marketing-Sprache zu unterlaufen.

### 1.3 Vergleichsdimensionen (25 Kriterien)

Siehe Abschnitt 3, Feature-Matrix.

### 1.4 Abgrenzung des Vergleichs

Nicht betrachtet werden Tools, deren Primärzweck weder Arzneimittel-Information noch Verordnungs-/Abrechnungsbegleitung für Vertragsärzte in Deutschland ist (z. B. reine Patientenportale, reine PVS-Abrechnungssoftware ohne Arzneimittel-Modul, reine Laborinformationssysteme).

---

## 2. Kurzprofile der recherchierten Tools

### 2.1 Kommerziell / Deutschland

#### 2.1.1 UpToDate / UpToDate Lexidrug (Wolters Kluwer)

- **Anbieter:** Wolters Kluwer Health (US, weltweite Vermarktung einschließlich EU)
- **Kurz:** Klinisches Nachschlagewerk mit evidenzbasierten Therapie-Empfehlungen, Drug-to-Drug-Interaction-Checker, medizinischen Kalkulatoren. Lexidrug (vormals Lexicomp) ist das in UpToDate integrierte Arzneimittel-Modul mit Dosierung, Interaktionen und Identifikation.
- **Preis:** Institutionelle Lizenzen nicht öffentlich ausgewiesen; Einzel-/Gruppenabos bis 19 Nutzer über Store verfügbar (kein Listenpreis öffentlich, Angebot auf Anfrage).
- **Zielgruppe:** Kliniker (Krankenhaus-dominiert), Einzelärzte, Studenten (mit Sonderpreisen).
- **Lizenz:** Kommerziell, proprietär.
- **Land:** Primär US, weltweit vertrieben; deutsche Nutzung v. a. im Krankenhaus.
- **Info-Stand:** 2026-04-12.
- **Links:** [wolterskluwer.com/uptodate](https://www.wolterskluwer.com/en/solutions/uptodate), [Lexidrug](https://www.wolterskluwer.com/en/solutions/uptodate/pro/lexidrug)

#### 2.1.2 AMBOSS

- **Anbieter:** AMBOSS GmbH (Berlin)
- **Kurz:** Medizinisches Wissensportal mit integrierter Arzneimitteldatenbank (Daten via ifap), Fortbildungsmodulen, Prüfungsvorbereitung. Zielt auf ärztliche Fortbildung und klinische Alltagsentscheidungen.
- **Preis:** Ärzt:innen 198 € / Jahr (ca. 16,50 € / Monat), Monatsabo 25 €; Rabatte für Marburger Bund (ca. 30 %), Hartmannbund (10 %); Klinik-Lizenzen separat.
- **Zielgruppe:** Ärzte (stationär + ambulant), Studenten.
- **Lizenz:** Kommerziell, proprietär.
- **Land:** DE, zunehmend internationaler.
- **Info-Stand:** 2026-04-12.
- **Links:** [amboss.com/de/preise](https://www.amboss.com/de/preise), [Arzneimitteldaten](https://www.amboss.com/de/arzneimitteldaten)

#### 2.1.3 Gelbe Liste Pharmindex (Vidal MMI)

- **Anbieter:** Medizinische Medien Informations GmbH (MMI), Langen
- **Kurz:** Klassisches Arzneimittelverzeichnis mit ATC-Systematik, Interaktionsprüfung, Fachinfos. MMI Pharmindex Pro ist der B2B-Webservice mit REST/SOAP-API zur Integration in Drittsoftware.
- **Preis:** Online-Basisversion für Fachkreise kostenfrei (nach Registrierung); Pharmindex Pro individuell kalkuliert, kein öffentlicher Listenpreis.
- **Zielgruppe:** Ärzte, Apotheker, Kliniken, Softwarehersteller (API).
- **Lizenz:** Kommerziell, proprietär.
- **Land:** DE.
- **Info-Stand:** 2026-04-12.
- **Links:** [mmi.de](https://www.mmi.de/gelbe-liste-pharmindex), [gelbe-liste.de](https://www.gelbe-liste.de/)

#### 2.1.4 Rote Liste / Fachinfo-Service

- **Anbieter:** Rote Liste Service GmbH (Berlin)
- **Kurz:** Verzeichnis aller in DE zugelassenen Arzneimittel mit Fachinformationen (PDFs tagesaktuell), App + Online-Version. Ca. 29.900 Medikamente, 1.994 Wirkstoffe.
- **Preis:** App und Online kostenfrei für Fachkreise; kommerzielle Datenlizenzen individuell.
- **Zielgruppe:** Ärzte, Apotheker, Pharma.
- **Lizenz:** Kommerziell, proprietär (Datenrechte bei der Rote Liste Service GmbH).
- **Land:** DE.
- **Info-Stand:** 2026-04-12.
- **Links:** [rote-liste.de](https://www.rote-liste.de/)

#### 2.1.5 ifap praxisCENTER

- **Anbieter:** ifap GmbH (München), Tochter der CompuGroup Medical AG
- **Kurz:** Arzneimitteldatenbank, die in über 60 PVS (u. a. CGM-Produkte) integriert ist. Liefert Verordnungshinweise, Interaktions-/Kontraindikations-Checks, Hinweise auf Praxisbesonderheiten und Nutzenbewertungs-Ergebnisse (AIS-Modul).
- **Preis:** Als PVS-Modul gebündelt, kein Standalone-Listenpreis öffentlich. Teil des PVS-Abos (PVS-Gesamtkosten laut Zi-Studie 130–600 €/Monat).
- **Zielgruppe:** Niedergelassene Ärzte (über PVS).
- **Lizenz:** Kommerziell, proprietär.
- **Land:** DE.
- **Info-Stand:** 2026-04-12.
- **Links:** [ifap.de](https://www.ifap.de/deu_de/), [praxisCENTER](https://www.ifap.de/deu_de/fuer-aerzte/ifap-praxiscenter.html)

#### 2.1.6 Lauer-Taxe / ABDA-Artikelstamm (CGM / WINAPO)

- **Anbieter:** CompuGroup Medical (CGM), Lauer-Fischer GmbH
- **Kurz:** Referenz-Datenbank des Apothekensektors für ca. 700.000 Artikel mit Preisen (AEK, AVK, Herstellerabgabepreis), Rabattverträgen, Engpassinformationen, Belieferbarkeit. 14-tägige Aktualisierung.
- **Preis:** Jahresabo, nach Nutzerzahl gestaffelt, kein öffentlicher Listenpreis.
- **Zielgruppe:** Apotheken (primär), Kliniken, Krankenkassen.
- **Lizenz:** Kommerziell, proprietär.
- **Land:** DE.
- **Info-Stand:** 2026-04-12.
- **Links:** [cgm.com/Lauer-Taxe](https://www.cgm.com/deu_de/loesungen/apotheke/apothekensysteme/lauer-taxe.html)

#### 2.1.7 KBV-Arztinformationssystem (AIS)

- **Anbieter:** KBV-Standard, umgesetzt durch die PVS-Hersteller
- **Kurz:** Seit Oktober 2020 gesetzlich vorgeschriebenes Modul in Verordnungssoftware, das G-BA-Nutzenbewertungen neuer Arzneimittel sichtbar macht (Zusatznutzen ja/nein, Therapiekosten pro Jahr). Eigenständiges Tool unter [ais.kbv.de](https://ais.kbv.de/).
- **Preis:** Inklusiv in jedem zertifizierten PVS; Web-Version für Ärzte kostenfrei zugänglich.
- **Zielgruppe:** Vertragsärzte.
- **Lizenz:** Gesetzlich vorgeschrieben; Umsetzung proprietär durch PVS-Hersteller.
- **Land:** DE.
- **Info-Stand:** 2026-04-12.
- **Bemerkung:** Die KBV hat selbst kommuniziert, dass das AIS missverstanden werden kann und Regressangst eher verstärkt — kein Schutz-, sondern ein Hinweis-Tool.
- **Links:** [ais.kbv.de](https://ais.kbv.de/), [Ärzteblatt-Artikel zu AIS](https://www.aerzteblatt.de/archiv/212740/Elektronische-Arzneimittelinformationen-Das-System-ersetzt-nicht-den-denkenden-Arzt)

#### 2.1.8 PVS-interne Verordnungsmodule (CGM TURBOMED / MEDISTAR / ALBIS, medatixx x.isynet, zollsoft tomedo)

- **Anbieter:** verschiedene (Marktführer CGM und medatixx, ca. 78 % Marktanteil)
- **Kurz:** In die PVS eingebaute Verordnungsmodule mit Arzneimitteldatenbank (oft via ifap), AIS-Integration, Interaktions-/Kontraindikations-Checks, e-Rezept-Ausgabe. tomedo explizit für Apple-Hardware.
- **Preis:** Gebündelt im PVS-Gesamtabo, Gesamtbelastung 130–600 €/Monat. Keine öffentlichen Listenpreise für Einzelmodule.
- **Zielgruppe:** Vertragsärzte.
- **Lizenz:** Kommerziell, proprietär.
- **Land:** DE.
- **Info-Stand:** 2026-04-12.
- **Bemerkung:** Eine dedizierte "Regress-Ampel" oder "Hash-Chain-Compliance-Log" ist in öffentlicher Produktdokumentation **nicht** beschrieben. Bestehende Ampel-Funktionen (z. B. in Bayern im AMTM-Kontext) sind **regionale KV-Rückmeldesysteme auf Quartalsbasis**, nicht Point-of-Prescription-Warnungen.
- **Links:** [CGM TURBOMED](https://www.cgm.com/deu_de/loesungen/praxissoftware/healthcare-software/cgm-turbomed.html), [CGM MEDISTAR](https://www.cgm.com/deu_de/loesungen/praxissoftware/healthcare-software/cgm-medistar.html), [tomedo](https://tomedo.de/praxissoftware/praxisprogramm-verordnungen/)

#### 2.1.9 Dr. Clever

- **Anbieter:** Simba n³ / Dr. Clever (Weinsberg)
- **Kurz:** EBM-Abrechnungsoptimierungs-Tool, das pseudonymisiert auf dem Praxisrechner läuft, Datenaustausch per .con-Datei mit dem PVS. Fokus: EBM-Abrechnung, nicht Arzneimittel-Verordnung.
- **Preis:** nicht öffentlich ausgewiesen, vermarktet mit "2.175 € Mehrhonorar pro Quartal im Durchschnitt".
- **Zielgruppe:** Hausärzte, Fachärzte (EBM-Abrechnung).
- **Lizenz:** Kommerziell, proprietär.
- **Land:** DE.
- **Info-Stand:** 2026-04-12.
- **Relevant, aber kein direktes Analogon:** Gleiches Companion-Modell (unabhängig vom PVS, pseudonymisiert), aber anderer Zweck (EBM statt Verordnung).
- **Links:** [dr-clever.de](https://dr-clever.de/)

### 2.2 Kommerziell / International

#### 2.2.1 Medscape Drug Interaction Checker

- **Anbieter:** WebMD Health (US)
- **Kurz:** Kostenloser Interaktions-Check zwischen bis zu 30 Wirkstoffen mit Schweregrad-Klassifikation (Contraindicated / Serious / Monitor Closely / Minor), Mechanismus-Beschreibung.
- **Preis:** kostenlos für Fachkreise (Registrierung).
- **Zielgruppe:** US-Ärzte primär; weltweit nutzbar, Inhalte US-zentriert.
- **Lizenz:** Kommerziell, proprietär; Nutzung kostenfrei.
- **Land:** US, weltweit zugänglich.
- **Info-Stand:** 2026-04-12.
- **Links:** [reference.medscape.com/drug-interactionchecker](https://reference.medscape.com/drug-interactionchecker)

#### 2.2.2 Epocrates

- **Anbieter:** Athenahealth / Epocrates (US)
- **Kurz:** Mobile-First Drug Reference, kostenloser Interaktions-Check (bis 30 Mittel), Pill-ID, 600+ medizinische Kalkulatoren. Premium-Version ("Plus") mit Leitlinien, Krankheitsinformation, ICD-Codes.
- **Preis:** Free-Tier; Plus-Tier kostenpflichtig (Preis öffentlich nicht durchgehend ausgewiesen).
- **Zielgruppe:** US-Ärzte, Medical Students, Pharmazeuten.
- **Lizenz:** Kommerziell, proprietär.
- **Land:** US.
- **Info-Stand:** 2026-04-12.
- **Links:** [epocrates.com](https://www.epocrates.com/discover)

#### 2.2.3 IBM/Merative Micromedex

- **Anbieter:** Merative (vormals IBM Watson Health)
- **Kurz:** Enterprise-Grade evidenzbasierte Arzneimittel-Datenbank mit RED BOOK (Preise für 300.000+ Artikel), AI-gestützter Suche, Interaktions-, Dosierungs- und Monographie-Modulen.
- **Preis:** Institutionelle Lizenz; Mobile-App 2,99 $/Jahr; Enterprise-Preise individuell.
- **Zielgruppe:** Kliniken, Pharmazeutische Hersteller, Apotheken (US-Markt).
- **Lizenz:** Kommerziell, proprietär.
- **Land:** US, international verfügbar.
- **Info-Stand:** 2026-04-12.
- **Links:** [merative.com/clinical-decision-support/micromedex](https://www.merative.com/clinical-decision-support/micromedex)

#### 2.2.4 Medi-Span (Wolters Kluwer) / First Databank

- **Anbieter:** Wolters Kluwer (Medi-Span), Hearst Health (First Databank)
- **Kurz:** OEM-Drug-Data-Anbieter mit Screening-Modulen für Interaktionen, Allergien, Dosierungen. In viele EMR/Pharmacy-Systeme eingebettet. Kein Endanwender-Produkt.
- **Preis:** B2B, nicht öffentlich.
- **Zielgruppe:** EMR-Hersteller, Krankenkassen, Pharmacy-Management.
- **Lizenz:** Kommerziell, proprietär.
- **Land:** US primär; Medi-Span mit Ausläufern in EU via Wolters Kluwer-Niederlassungen.
- **Info-Stand:** 2026-04-12.
- **Links:** [wolterskluwer.com/medi-span](https://www.wolterskluwer.com/en/solutions/medi-span)

### 2.3 Open-Source / Akademisch

#### 2.3.1 arriba Hausarzt (Philipps-Universität Marburg / DEGAM)

- **Anbieter:** Institut für Allgemeinmedizin Marburg, mit DEGAM
- **Kurz:** Shared-Decision-Making-Module für Hausärzte: kardiovaskuläre Prävention, VHF-Antikoagulation, Depressionsdiagnostik, Prostatakrebs-Früherkennung, PPI-Absetzen, Polypharmazie. Seit 2003 in cluster-randomisierten Studien evaluiert.
- **Preis:** Kostenlos als freie Software verfügbar. PVS-Integration für manche PVS.
- **Zielgruppe:** Hausärzte.
- **Lizenz:** "freie Software" (genaue Lizenzform nicht eindeutig publiziert).
- **Land:** DE.
- **Info-Stand:** 2026-04-12.
- **Relevant, aber kein direktes Analogon:** Gleiche Zielgruppe, Open-Source-Mindset, DE-Fokus — aber **Patienten-Gespräch** als Zielkontext, **nicht** Regress-/Wirtschaftlichkeits-Prävention. Keine Ampel gegen AM-RL, keine Praxisbesonderheiten-Erkennung, keine Hash-Chain.
- **Links:** [arriba-hausarzt.de](https://arriba-hausarzt.de/), [Uni Marburg](https://www.uni-marburg.de/de/fb20/bereiche/methoden-gesundheit/allgprmed/forschung/entscheidungen/arriba)

#### 2.3.2 OpenCDS

- **Anbieter:** Open-Source-Konsortium (ursprünglich Utah/USA)
- **Kurz:** Standards-basiertes Framework für Clinical Decision Support, unterstützt CDS Hooks und HL7 FHIR, nutzt JBoss Drools als Regel-Engine.
- **Preis:** Open Source, kostenfrei.
- **Zielgruppe:** EMR-Hersteller, Forschungseinrichtungen.
- **Lizenz:** Open-Source (Apache 2.0 lt. Repository).
- **Land:** US (Entwicklungsherkunft), weltweit einsetzbar.
- **Info-Stand:** 2026-04-12.
- **Links:** [opencds.org](https://opencds.org/)

#### 2.3.3 HL7 CDS Hooks / FHIR Clinical Reasoning

- **Anbieter:** HL7 International (Standard-Konsortium)
- **Kurz:** Standard (nicht Produkt) für Hook-basierte Integration von Entscheidungsunterstützung in EHR-Workflows. CDS Hooks 2.0 ist der aktuelle Stand.
- **Preis:** Spezifikation frei verfügbar.
- **Zielgruppe:** EHR-/PVS-Entwickler.
- **Lizenz:** HL7 Standard, Creative Commons.
- **Land:** global.
- **Info-Stand:** 2026-04-12.
- **Bemerkung:** Nicht selbst ein Tool, sondern Integrations-Standard. Relevant als mögliche Schnittstelle für eine künftige VerordnungsAmpel-PVS-Integration.
- **Links:** [cds-hooks.org](https://cds-hooks.org/), [HL7](https://cds-hooks.hl7.org/2.0/)

#### 2.3.4 openEHR Decision Logic Module (DLM) / GDL2

- **Anbieter:** openEHR Foundation (gemeinnützige Stiftung)
- **Kurz:** Guideline Definition Language 2 — formale Sprache zur Abbildung klinischer Leitlinien als IF-THEN-Regeln. Wird von Cambio Healthcare (Schweden) u. a. produktiv eingesetzt.
- **Preis:** Spezifikation frei; Tools (CDS Apps) teils kommerziell, teils open.
- **Zielgruppe:** Forschung, nordisch-skandinavischer Gesundheitssektor.
- **Lizenz:** Standard: Creative Commons; Implementierungen uneinheitlich.
- **Land:** global (europäisch stark).
- **Info-Stand:** 2026-04-12.
- **Links:** [specifications.openehr.org/GDL2](https://specifications.openehr.org/releases/CDS/latest/GDL2.html)

#### 2.3.5 OpenEMR / Twinlist / Plaisant (Medication Reconciliation)

- **Anbieter:** verschiedene akademische Projekte (USA)
- **Kurz:** Twinlist und Plaisant sind die zwei als Open-Source ausgewiesenen Medication-Reconciliation-Tools (Systematic Review Motter et al. 2024). Fokus: Abgleich von Medikationslisten beim Übergang Klinik↔Hausarzt.
- **Preis:** Open-Source, kostenlos.
- **Zielgruppe:** Forschung, Pilot-Einsätze.
- **Lizenz:** Open-Source (Details je Tool).
- **Land:** US primär; in Deutschland laut Hospital Pharmacy Europe kaum etabliert.
- **Info-Stand:** 2026-04-12.
- **Bemerkung:** Fokussiert auf Medikations-Abgleich, **nicht** auf Regress-Prävention oder Anlagen-III-Compliance. Keine Überschneidung mit VerordnungsAmpel-Kernzweck.
- **Links:** [Systematic Review (PMC 10700201)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10700201/)

#### 2.3.6 PRISCUS 2.0 Website

- **Anbieter:** BMBF-gefördertes Forschungsprojekt (Mann et al.)
- **Kurz:** Frei zugängliche Website mit der PRISCUS-Liste (177 Wirkstoffe, potenziell inadäquate Medikation im Alter).
- **Preis:** Kostenlos.
- **Zielgruppe:** Ärzte, Apotheker.
- **Lizenz:** Forschungs-Publikation, Liste frei abrufbar; Nutzung in Drittsoftware juristisch zu prüfen (keine offene Datenlizenz ausgewiesen).
- **Land:** DE.
- **Info-Stand:** 2026-04-12.
- **Links:** [priscus2-0.de](https://www.priscus2-0.de/)

### 2.4 Speziell Regress / Wirtschaftlichkeit

#### 2.4.1 KV-eigene Prüfungs-Rückmeldungen (AMTM Bayern, KV-Arzneimittel-Services)

- **Anbieter:** Regionale Kassenärztliche Vereinigungen (KVB, KVWL, KV Sachsen usw.)
- **Kurz:** Quartalsweise Feedback-Berichte an Ärzte zu Verordnungsverhalten, Arzneimitteltrends (AMTM Bayern mit Ampel), Ziel-Quoten (Generika, Leitsubstanzen), Regressbarometer.
- **Preis:** Für Mitglieder kostenlos (in KV-Beitrag enthalten).
- **Zielgruppe:** Vertragsärzte der jeweiligen KV.
- **Lizenz:** KV-intern, keine offene Nachnutzung.
- **Land:** DE, nach Bundesland unterschiedlich.
- **Info-Stand:** 2026-04-12.
- **Bemerkung:** Rückblickend (nach Quartalsende), **nicht** Point-of-Prescription. **Genau die Lücke**, die VerordnungsAmpel füllt.
- **Links:** [coliquio-insights.de/bayerische-wirkstoffpruefung](https://www.coliquio-insights.de/bayerische-wirkstoffpruefung/), [KV Berlin](https://www.kvberlin.de/fuer-praxen/alles-fuer-den-praxisalltag/verordnung/wirtschaftlichkeitspruefung)

#### 2.4.2 Virchowbund-Beratung / HARTMANN / arzt-wirtschaft.de

- **Kurz:** Publikationen, Online-Seminare, Rechtsberatung zum Thema Regress (keine Software).
- **Relevanz:** Informationsangebote, keine technischen Analoga.
- **Links:** [virchowbund.de](https://www.virchowbund.de/praxis-knowhow/abrechnung-finanzen/regress)

---

## 3. Feature-Matrix

Legende: ✅ voll vorhanden · 🟡 teilweise / eingeschränkt · ❌ nicht vorhanden · ❓ nicht öffentlich dokumentiert · n/a nicht anwendbar

| Kriterium | **VerordnungsAmpel** | UpToDate/Lexidrug | AMBOSS | Gelbe Liste | Rote Liste | ifap | AIS (KBV) | PVS-Module (CGM/medatixx) | Dr. Clever | Medscape | Epocrates | Lexicomp | Micromedex | arriba | OpenCDS | KV-AMTM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Preis-Modell** | Open-Source gratis | Abo (hoch) | Abo 198 €/a | Freemium | Freemium | PVS-Bundle | Inkl. PVS + frei | PVS-Bundle | Abo | Gratis | Freemium | Abo | Enterprise | Gratis | Open-Source | KV-Mitglied |
| **Zielgruppe** | Vertragsärzte DE | Kliniker weltweit | Ärzte/Studenten | Ärzte/Pharmazie | Ärzte/Pharmazie | Niedergelassene | Vertragsärzte | Niedergelassene | Ärzte (EBM) | US-Ärzte | US-Ärzte | Kliniker US | Kliniken | Hausärzte | EMR-Entwickler | Vertragsärzte |
| **Land/Rechtsraum** | DE | US/global | DE | DE | DE | DE | DE | DE | DE | US | US | US | US/intl. | DE | US/global | DE |
| **Ampel grün/gelb/rot** | ✅ | ❌ | ❌ | 🟡 (Schwere-Stufen) | ❌ | 🟡 (Hinweise) | ❌ | ❓ | ❌ | ✅ (4 Stufen) | 🟡 | ✅ | ✅ | ❌ | ❓ | 🟡 (AMTM Bayern) |
| **ICD-10-GM-Input** | ✅ | ❌ | 🟡 (Suche) | ❌ | ❌ | 🟡 | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 | ✅ (FHIR) | n/a |
| **ATC-Code-Support** | ✅ | ❓ | ❓ (ifap-Daten) | ✅ | 🟡 | ✅ | ✅ | ✅ | ❌ | ❓ | ❓ | ❓ | ❓ | ❌ | ✅ | ✅ |
| **AM-RL Anlage III integriert** | ✅ | ❌ | 🟡 | 🟡 | 🟡 | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **AM-RL Anlagen V/VI** | ✅ | ❌ | ❓ | ❓ | ❓ | ❓ | ❌ | ❓ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❓ |
| **PRISCUS 2.0 integriert** | ✅ | ❌ | ❓ | ✅ | ❓ | ❓ | ❌ | ❓ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 (Polypharm.) | ❌ | ❓ |
| **Praxisbesonderheiten-Erkennung (GKV-SV bundesweit)** | ✅ | ❌ | ❌ | ❌ | ❌ | 🟡 (Hinweis) | ❌ | 🟡 (Heilmittel-Rx) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 (rückbl.) |
| **Strukturierte Begründungspflicht (HSM, erzwungen)** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 (rule-based) | ❌ |
| **Vorab-Klärung KK-Antrag (Cannabis § 31 Abs. 6)** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 (Muster) |
| **Vorab-Klärung KK-Antrag (Soziotherapie § 37a, HKP § 37)** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❓ |
| **Manipulationssicherer Log (Hash-Chain)** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 (Audit-Log, nicht Hash-Chain) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Beweiskraft § 371a ZPO / § 630f BGB (dokumentiert)** | ✅ (Ziel) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❓ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Quartalsreminder KV-Kennziffern** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❓ | 🟡 (EBM) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 (rückbl.) |
| **Off-Label-Check BSG-Kriterien-Formular** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 (Mustervord.) |
| **Container-Logik (pflicht/verboten/stellungn./off_label)** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Integration in PVS** | 🟡 (Companion-Modus) | 🟡 | 🟡 (tomedo) | ✅ (API) | ❓ | ✅ (PVS-Kern) | ✅ (Pflicht) | ✅ (nativ) | 🟡 (Companion) | ❌ | ❌ | ❌ | ❌ | 🟡 | ✅ (CDS Hooks) | ❌ |
| **Verarbeitet Patientendaten** | ❌ (nur ICD+ATC) | ❌ (Info-Werk) | ❌ | ❌ | ❌ | 🟡 (via PVS) | ❌ | ✅ | 🟡 (pseudon.) | ❌ | ❌ | ❌ | ❌ | 🟡 (konsultat.) | ✅ | ❌ (aggreg.) |
| **DSGVO-Fokus aktiv kommuniziert** | ✅ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ✅ | ❌ | ❌ | ❌ | ❌ | 🟡 | ❓ | 🟡 |
| **Medical Device CE-Klasse** | ❌ (bewusst, Info-Werk) | ❌ (Info-Werk) | ❌ | ❌ | ❌ | ❓ | n/a | 🟡 (ggf. IIa für Module) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | n/a | n/a |
| **Lizenz / Source** | GPL-3.0-or-later | proprietär | proprietär | proprietär | proprietär | proprietär | proprietär | proprietär | proprietär | proprietär | proprietär | proprietär | proprietär | "freie Software" | Apache 2.0 | KV-intern |
| **Plattform** | CLI + PySide6 GUI + PWA (geplant) | Web+App | Web+App | Web+App | Web+App | Desktop (PVS) | PVS-Modul + Web | Desktop/Web | Desktop | Web+App | Mobile+Web | Web+App | Web+App | Web+PVS | Server | Web-Portale |
| **Offline-fähig** | ✅ | 🟡 | 🟡 (App) | 🟡 (App) | ✅ (App) | ✅ | 🟡 | ✅ | ✅ | 🟡 | ✅ | 🟡 | 🟡 | ✅ | ❌ | ❌ |
| **Quellenangabe (§ / Urteil / Anlage) pro Treffer** | ✅ | 🟡 (Studien) | 🟡 (Referenzen) | 🟡 (Fachinfo) | 🟡 (Fachinfo) | 🟡 | 🟡 (G-BA) | 🟡 | ❌ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ❓ | 🟡 |
| **CLI / API für Automation / LLM** | ✅ (CLI, skriptbar) | ❌ | ❌ | ✅ (REST/SOAP) | ❓ | ❓ (B2B) | ❌ | ❌ | ❌ | ❌ | ❌ | ❓ | ❓ | ❌ | ✅ (FHIR) | ❌ |
| **Update-Turnus Regeldaten** | Quartalsweise (geplant, GitHub Actions) | täglich | täglich | täglich | täglich | täglich (ifap) | Quartalsweise (G-BA) | ifap-Zyklus | monatlich | täglich | täglich | täglich | täglich | Release-Zyklus | Repo-Push | Quartalsweise |

**Hinweis zu 🟡 bei PVS-Modulen:** Die Binnen-Funktionalität der kommerziellen PVS-Module ist öffentlich nur partiell dokumentiert. Die Bewertungen "🟡" oder "❓" sind daher konservativ als "nicht verifiziert" zu lesen, nicht als Behauptung. Bei Förderantrag und README sollte dies transparent angegeben werden.

---

## 4. Analyse: Stärken und Schwächen der VerordnungsAmpel

### 4.1 Klare Stärken (belastbar belegt)

1. **§ 106 SGB V als Zweckbezug am Point-of-Prescription.** Kein anderes recherchiertes Tool zeigt am Verordnungspunkt Regress-Risikoindikatoren aus AM-RL Anlagen III/V/VI mit Container-Logik und Hash-Chain-Log. Die kommerziellen Tools (UpToDate, AMBOSS, Lexicomp) sind medizinische Informationswerke; Dr. Clever adressiert EBM-Abrechnung, nicht Arzneimittel-Verordnung; arriba adressiert Shared Decision Making; medimed prescriber® (siehe Nachtrag § 106) arbeitet rückblickend, nicht am Point-of-Prescription. Die VerordnungsAmpel füllt eine **belegte Workflow-Lücke**. Hinweis: Das Tool **verspricht keine Regress-Prävention** und nutzt diesen Begriff nicht als Zweckbestimmung — es ist ein Risikoindikatoren-Softwareentwurf zu Forschungszwecken.

2. **Hash-Chain-Compliance-Log mit Beweiskraftanspruch.** In der Recherche fand sich kein kommerzielles Arzneimittel-Tool mit einer expliziten kryptographischen Hash-Chain auf Ebene der einzelnen Verordnung plus dokumentiertem Anspruch auf Beweiskraft im Sozialgerichtsverfahren (§ 371a ZPO analog). PVS führen Audit-Logs, aber die öffentliche Doku-Tiefe reicht nicht bis zu einer kryptographischen Verkettung.

3. **Container-Logik (pflicht_vorab / verboten_vorab / stellungnahme / off_label).** Diese **saubere juristische Differenzierung** zwischen Fällen mit Pflicht zur Vorab-Klärung (§ 31 Abs. 6 Cannabis, § 37a Soziotherapie) und Fällen mit **Verbot** der Vorab-Klärung (§ 29 BMV-Ä) findet sich in keinem anderen Tool. AMBOSS, Gelbe Liste, ifap verweisen auf Rechtsgrundlagen, erzwingen aber keinen Workflow.

4. **Strukturierte Begründungspflicht als HSM (Hierarchical State Machine).** Die Erzwingung einer nachweisbaren, strukturierten Freitext-Eingabe vor Finalisierung der Verordnung und die Sealing-in-Log-Mechanik ist ein Unikat auf Basis der öffentlichen Produktdoku aller anderen Tools.

5. **Open-Source + DE-spezifisch + kostenlos.** arriba ist "freie Software", OpenCDS ist Apache 2.0 — aber keines der Tools kombiniert alle drei Eigenschaften mit einem Regress-Fokus auf deutsches Sozialrecht.

6. **Keine Patientendaten.** Durch die Beschränkung auf zwei anonyme Codes (ICD + ATC) bleibt die Architektur einfach und DSGVO-unbedenklich. Das ist gleichzeitig die rechtliche Grundlage für die Einstufung als Informationswerk (siehe RECHTSGUTACHTEN_MDSW.md, Schritt 2 Snitem-Subsumtion).

### 4.2 Klare Schwächen (ehrlich benennen)

1. **Tiefe der Arzneimittel-Datenbank.** Gelbe Liste, ifap und Lauer-Taxe halten ca. 30.000 – 700.000 Artikel mit tagesaktuellen Preisen, Rabattverträgen, PZN, Engpass-Daten. VerordnungsAmpel hat **keine PZN, keine Preise, keine Rabattverträge** und arbeitet mit ATC-Codes statt Produktebene. Das ist ein bewusster Trade-off, aber für einen Arzt, der kontextsensitiv nach "ist das das günstigste äquivalente Präparat?" fragt, unzureichend.

2. **UI-Reife.** Kommerzielle Anbieter investieren zweistellige Millionenbeträge in UX. Der Pre-Alpha-Stand der VerordnungsAmpel (CLI + PySide6-Tray) ist funktional, aber nicht wettbewerbsfähig mit ifap-praxisCENTER oder AMBOSS.

3. **Reichweite / Bekanntheit.** AMBOSS hat laut Marburger Bund/Hartmannbund fünfstellige Nutzerzahlen unter Ärzten. VerordnungsAmpel ist unbekannt.

4. **Keine tagesaktuelle Aktualisierung.** Gelbe Liste, ifap, Lauer-Taxe aktualisieren täglich bzw. zweiwöchentlich. Geplanter Quartalsbuild via GitHub Actions ist für AM-RL-Änderungen adäquat (G-BA publiziert quartalsweise), aber nicht für Rabattvertrags- oder Preisänderungen (die VerordnungsAmpel allerdings auch nicht abbildet).

5. **Keine Zertifizierung nach KBV-/GKV-Anforderungen.** Zertifizierte Verordnungssoftware (für e-Rezept, Heilmittel-Richtlinie) muss Kriterien nach KBV-Standard erfüllen. VerordnungsAmpel ist **bewusst** keine Verordnungssoftware, aber dieser Status sollte in der Kommunikation klar sein.

6. **Keine Interaktions- und Dosierungsprüfung.** Medscape, Epocrates, ifap und Lauer-Taxe liefern Wirkstoff-Interaktionen, Kontraindikationen, Dosierungsempfehlungen. VerordnungsAmpel verzichtet bewusst darauf (MDSW-Vermeidung). Ein Arzt muss für diese Fragen ein Drittsystem einsetzen.

### 4.3 Offene Positionierungs-Frage

Ist VerordnungsAmpel **Komplement** oder **Konkurrent** zu AMBOSS, ifap, den PVS-Modulen?

**Plausibelste Antwort:** Komplement. Die juristisch-sozialrechtlich-fokussierte Nische (Risikoindikatoren-Anzeige am Verordnungspunkt, § 106-Compliance-Log, Praxisbesonderheiten-Hinweise, BSG-konforme Begründungserfassung) ist von medizinischen Informationswerken nicht besetzt und würde sich in deren Produktstrategie auch nicht sinnvoll integrieren lassen, weil sie die MDSW-Klassifizierung dieser Werke verändern könnte.

---

## 5. Gap-Analyse: Welche Marktlücken füllt VerordnungsAmpel tatsächlich?

| Marktlücke | Beleg | Wird gefüllt durch VerordnungsAmpel |
|---|---|---|
| Point-of-Prescription-Warnung gegen **§-106-Regressrisiko** (nicht nur G-BA-Zusatznutzen wie AIS) | Ribbat 2023 (47 %), Goetz 2024 (27 % starke Rechtsangst), KBV-Kritik an AIS | ✅ Kernfunktion |
| Bundesweite **Praxisbesonderheiten-Erkennung** auf Basis GKV-SV-Liste (statt KV-spezifischer Heuristik) | Zi-Studie 2024, unterschiedliche KV-Regelwerke | ✅ Funktion 4 |
| **Erzwungene strukturierte Begründung** im Moment der Verordnung (SG Marburg 14.02.2024, BSG B 6 KA 26/13: nachträglich reicht nicht) | Rechtsprechung | ✅ Funktion 2 (HSM) |
| **Manipulationssicheres Dokumentations-Protokoll** mit potenzieller Beweiskraft vor Sozialgericht | Literatur Hash-Chain / Crosby 2009, § 371a ZPO | ✅ Funktion 5 |
| **Antrags-Assistenten für die fünf expliziten Pflicht-Vorab-Fälle** (Cannabis, HKP, Soziotherapie, Reha, Heilmittel-Sonderfälle) | § 31 Abs. 6, § 37, § 37a, § 40 SGB V | ✅ Funktion 3 |
| Warnung vor **verbotener** Vorab-Anfrage bei normalen Arzneimitteln (§ 29 BMV-Ä) — also Schutz **vor** eigener Falschhandlung | BMV-Ä | ✅ Container "verboten_vorab" |
| **Open-Source + DE-Sozialrechts-Fokus + quartalsweise Community-Regelpflege** | kein bestehendes Tool mit allen drei Eigenschaften | ✅ Projekt-Setup |

**Ergebnis:** Sieben konkrete, überprüfbare Marktlücken werden adressiert. Für jede einzelne Lücke gibt es Belege aus Rechtsprechung, Studien oder Verbände-Kommunikation.

---

## 6. Risiken und Überlappungen

### 6.1 Überlappungen mit Bestehendem

1. **ifap praxisCENTER** liefert laut Hersteller-Seite "Hinweise auf Praxisbesonderheiten". Der Funktionsumfang und die Bundesweitheit sind aus öffentlicher Doku nicht ablesbar. **Vor Förderantrag:** Screenshots oder Test-Installation einholen, um konkrete Überlappung messbar zu machen. Je nach Ergebnis kann die Funktion 4 ggf. **enger gefasst** oder **differenzierter** begründet werden.

2. **Medscape Drug Interaction Checker** nutzt eine 4-Stufen-Ampel (Contraindicated → Minor). Die Wording-Nähe zu "Ampel" ist oberflächlich; der Zweck (medizinische Interaktionen vs. sozialrechtliche Compliance) unterscheidet sich grundlegend.

3. **KV-AMTM Bayern** nutzt ein Ampel-System für Quartals-Feedback. VerordnungsAmpel arbeitet synchron (vor Verordnung), AMTM asynchron (nach Quartal).

4. **Dr. Clever** hat ein ähnliches Companion-Modell (PVS-unabhängig, pseudonymisiert, .con-Export). Für **EBM-Abrechnung**, nicht Arzneimittel. Keine direkte Überlappung, aber als Referenz für Produkt-Design und Arzt-Akzeptanz interessant.

### 6.2 Redundanz-Risiko

- Falls ein großer PVS-Hersteller eine "Regress-Ampel" als Modul ankündigt, könnte das die Nische schließen. Mitigation: Offene Lizenz (GPL-3.0-or-later), transparente Regelpflege, nicht-kommerzielle Positionierung. Das Projekt ist bewusst als reine OSS ohne eigene Trägerorganisation veröffentlicht — Dritte (Ärzteverbände, Forschungsgruppen, Civic-Tech-Initiativen) sind eingeladen, das Tool aufzugreifen und eigene Qualitätssicherungs- und Verbreitungsstrukturen aufzubauen.

- Falls die KBV das AIS um "Regress-Ampel-Funktionen" erweitert, könnte die Motivation der Ärzte, ein Drittsystem zu nutzen, sinken. Mitigation: Im Gutachten betont — VerordnungsAmpel ist **KV-unabhängig**, während das AIS in der Hand der KBV/GKV ist. Das Unabhängigkeits-Argument ist juristisch und projektpolitisch tragfähig.

### 6.3 Rechtsrisiken im Vergleich

- **UpToDate/AMBOSS** positionieren sich sprachlich als "Informationsangebot / educational purposes only" und sind nicht CE-zertifiziert. VerordnungsAmpel übernimmt diese Sprachregelung (siehe README, KONZEPT.md und Rechtsgutachten).
- **PVS-Module** mit Patienten-Medikationsplan-Anbindung können nach EuGH Snitem/Philips (C-329/16) zur MDSW werden. VerordnungsAmpel vermeidet dies durch Codes-only.

---

## 7. Empfehlungen für die Positionierung

### 7.1 Positionierung in README / Website

**Empfohlene Einleitungszeile (DE):**
> VerordnungsAmpel ist ein Open-Source-Nachschlagewerk für die sozialrechtliche Compliance (§ 106 SGB V, AM-RL Anlagen III/V/VI, GKV-SV-Praxisbesonderheiten) im ärztlichen Verordnungs-Workflow. Kein Medizinprodukt, keine Therapieempfehlung — sondern strukturierte Dokumentationshilfe und juristisch belastbarer Audit-Trail.

**Begriffs-Blacklist (aus MDSW-Gutachten):**
- Nicht: "Entscheidungsunterstützung", "KI-gestützte Therapieempfehlung", "klinisches Decision Support"
- Stattdessen: "Nachschlagewerk", "Plausibilitätsprüfung gegen öffentliche Regelwerke", "Dokumentationshilfe", "Compliance-Audit-Trail"

### 7.2 Differenzierung gegenüber den häufigsten Rück-/Kritikfragen

| Kritik | Antwort (faktenbasiert) |
|---|---|
| "Kann AMBOSS nicht alles davon?" | AMBOSS ist Arzt-Wissensplattform mit Arzneimitteldaten — kein Regress-Compliance-Log, keine AM-RL-III-Ampel im Moment der Verordnung, keine Vorab-Antragsassistenten, keine Hash-Chain. |
| "Ist das nicht mein PVS?" | Kein recherchiertes PVS hat in der öffentlichen Doku eine dedizierte Regress-Ampel mit strukturierter Begründungserzwingung und kryptographischer Hash-Chain. PVS haben Audit-Logs, aber nicht diese Tiefe. |
| "Warum Open Source, wenn es kommerzielle Tools gibt?" | Regelpflege bei AM-RL / PRISCUS / Praxisbesonderheiten soll **öffentlich nachvollziehbar** sein, nicht Herstellergeheimnis. Gerichte und Ärzte sollen die Regeln im Repo nachprüfen können. |
| "Ersetzt das mein AIS?" | Nein. AIS zeigt G-BA-Nutzenbewertung — ergänzend, nicht konkurrierend. |

### 7.3 Förderantrag-Narrativ

**Kernsatz:**
> Keines der in der Recherche April 2026 geprüften Tools (n = 15 Hauptprodukte, plus Standards/Rahmen) kombiniert AM-RL-Anlagen-III/V/VI-Ampel im Moment der Verordnung mit erzwungener strukturierter Begründung, Container-sensitivem Vorab-Klärungs-Workflow und manipulationssicherem Compliance-Log. Diese Kombination ist der spezifische Beitrag von VerordnungsAmpel_SOCIAL zur Schließung einer dokumentierten Versorgungs- und Rechtssicherheitslücke (Ribbat 2023, Goetz 2024, SG Marburg 14.02.2024).

**Abgrenzung für den Förderantrag:**
- arriba (Marburg / DEGAM) ist die nächstgelegene akademische Referenz — **nicht Konkurrent**, sondern Vorbild für wissenschaftlich evaluierte Open-Source-Arzt-Software in DE.
- Eine medizinische Review-Instanz (z. B. Therapiefreiheit e. V., DDG, BVDN, Virchowbund) wäre als Qualitätssicherungs-Mechanismus wertvoll — wird aber vom Urheber des OSS-Projekts NICHT aktiv angebahnt. Dritte können solche Kooperationen aufgreifen.

---

## 8. Offene Recherche-Lücken

1. **Genaue Funktionstiefe der PVS-Module** (CGM TURBOMED/MEDISTAR/ALBIS, medatixx x.isynet, tomedo) in Bezug auf: dedizierte Regress-Ampel, AM-RL-III-Erzwingung, Hash-Chain-Log, BSG-Off-Label-Formular. Nur mit Test-Zugang oder qualifizierten Pilot-Praxis-Interviews zu klären.
2. **MORE / MEDVERIS** (als Suche angefragt) haben keinen öffentlichen Software-Fußabdruck gefunden, den ich einem Regress-Präventions-Tool zuordnen könnte. Falls solche KV-nahen Tools existieren, sind sie nicht öffentlich vermarktet.
3. **Bestehende KV-interne Self-Check-Tools:** Einzelne KVen (KVB, KVWL, KV Sachsen) bieten Web-Portale und Broschüren; ob es interaktive Self-Check-Tools mit Code-Input gibt, konnte nur punktuell verifiziert werden.
4. **Versicherungs-Tools** (Regressversicherungen, Virchowbund-Mitgliedsleistungen): es wurde keine Software-Leistung identifiziert, sondern nur Beratung und Rechtsschutz.
5. **Genaue Lizenz von arriba** (MIT/GPL/eigene "freie Software"?) ist nicht zweifelsfrei bestätigt. Für einen Förderantrag, der arriba als Vorbild nennt, wäre eine Kontaktaufnahme mit Marburg sinnvoll.
6. **CE-Zertifizierung der PVS-Verordnungsmodule.** Ob diese in der Klasse IIa nach Regel 11 MDR fallen, ist nicht öffentlich eindeutig dokumentiert. BfArM-Register nur teilweise durchsucht.
7. **DrugSafe / vergleichbare AMTS-Systeme (Arzneimitteltherapie-Sicherheits-Tools).** Laut Rechtsgutachten als MDSW-Klasse-IIa-kategorisiert, aber nicht durchrecherchiert — sie sind thematisch nicht Regress, sondern Patientensicherheit.

Diese Lücken sind kein Blocker für einen Förderantrag, sollten aber im Pilot-Phase-Plan adressiert werden.

---

## 9. Quellenverzeichnis

Alle Links am 2026-04-12 abgerufen.

**UpToDate / Lexicomp / Medi-Span (Wolters Kluwer):**
- https://www.wolterskluwer.com/en/solutions/uptodate
- https://www.wolterskluwer.com/en/solutions/uptodate/pro/lexidrug
- https://www.wolterskluwer.com/en/solutions/medi-span

**AMBOSS:**
- https://www.amboss.com/de/preise
- https://www.amboss.com/de/arzneimitteldaten
- https://www.marburger-bund.de/bundesverband/meldungen/amboss-sorglos-abo-hoher-preisvorteil-fuer-mb-aerzte
- https://support.amboss.com/hc/de/articles/360056982912-Arzneimitteldatenbank

**Gelbe Liste / MMI / Rote Liste:**
- https://www.mmi.de/gelbe-liste-pharmindex
- https://www.mmi.de/mmi-pharmindex/mmi-pharmindex-pro
- https://www.gelbe-liste.de/
- https://www.rote-liste.de/
- https://www.rote-liste.de/produkte

**ifap / CGM / Lauer-Taxe:**
- https://www.ifap.de/deu_de/
- https://www.ifap.de/deu_de/fuer-aerzte/ifap-praxiscenter.html
- https://www.cgm.com/deu_de/loesungen/apotheke/apothekensysteme/lauer-taxe.html
- https://www.cgm.com/deu_de/loesungen/praxissoftware/healthcare-software/cgm-turbomed.html
- https://www.cgm.com/deu_de/loesungen/praxissoftware/healthcare-software/cgm-medistar.html
- https://de.wikipedia.org/wiki/Lauer-Taxe
- https://go.pharmazie.com/de/arzneimittel-rohdatenlizenzen/

**KBV / AIS / KV-Wirtschaftlichkeit:**
- https://ais.kbv.de/
- https://www.aerzteblatt.de/archiv/212740/Elektronische-Arzneimittelinformationen-Das-System-ersetzt-nicht-den-denkenden-Arzt
- https://www.medical-tribune.de/praxis-und-wirtschaft/abrechnung/artikel/arzneiinformationssystem-verordnungshilfe-oder-regressfalle
- https://www.kbv.de/praxis/verordnungen/arzneimittel/wirtschaftlichkeit
- https://www.kvberlin.de/fileadmin/user_upload/UEbersicht_der_Anlagen_der_Arzneimittel-Richtlinie.EY_DS_JK.pdf
- https://www.kbv.de/html/25289.php
- https://update.kbv.de/ita-update/Service-Informationen/Zulassungsverzeichnisse/KBV_ITA_SIEX_Verzeichnis_Zert_Software.pdf
- https://www.coliquio-insights.de/bayerische-wirkstoffpruefung/
- https://www.kvberlin.de/fuer-praxen/alles-fuer-den-praxisalltag/verordnung/wirtschaftlichkeitspruefung

**Medscape / Epocrates / Micromedex:**
- https://reference.medscape.com/drug-interactionchecker
- https://help.medscape.com/hc/en-us/articles/5019895680269
- https://www.epocrates.com/discover
- https://www.epocrates.com/products/features
- https://www.merative.com/clinical-decision-support/micromedex
- https://www.ibm.com/products/micromedex-red-book

**arriba / DEGAM:**
- https://arriba-hausarzt.de/
- https://www.uni-marburg.de/de/fb20/bereiche/methoden-gesundheit/allgprmed/forschung/entscheidungen/arriba
- https://www.degam.de/pressemitteilung-detail/studie-ueberversorgung-mit-magensaeureblockern-abbauen
- https://de.wikipedia.org/wiki/Arriba-Rechner

**OpenCDS / CDS Hooks / openEHR:**
- https://opencds.org/
- https://cds-hooks.org/
- https://cds-hooks.hl7.org/2.0/
- https://specifications.openehr.org/releases/CDS/latest/GDL2.html
- https://gdl-lang.org/

**PRISCUS 2.0:**
- https://www.priscus2-0.de/
- https://www.akdae.de/arzneimitteltherapie/arzneiverordnung-in-der-praxis/ausgaben-archiv/ausgaben-ab-2015/ausgabe/artikel?tx_lnsissuearchive_articleshow%5Barticle%5D=5503

**Regress / Virchowbund:**
- https://www.virchowbund.de/praxis-knowhow/abrechnung-finanzen/regress
- https://www.virchowbund.de/praxisaerzte-blog/wirtschaftlich-verordnen-was-heisst-das
- https://www.bundesgesundheitsministerium.de/service/begriffe-von-a-z/r/richtgroessen-und-wirtschaftlichkeitspruefung.html
- https://dr-clever.de/

**Off-Label / Cannabis / MD-Bund:**
- https://md-bund.de/fileadmin/dokumente/Publikationen/GKV/Begutachtungsgrundlagen_GKV/BGL_Off-Label-Use_240701.pdf
- https://md-bund.de/aktuell/aktuelle-meldungen/richtlinie-zur-begutachtung-von-cannabinoiden-ueberarbeitet.html
- https://www.kbv.de/html/cannabis-verordnen.php
- https://www.kvb.de/mitglieder/verordnungen/arzneimittel/cannabis

**tomedo:**
- https://tomedo.de/praxissoftware/praxisprogramm-verordnungen/
- https://tomedo.org/

**Hash-Chain / Audit-Trail / Medication Reconciliation:**
- https://static.usenix.org/event/sec09/tech/full_papers/crosby.pdf (Crosby 2009)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10700201/ (Motter et al. 2024, e-MedRec Systematic Review)
- https://hospitalpharmacyeurope.com/news/medication-reconciliation-in-germany-a-special-challenge/

---

*Dieses Dokument ist als Arbeitsgrundlage gedacht und sollte vor Einreichung eines Förderantrags durch gezielte Produktdemonstrationen (ifap praxisCENTER, ein PVS aus der CGM-Familie) verifiziert werden. Verbleibende Unsicherheiten sind in Abschnitt 8 benannt. Änderungsvorschläge bitte per Pull Request gegen das VerordnungsAmpel-Repository oder als redaktioneller Kommentar im Um:bruch-Workflow.*
