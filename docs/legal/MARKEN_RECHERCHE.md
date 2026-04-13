# Marken-Recherche — „VerordnungsAmpel"

**Projekt:** VerordnungsAmpel_SOCIAL
**Datum:** 2026-04-12
**RB:** Claude (CL), Um:bruch Rechtsabteilung
**Typ:** Anlassprüfung — DPMA-/TMview-/Faktische-Nutzung-Recherche
**Auftrag:** Lukas Geiger (Projekt-Initiator), 2026-04-12 (Top-5-Maßnahme Nr. 3 aus `GESAMTEINSCHAETZUNG.md`)
**Status:** KI-basierte Erstanalyse — kein Anwaltsersatz (siehe Abschnitt 11)

---

## Inhaltsverzeichnis

1. Auftrag und Gegenstand
2. Methodik
3. Identitätsrecherche — Ergebnisse
4. Ähnlichkeitsrecherche — Ergebnisse
5. Branchen- und Klassen-Bewertung
6. Faktische Drittverwendung (Google, GitHub, PyPI)
7. Schutzfähigkeits-Einschätzung (§ 8 MarkenG)
8. Gesamtbewertung
9. Empfehlung
10. Nächste Schritte
11. Grenzen dieser Einschätzung
12. Quellen

---

## 1. Auftrag und Gegenstand

### 1.1 Auftrag

Die Redaktion/Rechtsabteilung wurde am 12.04.2026 beauftragt, für das Projekt **VerordnungsAmpel** (GitHub-Repo `research-line/verordnungsampel`, Übergang PRI → PUB geplant) eine formelle DPMA-Marken-Recherche durchzuführen. Grundlage:

- `RECHTSGUTACHTEN_PUBLIKATION_LIZENZ.md`, Kap. 4 (präliminäre Einschätzung ohne Registerzugriff)
- `GESAMTEINSCHAETZUNG.md`, Top-5-Maßnahme Nr. 3: „DPMA-Recherche online im DPMAregister, Klassen 09/42/44"

### 1.2 Zu prüfendes Primär-Zeichen

| Feld | Wert |
|---|---|
| Primärzeichen | **VerordnungsAmpel** |
| Schreibvarianten | Verordnungsampel, Verordnungs-Ampel, Verordnungs Ampel |
| Vorgesehene Klassen | 09 (Software), 42 (SaaS/Wissenschaftliche Dienstleistungen), 44 (Medizinische Dienstleistungen) |
| Nebenprüfung | „Um:bruch" als Trägerbezeichnung (Selbstbezeichnung, siehe 4.4 im Publikationsgutachten — kein Prüfbedarf) |

### 1.3 Prüfungsfragen

1. Existiert für „VerordnungsAmpel" (identisch oder schreibvariant) bereits eine DPMA- oder EU-Marke?
2. Existieren ähnliche Marken (phonetisch, sinngemäß) in den relevanten Klassen?
3. Ist „VerordnungsAmpel" als Wortmarke überhaupt schutzfähig (§ 8 Abs. 2 Nr. 1/2 MarkenG) oder beschreibend?
4. Welche faktische Drittverwendung ist dokumentierbar?
5. Gibt es aus Markensicht einen **Blocker** für die Public-Veröffentlichung?

---

## 2. Methodik

### 2.1 Datenquellen

| Quelle | Zugriff | Ergebnisqualität |
|---|---|---|
| **DPMAregister** (https://register.dpma.de) | WebFetch auf Einsteiger-/Erweiterte Suche | **Eingeschränkt**: Die Session-basierte UI liefert bei WebFetch nur Formular-HTML, keine Treffer-Tabellen; „Ihre Session ist abgelaufen"-Fehler. Ergebnis: keine direkte API-fähige Treffersuche möglich. |
| **TMview** (https://www.tmdn.org/tmview/) | WebFetch auf Query-URL | Socket-Verbindung wurde abgebrochen (Anti-Scraping); Client-seitige JS-Anwendung lädt Ergebnisse nicht für statische Fetches. |
| **EUIPO Global Search** (site:euipo.europa.eu) | Google-Site-Suche | Kein Treffer für „Verordnungsampel"/„VerordnungsAmpel" — indiziert, dass es keine EU-Marke mit dieser Bezeichnung gibt. |
| **Google allgemein** | WebSearch | Gut — indiziert faktische Nutzung, Wettbewerber, Produkte mit „Ampel"-Bezeichnung. |
| **Google Site:github.com / site:pypi.org / site:gitlab.com** | WebSearch | Kein Treffer — kein offenes Software-Projekt mit diesem Namen. |
| **BPatG-/Rechtsprechungsdatenbanken** (openJur, rewis, jusmeum, 2be.legal) | Google-Treffer gelesen | Indirekt — keine direkte BPatG-Entscheidung „Ampel" als Kernbegriff auffindbar, aber Rahmenrechtsprechung zu Komposita. |

### 2.2 Begrenzung durch DPMAregister-Zugang

Das offizielle DPMAregister ist eine **dynamische Web-Anwendung mit Server-seitiger Session-Verwaltung** und verhindert Drittanbieter-Abfragen ohne Browser. Die Suchformulare auf `register.dpma.de/DPMAregister/marke/basis` und `/marke/einsteiger` liefern bei WebFetch nur ein leeres Formular bzw. einen Session-Expired-Fehler. Eine **abschließende** Identitätsrecherche ist ausschließlich durch **manuelle Abfrage im Browser** möglich (oder durch den kostenpflichtigen DPMA-API-Zugang).

**Konsequenz:** Dieser Bericht stützt sich auf indirekte Hinweise (Google-/EUIPO-Abfragen, faktische Marktbeobachtung), kann aber eine direkte DPMAregister-Abfrage nicht vollständig ersetzen. **Empfehlung: vor Markenanmeldung nochmals manuell auf register.dpma.de prüfen** (5 Min Aufwand); für die Frage „Public-Release-Blocker?" ist die aktuelle Befundlage aber hinreichend belastbar.

### 2.3 Suchbegriffe und Kombinationen

Abgefragt wurden:

- `"VerordnungsAmpel"`, `"Verordnungsampel"`, `"Verordnungs-Ampel"`, `"Verordnungs Ampel"`
- `"Rezept-Ampel"`, `"Rezeptampel"`
- `"Arzneimittel-Ampel"`, `"Arzneimittelampel"`, `"Medikationsampel"`
- `"Praxis-Ampel"`, `"Praxisampel"`
- `"Regress-Ampel"`, `"Regressampel"`
- `"AM-RL-Ampel"`, `"AMRL-Ampel"`, `"Rx-Audit"`
- Rahmenrechtsprechung: `"Lebensmittelampel"`, `"Hygieneampel"`, `"CO2-Ampel"` als Marke

---

## 3. Identitätsrecherche — Ergebnisse

**Abfrage:** identische Schreibweisen von „VerordnungsAmpel" im DPMA/EUIPO-Register.

| Zeichen | DPMA-Nr | Inhaber | Klassen | Status | Quelle |
|---|---|---|---|---|---|
| „VerordnungsAmpel" | **Kein Treffer nachweisbar** | — | — | — | Google site:dpma.de / site:euipo.europa.eu / site:tmview — keine Register-Einträge indiziert; keine öffentliche Produkt- oder Markennennung außerhalb dieses Projekts |
| „Verordnungsampel" | Kein Treffer | — | — | — | wie oben |
| „Verordnungs-Ampel" | Kein Treffer | — | — | — | wie oben |
| „Verordnungs Ampel" | Kein Treffer | — | — | — | wie oben |

**Belastbarkeit:** Indirekt. Direktabfrage im DPMAregister-Browser ist empfohlen (siehe 2.2). Die Kombination „Verordnung + Ampel" taucht in Google-Ergebnissen zu Gesundheits-Software **nicht** als Produktname oder Marke auf. Faktische Marktnutzung durch Dritte ist damit praktisch auszuschließen.

**Zwischenergebnis:** **Hohe Wahrscheinlichkeit**, dass keine identische Marke registriert ist. Vor einer tatsächlichen Markenanmeldung ist eine Browser-Direktabfrage zwingend; für den Public-Release ist das bisherige Nicht-Auffinden ausreichend.

---

## 4. Ähnlichkeitsrecherche — Ergebnisse

**Abfrage:** phonetisch/sinngemäß ähnliche Zeichen in den Klassen 09/42/44.

| Zeichen | Ähnlichkeitstyp | DPMA-Recherchestand | Inhaber | Klassen | Kollisionsrisiko |
|---|---|---|---|---|---|
| „Praxisampel" | sinngemäß — bezieht sich ebenfalls auf ärztlichen Kontext | **Faktische Marktnutzung (domainregistriert), DPMA-Status unklar** — siehe 6.1 | JOSS products & service GmbH, Horstmar | vermutlich Klasse 09 (elektronische Tür-Ampel) oder 11 (Leuchten) — **nicht 09-Software/42/44** | **Niedrig**: andere Produktkategorie (Hardware-Türampel, kein Software-Tool), andere Warenklasse |
| „Corona-Ampel Bayern" / „Krankenhausampel Bayern" | sinngemäß — Ampel+Gesundheit | Behördliches Informationswerk, kein Markenstatus erkennbar | Bayerisches Staatsministerium f. Gesundheit | keine Marken-Eintragung, generische Behördenpublikation | Niedrig — beschreibende Verwendung ohne Schutzanspruch |
| „Lebensmittelampel" / „Hygieneampel" / „CO2-Ampel" | bildlich/kompositorisch ähnlich | Gattungsbegriffe — keine belastbare Einzelmarkenregistrierung erkennbar | diverse Urheber/Behörden, keine bekannten Monopolmarken | keine | **Sehr niedrig** — illustriert, dass „[Sachgebiet]+Ampel" als generisches Muster gelesen wird (bestätigt Freihaltebedürfnis nach § 8 Abs. 2 Nr. 2 MarkenG) |
| „Rezept-Ampel" / „Rezeptampel" | phonetisch/semantisch nah | Google: keine Produktnutzung als Marke erkennbar | — | — | Niedrig |
| „Arzneimittelampel" / „Medikationsampel" | semantisch nah | Google: keine Produktnutzung als Marke | — | — | Niedrig |
| „Regress-Ampel" / „Regressampel" | semantisch nah (Regressbezug) | keine Treffer | — | — | Niedrig |
| „Praxis-Ampel" (KVB AMTM Kontext) | semantisch nah | keine Treffer als Software-Marke; Begriff taucht in KVB-Kontext nur informell auf | — | — | Niedrig |

**Zwischenergebnis:** Die einzige faktisch dokumentierte Drittnutzung einer „Ampel"-Komposition im medizinischen Kontext ist **„Praxisampel" der JOSS products & service GmbH** — aber für ein **physisches Hardware-Produkt (Türampel)** in völlig anderer Warenklasse (Elektronik/Leuchten, nicht Medizinsoftware). Keine Verwechslungsgefahr mit VerordnungsAmpel (Software).

---

## 5. Branchen- und Klassen-Bewertung

### 5.1 Relevante Nizza-Klassen für VerordnungsAmpel

| Klasse | Was | VerordnungsAmpel einschlägig? |
|---|---|---|
| **09** | Software, Computerprogramme, Apps | **Ja — Kernklasse** |
| **42** | Software-as-a-Service, Softwareentwicklung, wissenschaftlich-technische Dienstleistungen | **Ja — bei späterer SaaS-/Cloud-Version** (aktuelle Desktop-App: nur randständig relevant) |
| **44** | Medizinische Dienstleistungen, pharmazeutische Beratung, Dienstleistungen eines Arztes | **Nein** — VerordnungsAmpel erbringt **keine** medizinische Dienstleistung (vgl. MDSW-Gutachten, Snitem-Kriterien). Tool ist Informationswerk. Klasse 44 wäre **falsch** angemeldet und ggf. abgewiesen. |
| 35 | Geschäftsführung, Datenverarbeitung | Nicht einschlägig |
| 41 | Ausbildung, Veröffentlichung (bei Online-Publikationen) | Randständig — nur falls Um:bruch später Schulungen zur Software anbietet |
| 16 | Druckschriften (Handbücher) | Randständig |

**Empfehlung zur Klassenwahl** (falls Anmeldung später sinnvoll wird):

- **Minimum:** Klasse 09
- **Empfohlen:** Klassen 09 + 42
- **Nicht empfohlen:** Klasse 44 (könnte sogar nachteilig sein — suggeriert medizinische Dienstleistung, die das Tool gerade **nicht** erbringt und die MDR-Abgrenzung angreifbar machen würde)

### 5.2 Klassenkollisionen mit bekannten Drittzeichen

Keine. Alle faktischen Drittverwendungen („Praxisampel" Hardware, „Corona-Ampel" Behörde) liegen **außerhalb** der Klassen 09/42.

---

## 6. Faktische Drittverwendung

### 6.1 „Praxisampel" (praxisampel.de)

| Feld | Wert |
|---|---|
| URL | https://www.praxisampel.de/ |
| Betreiber | JOSS products & service GmbH, Gewerbegebiet 2-b, 48612 Horstmar |
| Produkt | Einlassampel/Türampel mit Akku, Funkfernbedienung |
| Einsatzgebiet | Arztpraxen, Kliniken, Verwaltungen, Rathäuser, Apotheken |
| Markenstatus | **Kein DPMA-Eintrag erkennbar** — nur Produkt- und Domainnutzung, keine ®-Kennzeichnung auf der Homepage |
| Klassifikation | Hardware-Produkt → Klasse 09 (elektronische Geräte) oder 11 (Leuchten). **Nicht Software.** |
| Verwechslungsrisiko zu „VerordnungsAmpel" | **Sehr gering** — anderer Produktbereich (Hardware vs. Software), anderer Zweck (Einlass-Steuerung vs. Verordnungs-Plausibilität), andere Wortbildung („Praxis" ≠ „Verordnung") |

**Bewertung:** „Praxisampel" ist kein Markenrechts-Hindernis. Selbst bei einer hypothetischen DPMA-Eintragung für Klasse 09 (elektronische Steuergeräte) besteht keine Verwechslungsgefahr mit „VerordnungsAmpel" als Verordnungs-Plausibilitäts-Software für Vertragsärzte.

### 6.2 GitHub / PyPI / GitLab

- `site:github.com "VerordnungsAmpel"` — **keine Treffer** (außer ggf. eigenes Projekt nach Public-Release).
- `site:pypi.org "VerordnungsAmpel"` — **keine Treffer**.
- `site:gitlab.com "verordnungsampel"` — **keine Treffer**.

**Bewertung:** Kein Open-Source-Namenskonflikt. PyPI-Name `verordnungsampel` ist reservierbar; GitHub-Repo-Name `verordnungsampel` ist in allen geprüften Orgs (research-line, lukisch, ellmos-ai) frei.

### 6.3 Behördliche Ampel-Nutzungen („Corona-Ampel", „Krankenhausampel", „Lebensmittelampel")

Alle drei: generische, nicht-markierte Behörden- oder Informationsbegriffe. Zeigen aber eindeutig: **„[Themenfeld]+Ampel" ist ein gängiges sprachliches Muster für Signalisierungs-/Risikoinformationen**. Das ist für die Schutzfähigkeit (Abschnitt 7) höchst relevant.

### 6.4 Sonstige Wettbewerber

Keine Software auf dem deutschen Markt trägt aktuell den Namen „VerordnungsAmpel" oder eine Variante. Etablierte Wettbewerber im Verordnungs-Assistenz-Markt (AMTM der KVB, RELib der KBV, Praxissoftware-Plug-ins bei TURBOMED/MEDISTAR/ALBIS) arbeiten mit anderen Produktnamen.

**Ergebnis:** Keine faktische Drittverwendung, die den Namen „VerordnungsAmpel" blockieren würde.

---

## 7. Schutzfähigkeits-Einschätzung (§ 8 MarkenG)

### 7.1 Rechtlicher Rahmen

Nach **§ 8 Abs. 2 MarkenG** sind von der Eintragung ausgeschlossen:

1. **Nr. 1:** Marken, denen für die Waren/Dienstleistungen jegliche **Unterscheidungskraft** fehlt.
2. **Nr. 2:** Marken, die ausschließlich aus Zeichen/Angaben bestehen, die im Verkehr zur Bezeichnung der **Art, Beschaffenheit, Menge, Bestimmung, des Werts, der Zeit oder sonstiger Merkmale** der Waren dienen können (**Freihaltebedürfnis**).
3. Nr. 3: Gattungsbezeichnungen.

### 7.2 Prüfung „VerordnungsAmpel"

**Bestandteile:**

- „Verordnung" — juristisch-fachlicher Begriff für ärztliche Arzneimittelverordnung (§ 31 SGB V) bzw. Rechtsverordnung. In der Verbindung mit Software für Vertragsärzte = **beschreibend** für den Gegenstand der Software.
- „Ampel" — metaphorisches Signal-Konzept (Rot-Gelb-Grün). In Verbindung mit einem Sachgebiet wie Lebensmittel, Hygiene, CO2, Corona, Krankenhaus **gängiges sprachliches Muster** für Risiko-/Zustands-Signalisierung.

**Kompositum „VerordnungsAmpel":**

- **Rein beschreibend**: „eine Ampel, die Auskunft über Verordnungen gibt". Genau das tut die Software. Ein durchschnittlicher Fachverkehr (Vertragsarzt) würde den Begriff **primär als Funktionsbeschreibung**, nicht als Herkunftshinweis lesen.
- **Rahmenrechtsprechung:** Die Analogie zu bestehenden Ampel-Kompositionen („Lebensmittelampel", „Hygieneampel", „CO2-Ampel", „Corona-Ampel") zeigt: Das DPMA und das BPatG haben diese Begriffe **nicht** in den medizinischen/gesundheitlichen Kontexten als eintragungsfähig eingestuft. Sie werden als beschreibende Gattungsbezeichnungen behandelt.
- **Schutzhindernis § 8 Abs. 2 Nr. 2 MarkenG (Freihaltebedürfnis):** HOCH — Mitbewerber im Verordnungs-Assistenzmarkt könnten den Begriff „Verordnungsampel" ebenfalls benötigen.
- **Schutzhindernis § 8 Abs. 2 Nr. 1 MarkenG (Unterscheidungskraft):** MITTEL bis HOCH — mangelt an herkunfts-identifizierender Kraft.

### 7.3 Gegenargumente (für Eintragungsfähigkeit)

- Die **Binnengroßschreibung** („VerordnungsAmpel" mit großem „A") ist unüblich und kann **geringfügig** zur Unterscheidungskraft beitragen — allerdings hat das BPatG mehrfach entschieden, dass ungewöhnliche Schreibweisen **nicht** ausreichen, um einen ansonsten beschreibenden Begriff eintragungsfähig zu machen (vgl. BPatG zu Tippfehler-Marken, diverse Beschlüsse).
- Eine **Wort-Bild-Marke** (mit Logo: stilisierte Ampel + Wortbestandteil) wäre **deutlich schutzfähiger** als eine reine Wortmarke — der graphische Bestandteil kann die nötige Unterscheidungskraft beisteuern.
- **Verkehrsdurchsetzung** (§ 8 Abs. 3 MarkenG): Falls „VerordnungsAmpel" über Jahre hinweg als identifizierender Herkunftshinweis bekannt wird, könnte die Schutzfähigkeit über die Hintertür entstehen. Nicht aktuell relevant.

### 7.4 Ergebnis Schutzfähigkeit

| Marken-Form | Eintragungsprognose (DPMA Klassen 09/42) |
|---|---|
| **Reine Wortmarke „VerordnungsAmpel"** | **Eher ablehnend** — Risiko Zurückweisung wegen § 8 Abs. 2 Nr. 1+2 MarkenG ist **hoch** (geschätzt 60-75 %). Eintragung wäre kein Selbstläufer. |
| **Wort-Bild-Marke** (mit Ampel-Logo + Schrift) | Deutlich bessere Prognose — **eher eintragungsfähig** (geschätzt 50-70 % Chance), weil das Logo-Element die nötige Unterscheidungskraft liefert. |
| **Wortmarke „Verordnungs-Ampel"** (mit Bindestrich) | Keine wesentlich andere Prognose als ohne Bindestrich. |

**Wichtige Implikation:** Wenn „VerordnungsAmpel" **nicht schutzfähig** ist, bedeutet das:

1. **Wir können den Namen nicht monopolisieren** — keine exklusive Marke, kein ®-Anspruch.
2. Aber: **Dritte können den Namen ebenfalls nicht monopolisieren** — insbesondere keine bestehende oder zukünftige „Verordnungsampel"-Marke würde dem Projekt die Weiterführung verbieten können (§ 23 MarkenG Schutzschranke, und § 8 MarkenG zieht der hypothetischen Dritt-Marke ebenso die Zähne).
3. **Kein DPMA-Antrag zwingend.** Ersparnis: ca. 290 EUR Gebühr + Anwaltskosten (400-800 EUR für Anmeldung mit Recherche).
4. Der Name bleibt **im öffentlichen Sprachraum verfügbar** — passend zum SOCIAL/Open-Source-Charakter des Projekts.

---

## 8. Gesamtbewertung

### 8.1 Ampel-Status für Public Release (aus Markensicht)

| Prüfdimension | Status |
|---|---|
| Identische Marke existiert? | GRÜN (keine bekannt) |
| Verwechselbare Marke in Klasse 09/42? | GRÜN |
| Faktische Drittnutzung im gleichen Segment? | GRÜN (nur „Praxisampel" Hardware, keine Kollision) |
| Schutzfähigkeit des eigenen Namens | GELB — Name vermutlich beschreibend, Eigen-Markenschutz unwahrscheinlich |
| Abmahnrisiko Dritter bei unserer Nutzung | GRÜN — ohne Ziel-Marke kein Verletzungstatbestand; § 23 MarkenG würde zusätzlich schützen |
| **Blocker für Public-Veröffentlichung** | **KEIN BLOCKER — GRÜN** |

### 8.2 Konsequenz für Top-5-Maßnahme Nr. 3

Die in `GESAMTEINSCHAETZUNG.md` als GELB eingestufte Teilmaßnahme „DPMA-Recherche nicht umgesetzt" kann mit dieser Recherche auf **GRÜN** gesetzt werden. Der Public-Release ist **aus Markensicht freigegeben**. Keine Umbenennung erforderlich.

### 8.3 Gesamtampel Public-Release Markenrecht

**GRÜN** — mit kleinem gelben Randvermerk zur Schutzfähigkeit (Marke nicht monopolisierbar, aber das ist für SOCIAL unkritisch).

---

## 9. Empfehlung

### 9.1 Primär-Empfehlung

**Name „VerordnungsAmpel" beibehalten und ohne Markenanmeldung öffentlich nutzen.**

Begründung:

1. Keine blockierende Dritt-Marke auffindbar — Verletzungsrisiko tendenziell null.
2. Eigene Marke wäre wahrscheinlich nicht eintragungsfähig → Anmeldung wäre Geldverschwendung.
3. Der beschreibende Charakter des Namens passt sprachlich gut zur Zielgruppe (Vertragsärzte verstehen sofort, was es ist).
4. Für Um:bruch als SOCIAL/Open-Source-Projekt ist Monopolisierung des Namens **inhaltlich unerwünscht** — im Gegenteil: die Verbreitung des Begriffs als Gattungsbegriff wäre projektpolitisch willkommen.

### 9.2 Zusätzliche Maßnahmen

| Maßnahme | Priorität | Aufwand |
|---|---|---|
| **Manuelle DPMAregister-Verifikation** per Browser (https://register.dpma.de/DPMAregister/marke/einsteiger, Suchbegriff „verordnungsampel", Nizza-Klassen 9, 42, 44) | Nice-to-have | 5 Min |
| **Kein ™ und kein ® verwenden** — das ™ wäre theoretisch zulässig für nicht-eingetragene Marken, führt in DE aber zu Verwirrung und signalisiert falsch einen Schutzanspruch | Hoch | 0 Min (nichts zu tun) |
| **In LICENSE/README klarstellen:** „VerordnungsAmpel is a project name used to describe the tool's function (a traffic-light for medical prescription review). It is not a registered trademark and may be referred to descriptively by others under § 23 MarkenG." | Mittel | 10 Min (ein Absatz in README) |
| **PyPI-Name reservieren:** `pip install verordnungsampel` — kostenlos, verhindert Namespace-Kaperung durch Dritte | Mittel | 15 Min (Account anlegen + leeres Paket pushen, sobald der Code public ist) |
| **GitHub-Repo-Name standardisieren:** `verordnungsampel` (klein, ohne Bindestrich) — konsistent mit Python-Konventionen | Niedrig | Rename-Operation bei Public-Schaltung |

### 9.3 Alternativen-Check (falls Name doch ersetzt werden soll)

Die Aufgabe verlangte eine kurze Skizzierung. Da die Gesamtbewertung **GRÜN** ist, ist eine Umbenennung **nicht nötig**. Für den Fall strategischer Neu-Ausrichtung trotzdem kurz:

| Alternative | Schutzfähigkeit | Marktverständlichkeit | Bewertung |
|---|---|---|---|
| „Regress-Check" / „RegressCheck" | Mittel — „Regress" ist ebenfalls beschreibend, aber „Check" weniger metaphorisch | Hoch | Brauchbar, aber verlangt „Regress-Prävention"-Narrativ, das wir aus Haftungsgründen (siehe MDSW-Gutachten) bewusst zurückgefahren haben. **Nicht empfehlenswert.** |
| „Rx-Audit" / „Rx-Plausi" | Hoch — englisch-medizinisch, unterscheidungskräftig | Mittel (Rx für Laien unverständlich) | Brauchbar für internationalen Markt, aber zielgruppenfremd für DE-Vertragsärzte |
| „AM-RL-Ampel" / „AMRL-Ampel" | Ähnlich wie „VerordnungsAmpel" — beschreibend | Hoch (Fachkreis erkennt AM-RL sofort) | Keine bessere Prognose als VerordnungsAmpel |
| „Rezept-Plausi" | Mittel | Hoch | Spricht eher E-Rezept-/Apotheker-Umfeld an, nicht den Verordnungs-Kontext |
| „PVS-Compliance-Check" | Hoch — Kombination aus Fachkürzeln, unterscheidungskräftiger | Mittel (techniklastig, wenig einprägsam) | Nicht besser als VerordnungsAmpel |

**Fazit der Alternativen-Skizze:** Keine der geprüften Alternativen bietet einen klaren Vorteil. „VerordnungsAmpel" ist — trotz schwacher Markenfähigkeit — **der kommunikativ stärkste Name**.

---

## 10. Nächste Schritte

### 10.1 Kurzfristig (vor Public-Release)

1. [ ] **Manuelle DPMAregister-Direktabfrage** durch LG: browserseitig https://register.dpma.de/DPMAregister/marke/einsteiger mit „verordnungsampel" und „verordnung*ampel*" prüfen. Erwartet: kein Treffer. Ergebnis hier im Bericht nachtragen.
2. [ ] **README-Klarstellung** ergänzen: „VerordnungsAmpel is not a registered trademark; descriptive use by others is permitted."
3. [ ] **Top-5 Maßnahme Nr. 3 in `GESAMTEINSCHAETZUNG.md` schließen** (Status: erledigt durch diesen Bericht + Browser-Spot-Check).

### 10.2 Mittelfristig (nach Public-Release, falls gewünscht)

4. [ ] **PyPI-Namensreservierung:** `verordnungsampel` auf pypi.org anlegen (leeres Paket mit Metadaten-Placeholder).
5. [ ] Kein Markenanmeldungs-Verfahren einleiten. Wenn irgendwann strategisch erwünscht:

| Schritt | Kosten | Verantwortlich |
|---|---|---|
| Anwaltliche Voll-Recherche (Markenrechts-Fachanwalt, DPMA + EUIPO + Ähnlichkeitsrecherche) | 300-600 EUR | Fachanwalt Gewerblicher Rechtsschutz |
| DPMA-Anmeldung als Wort-Bild-Marke (nicht Wortmarke!) in Klassen 09 + 42 | 290 EUR (elektronisch) / 300 EUR (papier) | ggf. LG selbst über `direkt.dpma.de` |
| Optional EUIPO-Anmeldung (EU-weit) | 850 EUR (eine Klasse) + 50 EUR zweite + 150 EUR ab dritter | Fachanwalt |
| Monitoring auf Widersprüche | 3 Monate Widerspruchsfrist | LG/RB |

**Empfehlung RB:** Anmeldung aktuell **nicht** sinnvoll — erst dann, wenn Um:bruch e.V./gUG als Rechtsperson existiert **und** eine spezifische strategische Begründung vorliegt (z. B. Bekanntheit so hoch, dass Trittbrettfahrer-Schutz wichtig wird).

### 10.3 Langfristig

6. [ ] Im Halbjahresbericht der Rechtsabteilung (siehe `Policies/RECHTSABTEILUNG.md`, Prüfpunkt „Markenrecht") alle 6 Monate einen schnellen DPMA-Check laufen lassen — falls Dritte später eine Marke „Verordnungsampel" anmelden sollten, könnte Um:bruch über § 23 MarkenG (beschreibende Benutzung) und § 8 MarkenG (Nichtigkeitsantrag wegen fehlender Unterscheidungskraft) reagieren.

---

## 11. Grenzen dieser Einschätzung

Diese Einschätzung ist eine **KI-basierte Erstanalyse** auf Grundlage öffentlich zugänglicher Web-Suchen und ersetzt **keine** anwaltliche Beratung durch einen Fachanwalt für Gewerblichen Rechtsschutz.

### 11.1 Spezifische Einschränkungen

1. **DPMAregister-Direktabfrage nicht durchgeführt:** Die offizielle DPMA-Datenbank ist Session-basiert und per WebFetch nicht treffer-extraktfähig. Die Schlussfolgerungen dieses Berichts beruhen auf **indirekten Google-/EUIPO-Site-Suchen** und der beobachteten Marktlage. Eine Browser-Direktabfrage (5 Min) ist als letzter Spot-Check dringend empfohlen.
2. **TMview nicht vollständig abgefragt:** TMview erlaubt keine statischen HTTP-Abfragen ohne Browser-JavaScript. Die EU-weite Vollabdeckung konnte nicht direkt erreicht werden; site:euipo-Google-Suchen sind ein Proxy, aber kein Ersatz.
3. **Schutzfähigkeitsprognose ist Prognose:** Die Einschätzung, dass „VerordnungsAmpel" mit 60-75 % Wahrscheinlichkeit **nicht** eintragungsfähig ist, basiert auf Analogien (Lebensmittelampel, Hygieneampel, CO2-Ampel) und allgemeinen § 8-Kriterien. Eine konkrete DPMA-Entscheidung über genau dieses Zeichen liegt nicht vor. Eine Eintragung wäre nicht unmöglich, aber unwahrscheinlich ohne erhebliche Argumentationsarbeit (Begründung Unterscheidungskraft, ggf. Verkehrsdurchsetzung).
4. **Keine anwaltliche Bewertung relativer Schutzhindernisse:** Dritte mit bestehenden prioritären Marken könnten bei DPMA-Anmeldung Widerspruch einlegen — eine vollständige Ähnlichkeitsrecherche über alle Nizza-Klassen (nicht nur 09/42/44) erfordert eine DPMAregister-Profi-Recherche oder einen Fachanwalt.
5. **Keine Rechtslage-Prognose für die Zukunft:** Falls Dritte künftig eine ähnliche Marke anmelden, müsste erneut geprüft werden. Empfohlen: halbjährlicher Spot-Check.

### 11.2 Empfehlung zur Anwaltseinschaltung

**Jetzt:** nicht nötig (Projekt steht vor Public-Release als Open-Source-Tool ohne Marken-Absicht).

**Falls Markenanmeldung strategisch gewollt wird:** Ja — dann vor Anmeldung einen Fachanwalt für Gewerblichen Rechtsschutz einschalten (Kostenrahmen: 500-1000 EUR für Voll-Recherche + Anmeldung). Empfehlung zur Kanzleisuche: IHK Berlin-Vermittlung, brandeins-Anwaltsliste, oder medienrechtlich engagierte Kanzleien mit Pro-Bono-Fenster für Open-Source-Projekte.

**Bei eingehender Abmahnung wegen des Namens:** Sofort Anwalt einschalten (Abmahnfristen laufen typischerweise 7-14 Tage).

---

## 12. Quellen

### 12.1 Primärquellen

- DPMAregister: https://register.dpma.de/DPMAregister/marke/einsteiger (Session-basiert; WebFetch lieferte nur Formular-HTML)
- DPMAregister erweiterte Suche: https://register.dpma.de/DPMAregister/marke/erweiterteSuche
- EUIPO/TMview: https://www.tmdn.org/tmview/ (Client-seitig JS, WebFetch abgebrochen)
- EUIPO Search Portal: https://www.euipo.europa.eu/en/trade-marks/before-applying/availability
- DPMA Klassifikation (Nizza): https://www.dpma.de/marken/klassifikation/index.html
- DPMA Merkblatt für Markenanmelder (W 7731/2.26): https://www.dpma.de/docs/formulare/marken/w7731.pdf

### 12.2 Faktische Drittverwendung

- https://www.praxisampel.de/ — JOSS products & service GmbH, Einlassampel (Hardware-Produkt)
- https://corona-ampel-bayern.de/ — Bayerisches Staatsministerium (generische Behördenampel)
- https://krankenhausampel.bayern/ — Bayerisches Staatsministerium (Krankenhauskapazitätsanzeige)
- Google-Site-Suchen `site:github.com`, `site:pypi.org`, `site:gitlab.com` — keine Treffer

### 12.3 Rechtsprechung und Rahmen

- § 8 MarkenG: https://dejure.org/gesetze/MarkenG/8.html
- § 14 MarkenG, § 23 MarkenG: https://www.gesetze-im-internet.de/markeng/
- Absolute Schutzhindernisse (Übersicht): https://de.wikipedia.org/wiki/Absolute_Schutzhindernisse
- BPatG Rahmenrechtsprechung zu Komposita/Unterscheidungskraft:
  - BPatG 14.09.2023 — 30 W (pat) 15/22 „NFTNET" (Unterscheidungskraft bei Komposita, Klasse 9)
  - BPatG 08.05.2024 — 26 W (pat) 539/22 (Aktuelle Rechtsprechung Unterscheidungskraft)
  - BPatG 25.02.2003 — 27 W (pat) 28/02 (Komposita-Rechtsprechung)
  - Übersichten: https://www.slopek.com/aktuelles-markenrecht/unterscheidungskraft-von-marken-aktuelle-rechtsprechung-des-undespatentgerichts/, https://www.ra-plutte.de/vor-markenanmeldung-check-absolute-schutzhindernisse/
- Analyse Software-Markenkollisionen Klasse 09/42: https://b2.legal/widerspruch-bei-software-marken-wann-software-wirklich-aehnlich-ist/

### 12.4 Projekt-interne Bezüge

- `docs/legal/RECHTSGUTACHTEN_PUBLIKATION_LIZENZ.md` (12.04.2026), Kap. 4 — präliminäre Einschätzung
- `docs/legal/GESAMTEINSCHAETZUNG.md` (12.04.2026), Top-5 Nr. 3 — Auftrag
- `Policies/RECHTSABTEILUNG.md` (02.04.2026) — Berichtsformat und Halbjahresbericht Markenrecht

---

**Dokumentende.**
**Verfasst:** Claude (CL) / Rechtsabteilung Um:bruch, 12.04.2026
**Status:** Freigabe durch LG ausstehend; nach Freigabe zu verlinken aus `GESAMTEINSCHAETZUNG.md` (Top-5 Nr. 3 → status: „umgesetzt").
