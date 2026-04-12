# Rechtliche Folgeprüfung — VerordnungsAmpel_SOCIAL als "Research Use Only"-Software?

**Datum:** 2026-04-12
**RB:** Claude (CL), Um:bruch Rechtsabteilung
**Typ:** Folgegutachten zum Hauptgutachten `RECHTSGUTACHTEN_MDSW.md` (2026-04-12)
**Auftrag:** Lukas Geiger (Projekt-Initiator, Um:bruch), 2026-04-12
**Mandantenfrage:** *"Sollten wir die VerordnungsAmpel als reine Forschungs-/Research-Software kennzeichnen, um das Haftungsrisiko weg von uns zu nehmen?"*
**Status:** KI-basierte Erstanalyse — kein Anwaltsersatz (siehe Abschnitt 9)

---

## 1. Gegenstand und Bezug zum Hauptgutachten

### 1.1 Ausgangslage

Das Hauptgutachten vom 12.04.2026 (`RECHTSGUTACHTEN_MDSW.md`) hat die VerordnungsAmpel_SOCIAL in ihrer aktuellen MVP-Spezifikation (KONZEPT.md v1, Stand 2026-04-08) rechtlich als **Informationswerk/Nachschlagewerk** und **nicht** als Medical Device Software (MDSW) im Sinne der Verordnung (EU) 2017/745 (MDR) eingeordnet. Die Gesamt-Risikoeinschätzung lautet **"mittel"**, abhängig von einer sorgfältigen Zweckbestimmung, neutraler UI und diszipliniertem Marketing.

Das vorliegende Folgegutachten beantwortet die ergänzende Frage des Mandanten, **ob eine zusätzliche oder alternative Kennzeichnung als "Research Use Only"-Software (RUO)** das rechtliche Risikoprofil weiter verbessern würde. Konkret geht es darum, ob eine solche Kennzeichnung

(a) das Haftungsrisiko gegenüber Arzt, Patient oder Krankenkasse reduziert,
(b) die Gefahr einer MDSW-Einstufung weiter verringert,
(c) das Tool zugleich praxistauglich für die angestrebten Pilotanwender hält.

### 1.2 Verhältnis zum Hauptgutachten

Das Folgegutachten baut auf der Subsumtion des Hauptgutachtens auf, hinterfragt diese aber nicht. Insbesondere wird weiterhin unterstellt:

- keine Verarbeitung patientenspezifischer Daten (Snitem-Kernmerkmal fehlt),
- reine Table-Lookup-Funktion ohne Interpretation (MDCG 2019-11 Rev. 1 Step 3 verneint),
- sozialrechtlicher, nicht medizinischer Zweck (Art. 2 Nr. 1 MDR verneint).

Das Folgegutachten klärt eine eigenständige Zusatzfrage: **Was bringt — oder was schadet — die zusätzliche RUO-Kennzeichnung?**

---

## 2. Was bedeutet "Research Use Only" rechtlich?

### 2.1 Die RUO-Kategorie ist primär eine IVDR/FDA-Kategorie, nicht eine MDR-Kategorie

#### 2.1.1 Status im US-Recht (FDA)

"Research Use Only" ist in den USA eine formale regulatorische Kategorie der Food and Drug Administration für In-vitro-Diagnostika (21 CFR 809.10(c)). Ein RUO-Produkt muss mit der Aufschrift versehen sein:

> "For Research Use Only. Not for use in diagnostic procedures."

Die FDA-Praxis ist streng: Die Kennzeichnung **allein** reicht nicht; der Hersteller darf das Produkt auch faktisch nicht für klinische Zwecke vermarkten oder unterstützen. Tut er es doch, werden RUO-Produkte als unzulässig in den Verkehr gebrachte IVDs behandelt (FDA Guidance "Distribution of IVD Products Labeled for Research Use Only or Investigational Use Only", November 2013).

#### 2.1.2 Status im EU-Recht (IVDR)

Die Verordnung (EU) 2017/746 (IVDR) kennt in Art. 2 Nr. 2 die Definition des In-vitro-Diagnostikums und in Art. 5 Abs. 5 die Privilegierung von Geräten, die **ausschließlich für Forschungszwecke** verwendet werden und nicht in Verkehr gebracht werden. **Reine Forschungsprodukte, die nicht zu einem medizinischen Zweck bestimmt sind,** liegen nach herrschender Meinung ausserhalb des Anwendungsbereichs der IVDR — Art. 5 Abs. 1 IVDR greift nur, wenn eine Zweckbestimmung nach Art. 2 Nr. 2 IVDR vorliegt (vgl. [EUR-Lex 32017R0746](https://eur-lex.europa.eu/eli/reg/2017/746/oj); [mdi-europa IVDR-Überblick](https://mdi-europa.com/ivdr-in-vitro-diagnostic-medical-devices-regulation-eu-2017-746/)).

In der Pathologie-Praxis werden daher drei Produktkategorien nebeneinander verwendet: CE-IVDs, In-house-IVDs nach Art. 5 Abs. 5 IVDR, und RUO-Geräte ausserhalb der IVDR ([Pathologie/Springer 2022](https://link.springer.com/article/10.1007/s00292-022-01176-z)). Die RUO-Kategorie ist dort etabliert — aber sie ist nicht explizit kodifiziert, sondern eine Negativabgrenzung: "RUO ist, was keine IVDR-Zweckbestimmung hat."

#### 2.1.3 Status im EU-Recht (MDR)

**Die MDR kennt keinen eigenen Status "Research Use Only" für Software.** Es gibt nur zwei relevante Ausnahmepfade:

1. **Produkt ohne medizinische Zweckbestimmung nach Art. 2 Nr. 1 MDR.** Wird ein Produkt nicht für einen der in Art. 2 Nr. 1 aufgezählten medizinischen Zwecke (Diagnose, Therapie, Monitoring, Prognose etc.) bestimmt, so greift die MDR **gar nicht**. Dies ist der **Standardpfad** für die VerordnungsAmpel (siehe Hauptgutachten, Schritt 5 der Subsumtion).

2. **Produkte für klinische Prüfungen nach Art. 62 ff. MDR.** Prüfmuster ("Prüfprodukte"), die in einer klinischen Prüfung (clinical investigation) eingesetzt werden, unterliegen einem eigenen Regime (Erwägungsgrund 63 ff., Anhang XV MDR). Sie müssen nicht CE-zertifiziert sein, brauchen aber eine Genehmigung der zuständigen Behörde, eine Ethikkommissions-Zustimmung, ein Prüfplan-Dokument und eine Haftpflichtversicherung. Dies ist **kein** Schutzschirm im Sinne des Mandanten — im Gegenteil: es erzeugt erheblichen regulatorischen Aufwand.

Erwägungsgrund 32 MDR verweist auf "klinische Prüfungen zum Nachweis der Konformität" und betrifft damit die zweite Konstellation.

Eine freistehende MDR-Kategorie "RUO-Software, unterhalb der klinischen Prüfung, aber mit Haftungsprivileg" existiert **nicht** ([Johner Institute, "Clinical investigations under MDR"](https://blog.johner-institute.com/regulatory-affairs/clinical-investigations-of-medical-devices/); [TÜV Süd "Artikel 5 MDR"](https://de-mdr-ivdr.tuvsud.com/Artikel-5-Inverkehrbringen-und-Inbetriebnahme.html)).

### 2.2 Rechtliche Kernwirkung einer RUO-Kennzeichnung

Eine freiwillige RUO-Kennzeichnung ist damit rechtlich gesehen **kein eigener Status**, sondern:

| Funktion | Rechtliche Einordnung |
|---|---|
| **(i) Teil der Zweckbestimmung nach Art. 2 Nr. 12 MDR** | Der Hersteller dokumentiert, welchem Zweck das Produkt dient und welchem nicht. Dies formt die Zweckbestimmung mit. |
| **(ii) Teil der Produktinstruktion nach § 3 ProdHaftG** | Die Kennzeichnung wirkt als Warnhinweis gegenüber dem Nutzer. Entscheidend ist, ob der Hinweis objektiv geeignet ist, vorhersehbare Fehlanwendungen auszuschliessen. |
| **(iii) Indiz für bestimmungsgemässen Gebrauch im Haftungsrecht** | Ein klinischer Einsatz gegen den ausdrücklichen Hinweis wird zur "Zuwiderhandlung gegen die Gebrauchsanleitung" und kann Mitverschulden begründen. |

Sie wirkt **nicht** wie eine Zertifizierung, eine Ausnahme oder eine Zulassung. Sie verlagert Verantwortung, wenn sie ernst genommen wird.

### 2.3 Die Grenze der Wirksamkeit: objektive Zweckbestimmung

Sowohl der Europäische Gerichtshof (C-329/16 Snitem, Urt. v. 07.12.2017) als auch das BfArM (FAQ Abgrenzung/Klassifizierung, Stand 2025) betonen, dass die **objektive** Zweckbestimmung massgeblich ist:

> "Erklärungen wie ein Hinweis im App-Store 'Dies ist kein Medizinprodukt' umgehen die genannten Kriterien nicht und werden bei BfArM-Entscheidungen nicht berücksichtigt, wenn ein medizinischer Zweck vom Hersteller in Kennzeichnung, Gebrauchsanweisung oder Werbemitteln angegeben oder vermittelt wird."
> ([BfArM FAQ Abgrenzung/Klassifizierung](https://www.bfarm.de/DE/Medizinprodukte/_FAQ/Klassifizierung-Abgrenzung/faq-liste.html))

Damit ist die juristische Grundregel klar: **Ein "RUO"- oder "kein Medizinprodukt"-Disclaimer ist nur so viel wert wie die konsistente Produktgestaltung dahinter.** Widerspricht das Produkt in Features, Marketing oder Vertriebskanal dem Disclaimer, greift der Disclaimer nicht.

Der EuGH hat dies in Snitem (Rn. 33) abstrakt bestätigt: Die Qualifikation als Medizinprodukt folgt aus der Gesamtbeurteilung der Produkteigenschaften, nicht aus einzelnen Etikettenaussagen.

---

## 3. Faktische Wirkung vs. rechtliche Wirkung einer RUO-Kennzeichnung

### 3.1 Tatsächliche Schutzwirkung: eher gering, aber nicht null

Ein RUO-Hinweis hat in mehreren Dimensionen eine messbare Schutzwirkung — aber er ist kein "Reset-Knopf" für die Haftung.

#### 3.1.1 Dokumentationswert

Die RUO-Kennzeichnung ist schriftlich fixiert, datiert, ggf. beim Erststart bestätigt. Sie erzeugt **Beweisbarkeit des Herstellerwillens**, die vor Zivil- und Strafgerichten nicht ignoriert wird. In späteren Prozessen ist sie Anknüpfungspunkt für:

- Mitverschulden des Nutzers (§ 254 BGB), wenn dieser das Produkt entgegen dem expliziten Hinweis für Patientenversorgung nutzt.
- Verschuldensabgrenzung im Strafrecht (§ 229 StGB): Wenn der Hersteller dokumentiert "nicht für klinischen Einsatz bestimmt", verschiebt sich das Fahrlässigkeitsgewicht auf den Anwender.
- Abweisung werberechtlicher Angriffe (HWG), weil das Produkt nachweislich nicht als medizinisches vermarktet wird.

#### 3.1.2 Grenze durch vorhersehbare Fehlanwendung (Art. 2 Nr. 22 MDR)

Die MDR und die ISO 14971 fordern vom Hersteller, **vorhersehbare Fehlanwendungen** ("reasonably foreseeable misuse") zu erkennen und durch Risikosteuerung zu minimieren ([Johner Institut: Vorhersehbarer Missbrauch](https://www.johner-institut.de/blog/iso-14971-risikomanagement/vorhersehbarer-missbrauch/); Art. 2 Nr. 22 MDR). Übertragen auf die VerordnungsAmpel bedeutet das:

> Wenn die Software einem Vertragsarzt angeboten wird, dessen Alltag aus Patientenversorgung besteht, ist der klinische Einsatz des Tools **vorhersehbar**. Ein Disclaimer "nur für Forschung" hilft wenig, wenn das Produkt so gestaltet ist, dass es sich in den ärztlichen Verordnungsfluss einfügt.

Damit reduziert eine RUO-Kennzeichnung das Risiko nicht vollständig — sie reduziert es dort, wo eine Nutzung tatsächlich **unvorhersehbar** wird. Die reine Formulierung "nur Forschung" verhindert nicht, dass ein Arzt das Tool in der Sprechstunde öffnet.

#### 3.1.3 Augenwischerei-Risiko

Ein aggressiver oder zu weit gefasster Disclaimer kann sogar **schaden**:

1. **Werberechtlich (§ 3 HWG):** Widersprüchliche Aussagen ("kein Medizinprodukt" einerseits, "hilft bei Verordnungen" andererseits) begründen Irreführung.
2. **Produkthaftungsrechtlich:** Nach § 14 ProdHaftG sind Haftungsausschlüsse unwirksam; eine RUO-Kennzeichnung, die den Eindruck vermittelt, "wir haften nicht", ist nach § 309 Nr. 7 BGB sogar unzulässige AGB-Klausel ([it-recht-kanzlei.de Disclaimer-Produkthaftung](https://www.it-recht-kanzlei.de/disclaimer-haftungsausschluss-produkthaftung-selbstformuliert.html)).
3. **Deliktsrechtlich:** Schwere oder vorsätzliche Verkehrspflichtverletzungen sind nicht durch Disclaimer abdingbar (BGH, ständige Rspr., z. B. NJW 2009, 1669 zu Instruktionspflichten).

### 3.2 Rechtsvergleich: Parallelen aus anderen Domänen

**"Nur zu Bildungszwecken" bei Hacking-Tools:** Die Rechtsprechung (OLG Hamm 2009, BGHSt 45, 216) zeigt, dass ein Bildungs-Disclaimer die strafrechtliche Beihilfe-Haftung nicht ausschliesst, wenn das Tool objektiv zur Begehung einer Straftat geeignet ist.

**"Nur zur Anschauung" bei Waffen-Replika:** Die Rechtsprechung zu § 1 WaffG unterstellt, dass die objektiven Gebrauchsmöglichkeiten die deklarierte Zweckbestimmung überwiegen, wenn das Produkt funktional voll einsatzfähig ist.

**"Supplement, kein Arzneimittel":** Der BGH (Urt. v. 26.06.2008 — I ZR 61/05) hat wiederholt entschieden, dass ein Werbe-Disclaimer die objektive Produktqualifikation nicht verändern kann; entscheidend ist die überwiegende Zweckbestimmung nach Verkehrsauffassung ([it-recht-kanzlei.de Nahrungsergänzung-Arzneimittel](https://www.it-recht-kanzlei.de/5/HWG_Gesetz_ueber_die_Werbung_auf_dem_Gebiet_des_Heilwesens/nahrungsergaenzungsmittel-arzneimittel.html)).

**Zwischenergebnis:** In allen drei Domänen wirkt der Disclaimer als **Indiz**, niemals als **Schutzschild**. Er verschiebt die Darlegungslast, kehrt aber nicht die Rechtslage um. Dieses Muster wird auf die VerordnungsAmpel übertragen.

### 3.3 Positive Wirkungen einer RUO-Kennzeichnung (nicht null)

Trotz der Grenzen hat eine gut integrierte RUO-Logik **drei reale Vorteile**:

1. **Klarstellung der Zielgruppe:** Forschungs-/Evaluations-Kontexte (z. B. Pilot mit 10 Praxen, akademischer Partner) werden legitimiert, ohne Ärzte ausserhalb des Pilots anzusprechen. Das begrenzt die Werbe-Reichweite und die Nutzungs-Wahrscheinlichkeit.
2. **Kohärenz mit dem Pilot-Design:** Die VerordnungsAmpel plant laut KONZEPT.md eine Pilot-Phase mit 10 Praxen vor dem Public Release. Solange die Software in diesem definierten Kontext läuft, ist sie faktisch eine Evaluations-Software. Eine RUO-Kennzeichnung macht diesen Status rechtlich sauber.
3. **Schutz vor Werbe-Effekten:** Selbst bei Open-Source-Veröffentlichung auf GitHub kann durch konsequente RUO-Formulierung verhindert werden, dass Dritte die Software als "vom Anbieter empfohlen" weiterverteilen.

Das Instrument RUO ist also **taktisch nützlich**, nicht juristisch mächtig.

---

## 4. Zivilrechtliche Haftung (ProdHaftG, § 823 BGB, Instruktionspflichten)

### 4.1 Anwendbarkeit des ProdHaftG auf Software

Software fällt seit der gefestigten Kommentarliteratur und der BGH-Rechtsprechung unter den Produktbegriff des § 2 ProdHaftG, jedenfalls wenn sie auf einem körperlichen Datenträger verkörpert oder als SaaS einem Nutzerkreis zur Verfügung gestellt wird (vgl. [wi-lex Produkthaftung Software](https://wi-lex.de/index.php/lexikon/uebergreifender-teil/kontext-und-grundlagen/it-recht/produkt-und-produzentenhaftung-bei-software/); zur Neuregelung durch die Produkthaftungs-RL (EU) 2024/2853 mit Umsetzungsfrist Dezember 2026). Das bedeutet:

- **Verschuldensunabhängige Haftung** für Fehler, die zu Personen- oder erheblichen Sachschäden führen (§ 1 ProdHaftG).
- **Haftungsausschluss über AGB nicht möglich** (§ 14 ProdHaftG).
- **Instruktionspflicht** als eigenständiger Fehlerbegriff (§ 3 ProdHaftG).

### 4.2 Wirkung der RUO-Kennzeichnung in den einzelnen Haftungssträngen

#### 4.2.1 Konstruktionsfehler (§ 3 ProdHaftG Nr. 1)

Ein Konstruktionsfehler läge vor, wenn die VerordnungsAmpel bereits im Design unsicher wäre (z. B. fehlerhafte Regelwerks-Zuordnung). RUO-Kennzeichnung **reduziert das nicht**: der Algorithmus muss stimmen, unabhängig vom Einsatzszenario.

**Reduzierend wirkt nur** die Transparenz der Datenquellen (Version, Stand, Original-Quelle mit Verweis).

#### 4.2.2 Fabrikationsfehler

Bei reiner Software nicht relevant (keine physische Produktion).

#### 4.2.3 Instruktionsfehler (§ 3 ProdHaftG Nr. 2)

**Hier liegt der Hebel der RUO-Kennzeichnung.** Ein Instruktionsfehler liegt vor, wenn der Hersteller vor Gefahren bei bestimmungsgemäßem Gebrauch und vorhersehbarer Fehlanwendung nicht ausreichend warnt. Entscheidend ist, ob die Warnung

(a) klar und verständlich ist,
(b) an der richtigen Stelle platziert ist (nicht versteckt in AGB),
(c) den Gefahrenmechanismus benennt,
(d) eine Handlungsanweisung gibt.

Wenn die VerordnungsAmpel ernsthaft als RUO gekennzeichnet ist und der Nutzer sie dennoch produktiv in der Patientenversorgung einsetzt, verschiebt sich das Verschulden Richtung Anwender. **Der Hersteller hat seine Instruktionspflicht erfüllt.**

Wichtig: Die Rechtsprechung anerkennt Warnhinweise nur, wenn sie **positiv wirksam** sind — also nicht nur in AGB-Kleingedrucktem, sondern an exponierter Stelle (Startscreen, README, Kopf- oder Fusszeile, Eingangs-Dialog).

#### 4.2.4 § 823 BGB Produzentenhaftung

Parallel zum ProdHaftG greift die Produzentenhaftung nach § 823 Abs. 1 BGB über die von der Rechtsprechung entwickelten Verkehrspflichten (BGH, ständige Rspr. seit "Hühnerpest"-Entscheidung 1968, NJW 1969, 269). Hier wird Verschulden geprüft, was den Hersteller potenziell schlechter stellt (Beweislastumkehr).

Auch hier reduziert eine RUO-Kennzeichnung die Pflichtenlage, wenn sie **konsistent und ernst gemeint** ist. Sie eliminiert sie nicht.

### 4.3 Die zentralen Beispielfälle

Drei Szenarien zeigen die praktische Wirkung:

| Szenario | Ohne RUO | Mit RUO |
|---|---|---|
| **(1) Arzt nutzt Tool, vertraut Ampel GRÜN zu Unrecht, Patient wird geschädigt** | Haftung Hersteller wegen Instruktionsfehlers möglich; Ampel-Farbe weckt Vertrauen | Haftung Hersteller stark reduziert, sofern RUO-Hinweis prominent und unmissverständlich. Haftung des Arztes steigt. |
| **(2) Regulierungsbehörde leitet MDR-Klassifizierungsverfahren ein** | Zweckbestimmung muss die nicht-medizinische Natur tragen | RUO-Kennzeichnung stärkt die Argumentation; die Software ist nicht für klinischen Einsatz bestimmt |
| **(3) KV-Abrechnungsprüfung rückt nach** | Log-Datei als Beweis, aber produktiver Einsatz ist belastet, wenn Ampel rot war | Unverändert. RUO ändert die sozialrechtliche Lage nicht. |

Die Tabelle illustriert: RUO-Kennzeichnung hilft **haftungsrechtlich erheblich** in Szenario 1, **unterstützend** in Szenario 2, **gar nicht** in Szenario 3.

---

## 5. Strafrechtliche Dimension

### 5.1 Fahrlässige Körperverletzung / Tötung (§§ 229, 222 StGB)

Für die **ärztliche** Seite ist die Lage klar: Der Arzt schuldet den Facharztstandard. Er darf sich nicht blind auf ein Companion-Tool verlassen ([dejure § 229 StGB](https://dejure.org/gesetze/StGB/229.html)). Selbst ein zertifiziertes CDSS (Clinical Decision Support System) entbindet ihn nicht von der eigenen Prüfung.

Für die **Hersteller-Seite** kommt eine Beihilfe-/Täterstellung nach Fahrlässigkeitsdogmatik nur in Betracht, wenn:

- das Tool objektiv fehlerhaft ist (falsche Regelwerks-Daten, falsche Ampel),
- dieser Fehler vorhersehbar war,
- der Hersteller Sorgfaltspflichten verletzt hat (z. B. keine Regelwerks-Aktualisierung),
- der Kausalverlauf zur Körperverletzung führt.

**Die RUO-Kennzeichnung hilft hier doppelt:**

(a) Sie entkräftet die Vorhersehbarkeit des klinischen Kausalverlaufs (das Tool sollte ja nicht klinisch eingesetzt werden),
(b) Sie stärkt die Sorgfaltspflichterfüllung durch Warnhinweis.

Allerdings: Auch hier gilt die Grenze der **vorhersehbaren Fehlanwendung**. Ein Gericht kann feststellen, dass ein Companion-Tool für Vertragsärzte faktisch vorhersehbar in der Patientenversorgung landet — dann hilft der Disclaimer nur partiell.

### 5.2 Verstoß gegen MPDG (§§ 92 ff. MPDG)

Der schlimmste strafrechtliche Fall wäre, wenn die VerordnungsAmpel vom BfArM als MDSW eingestuft und ohne CE-Kennzeichnung in Verkehr gebracht worden wäre — dann § 92 MPDG (Freiheitsstrafe bis zu einem Jahr oder Geldstrafe).

Eine RUO-Kennzeichnung **reduziert dieses Risiko erheblich**, weil sie die Nicht-Medizinprodukt-Zweckbestimmung dokumentiert. Sie beseitigt es nicht, weil die objektive Zweckbestimmung (siehe 2.3) vorgeht.

### 5.3 § 203 StGB Berufsgeheimnis

Hier nicht relevant, weil die VerordnungsAmpel keine Patientendaten verarbeitet. Eine RUO-Kennzeichnung hätte hier keine Wirkung.

### 5.4 Zwischenergebnis zum Strafrecht

| Straftatbestand | Schutz durch RUO-Kennzeichnung |
|---|---|
| §§ 229, 222 StGB (fahrlässige Körperverletzung/Tötung) | **mittel** — stärkt Nicht-Vorhersehbarkeit + Instruktion |
| § 92 MPDG (MDSW ohne CE) | **hoch** — dokumentiert Nicht-Medizinprodukt-Zweck |
| § 203 StGB | **irrelevant** |

---

## 6. Vergleichsfälle: UpToDate, AMBOSS, Medscape, akademische Tools

### 6.1 UpToDate (Wolters Kluwer)

UpToDate ist das weltweit meistgenutzte Arzt-Nachschlagewerk. Die offiziellen Nutzungsbedingungen (Terms of Use, Stand 04/2026) enthalten folgende Kernaussagen:

> "UpToDate is not a Health Care Provider nor is it engaged in the practice of medicine." ([Wolters Kluwer Clinical Effectiveness Terms](https://www.wolterskluwer.com/en/know/clinical-effectiveness-terms))

> "intended and presented only for general educational purposes as a guide and reference."

> "[information] should not be used as a substitute for professional medical advice and judgment"

> "you are solely responsible for all decisions regarding medical diagnosis and treatment"

Bemerkenswert ist die Haftungsbegrenzung:

> "total liability … shall not exceed … the greater of (a) total subscription fees paid … in the twelve-month period preceding … and (b) $100 U.S.D."

Und der klare Ausschluss klinischer Nutzung für bestimmte Zusatzfunktionen:

> "may not be used … for any clinical, medical, diagnostic or therapeutic purposes"

**Muster:** UpToDate vermeidet RUO-Sprache, benutzt stattdessen "educational purposes" und delegiert die Verantwortung konsequent an den Arzt. UpToDate ist **nicht** CE-zertifiziert, wird aber faktisch klinisch eingesetzt. Die Haftungsstrategie beruht auf **aggressiver vertraglicher Haftungsbegrenzung + Disclaimer + klarer Nicht-Medizinprodukt-Positionierung**.

### 6.2 AMBOSS

AMBOSS ist ein in Deutschland stark verbreitetes medizinisches Nachschlagewerk (Web + App). Die öffentliche Positionierung lautet "Wissensplattform" und "Lernplattform". AMBOSS ist **nicht** als Medizinprodukt registriert, führt kein CE-Zeichen und beansprucht keinen diagnostischen oder therapeutischen Zweck im MDR-Sinn.

Die im April 2026 online zugänglichen AMBOSS-Nutzungsbedingungen waren aufgrund Session-Wall nicht direkt abrufbar, wie vom bisherigen öffentlichen Eindruck bestätigt (vgl. Hauptgutachten Abschnitt 2.7). Die öffentliche Kommunikation (amboss.com-Hauptseite, App Store-Listings) vermeidet klinisch-empfehlende Sprache ("AMBOSS hilft Dir, schneller den richtigen Behandlungsschritt zu finden" wird nicht als verbindliche Empfehlung formuliert).

**Muster:** Analog UpToDate — Positionierung als Informations-/Lernplattform, nicht als CDSS. Keine explizite RUO-Kennzeichnung; stattdessen konsequente Zweckbestimmungs-Disziplin.

### 6.3 Medscape (WebMD/Aptus Health)

Medscape ist eine globale Informationsplattform für Ärzte. Die Nutzungsbedingungen sind öffentlich zugänglich ([Medscape Terms of Use](https://www.medscape.com/public/termsofuse)) und enthalten folgende Kernaussagen:

> "in no way intended to serve as a diagnostic service or platform, to provide certainty with respect to a diagnosis, to recommend a particular product or therapy or to otherwise substitute for the clinical judgment of a qualified healthcare professional."

> "you should not rely on that information as professional medical advice or use the Services as a replacement for any relationship with your physician or other qualified healthcare professional."

Der Medscape Drug Interaction Checker ist — soweit öffentlich recherchierbar — in der EU **nicht als Medizinprodukt zertifiziert**, weil er keine patientenspezifischen Daten verarbeitet (vgl. Hauptgutachten Abschnitt 2.7, Snitem-Kriterium).

**Muster:** Identisch zu UpToDate. Die EU-spezifische Seite ([EEA Notice](https://www.medscape.com/public/eu-users)) erwähnt kein Medizinprodukt-Attribut.

### 6.4 Akademische Open-Source-Tools (OHDSI, OpenEHR)

**OHDSI** (Observational Health Data Sciences and Informatics) produziert Tools wie ATLAS, WebAPI, die in der Forschung verwendet werden. Die GitHub-Repositories enthalten typischerweise einen Haftungsausschluss unter Apache 2.0 und explizite Hinweise:

> "This software is not a medical device and is not intended to be used to diagnose, treat, cure, or prevent any disease."
> (typisch für akademische Medizin-OSS-Projekte unter Apache-2.0)

**OpenEHR**: Der openEHR-Standard ist eine Spezifikation und Daten-Infrastruktur, keine klinische Software. Implementierungen haben typischerweise Haftungsausschlüsse analog OHDSI.

**Muster:** Open-Source-Tools setzen offen auf RUO-ähnliche Hinweise in Kombination mit Apache/MIT/GPL-Lizenz-Disclaimern ("AS IS, WITHOUT WARRANTY OF ANY KIND"). Die Schutzwirkung folgt aus der Kombination Lizenz-Haftungsausschluss + Open-Source-Natur + typischer Nutzung durch Forscher, nicht durch Endanwender in der Patientenversorgung.

### 6.5 BfArM-Position zu Forschungssoftware

Das BfArM hat in seinen FAQ zur Abgrenzung ([BfArM FAQ](https://www.bfarm.de/DE/Medizinprodukte/_FAQ/Klassifizierung-Abgrenzung/faq-liste.html)) festgestellt:

> "Die Zuordnung eines Produkts zu Medizinprodukten (Abgrenzung von anderen Produkten) erfolgt durch den Hersteller über die sich aus der Kennzeichnung, der Gebrauchsanweisung und aus Werbematerialien ergebende Zweckbestimmung und muss der Definition der Medizinprodukte gemäß Artikel 2 Nr. 1 der MDR entsprechen."

Und:

> "Erklärungen wie ein Hinweis im App-Store 'Dies ist kein Medizinprodukt' umgehen die genannten Kriterien nicht und werden bei BfArM-Entscheidungen nicht berücksichtigt, wenn ein medizinischer Zweck … angegeben oder vermittelt wird."

Das bedeutet: Reine Forschungssoftware wird in der BfArM-Lesart nur dann privilegiert, wenn sie **objektiv** keinem medizinischen Zweck dient. Die Kennzeichnung "RUO" allein reicht nicht — sie muss durch Produktgestaltung gestützt werden.

### 6.6 Zwischenergebnis Vergleichsfälle

Keines der drei großen klinischen Nachschlagewerke (UpToDate, AMBOSS, Medscape) deklariert sich als "Research Use Only". Alle drei nutzen stattdessen:

1. "Educational purposes / Informationsplattform" statt "Research Use Only"
2. Klare Delegation der medizinischen Verantwortung an den Arzt
3. Haftungsbegrenzung in AGB (teilweise angreifbar, aber praxisrelevant)
4. Keine Patientenspezifik in der Kern-Architektur

Akademische Open-Source-Tools nutzen dagegen **aktiv RUO-ähnliche Formulierungen** in Kombination mit Open-Source-Lizenz-Disclaimern. Sie richten sich an Forschende, nicht an Endanwender.

Die VerordnungsAmpel liegt **zwischen** beiden Welten: Sie soll langfristig Vertragsärzten zur Verfügung stehen (Pflicht-Einsatz-Kontext), wird aber als Open-Source-Projekt unter Förderung des Prototype Fund entwickelt. Diese Zwitterstellung spricht für eine **abgestufte** Kennzeichnungsstrategie (siehe Variante C in Abschnitt 7).

---

## 7. Analyse der drei Varianten

### 7.1 Variante A: Reine Research-Use-Only-Kennzeichnung

**Kernbotschaft:** "Dieses Tool ist ein Forschungsprototyp. Jede Nutzung ausserhalb kontrollierter Forschungs- und Evaluations-Kontexte ist untersagt."

| Dimension | Bewertung |
|---|---|
| **MDR-Schutz** | Sehr hoch (Software ist nicht in Verkehr gebracht nach Art. 5 MDR, falls konsequent umgesetzt) |
| **Haftungsreduktion** | Hoch, aber nur bei konsistenter Nutzungsbegrenzung |
| **Praxisnützlichkeit** | **Sehr gering** — das Tool erreicht genau die Zielgruppe nicht, für die es gebaut wurde |
| **Förderfähigkeit** | Prototype Fund-kompatibel, aber dauerhafter Pilot-Status ist unbefriedigend |
| **Strategisches Risiko** | **Sehr hoch** — Projektziel (155.678 Vertragsärzte entlasten) scheitert strukturell |
| **Drift-Risiko** | Mittel — wenn das Tool nach Pilot-Ende "einfach so" weiter genutzt wird, entfaltet der Disclaimer keine Wirkung |

**Problem:** Die VerordnungsAmpel soll laut KONZEPT.md **nach** der Pilot-Phase als öffentliches Tool für alle Vertragsärzte verfügbar werden. Eine reine RUO-Kennzeichnung würde diesen Übergang blockieren oder unrealistisch machen, weil sie entweder falsch würde (Drift-Risiko) oder das Produktziel unterläuft.

### 7.2 Variante B: Informationswerk-Kennzeichnung (Status quo des Hauptgutachtens)

**Kernbotschaft:** "Dieses Tool ist ein öffentliches Nachschlagewerk zu sozialrechtlichen Verordnungsregelwerken. Es ist kein Medizinprodukt und ersetzt keine ärztliche Entscheidung."

| Dimension | Bewertung |
|---|---|
| **MDR-Schutz** | Hoch, wenn Zweckbestimmung konsequent durchgehalten wird |
| **Haftungsreduktion** | Mittel — deckt Instruktionsfehler, aber nicht die vollständige vorhersehbare Fehlanwendung |
| **Praxisnützlichkeit** | Hoch — das Tool kann genutzt werden, wie es gedacht ist |
| **Förderfähigkeit** | Gut |
| **Strategisches Risiko** | Mittel — MDSW-Drift bleibt möglich, wenn Features wachsen |
| **Drift-Risiko** | Mittel |

Dies ist die im Hauptgutachten empfohlene Variante.

### 7.3 Variante C: Kombinierte Kennzeichnung (Informationswerk + Nicht-klinisch-validiert + Nutzung auf eigenes Risiko)

**Kernbotschaft:** "Dieses Tool ist ein öffentliches Informations- und Nachschlagewerk (kein Medizinprodukt). Es ist **nicht klinisch validiert**, ersetzt keine ärztliche Entscheidung, und die **medizinische Verantwortung liegt beim verordnenden Arzt**. In der Pilot-Phase: ausschliesslich für Evaluations-Zwecke durch akkreditierte Pilot-Praxen."

Diese Variante kombiniert die juristische Schutzwirkung des Informationswerks (niedriges MDR-Risiko) mit den Schutzelementen einer RUO-Kennzeichnung (explizit "nicht klinisch validiert" + "eigenes Risiko").

| Dimension | Bewertung |
|---|---|
| **MDR-Schutz** | Hoch bis sehr hoch (Zweckbestimmung + explizite Nicht-Validierung) |
| **Haftungsreduktion** | Hoch — deckt Instruktionsfehler UND Vorhersehbarkeits-Einwand |
| **Praxisnützlichkeit** | Hoch — das Tool ist nutzbar |
| **Förderfähigkeit** | Sehr gut — Prototype Fund bevorzugt explizit Forschungs-/Pilot-Kontext |
| **Strategisches Risiko** | Niedrig — die Kennzeichnung skaliert mit dem Projektreifegrad |
| **Drift-Risiko** | Niedrig — bei Funktionserweiterung kann die Kennzeichnung anlass-spezifisch geändert werden |

**Diese Variante ist rechtlich am belastbarsten und zugleich praxistauglich.**

### 7.4 Strategischer Gestaltungs-Vorschlag für Variante C

Die Variante C ist in drei Stufen aufzubauen:

**Stufe 1 (MVP + Pilot, 2026):**
- Explizite Forschungs-Phase-Kennzeichnung: "Pilot-Release für akkreditierte Evaluations-Praxen"
- RUO-nahe Sprache in README, Startscreen, Footer
- Formelles Pilotteilnahmevereinbarungs-Dokument mit Arzt-Seite

**Stufe 2 (Public Beta, 2027):**
- Wechsel auf Informationswerk-Sprache, aber mit explizitem Hinweis "nicht klinisch validiert"
- Haftungs-Delegations-Klausel: "Medizinische Verantwortung beim Arzt"
- Versions-Transparenz und Quellenangaben zu jedem Regelwerk

**Stufe 3 (nach Anwalts-Freigabe / ggf. BfArM-Klassifikation, 2028+):**
- Informationswerk-Kennzeichnung als Standardmodus
- Optional: BfArM-Abgrenzungsantrag nach § 6 MPDG für Rechtssicherheit

---

## 8. Empfehlung mit konkreten UI-/Marketing-Bausteinen

### 8.1 Empfehlung (Kurzfassung)

**Variante C — kombinierte Kennzeichnung — wird empfohlen.** Reine RUO-Kennzeichnung (Variante A) untergräbt das Projektziel; reine Informationswerk-Kennzeichnung (Variante B) nutzt den verfügbaren Schutzspielraum nicht voll aus. Die Kombination bietet die höchste Haftungs-Resilienz bei gleichbleibender Praxistauglichkeit.

**Die RUO-Sprache wird tragend in der Pilot-Phase (2026) eingesetzt, danach aber in eine differenziertere Informationswerk-Sprache überführt, die die Kernelemente des RUO-Schutzes bewahrt.**

### 8.2 Konkrete Textbausteine

#### 8.2.1 `README.md` (Projekthauptseite, Pilot-Phase)

```markdown
## Status und Zweckbestimmung

**VerordnungsAmpel_SOCIAL ist ein Forschungs- und Pilotprojekt.**

Dieses Tool ist ein öffentliches Informations- und Nachschlagewerk zu
sozialrechtlichen Verordnungsregelwerken (AM-RL des G-BA, § 29 BMV-Ä,
§ 31 Abs. 6 SGB V, PRISCUS-Liste). Es dient der strukturierten
Dokumentationshilfe zur Regress-Prävention nach § 106 SGB V.

**Was dieses Tool NICHT ist:**
- Es ist kein Medizinprodukt im Sinne der Verordnung (EU) 2017/745 (MDR).
- Es ist nicht CE-zertifiziert.
- Es stellt keine Diagnose, gibt keine Therapieempfehlung, bewertet keine
  konkreten Patientinnen/Patienten.
- Es ist nicht klinisch validiert.
- Es verarbeitet keine personenbezogenen Patientendaten.

**Medizinische Verantwortung:** Die Verantwortung für jede Verordnung
liegt ausschliesslich beim verordnenden Arzt. Dieses Tool ersetzt keine
ärztliche Prüfung.

**Pilot-Phase 2026:** Die Nutzung ist in dieser Phase ausschliesslich für
akkreditierte Pilot-Praxen und akademische Evaluations-Partner bestimmt.
Nutzung ausserhalb dieses Rahmens erfolgt auf eigenes Risiko.
```

#### 8.2.2 `pyproject.toml` — Metadaten

```toml
[project]
name = "verordnungsampel-social"
description = "Informations- und Nachschlagewerk zu sozialrechtlichen Verordnungsregelwerken. Kein Medizinprodukt. Nicht klinisch validiert. Nutzung in Verantwortung des verordnenden Arztes."
keywords = [
    "information-tool",
    "regress-praevention",
    "sgb-v",
    "am-rl",
    "research-prototype",
    "not-a-medical-device"
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Topic :: Scientific/Engineering :: Medical Science Apps."
]
```

Der letzte Classifier ist bewusst neutral gehalten. Zu vermeiden sind Classifier, die einen diagnostischen oder therapeutischen Zweck nahelegen.

#### 8.2.3 GUI-Startscreen (PWA und CLI)

**CLI-Eingangs-Banner (erste Ausführung + ggf. persistent):**

```
==========================================================
VerordnungsAmpel - Informationswerk zu Verordnungsregelwerken
Version 0.x.y (Pilot 2026)

WICHTIG:
* Kein Medizinprodukt. Nicht CE-zertifiziert. Nicht klinisch validiert.
* Keine Diagnose, keine Therapieempfehlung, keine Patientenbewertung.
* Medizinische Verantwortung liegt ausschliesslich beim verordnenden Arzt.
* Pilot-Phase 2026: Nutzung nur durch akkreditierte Pilot-Praxen.
  Darueber hinaus: Nutzung auf eigenes Risiko.

Mit Bestaetigung (Enter) stimmen Sie der Kenntnisnahme zu.
==========================================================
```

**PWA-Startscreen:**
- Überschrift: *"Informationswerk zu Verordnungsregelwerken"*
- Erste Zeile: *"Kein Medizinprodukt * Nicht klinisch validiert * Verantwortung beim Arzt"*
- Pflicht-Checkbox bei Erststart: *"Ich habe die Zweckbestimmung zur Kenntnis genommen und nutze die Software in eigener medizinischer Verantwortung."*
- Akzept wird lokal protokolliert (im Compliance-Log, mit Datum + Version der Zweckbestimmung).

**Persistente Fußzeile:**
```
Informationswerk * Kein Medizinprodukt * Keine Therapieempfehlung *
Medizinische Verantwortung beim Arzt * Nicht klinisch validiert
```

#### 8.2.4 Förderantrag Prototype Fund

Vorgeschlagene Formulierung im Förderantrag:

> "VerordnungsAmpel_SOCIAL ist ein Forschungs- und Pilotprojekt zur
> Entwicklung eines Open-Source-Informationswerks zu sozialrechtlichen
> Verordnungsregelwerken. Ziel ist die strukturierte Dokumentationshilfe
> zur Regress-Prävention nach § 106 SGB V für niedergelassene Vertragsärzte.
>
> Das Projekt positioniert sich ausdrücklich nicht als Medizinprodukt
> (weder MDSW im Sinne der MDR noch DiGA im Sinne des SGB V). Es verarbeitet
> keine personenbezogenen Patientendaten und trifft keine medizinischen
> Aussagen. Die medizinische Verantwortung für jede Verordnung liegt
> ausschliesslich beim verordnenden Arzt.
>
> In der geförderten Pilot-Phase wird das Tool ausschliesslich durch
> akkreditierte Pilot-Praxen und akademische Evaluations-Partner eingesetzt."

Diese Sprache erfüllt zwei Zwecke: (a) sie ist MDR-neutral und RUO-nah, (b) sie signalisiert dem Prototype Fund die typische Profil-Passung (Open Source, Pilot, nicht-kommerziell).

#### 8.2.5 GUI bei Ampel-Ergebnis — kontextbezogener Hinweis

Bei jedem GELB/ROT-Ergebnis:
```
Dieser Hinweis basiert auf der AM-RL Anlage III, Position X.Y (Stand 2026-Q2).
Er ersetzt KEINE eigene Pruefung durch den verordnenden Arzt.
Dieses Tool ist kein Medizinprodukt.
```

Bei jedem GRÜN-Ergebnis:
```
Kein Treffer in den geprueften Regelwerken (AM-RL III/V/VI, PRISCUS,
Praxisbesonderheiten-Liste). Dies ist KEINE Verordnungs-Freigabe.
Die medizinische Indikationspruefung liegt beim Arzt.
```

#### 8.2.6 Werbe- und Kommunikationsregeln (verbindlich)

**Zu vermeiden — triggert MDR-Risiko oder entwertet RUO-Schutz:**

- "Klinische Entscheidungsunterstützung"
- "KI-Ampel für sichere Verordnung"
- "Sicherheit für den Patienten" als Primärnutzen
- "Diagnose", "Prognose", "Prädiktion"
- "Zertifizierte Software"
- "Ärzte-zugelassenes Tool"

**Empfohlen — stützt Zweckbestimmung und RUO-Schutz:**

- "Nachschlagewerk"
- "Informationswerkzeug"
- "Regress-Prävention"
- "Dokumentationshilfe"
- "Rechts-Referenz für Verordnungen"
- "Pilot-Projekt für Praxis-Compliance"

### 8.3 Eskalationsstufen

**Falls während des Pilots ein Schadensfall eintritt** (Arzt vertraut Ampel falsch, Patient schadet):

1. Sofortige Analyse des konkreten Datensatzes und der Regelwerksversion
2. Dokumentation der konkreten Nutzungs-Kette (Log-Datei)
3. Anwaltliche Beratung zu Meldepflichten und Kommunikation
4. Pilot-Vereinbarung hilft: diese dokumentiert die RUO-Akzeptanz des Pilot-Arztes

**Falls ein MDR-Klassifizierungsverfahren eingeleitet wird:**

1. RUO-/Nicht-klinisch-validiert-Dokumentation einreichen
2. Subsumtion des Hauptgutachtens (Snitem-Kriterium) verfügbar machen
3. Anwalt zur formalen Verteidigung einschalten
4. Ggf. freiwilliger Antrag nach § 6 MPDG zur verbindlichen Klärung

---

## 9. Grenzen dieser Einschätzung + Anwaltsempfehlung

### 9.1 Was diese Einschätzung leistet

- Analyse der RUO-Kategorie im EU-Recht mit Abgrenzung zu FDA und IVDR.
- Bewertung der Schutzwirkung in Produkthaftung, Deliktsrecht, Strafrecht.
- Vergleich mit etablierten Tools (UpToDate, AMBOSS, Medscape).
- Konkrete Handlungsempfehlung (Variante C) mit UI-/Marketing-Bausteinen.
- Transparente Quellenangabe.

### 9.2 Was diese Einschätzung nicht leistet

- Keine verbindliche Rechtsauskunft.
- Keine Prüfung konkreter vertraglicher Dokumente mit Pilot-Praxen (wird separat benötigt).
- Keine Gewährleistung, dass eine Marktaufsichtsbehörde oder ein Gericht die vorgeschlagenen Formulierungen akzeptiert.
- Keine Prüfung DSGVO- und datenschutzrechtlicher Konsequenzen (siehe separates DSGVO-Konzept).
- Keine Prüfung der Prototype-Fund-Förderrichtlinien im konkreten Antragsjahr.

### 9.3 Empfohlene Eskalation

**Vor Public-Release-Ankündigung** und **vor Vertrags-Template-Freigabe für Pilot-Praxen** wird die Konsultation eines Fachanwalts für Medizin- oder Medizinprodukterecht dringend empfohlen. Kostenrahmen Erstberatung 190–400 EUR netto nach RVG.

**Fokusfragen für das Anwaltsgespräch:**

1. Wird Variante C (kombinierte Kennzeichnung) als belastbar beurteilt? Sind die Textbausteine in Punkt 8.2 wasserfest?
2. Muss die Pilot-Vereinbarung mit akkreditierten Praxen besondere Haftungsklauseln enthalten?
3. Welche Kombination aus Lizenz (GPL-3.0) + RUO-Hinweis + Haftungsausschluss ist maximal wirksam?
4. Wird eine Produkt-Haftpflichtversicherung (z. B. IT-Haftpflicht mit MedTech-Klausel) empfohlen? Kostenrahmen?
5. Soll der Übergang von Pilot- zu Public-Beta-Kennzeichnung formalisiert werden (z. B. Board-Beschluss, Versionsnote)?

**Illustrative Anwalts-Kandidaten** (rein hinweisend; nicht geprüft): Taylor Wessing (Medical Devices/Health Tech), CMS Hasche Sigle (Life Sciences), Fieldfisher (eHealth), Noerr (Life Sciences + Datenschutz), Voelker & Partner (Medical Apps); Fachverbandsempfehlungen: bvitg, Spitzenverband Digitale Gesundheitsversorgung (SVDGV).

### 9.4 Anwendungsbereich dieser Einschätzung

Diese Einschätzung bezieht sich auf die VerordnungsAmpel_SOCIAL in der Spezifikation laut KONZEPT.md v1 (Stand 2026-04-08) sowie das parallele Hauptgutachten `RECHTSGUTACHTEN_MDSW.md` vom 12.04.2026. Bei Feature-Erweiterungen (insbesondere: Patienten-IDs, klinische Messwerte, Therapievorschläge, KI-Modelle zur Indikationsprüfung) ist das Gutachten **zwingend neu zu erstellen**.

---

## 10. Quellenverzeichnis

### 10.1 Primärrecht (EU)

- Verordnung (EU) 2017/745 (MDR) — Art. 2 Nr. 1, Nr. 12, Nr. 22, Art. 5, Art. 62 ff., Erwägungsgründe 19, 32, 63 — [EUR-Lex 32017R0745](https://eur-lex.europa.eu/eli/reg/2017/745/oj).
- Verordnung (EU) 2017/746 (IVDR) — Art. 2 Nr. 2, Nr. 13, Art. 5 Abs. 1 und 5 — [EUR-Lex 32017R0746](https://eur-lex.europa.eu/eli/reg/2017/746/oj).
- Produkthaftungs-Richtlinie (EU) 2024/2853 (Nachfolge 85/374/EWG) — Umsetzungsfrist Dezember 2026.

### 10.2 Leitfäden und Behördenquellen

- MDCG 2019-11 Rev. 1 (06/2025) — Guidance on Qualification and Classification of Software — [health.ec.europa.eu](https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en).
- BfArM — FAQ Abgrenzung und Klassifizierung (Stand 2025) — [bfarm.de](https://www.bfarm.de/DE/Medizinprodukte/_FAQ/Klassifizierung-Abgrenzung/faq-liste.html).
- BfArM — Feststellung rechtlicher Status und Klassifizierung nach § 6 MPDG — [bfarm.de](https://www.bfarm.de/DE/Medizinprodukte/Aufgaben/Festellung-rechtlicher-Status-und-Klassifizierung/_artikel.html).
- BfArM — Klinische Prüfungen und Leistungsstudien — [bfarm.de](https://www.bfarm.de/DE/Medizinprodukte/Aufgaben/Klinische-Pruefungen-und-Leistungsstudien/Klinische-Pruefungen/Anzeige-nach-Inverkehrbringen-pmcf-KP/_artikel.html).
- FDA — Guidance "Distribution of IVD Products Labeled for Research Use Only or Investigational Use Only" (November 2013).

### 10.3 Deutsches Recht

- Medizinprodukterecht-Durchführungsgesetz (MPDG) v. 28.04.2020, insb. §§ 6, 92 ff. — [gesetze-im-internet.de](https://www.gesetze-im-internet.de/mpdg/).
- Produkthaftungsgesetz (ProdHaftG), insb. §§ 1, 3, 14 — [dejure.org § 3 ProdHaftG](https://dejure.org/gesetze/ProdHaftG/3.html).
- § 823 Abs. 1 BGB — Produzentenhaftung nach BGH, ständige Rspr. seit "Hühnerpest" 1968 (NJW 1969, 269).
- §§ 229, 222 StGB — Fahrlässige Körperverletzung/Tötung — [dejure § 229 StGB](https://dejure.org/gesetze/StGB/229.html).
- § 203 StGB — Berufsgeheimnis.
- § 309 Nr. 7, 8 BGB — AGB-Grenzen der Haftungsbegrenzung.
- Heilmittelwerbegesetz (HWG), insb. §§ 3, 3a.

### 10.4 Rechtsprechung

- EuGH, Urt. v. 07.12.2017 — Rs. C-329/16 (Snitem/Philips France) — [curia.europa.eu](https://curia.europa.eu/juris/liste.jsf?language=de&td=ALL&num=C-329/16).
- BGH, Urt. v. 26.06.2008 — I ZR 61/05 (Nahrungsergänzung/Arzneimittel-Abgrenzung, Zweckbestimmungs-Maßstab).
- BGH, Urt. v. 30.03.2006 — I ZR 24/03 (Wirksamkeit eines Disclaimer zur Reichweitenbeschränkung) — [aufrecht.de Kommentar](https://www.aufrecht.de/urteile/internetrecht/wirksame-beschraenkung-des-verbreitungsgebiets-durch-disclaimer-bgh-urteil-vom-300306-az-i-zr-2403).
- BGH, Urt. v. 16.06.2009 — VI ZR 107/08 (Instruktionspflichten, Reichweite und Grenzen) — [Stephan-Lorenz.de Urteilsdatenbank](https://lorenz.userweb.mwn.de/urteile/vizr107_08.htm).

### 10.5 Fachkommentare und Leitartikel

- Johner Institut — "Zweckbestimmung und bestimmungsgemäßer Gebrauch" — [johner-institut.de](https://www.johner-institut.de/blog/regulatory-affairs/zweckbestimmung/).
- Johner Institut — "Vorhersehbarer Missbrauch" — [johner-institut.de](https://www.johner-institut.de/blog/iso-14971-risikomanagement/vorhersehbarer-missbrauch/).
- Johner Institut — "Clinical investigations of medical devices under MDR" — [blog.johner-institute.com](https://blog.johner-institute.com/regulatory-affairs/clinical-investigations-of-medical-devices/).
- Johner Institut — "Produkthaftung: Medizinproduktehersteller aufgepasst!" — [johner-institut.de](https://www.johner-institut.de/blog/regulatory-affairs/produkthaftung/).
- TÜV Süd — "Artikel 5 MDR: Inverkehrbringen und Inbetriebnahme" — [de-mdr-ivdr.tuvsud.com](https://de-mdr-ivdr.tuvsud.com/Artikel-5-Inverkehrbringen-und-Inbetriebnahme.html).
- IT-Recht Kanzlei — "Rechtscheck: Kann ein Disclaimer die Produkthaftung ausschliessen?" — [it-recht-kanzlei.de](https://www.it-recht-kanzlei.de/disclaimer-haftungsausschluss-produkthaftung-selbstformuliert.html).
- IT-Recht Kanzlei — "BGH-Urteil: Zur Abgrenzung Nahrungsergänzungsmittel und Arzneimittel" — [it-recht-kanzlei.de](https://www.it-recht-kanzlei.de/5/HWG_Gesetz_ueber_die_Werbung_auf_dem_Gebiet_des_Heilwesens/nahrungsergaenzungsmittel-arzneimittel.html).
- wi-lex — "Produkt- und Produzentenhaftung bei Software" — [wi-lex.de](https://wi-lex.de/index.php/lexikon/uebergreifender-teil/kontext-und-grundlagen/it-recht/produkt-und-produzentenhaftung-bei-software/).
- Müller, A.-K. — "Software als 'Gegenstand' der Produkthaftung" (DWV/FU Berlin) — [refubium.fu-berlin.de](https://refubium.fu-berlin.de/bitstream/handle/fub188/27647/Müller_Software_als_Gegenstand_der_Produkthaftung.pdf).
- Hoffmeister et al. — "Structure and content of the EU-IVDR" (Pathologie 2022) — [link.springer.com](https://link.springer.com/article/10.1007/s00292-022-01176-z).

### 10.6 Vergleichs-Quellen

- UpToDate (Wolters Kluwer) Terms of Use — [wolterskluwer.com Clinical Effectiveness Terms](https://www.wolterskluwer.com/en/know/clinical-effectiveness-terms).
- Medscape Network Terms of Use — [medscape.com/public/termsofuse](https://www.medscape.com/public/termsofuse).
- Medscape EEA Notice — [medscape.com/public/eu-users](https://www.medscape.com/public/eu-users).
- AMBOSS — [amboss.com](https://www.amboss.com/) (Produktkommunikation, nicht MDR-deklariertes Nachschlagewerk; AGB sessionpflichtig).
- OHDSI — [ohdsi.org](https://www.ohdsi.org/) (Apache-2.0 + typischer Research-Use-Disclaimer).
- openEHR — [openehr.org](https://www.openehr.org/) (Spezifikation ohne MDR-Anspruch).

### 10.7 Hintergrund Projekt

- VerordnungsAmpel_SOCIAL KONZEPT.md v1, Stand 2026-04-08 (lokal).
- `RECHTSGUTACHTEN_MDSW.md`, Stand 2026-04-12 (lokal, Hauptgutachten).
- `DSGVO_KONZEPT.md`, Stand 2026 (lokal).
- Um:bruch Policy `Policies/RECHTSABTEILUNG.md`, Stand 02.04.2026.

---

## Disclaimer (Schlussklausel)

Diese Einschätzung ist eine **KI-basierte Erstanalyse** der Um:bruch-Rechtsabteilung (Rolle RB, Besetzung Claude) und **ersetzt keine anwaltliche Beratung**. Die Risikoeinschätzung der vorgeschlagenen Variante C ist **niedrig bis mittel**; vor Public Release (spätestens vor Prototype-Fund-Einreichung) wird eine Konsultation eines Fachanwalts für Medizinprodukterecht empfohlen.

**Prüfende Stelle:** Um:bruch e. V. (i. Gr.) — Rechtsabteilung RB
**Bearbeiter:** Claude (CL), als KI-Rolle
**Ablage:** `_editorial/recht_2026-04-12_VerordnungsAmpel_RUO.md` (Referenzkopie für die Um:bruch-Redaktionssitzung)

*Ende des Folgegutachtens.*
