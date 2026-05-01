# Rechtliche Prüfung — Veröffentlichungsfähigkeit auf GitHub und Lizenz-Audit

**Projekt:** VerordnungsAmpel_SOCIAL
**Datum:** 2026-04-12
**RB:** Claude (CL), Um:bruch Rechtsabteilung
**Typ:** Zweites Folgegutachten (nach MDSW-Hauptgutachten und DSGVO-Konzept)
**Auftrag:** Lukas Geiger (Projekt-Initiator VerordnungsAmpel_SOCIAL), 2026-04-12
**Status:** KI-basierte Erstanalyse — kein Anwaltsersatz (siehe Abschnitt 10)

---

## Inhaltsverzeichnis

1. Gegenstand und Bezug zu Haupt- und DSGVO-Gutachten
2. Veröffentlichungsfähigkeit auf GitHub (ToS, Medical-Content, Sanctions)
3. Urheberrechtliche Analyse der Repository-Inhalte
4. Namens- und markenrechtliche Prüfung
5. Lizenz-Audit (Hauptlizenz, Dependencies, Content, Copyright)
6. CONTRIBUTING / DCO / CLA
7. Organisation — Beibehaltung `research-line` vs. eigene Org
8. Checkliste vor Public Release (Gate-Items)
9. Empfehlung für den Transitionspfad PRI → PUB
10. Grenzen dieser Einschätzung, Anwaltsempfehlung
11. Quellenverzeichnis

---

## 1. Gegenstand und Bezug zu anderen Gutachten

### 1.1 Auftrag

Geprüft werden zwei konkrete Mandantenfragen:

1. Darf das Projekt **VerordnungsAmpel** auf GitHub (aktuell privat in `research-line/verordnungsampel`, später geplant public) veröffentlicht werden?
2. Sind die gesetzten **Lizenzen** (`LICENSE`, `pyproject.toml`, Dependency-Lizenzen, Content-Lizenzen) korrekt?

### 1.2 Abgrenzung zu bereits vorliegenden Gutachten

Dieses Gutachten baut auf zwei Vorarbeiten auf:

- **`RECHTSGUTACHTEN_MDSW.md`** (12.04.2026, CL) — stellt fest, dass die VerordnungsAmpel bei sauberer Zweckbestimmung **kein Medizinprodukt** i. S. v. Art. 2 Nr. 1 MDR ist. Ausschlaggebend: keine patientenspezifische Datenverarbeitung (Abgrenzung nach EuGH C-329/16 — Snitem), reine Katalog-Lookup-Funktion ohne Interpretation.
- **`DSGVO_KONZEPT.md`** (12.04.2026, CL) — stellt fest, dass die Software als lokales Werkzeug keine personenbezogenen Patientendaten im klassischen Sinn verarbeitet; DSGVO-Rollen sind: Vertragsarzt = Verantwortlicher; Um:bruch/Lukas Geiger = Hersteller, **weder** Auftragsverarbeiter **noch** Verantwortlicher.

Beide Vorarbeiten sind **Grundlage** des vorliegenden Gutachtens. Wo sie ihre Aussagen relativieren (z. B. Notwendigkeit eines Disclaimers, sauberen Zweckbestimmungstextes), übernimmt dieses Gutachten diese Relativierungen übergangslos.

### 1.3 Prüfmaßstab

| Bereich | Normen / Leitlinien |
|---|---|
| GitHub-Nutzungsbedingungen | GitHub Terms of Service (Stand 2024, inkl. Privacy Statement 2024); GitHub Acceptable Use Policies (AUP); GitHub and Trade Controls (OFAC/EAR) |
| Medizinprodukterecht | MDR (VO 2017/745); MDCG 2019-11 Rev. 1 (06/2025) — nur Cross-Check |
| Urheberrecht | §§ 5, 62, 63, 69a ff. UrhG; §§ 7, 8 UrhG |
| Markenrecht | §§ 14, 23 MarkenG; DPMA-Register |
| Open-Source-Lizenzen | GPL-3.0-or-later; LGPL-3.0 (PySide6); MIT (pytest, pytest-qt); PSF (Python Stdlib); GNU License Compatibility Matrix |
| REUSE-Compliance | REUSE Specification Version 3.3 (FSFE); SPDX License List v3.28 |

---

## 2. Veröffentlichungsfähigkeit auf GitHub

### 2.1 GitHub Terms of Service und Acceptable Use Policies

GitHub (Inc., US-Unternehmen mit Sitz in San Francisco, seit 2018 Microsoft-Tochter) unterwirft alle Inhalte den GitHub Terms of Service sowie den GitHub Acceptable Use Policies (AUP). Die AUP schließen folgende Inhalte/Verhalten aus (relevant hier):

| Ausschlussgrund | Kurzprüfung VerordnungsAmpel |
|---|---|
| Aktive Malware, Exploits, Phishing-Kits | nicht einschlägig |
| Urheberrechts-/Markenverletzung | siehe Abschnitt 3 und 4 (unproblematisch) |
| Doxing, Privacy-Verletzung | keine personenbezogenen Daten Dritter im Repo (siehe 2.5) |
| Unlawful, abusive, defamatory, fraudulent | nicht einschlägig |
| Inaccurate or scientifically unsupported medical claims that endanger public health | **relevant — siehe 2.2** |
| Sanctioned countries / SDN-parties | Entwickler in DE, nicht einschlägig |

**Zwischenergebnis:** Keine der AUP-Ausschlusskategorien trifft auf den inhaltlichen Kern des Repos zu.

### 2.2 Medizinbezogene Inhalte auf GitHub

Die GitHub AUP verbieten medizinisch **irreführende** oder **wissenschaftlich unbelegte** Aussagen, die „public health or safety" gefährden. Sie verbieten **nicht** medizinische Software oder medizinbezogene Inhalte generell. Zahlreiche etablierte Projekte dieser Kategorie (OpenMRS, OHDSI, GNU Health, FHIR-Implementations) sind dauerhaft auf GitHub gehostet.

Die VerordnungsAmpel ist:

- **faktentreu** (Quellenverweise auf AM-RL, PRISCUS 2.0, § 31 SGB V, BSG-Urteile),
- **nicht diagnostisch** (gibt keine medizinische Empfehlung, nur juristisch-administrative Plausibilität),
- mit eindeutigem **Disclaimer** versehen (README.md, LICENSE, PDFs).

Damit liegt **kein AUP-Konflikt** vor.

**Empfehlung (Mindestkennzeichnung):** Der Haftungshinweis „Informationswerk — kein Medizinprodukt" soll an drei Stellen sichtbar sein:

1. In der GitHub-Repository-Description (einzeilig, englisch: *„Open-source reference tool for German outpatient physicians — information/reference work, not a medical device."*).
2. Im Kopf der README.md (bereits so vorhanden, Zeile 24 DE / Zeile 145 EN).
3. Im LICENSE-Anhang (bereits vorhanden).

### 2.3 US-Sanktionen und Exportkontrolle

GitHub unterliegt US-Recht (OFAC, EAR, ITAR). Relevant ist das Dokument „GitHub and Trade Controls". Gesperrt bzw. eingeschränkt sind Nutzer in Crimea, Kuba, Iran, Nordkorea und Syrien; für Iran gibt es eine OFAC-Lizenz, die auch private Repositories und GitHub Actions erlaubt.

**Relevanz für VerordnungsAmpel:** keine. Projekt entsteht in Deutschland, Entwickler und vorgesehener Nutzerkreis (Vertragsärzte in DE) liegen **außerhalb** aller SDN-Länder. Der Code enthält **keine Dual-Use-Güter** nach EAR (keine Kryptographie-Exportbeschränkungen: nur Standard-Python-Hashbibliothek `hashlib`, keine eigene Krypto-Implementierung).

Keine Auflagen aus der Exportkontrolle ableitbar.

### 2.4 Urheber und Trägerfrage — Um:bruch als nicht eingetragener Verein

**Hintergrund:** Um:bruch (Think Tank) ist gegenwärtig **kein eingetragener Verein**. LICENSE schreibt „Lukas Geiger / Um:bruch e.V."; das suggeriert eine juristische Person, die es **noch nicht** gibt (vgl. `Konzeption/RECHTSFORM.md`: e.V. vs. gUG in Prüfung).

**Juristische Bewertung:**
- Urheber nach § 7 UrhG ist ausschließlich der Schöpfer des Werks. Das ist hier die **natürliche Person Lukas Geiger** (ggf. mit Ko-Autorenschaft der KI-Beiträge; Claude/Gemini sind als Werkzeuge zu behandeln, keine Miturheber nach deutschem Recht — vgl. BGH I ZR 112/22 zur Frage der „schöpferischen Leistung").
- „Um:bruch e.V." in der LICENSE-Datei ist **unrichtig**, weil der e.V. nicht existiert. Das ist zwar nicht sittenwidrig, kann aber im Streitfall als **Irreführung** (§ 5 UWG) oder als **unrichtige Angabe im Impressum** interpretiert werden.

**Empfehlung:** LICENSE-Zeile 4 ändern in:

```
Copyright (C) 2026 Lukas Geiger (c/o Um:bruch Think Tank)
```

Optional ergänzen: *„Um:bruch is an informal think tank; legal entity pending (planned as e.V.)."* Das schafft Transparenz ohne Falschbehauptung. Sobald der e.V. gegründet ist, kann die Zeile ergänzt werden („Lukas Geiger / Um:bruch e.V.") und eine Lizenzänderung per Neu-Commit dokumentiert werden.

### 2.5 Datenschutz der Repository-Inhalte

| Prüfpunkt | Status |
|---|---|
| Entwickler-Name im `pyproject.toml` | „Lukas Geiger, hallo@um-bruch.org" — Selbstnennung durch Urheber, **unproblematisch** (konkludente Einwilligung, Art. 6 Abs. 1 lit. f DSGVO berechtigtes Interesse an Urheberzuordnung). |
| Entwickler-Mail `hallo@um-bruch.org` | Projekt-Postfach, kein natürlich-personenbezogenes Mailkonto → **unproblematisch**. |
| Fiktive Beispiel-Pseudonyme in Tests (`P-4711`) | Nicht personenbeziehbar → **unproblematisch**. |
| „Dr. Mueller" im README-Beispielaufruf (Zeile 73) | Frei erfundener Mustername, vgl. „Max Mustermann" → **unproblematisch**, aber **Empfehlung:** ersetzen durch `--arzt "Dr. med. Musterarzt"` und `--praxis "Musterpraxis"`, um jeden Bezug zu realen „Dr. Müllern" zu vermeiden. |
| Echte Patientendaten | keine |
| AM-RL-Seed-Daten | öffentliche amtliche Werke (siehe 3.1) |
| Interne Steuerungsdateien (`AUFGABEN.txt`, `_codebases/`) | in `.gitignore` korrekt ausgeschlossen (Zeile 3, 74) ✅ |

**Blocker:** `AUFGABEN.txt` liegt aktuell im Projekt-Root (Self-Check Bash, Abschnitt „List project root"), ist aber via `.gitignore` Zeile 74 ausgeschlossen. Vor dem ersten `git init`/`git add` **prüfen**, dass AUFGABEN.txt nicht versehentlich vorher schon committet wurde (`git log --all --full-history -- AUFGABEN.txt`). Für ein neu zu erstellendes Repo unproblematisch.

### 2.6 Zwischenergebnis Veröffentlichungsfähigkeit

Das Repository ist — nach Behebung des LICENSE-Trägerhinweises (2.4) und zwei kosmetischer Anpassungen in README.md (2.5) — **veröffentlichungsfähig**. Keine AUP-, Sanktions- oder Datenschutzblocker.

---

## 3. Urheberrechtliche Analyse der Repository-Inhalte

### 3.1 AM-RL-Anlagen (G-BA-Richtlinien)

**Rechtslage:** § 5 Abs. 1 UrhG („amtliche Werke") stellt Gesetze, Verordnungen, amtliche Erlasse und Bekanntmachungen gemeinfrei. Richtlinien des Gemeinsamen Bundesausschusses sind **untergesetzliche Normen** nach § 92 SGB V und werden im Bundesanzeiger veröffentlicht (§ 94 Abs. 2 SGB V). Die h. M. (Wandtke/Bullinger-Marquardt, § 5 UrhG Rn. 14; Dreier/Schulze-Dreier, § 5 Rn. 10) und die Praxis des G-BA selbst behandeln AM-RL-Anlagen als amtliche Werke i. S. d. § 5 Abs. 1 UrhG. Sie sind **urheberrechtsfrei** und dürfen vollständig reproduziert werden.

Einschränkung: § 62 UrhG (Änderungsverbot) und § 63 UrhG (Quellenangabe) gelten analog. Die VerordnungsAmpel hält beides ein: die Seed-Daten geben jeweils `quelle`, `paragraph`, `g_ba_beschluss` an; der Originaltext wird nicht verändert, nur strukturiert abgebildet.

**Ergebnis:** AM-RL-Seed-Daten sind unproblematisch weiterverwendbar. **Empfehlung:** In `data/seed/README.md` einen Vermerk ergänzen: *„Die Inhalte der Anlagen III/V/VI stammen aus der Arzneimittel-Richtlinie des Gemeinsamen Bundesausschusses (§ 92 SGB V), amtliches Werk nach § 5 Abs. 1 UrhG. Stand: [Quartal]. Quelle: https://www.g-ba.de/richtlinien/3/"*.

### 3.2 PRISCUS 2.0

**Publikation:** Mann NK, Mathes T, Sönnichsen A, Pieper D, Blom JW, Thürmann PA: *Potentially inadequate medications in the elderly: PRISCUS 2.0 — first update of the PRISCUS list.* Dtsch Arztebl Int 2023; 120: 3–10. DOI: 10.3238/arztebl.m2022.0377. Publikation im Deutschen Ärzteblatt ist über PMC/PubMed frei zugänglich.

**Copyright-Status:** Das Deutsche Ärzteblatt publiziert nach eigener Policy die wissenschaftlichen Originalartikel (Heft „Medizin", ab 2021) unter **Open Access** (freier Online-Zugang). Die **Lizenz ist jedoch nicht durchgängig CC BY 4.0** — die aerzteblatt.de-AGB weisen Artikel als „frei zugänglich", aber „urheberrechtlich geschützt" aus (§§ 15 ff. UrhG). Für die **reine Fakteninformation** (Liste der 187 PIM-Wirkstoffe mit Altersbewertung) gilt jedoch **§ 69a UrhG (Schutz nur für Werke, nicht für bloße Fakten)** bzw. der Grundsatz, dass wissenschaftliche Erkenntnisse als solche **nicht urheberrechtlich schützbar** sind (BGH „Inkasso-Programm", I ZR 52/83; Fromm/Nordemann-A. Nordemann § 2 Rn. 40).

**Praktische Bewertung:** Die Übernahme der PRISCUS-2.0-Wirkstoffliste (ATC-Codes + Altersschwelle + PIM-Status) ist als Übernahme reiner Faktendaten zulässig; Urheberrecht bestünde an der **Darstellung** (Tabellenlayout, Erläuterungstexte), nicht an der Liste selbst. Die VerordnungsAmpel übernimmt **nur die Fakten**, nicht die redaktionellen Texte. Zitiert wird mit vollständiger Quellenangabe.

**Empfehlung:** `data/seed/priscus.json` muss einen Header-Kommentar oder eine Begleitdatei enthalten: *„Quelle: Mann et al., Dtsch Arztebl Int 2023; 120:3–10. DOI 10.3238/arztebl.m2022.0377. Die Wirkstoffliste ist als wissenschaftliche Tatsachensammlung nicht urheberrechtlich geschützt; die Textzitate werden unter dem Zitatrecht § 51 UrhG eingebettet."*

**Rest-Risiko:** Falls die VerordnungsAmpel irgendwann die **Original-Erläuterungstexte** (mehr als nur stichwortartig) einbezieht, wäre die Zulässigkeit über § 51 UrhG (Zitatrecht) hinaus nicht mehr gesichert — dann wäre entweder (a) Kontakt zum Deutschen Ärzteblatt/den Autoren aufzunehmen, oder (b) das Material als externes Nachschlagewerk zu verlinken statt einzubetten.

### 3.3 WHO ATC-Klassifikation

**Rechtslage:** Das ATC/DDD-System wird vom WHO Collaborating Centre for Drug Statistics Methodology (Oslo) gepflegt. Die Web-Version unter `atcddd.fhi.no` ist **kostenfrei**, der elektronische Datensatz (Excel) wird für 200 EUR verkauft. Das WHOCC untersagt **kommerzielle** Weiterverwendung/-verteilung; nicht-kommerzielle Nutzung und Web-Scraping sind zulässig, solange keine kommerzielle Aktivität erfolgt.

**Bewertung für VerordnungsAmpel_SOCIAL:** Das Projekt ist GPL-3.0 (nicht-kommerziell im Sinne „kein Verkauf"; Spenden-Finanzierung im Rahmen Prototype Fund / Um:bruch ist **keine kommerzielle Verwertung** i. S. d. WHOCC-Disclaimers, siehe analog OHDSI-Projekt). Die Übernahme einzelner ATC-Codes als Referenz in Seed-Daten — **ohne Nachbau des gesamten Index** — ist unproblematisch.

**Empfehlung:**
- Keine Komplett-Replikation des ATC-Index (wäre dubios).
- Stattdessen: Seed-Datei enthält nur die Codes, die für den Abgleich mit AM-RL/PRISCUS **konkret benötigt** werden.
- Quellenvermerk in `data/seed/atc.json` bzw. im entsprechenden Modul: *„ATC-Codes nach WHO Collaborating Centre for Drug Statistics Methodology (Oslo). Nutzung nicht-kommerziell im Sinne des WHOCC-Copyright-Disclaimers. Quelle: https://atcddd.fhi.no/atc_ddd_index/"*.

**Rest-Risiko:** Gering. Bei Wechsel zu kommerziellem Modell (Convenience-Pricing im Store, Cashcow) müsste die ATC-Nutzung neu bewertet und ggf. eine WHOCC-Lizenz erworben werden. Für SOCIAL/Open-Source-Fall keine Auflagen.

### 3.4 ICD-10-GM (BfArM)

**Rechtslage:** Das BfArM gibt die ICD-10-GM im Auftrag des BMG heraus. Nach BfArM-Downloadbedingungen (Stand 2025) sind die Dateien **kostenfrei**; ein Nutzungsvertrag kommt durch Download zustande; zu beachten sind § 62 UrhG (Änderungsverbot) und § 63 UrhG (Quellenangabe). **Wichtige Einschränkung:** der Original-Datenbestand im erworbenen Format darf nicht vollständig weitergegeben werden, **aber abgeleitete Mehrwertprodukte** dürfen hergestellt und vertrieben werden.

**Bewertung für VerordnungsAmpel:** Die Verwendung einzelner ICD-10-GM-Codes zur Referenzierung ist ein **abgeleitetes Mehrwertprodukt** (Plausibilitätsprüfung, keine Replikation des vollständigen Klassifikationswerks). Das ist nach BfArM-Bedingungen zulässig.

**Empfehlung:** Falls die Seed-Datenbank später größere Teile der ICD-10-GM spiegelt, Quellenvermerk ergänzen: *„ICD-10-GM nach BfArM, Version [Jahr], https://www.bfarm.de/DE/Kodiersysteme/Klassifikationen/ICD/ICD-10-GM/"*. Aktuell werden nur punktuell Codes referenziert — kein Ausweis nötig, aber empfohlen.

### 3.5 BSG-/LSG-/SG-Urteile

Entscheidungen deutscher Gerichte sind **amtliche Werke** nach § 5 Abs. 1 UrhG (wörtlich: „Entscheidungen und amtlich verfaßte Leitsätze zu Entscheidungen"). Damit gemeinfrei. Amtliche Aktenzeichen und Tenor dürfen zitiert werden.

Erwähnte Urteile:
- **BSG v. 05.11.2014, B 6 KA 26/13** (Dokumentation zum Zeitpunkt der Verordnung)
- **SG Marburg v. 14.02.2024, S 18 KA 96/23** (Praxisbesonderheiten)
- **LSG Baden-Württemberg v. 15.11.2023** (Wirtschaftlichkeitsprüfung)
- **EuGH v. 07.12.2017, C-329/16** (Snitem/Philips — nur im MDSW-Gutachten zitiert)

Sämtlich frei zitierbar. Keine Auflagen.

### 3.6 Rechtsgutachten im Repo (`docs/legal/*.md`)

**Werksart:** Die Gutachten (`RECHTSGUTACHTEN_MDSW.md`, `DSGVO_KONZEPT.md`, dieses Dokument) sind **eigenschöpferische Werke** i. S. v. § 2 Abs. 1 Nr. 1 UrhG (Sprachwerke) und genießen Urheberrechtsschutz.

**Urheber:** Lukas Geiger bzw. Um:bruch Think Tank (Claude und Gemini als Werkzeuge; eigenständiger Werksschutz für KI-generierten Text nach deutschem Recht strittig, aber Überarbeitung durch den menschlichen Nutzer etabliert Urheberschaft).

**Lizenzempfehlung:** Da sich die Gutachten inhaltlich auf öffentliche Rechtsfragen beziehen und andere Open-Source-Projekte/Vertragsärzte davon profitieren sollen, wird **CC BY 4.0** empfohlen. Das ist kompatibel zu GPL-3.0 für den Code (unterschiedliche Lizenzen für Code vs. Dokumentation sind SPDX-Standard) und entspricht der üblichen Praxis in wissenschaftsnahen Open-Source-Projekten (vgl. KDE, FSFE).

**Umsetzung:** Am Dateikopf jedes Gutachtens ergänzen:

```markdown
<!--
SPDX-FileCopyrightText: 2026 Lukas Geiger (Um:bruch Think Tank)
SPDX-License-Identifier: CC-BY-4.0
-->
```

Und in `LICENSES/CC-BY-4.0.txt` (REUSE-Struktur) den Volltext ablegen.

### 3.7 Seed-Daten-JSON — Auswahl und Struktur

Auch wenn die Einzelinhalte gemeinfrei sind, kann die **Auswahl, Anordnung und Strukturierung** der Seed-Daten ein eigenständiges **Datenbank-Werk** (§ 4 UrhG) oder ein **sui-generis-Datenbankschutz** nach §§ 87a ff. UrhG begründen.

**Empfehlung:** Für die Datenbank-Struktur der Seed-Daten eine explizite Lizenz setzen. Da die Daten in ein GPL-3.0-Programm eingebettet sind und als Ganzes funktional mit dem Code verzahnt bleiben, ist **GPL-3.0-or-later** (wie für den Code) konsistent. Alternative wäre CC0 (Public Domain Dedication) für maximale Wiederverwendbarkeit außerhalb des Projekts — das wäre für einen SOCIAL-Impact-fokussierten Think Tank die freundlichste Option.

**Vorschlag:** Die JSON-Dateien unter `data/seed/` erhalten den Header-Kommentar:

```json
// SPDX-FileCopyrightText: 2026 Lukas Geiger (Um:bruch Think Tank)
// SPDX-License-Identifier: CC0-1.0
// Inhalte: amtliche Werke nach § 5 UrhG (AM-RL) + wissenschaftliche Fakten (PRISCUS 2.0)
// Struktur und Auswahl: CC0-1.0 (zur maximalen Wiederverwendung)
```

JSON erlaubt keine Kommentare nativ; alternativ eine Begleitdatei `data/seed/README.md` mit SPDX-Header.

---

## 4. Namens- und markenrechtliche Prüfung

### 4.1 „VerordnungsAmpel" — Eintragungsfähigkeit und Kollisionen

**Vorgehen:** Eine vollständige DPMA-Recherche wurde im Rahmen dieses Gutachtens **nicht** durchgeführt (keine Umlaut/Schreibvariations-Prüfung im DPMAregister möglich in dieser Session). Eine **formelle DPMA-Identitäts- und Ähnlichkeitsrecherche** wird vor der Public-Veröffentlichung dringend empfohlen.

**Präliminäre Einschätzung (ohne Registerzugriff):**
- „Verordnung" (Rezept / gesetzliche Regelung) und „Ampel" (Signalgeber, Metapher für Risiko-Signaling) sind **beschreibende** Begriffe.
- Die Kombination hat durchaus Unterscheidungskraft (§ 8 Abs. 2 Nr. 1 MarkenG) — vergleichbar mit „LebensmittelAmpel" oder „CO2-Ampel".
- Risiko eines Freihaltebedürfnisses nach § 8 Abs. 2 Nr. 2 MarkenG ist mittelgradig, weil „Verordnungsampel" ein plausibler generischer Begriff für Entscheidungshilfen im Verordnungskontext werden könnte.
- Eine **Wort-Bild-Marke** (mit Logo) wäre schutzfähiger als eine reine Wortmarke.

**Empfehlung:**

1. **DPMA-Recherche (formell):** Identität und Ähnlichkeit über DPMAregister (dpma.de) in den Klassen 09 (Software), 42 (Software-as-a-Service, wissenschaftliche Dienstleistungen), 44 (medizinische Dienstleistungen). Geschätzte Dauer: 20 Minuten via Webinterface. **Zwingend vor Markenanmeldung.**
2. **Markenanmeldung (optional, nicht zwingend vor Public Release):** Erst erwägen, wenn der Think Tank eine Rechtsform hat (e.V./gUG). Anmeldung kostet ab ca. 290 EUR (elektronisch, 3 Klassen). Ohne Marke bleibt der Schutz über Wettbewerbsrecht (§§ 3, 5 UWG — geschäftliche Bezeichnung nach § 5 Abs. 2 MarkenG bei Benutzung mit ausreichender Verkehrsgeltung).
3. **Für jetzt ausreichend:** Projektname auf GitHub verwenden, **keine** Markensymbole (®, ™) setzen. `™` (TM) wäre zulässig als Hinweis auf eine nicht eingetragene Marke, ist in der EU aber unüblich und kann Verwirrung stiften.

### 4.2 Nennung fremder Marken in Beispielen

Das README und die CLI-Beispiele nennen **fremde Marken**:
- „AOK Nordost" (Beispielaufruf Zeile 73)
- „TURBOMED", „MEDISTAR", „ALBIS" (KONZEPT.md — Marktanalyse)
- „BARMER", „TK" (nicht direkt im Repo, aber in Strategiedokumenten)

**Rechtsrahmen:** § 23 Nr. 2 und Nr. 3 MarkenG erlauben die Benennung fremder Marken, soweit sie **beschreibend** oder zur **Bestimmung des Zwecks** (Kompatibilitätshinweis, Vergleich, Bezugnahme) notwendig ist. Grenzen: kein Logo-Gebrauch, keine Verwechslungsgefahr, keine Anbieter-Verbindung suggerieren, keine Herabsetzung (§ 4 UWG).

**Bewertung:**
- „AOK Nordost" im Beispielbefehl: rein illustrativ, kein Logo, keine Suggestion einer Partnerschaft → **zulässig** nach § 23 Nr. 2 MarkenG (Nennung zur Bestimmung der Zweckbestimmung des Outputs).
- Marktanalyse-Nennungen: deskriptiv und recherchebelegt → **zulässig**.

**Empfehlung:**

1. Im README-Beispiel das Beispiel der Krankenkasse neutralisieren: `--kk "Musterkasse"` statt `--kk "AOK Nordost"`. Minimiert rein kosmetisch das (ohnehin geringe) Risiko einer Abmahnung.
2. In der KONZEPT.md keinen Änderungsbedarf, weil die Nennungen dort belegbar (Zi-Studie, Marktanalyse) und kritisch sind — zulässige Meinungsäußerung (Art. 5 GG).

### 4.3 „Therapiefreiheit e.V."

Im `KONZEPT.md` und `DSGVO_KONZEPT.md` wird „Therapiefreiheit e.V." als medizinischer Review-Partner bzw. Mit-Träger genannt. Sofern **kein tatsächlicher Kontakt / keine Vereinbarung** existiert (laut Memory-Notiz: „kein echter Kontakt"), ist die Nennung problematisch:

- **Irreführung** (§ 5 UWG): Suggestion einer Kooperation, die nicht besteht.
- **Namensrecht** (§ 12 BGB): Nennung eines fremden Vereinsnamens ohne Einverständnis ist zivilrechtlich angreifbar.

**Empfehlung (Blocker-Level):** Vor Public Release **zwingend** entweder

(a) formalen Kontakt mit Therapiefreiheit e.V. aufnehmen und schriftliche Zustimmung zur Nennung einholen, oder

(b) die Nennung im Repo ersetzen durch eine neutrale Formulierung, z. B. *„medizinischer Review-Partner (noch zu gewinnen)"* bzw. *„Kooperationspartner in Vorbereitung"*.

Relevante Dateien: `KONZEPT.md` (Kopfzeile Trägerschaft), `docs/legal/DSGVO_KONZEPT.md` (Abschnitt 2, 1.1).

### 4.4 „Um:bruch" als Selbstbezeichnung

Selbstbezeichnungen sind markenrechtlich unproblematisch (§ 14 MarkenG schützt nur Rechte Dritter, nicht die eigene Selbstbezeichnung). Die Domain `um-bruch.org` ist im Besitz des Mandanten. Kein Prüfbedarf.

---

## 5. Lizenz-Audit

### 5.1 Hauptlizenz

**Ist-Zustand:**
- `LICENSE` enthält GPL-3.0-Verweis, aber **nicht den Volltext** der GPL-3.0 (nur Kopf + Disclaimer, ca. 36 Zeilen, mit Link auf gnu.org). Das ist **nicht formal korrekt** — GPL-3.0 Abschnitt „How to Apply These Terms to Your New Programs" verlangt den vollständigen Lizenztext.
- `pyproject.toml`: `license = { text = "GPL-3.0-or-later" }` ✅ korrekt.
- README.md: „GPL-3.0-or-later" ✅ korrekt.

**Blocker #1:** LICENSE-Datei enthält nicht den vollständigen GPL-3.0-Lizenztext. GitHub's License Detection (Linguist / licensee) erkennt GPL-3.0 nur bei ≥90 % Textübereinstimmung mit dem SPDX-Template. Aktuell würde das Repo **keine** GPL-3.0-Badge von GitHub bekommen.

**Lösung:**

1. Den vollständigen GPL-3.0-Text von https://www.gnu.org/licenses/gpl-3.0.txt in `LICENSE` einfügen (ca. 674 Zeilen).
2. Den aktuellen Kopf (Projektbeschreibung + Disclaimer) **oberhalb** in einer separaten Datei `NOTICE` oder `DISCLAIMER.md` ablegen. Alternativ: beides in `LICENSE`, mit klarer Trennung: Erst GPL-3.0-Volltext, dann am Ende als Anhang die Projekthinweise.
3. Copyright-Zeile präzisieren: `Copyright (C) 2026 Lukas Geiger (c/o Um:bruch Think Tank)` (siehe 2.4).

**Passung von GPL-3.0 zum SOCIAL-Charakter:** GPL-3.0 (strong copyleft) passt zum SOCIAL-Charakter: kein proprietärer Fork möglich, jede Weiterverbreitung muss quelloffen erfolgen. Alternativ AGPL-3.0 wäre relevant, wenn das Tool als Webdienst gehostet würde (Art. 13 AGPL). Aktuell ist es ein lokales Tool → GPL-3.0 ausreichend. Falls die PWA-Variante später einen zentralen Dienst darstellt: **AGPL-3.0 erwägen** (SaaS-Loophole schließen).

### 5.2 Dependency-Lizenzen

| Paket | Lizenz | SPDX-ID | GPL-3.0-Kompatibilität | Distributionsauflagen |
|---|---|---|---|---|
| Python Stdlib (sqlite3, json, hashlib, argparse, datetime) | Python Software Foundation License 2.0 | `PSF-2.0` | ✅ kompatibel (FSF-bestätigt) | keine |
| **PySide6** ≥6.6.0 | LGPL-3.0-only (mit GPL-3.0-Option) | `LGPL-3.0-only` | ✅ kompatibel (LGPL→GPL-Upgrade erlaubt) | siehe 5.2.1 |
| pytest ≥7.0 | MIT | `MIT` | ✅ kompatibel | Dev-only |
| pytest-cov ≥4.0 | MIT | `MIT` | ✅ kompatibel | Dev-only |
| pytest-qt ≥4.4 | MIT | `MIT` | ✅ kompatibel | Dev-only |

#### 5.2.1 PySide6-LGPL-Auflagen bei Distribution

Die LGPL-3.0 stellt drei zentrale Pflichten (Qt-Dokumentation „Obligations of the GPL and LGPL"):

1. **Dynamische Verlinkung:** PySide6 wird als separate Python-Bibliothek geladen, nicht statisch eingebunden → dynamische Verlinkung ist die Default-Annahme für Python-Imports → **Auflage erfüllt**.
2. **Hinweis auf LGPL:** Nutzer müssen über die Verwendung von PySide6 (LGPL) informiert werden → **über THIRD_PARTY_LICENSES.txt erfüllbar**.
3. **Austauschbarkeit:** Nutzer muss PySide6 gegen eine eigene Version austauschen können → bei `pip install PySide6` trivial erfüllt; bei PyInstaller/cx_Freeze-Binary-Bundling wird eine Relink-Option benötigt (siehe 5.2.2).

**Für VerordnungsAmpel (Source-Distribution via PyPI/GitHub):** Alle Pflichten erfüllt. **Keine gesonderte Aktion nötig**, außer Dokumentation in `THIRD_PARTY_LICENSES.txt`.

#### 5.2.2 Rest-Risiko Binary-Distribution

Wenn später eine Windows-EXE via PyInstaller gebaut und verteilt wird (z. B. Windows Store / `.msix`-Paket): Die PyInstaller-Bundles enthalten die PySide6-DLLs. Das wird nach Qt-Policy als **gekoppelte Distribution** gewertet. Auflagen:

- Offenlegung: LGPL-Text in der EXE-Verteilung beigelegt.
- Austauschbarkeit: Nutzer muss die Qt/PySide6-DLL gegen eine eigene austauschen können → bei PyInstaller Single-File-Executables ist das problematisch; Single-Folder-Distribution ist konform.

**Empfehlung:** Bei Binary-Distribution **Single-Folder**-Modus wählen und in `BINARY_LICENSES.txt` die Rekompilierungs-/Austausch-Anleitung dokumentieren. Alternativ: für Binaries auf das Gesamt-Copyleft der GPL-3.0 umsteigen (was ohnehin passiert, da das Gesamtwerk GPL-3.0 ist — die LGPL-Austauschbarkeit bleibt erforderlich).

#### 5.2.3 Textvorschlag für `THIRD_PARTY_LICENSES.txt`

```
VerordnungsAmpel — Third-Party Software Notices

This product includes software developed by third parties. The respective
licenses are reproduced below.

================================================================================
Python Standard Library
--------------------------------------------------------------------------------
Copyright (c) 2001-2026 Python Software Foundation; All Rights Reserved
License: PSF License Agreement for Python (PSF-2.0)
Full license: https://docs.python.org/3/license.html

================================================================================
PySide6  (Qt for Python)
--------------------------------------------------------------------------------
Copyright (c) The Qt Company Ltd. and Qt for Python contributors
License: GNU Lesser General Public License v3.0 (LGPL-3.0-only)
Full license: https://www.gnu.org/licenses/lgpl-3.0.txt

PySide6 is used as a Python binding for the Qt framework and is dynamically
linked at import time. Users may replace PySide6 with a modified version by
installing the desired package into the Python environment
(e.g. `pip install PySide6==<version>`).

================================================================================
pytest  (Development dependency)
--------------------------------------------------------------------------------
Copyright (c) 2004 Holger Krekel and others
License: MIT
Full license: https://github.com/pytest-dev/pytest/blob/main/LICENSE

================================================================================
pytest-cov  (Development dependency)
--------------------------------------------------------------------------------
Copyright (c) 2010 Meme Dough
License: MIT
Full license: https://github.com/pytest-dev/pytest-cov/blob/master/LICENSE

================================================================================
pytest-qt  (Development dependency)
--------------------------------------------------------------------------------
Copyright (c) 2015 Bruno Oliveira and pytest-qt contributors
License: MIT
Full license: https://github.com/pytest-dev/pytest-qt/blob/master/LICENSE

================================================================================
Data sources (non-software)
--------------------------------------------------------------------------------
Arzneimittel-Richtlinie des G-BA (Anlagen III/V/VI):
  amtliches Werk nach § 5 Abs. 1 UrhG (urheberrechtsfrei)
  Quelle: https://www.g-ba.de/richtlinien/3/
  Änderungsverbot nach § 62 UrhG, Quellenangabe nach § 63 UrhG beachtet.

PRISCUS 2.0:
  Mann NK et al., Dtsch Arztebl Int 2023; 120:3-10
  DOI 10.3238/arztebl.m2022.0377
  Wirkstoffliste als wissenschaftliche Fakteninformation nicht urheberrechtlich
  schutzfähig; Zitate unter Zitatrecht (§ 51 UrhG).

ATC-Codes:
  WHO Collaborating Centre for Drug Statistics Methodology (Oslo)
  Nutzung nicht-kommerziell; Quelle: https://atcddd.fhi.no/atc_ddd_index/

ICD-10-GM:
  BfArM, https://www.bfarm.de/DE/Kodiersysteme/Klassifikationen/ICD/ICD-10-GM/
  Nutzung gemäß Downloadbedingungen (2025);
  Änderungsverbot (§ 62 UrhG) und Quellenangabe (§ 63 UrhG) beachtet.

Entscheidungen von BSG, LSG, SG, EuGH:
  amtliche Werke (§ 5 Abs. 1 UrhG), urheberrechtsfrei.
```

### 5.3 Content-Lizenzen

Empfohlene Aufteilung (SPDX-Identifier in Klammern):

| Bereich | Lizenz | SPDX-ID | Begründung |
|---|---|---|---|
| Source-Code (`src/`, `tests/`, `*.bat`) | GPL-3.0-or-later | `GPL-3.0-or-later` | Projektkernlizenz, strong copyleft |
| Seed-Daten (`data/seed/*.json`) | CC0-1.0 | `CC0-1.0` | Maximale Wiederverwendbarkeit; Inhalte sind ohnehin gemeinfreie Fakten |
| Dokumentation (README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CHANGELOG) | GPL-3.0-or-later (konform GPL-3.0 Kap. 5) oder CC BY 4.0 | `GPL-3.0-or-later` oder `CC-BY-4.0` | GPL-3.0 ist für Dokumentation der Software ausreichend; CC BY 4.0 wäre permissiver. **Empfehlung: GPL-3.0-or-later lassen** (Konsistenz), CC BY 4.0 nur für **Gutachten**. |
| Rechtsgutachten (`docs/legal/*.md`) | CC BY 4.0 | `CC-BY-4.0` | Fachliche Texte, die breiter weiterverwendbar sein sollen (andere Projekte, Anwaltskanzleien) |
| Icons (`src/verordnungsampel/gui/icons/*.svg`) | CC BY 4.0 oder GPL-3.0-or-later | `CC-BY-4.0` | Sofern selbst erstellt; falls Drittquellen (z. B. Material Icons) → separate Lizenzliste |
| Screenshots (`README/screenshots/*.png`) | CC BY-SA 4.0 | `CC-BY-SA-4.0` | Share-Alike schützt vor unautorisierter Werbung |

### 5.4 Copyright-Header in Quellcode-Dateien

**Ist-Zustand:** Stichprobe unklar (Source wurde in diesem Gutachten nicht en détail durchleuchtet). In neuen Projekten ist es üblich, jede `.py`-Datei mit dem Standard-GPL-3.0-Header zu versehen:

```python
# SPDX-FileCopyrightText: 2026 Lukas Geiger (Um:bruch Think Tank)
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of VerordnungsAmpel.
#
# VerordnungsAmpel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# VerordnungsAmpel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
```

Der lange Block kann durch **REUSE-konforme Kurz-Header** ersetzt werden:

```python
# SPDX-FileCopyrightText: 2026 Lukas Geiger (Um:bruch Think Tank)
# SPDX-License-Identifier: GPL-3.0-or-later
```

Das genügt der REUSE Specification v3.3, solange im Projekt-Root eine `LICENSES/GPL-3.0-or-later.txt`-Datei existiert (REUSE-Konvention).

### 5.5 REUSE-Compliance

**Empfehlung: ja, REUSE-Compliance anstreben**, weil:

- Saubere Lizenzzuordnung Datei-für-Datei (wichtig bei heterogenen Lizenzen wie GPL-3.0 + CC-BY-4.0 + CC0-1.0).
- Automatisierbar via `reuse lint` (CI-tauglich).
- Entspricht der Praxis moderner Open-Source-Projekte (FSFE, KDE, Qt seit 2022 auf SPDX umgestellt).
- Schafft Rechtsklarheit bei späteren Audits (z. B. OFA/Prototype Fund, SAFE-FOSS-Reviews).

**Konkrete Umsetzung:**

1. `LICENSES/` Verzeichnis anlegen mit:
   - `GPL-3.0-or-later.txt` (Volltext)
   - `CC-BY-4.0.txt`
   - `CC0-1.0.txt`
   - `LGPL-3.0-only.txt` (für PySide6-Referenz)
   - `MIT.txt` (für pytest-Referenz)
   - `PSF-2.0.txt` (für Python)
2. Jede Datei erhält SPDX-Tag (Header-Kommentar); bei nicht kommentierbaren Dateien (JSON, PNG): `.license`-Sidecar-Datei oder Eintrag in `.reuse/dep5`.
3. CI-Workflow: `uses: fsfe/reuse-action@v3` in `.github/workflows/reuse.yml` ergänzen.

### 5.6 Zwischenergebnis Lizenz-Audit

**Sind die Lizenzen korrekt?** — Zwei Schwächen:

1. **LICENSE-Datei enthält nicht den GPL-3.0-Volltext** (Blocker, leicht zu beheben).
2. **„Um:bruch e.V." existiert nicht** — Copyright-Zeile unrichtig (leicht zu beheben).

Im Übrigen: Lizenzwahl (GPL-3.0-or-later) ist **konsistent und kompatibel** mit allen Dependencies. Keine lizenzrechtlichen Konflikte.

---

## 6. CONTRIBUTING, DCO, CLA

### 6.1 Ist-Zustand

`CONTRIBUTING.md` nutzt **Developer Certificate of Origin (DCO)** — jeder Commit muss `--signoff` haben. Kein CLA erforderlich.

### 6.2 Bewertung

DCO ist für **reine GPL-Projekte** die **angemessene Form**. Ein CLA wird typischerweise dann gefordert, wenn:

- das Projekt **Dual-Licensing** (z. B. AGPL + proprietär) anstrebt,
- der Projektträger künftige Lizenzwechsel offenhalten will (z. B. von GPL auf Apache),
- eine **juristische Person** als Rechteinhaber etabliert werden soll (Patent-Grants, Gewährleistungsausschlüsse).

Keines dieser Szenarien trifft auf VerordnungsAmpel_SOCIAL zu. DCO ist ausreichend. (Analog zum Linux Kernel, Git selbst, Chef, GitLab für die Community-Edition.)

### 6.3 Empfehlung

DCO-Workflow beibehalten. Zusätzlich:

1. **`.github/PULL_REQUEST_TEMPLATE.md`** anlegen mit Checkboxen:
   - [ ] DCO-signoff vorhanden (`git commit --signoff`)
   - [ ] Tests bestanden
   - [ ] CHANGELOG.md aktualisiert
   - [ ] Bei neuen Regelwerken: Quellen-Referenz angegeben

2. **GitHub Branch Protection** (Admin-Setting, nicht im Repo):
   - `main`-Branch: PR-Review required, Status-Checks (Tests) required, DCO-Check required (via `https://github.com/apps/dco`).

### 6.4 Verhältnis zu Forschungs-RUO-Kennzeichnung

Laut Auftrag existiert ein paralleles RUO-Gutachten (Research Use Only). Eine RUO-Kennzeichnung **berührt die Lizenz nicht**. RUO ist eine **Zweckbestimmung** des Herstellers; die Lizenz GPL-3.0 regelt die **Verbreitung und Modifikation** des Codes. Beide Ebenen sind unabhängig. Falls RUO gewählt wird, ist das im README und in der `pyproject.toml` unter `keywords`/`classifiers` zu ergänzen (z. B. `Intended Audience :: Science/Research`), nicht in der Lizenz.

---

## 7. Organisation — Beibehaltung `research-line` vs. eigene Org

### 7.1 Aktueller Stand

Das Repo liegt unter `https://github.com/research-line/verordnungsampel` (privat). Die Organisation `research-line` beherbergt wissenschaftlich orientierte Projekte (z. B. `regressangst` = Um:bruch-Studie ST-001).

### 7.2 Optionen

| Option | Vorteile | Nachteile |
|---|---|---|
| **A) `research-line` beibehalten** | Konsistenz mit Parallel-Projekt `regressangst`; wissenschaftsnahes Branding; keine Migrationskosten | Naming suggeriert primär „Forschung" — VerordnungsAmpel ist aber auch ein Praxis-Tool |
| **B) Migration nach `lukisch` (persönlich)** | Volle Kontrolle, keine Multi-Org-Koordination nötig | Wirkt „Solo", reduziert Trägerwirkung des Think Tanks |
| **C) Neue Organisation `umbruch-tools` oder `umbruch-de`** | Klares Branding; eigener Projekt-Hub für Um:bruch-Softwareprojekte; wächst mit Think Tank | Aufwand: neue Org gründen, Billing, Forks, Issue-URLs aktualisieren |

### 7.3 Empfehlung

**Phase 1 (Prototype-Fund-Antrag, Pilot-Phase):** `research-line` beibehalten. Der wissenschaftliche Kontext passt zum Förderformat.

**Phase 2 (ab Go-Live, v1.0.0 oder Übergang zu e.V./gUG):** Migration zu einer eigenen Organisation `umbruch-tools` (oder analoger Name) **empfehlenswert**. Das signalisiert Eigenständigkeit, bündelt zukünftige Projekte (Regress-Melder, MetaMedia, weitere Um:bruch-Tools) und ist markenrechtlich sauberer.

GitHub unterstützt Transfers nativ (Settings → Transfer ownership), alle Issues/PRs/Stars werden mitverschoben, ein HTTP-Redirect bleibt dauerhaft bestehen. **Kein Breaking Change** für Nutzer, nur README-Update und neue Clone-URL.

---

## 8. Checkliste vor Public Release (Gate-Items)

Die folgende Checkliste ist **verbindlich** durchzugehen, bevor das Repository von `private` auf `public` geschaltet wird:

### 8.1 Rechtliche Gates

- [ ] **LICENSE-Datei:** GPL-3.0-Volltext vollständig eingefügt (≥ 90 % SPDX-Übereinstimmung für GitHub-License-Detection)
- [ ] **Copyright-Zeile:** „Um:bruch e.V." → „Lukas Geiger (c/o Um:bruch Think Tank)" (da e.V. nicht existiert)
- [ ] **MDSW-Gutachten:** Finalisiert (vorhanden, `RECHTSGUTACHTEN_MDSW.md`); optional: Fachanwalts-Review vor Release v1.0.0
- [ ] **RUO-Gutachten:** Entscheidung dokumentiert, relevante Kennzeichnung im README (ggf. „for research use / pilot deployment only")
- [ ] **DSGVO-Konzept:** Implementierung der CLI-Befehle E1–E8 (vgl. `DSGVO_KONZEPT.md`) — falls noch nicht umgesetzt, vor Public-Release nachholen
- [ ] **DPMA-Recherche „VerordnungsAmpel":** Formell durchgeführt (Klassen 09, 42, 44), Ergebnis in `docs/legal/MARKEN_RECHERCHE.md` protokolliert
- [ ] **„Therapiefreiheit e.V." im Repo:** Entweder schriftliche Kooperationszusage eingeholt oder Nennung neutralisiert (Blocker)

### 8.2 Datenschutz / Privacy

- [ ] Kein Eigenname „Dr. Müller" o. ä. in Beispielen — durch „Dr. med. Musterarzt"/„Musterpraxis" ersetzt
- [ ] Keine echten Krankenkassen-Namen in Beispielen (kosmetisch: „Musterkasse" statt „AOK Nordost")
- [ ] Keine realen Patientendaten, Pseudonyme, IPs, Mailadressen (außer `hallo@um-bruch.org` als Projektadresse)
- [ ] `AUFGABEN.txt`, `TEST*.txt`, `tmpclaude-*` nicht committet (verifiziert via `git log --all --full-history -- AUFGABEN.txt`)
- [ ] `_codebases/` (externe Referenz-Codes) nicht committet

### 8.3 Lizenz-Hygiene

- [ ] `THIRD_PARTY_LICENSES.txt` angelegt (Vorschlag in Abschnitt 5.2.3)
- [ ] `LICENSES/`-Verzeichnis mit SPDX-Volltexten (GPL-3.0-or-later, LGPL-3.0-only, MIT, CC-BY-4.0, CC0-1.0, PSF-2.0)
- [ ] SPDX-Header in `src/**/*.py` (optional, aber empfohlen)
- [ ] `.reuse/dep5` für Binary-Dateien ohne Kommentar-Möglichkeit (JSON, PNG)
- [ ] REUSE-Compliance-Check: `reuse lint` läuft durch

### 8.4 Inhaltliche Kennzeichnung

- [ ] README.md hat den „kein Medizinprodukt"-Disclaimer direkt nach dem Titel (Zeile 24/145 vorhanden ✅)
- [ ] GitHub-Repository-Description gesetzt (englisch, <150 Zeichen): „Open-source reference tool for German outpatient physicians — information work, not a medical device."
- [ ] GitHub-Topics gesetzt: `healthcare`, `germany`, `prescription`, `reference-tool`, `open-source`, `gpl-3`, `umbruch`
- [ ] AM-RL-Seed-Daten mit Quellenangabe (`data/seed/README.md`)
- [ ] Quellenangabe für PRISCUS 2.0 (`data/seed/priscus.json` oder Begleitdatei)

### 8.5 Release-Prozess (aus GITHUB-POLICY Abschnitt 8)

- [ ] CHANGELOG.md hat Eintrag für v0.2.0 (oder v1.0.0 bei stabiler Freigabe)
- [ ] `git tag -a v0.x.0 -m "..."` + `git push origin v0.x.0`
- [ ] GitHub Release erstellt (`gh release create v0.x.0 ...`)
- [ ] `.github/FUNDING.yml` angelegt (Spendenlinks — SOCIAL-Pflicht laut GITHUB-POLICY §10)
- [ ] `.github/ISSUE_TEMPLATE/bug_report.md` + `feature_request.md` angelegt (SOCIAL-Pflicht)
- [ ] Screenshots für GUI in `README/screenshots/` (GUI-Pflicht laut §1)

### 8.6 SOCIAL-spezifisch

- [ ] Spenden-Links in README (GitHub Sponsors / Ko-fi / Betterplace)
- [ ] Community-Kanäle: Discussions aktiviert, Issue-Labels gesetzt (`bug`, `enhancement`, `rechtsprechung`, `good-first-issue`)

---

## 9. Empfehlung für den Transitionspfad PRI → PUB

### 9.1 Phasenmodell

| Phase | Status | Ziel | Gate |
|---|---|---|---|
| **P0 – aktuell** | `research-line/verordnungsampel` PRI, v0.1.0 | Entwicklung, interne Reviews | MDSW/DSGVO-Gutachten vorliegend ✅ |
| **P1 – Blocker-Behebung** | PRI | LICENSE fix, Copyright-Zeile, Therapiefreiheit-Klärung, DPMA-Recherche | Alle Items in 8.1 abgehakt |
| **P2 – Lizenz-Hygiene** | PRI | REUSE-Compliance, THIRD_PARTY_LICENSES.txt, SPDX-Header | Alle Items in 8.3 abgehakt |
| **P3 – Inhaltliche Feinpolitur** | PRI | README-Beispiele neutralisiert, Screenshots, FUNDING.yml, Issue-Templates | Alle Items in 8.4+8.5+8.6 abgehakt |
| **P4 – Pre-Public-Test** | PRI | Einladung 2–3 externer Reviewer (z. B. aus Prototype-Fund-Netzwerk), Feedback sammeln | Kein Finding mehr mit Schweregrad „blocker" |
| **P5 – Public-Go-Live** | `PUB`, v0.2.0 oder v1.0.0 | Repo auf public stellen, GitHub Release, Announcement (Um:bruch-Website + RSS + Social Media) | Alle Gates 8.x grün |
| **P6 – Post-Launch** | PUB | Org-Migration auf `umbruch-tools` (optional); Markenanmeldung DPMA (optional bei positiver Resonanz); AGPL-Wechsel prüfen, falls PWA kommt | Laufende Beobachtung |

### 9.2 Geschätzter Zeitaufwand

- P1: 2–4 h (inkl. DPMA-Recherche, Therapiefreiheit-Mail, LICENSE-Fix)
- P2: 2–3 h (REUSE-Setup + SPDX-Header)
- P3: 2 h (README-Politur + Template-Dateien)
- P4: 1–2 Wochen Reaktionszeit (abhängig von Reviewer-Verfügbarkeit)
- P5: 30 min

**Realistisch: 1–2 Arbeitswochen bis Public-Ready**, mit dem Großteil der Zeit in P4 (Reviewer-Feedback).

### 9.3 Kritikalitäts-Triage

**Kritisch (Blocker):**
- LICENSE-Volltext (Abschnitt 5.1)
- „Um:bruch e.V."-Angabe (Abschnitt 2.4)
- „Therapiefreiheit e.V."-Nennung ohne Zustimmung (Abschnitt 4.3)

**Wichtig (sollte vor PUB):**
- DPMA-Recherche (Abschnitt 4.1)
- THIRD_PARTY_LICENSES.txt (Abschnitt 5.2.3)
- Beispiel-Neutralisierung (Abschnitt 4.2)
- FUNDING.yml + Issue-Templates (GITHUB-POLICY-Pflicht)

**Optional / Nice-to-have:**
- REUSE-Compliance mit CI-Integration
- Markenanmeldung beim DPMA
- Migration zu `umbruch-tools`-Org

---

## 10. Grenzen dieser Einschätzung

### 10.1 Methodische Grenzen

- Dieses Gutachten ist eine **KI-basierte rechtliche Ersteinschätzung**, kein anwaltliches Gutachten i. S. d. RDG.
- Es ersetzt **keine** fachanwaltliche Prüfung für: Markenanmeldung beim DPMA, endgültige Lizenztext-Redaktion bei Binary-Distribution, Vertragsgestaltung mit externen Mitträgern (z. B. Therapiefreiheit e.V. bei tatsächlicher Kooperation).
- Es wurde **keine förmliche DPMA-Recherche** durchgeführt; diese muss vor Markenanmeldung bzw. ggf. vor Public-Release erfolgen.
- Ich habe **keine** Source-Datei-Einzelprüfung durchgeführt — die Stichprobe in Abschnitt 5.4 beruht auf der projektweiten Konvention. Vor Release sollte ein Skript (`reuse lint` oder vergleichbar) über alle Quelldateien laufen.

### 10.2 Anwaltsempfehlung

Für folgende Punkte wird eine **anwaltliche Zweitmeinung** empfohlen:

1. **Vor Markenanmeldung „VerordnungsAmpel":** Fachanwalt für Gewerblichen Rechtsschutz (z. B. über IHK-Vermittlung oder Brandeins-Liste, ca. 500–1000 EUR für Erstanmeldung inkl. Recherche).
2. **Bei Binary-Distribution im Windows Store / über Drittverteiler:** Prüfung der LGPL-Distributionsauflagen und AGBs des Stores (insb. Microsofts „Medizinsoftware"-Review, sofern getriggert).
3. **Bei tatsächlicher Kooperation mit „Therapiefreiheit e.V." oder dem künftigen Um:bruch-e.V.:** Kooperations-/Konsortialvertrag, Entwicklerverträge, ggf. Lizenz-Einräumungserklärung.
4. **Sobald ein Umsatz-/Förderfluss startet** (Prototype Fund, Spenden > Bagatellgrenze): Beratung zur Vereinsgründung (e.V./gUG) und zur Gemeinnützigkeit nach § 52 AO durch Steuerberater mit gemeinnützigkeitsrechtlicher Spezialisierung.

### 10.3 Beobachtungspflichten

- **GitHub AUP/ToS:** können sich ändern (letzte Änderung Microsoft-Ära: häufig einmal/Jahr). Bei größeren Repo-Milestones kurz querlesen.
- **G-BA AM-RL-Anlagen:** quartalsweise Aktualisierung (vgl. CONTRIBUTING.md). Seed-Daten entsprechend pflegen — das ist aber keine **rechtliche**, sondern eine **inhaltliche** Pflicht.
- **MDCG-Leitlinien:** MDCG 2019-11 Rev. 1 (06/2025) gilt; eine mögliche Rev. 2 würde die MDSW-Einstufung potenziell beeinflussen → dann MDSW-Gutachten aktualisieren.

---

## 11. Quellenverzeichnis

### 11.1 GitHub-Policies

- GitHub Acceptable Use Policies, https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies
- GitHub Terms of Service, https://docs.github.com/en/site-policy/github-terms/github-terms-of-service
- GitHub and Trade Controls, https://docs.github.com/en/site-policy/other-site-policies/github-and-trade-controls
- GitHub Blog, „Global software collaboration in the face of sanctions" (12.09.2019), https://github.blog/2019-09-12-global-software-collaboration-in-the-face-of-sanctions/

### 11.2 Gesetze und amtliche Regelwerke

- UrhG: §§ 5, 7, 8, 62, 63, 69a, 87a ff. UrhG — https://www.gesetze-im-internet.de/urhg/
- MarkenG: §§ 14, 23 MarkenG — https://www.gesetze-im-internet.de/markeng/
- UWG: §§ 3, 5 UWG — https://www.gesetze-im-internet.de/uwg_2004/
- BGB: § 12 BGB — https://www.gesetze-im-internet.de/bgb/
- SGB V: §§ 31, 92, 94, 106 SGB V — https://www.gesetze-im-internet.de/sgb_5/
- MDR, VO (EU) 2017/745, EUR-Lex CELEX:32017R0745

### 11.3 Rechtsprechung

- BGH, Urt. v. 09.05.1985, I ZR 52/83 („Inkasso-Programm")
- BGH, Urt. v. 11.06.2024, I ZR 112/22 (KI-generierte Werke, zur Urheberschaft)
- BSG, Urt. v. 05.11.2014, B 6 KA 26/13 (Dokumentation zum Verordnungszeitpunkt)
- SG Marburg, Urt. v. 14.02.2024, S 18 KA 96/23
- LSG Baden-Württemberg, Urt. v. 15.11.2023
- EuGH, Urt. v. 07.12.2017, Rs. C-329/16 (Snitem/Philips)

### 11.4 Open-Source-Lizenzen und Spezifikationen

- GNU General Public License v3, https://www.gnu.org/licenses/gpl-3.0.txt
- GNU Lesser General Public License v3, https://www.gnu.org/licenses/lgpl-3.0.txt
- GNU License Compatibility Matrix, https://www.gnu.org/licenses/gpl-faq.html
- Qt for Python — Obligations of the GPL and LGPL, https://www.qt.io/development/open-source-lgpl-obligations
- REUSE Specification v3.3, https://reuse.software/spec-3.3/
- SPDX License List, https://spdx.org/licenses/
- Developer Certificate of Origin, https://developercertificate.org/
- Kemitchell, „The Developer Certificate of Origin is Not a Contributor License Agreement" (2021), https://writing.kemitchell.com/2021/07/02/DCO-Not-CLA

### 11.5 Datenquellen

- G-BA, Arzneimittel-Richtlinie und Anlagen, https://www.g-ba.de/richtlinien/3/
- BfArM, ICD-10-GM, https://www.bfarm.de/DE/Kodiersysteme/Klassifikationen/ICD/ICD-10-GM/
- BfArM, Downloadbedingungen (2025), https://www.bfarm.de/SharedDocs/Downloads/DE/Kodiersysteme/downloadbedingungen-2025.pdf
- WHO Collaborating Centre for Drug Statistics Methodology, ATC/DDD Index, https://atcddd.fhi.no/atc_ddd_index/
- Mann NK, Mathes T, Sönnichsen A, Pieper D, Blom JW, Thürmann PA: *Potentially inadequate medications in the elderly: PRISCUS 2.0 — first update of the PRISCUS list.* Dtsch Arztebl Int 2023; 120: 3–10. DOI: 10.3238/arztebl.m2022.0377. https://www.aerzteblatt.de/archiv/229048/

### 11.6 Internes / Querverweise

- `docs/legal/RECHTSGUTACHTEN_MDSW.md` (Um:bruch/CL, 2026-04-12)
- `docs/legal/DSGVO_KONZEPT.md` (Um:bruch/CL, 2026-04-12)
- Projektinterne GitHub-Publishing-Policy (Um:bruch/LG, lokaler Stand 2026-02-22)
- `KONZEPT.md` (Projekt-Konzept, 2026-04-08)

---

**Gutachten-Status:** v1.0 — KI-basierte Erstanalyse. Für Blocker-Behebung und Public-Release direkt verwendbar; für Markenanmeldung und rechtsverbindliche Außenerklärungen anwaltliche Zweitmeinung einholen (Abschnitt 10.2).

**Autor:** Claude (CL) i. A. Um:bruch Rechtsabteilung (RB)
**Fassung vom:** 2026-04-12
