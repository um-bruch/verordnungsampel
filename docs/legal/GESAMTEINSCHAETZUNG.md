# Rechts-Gesamteinschätzung — VerordnungsAmpel_SOCIAL

**Datum:** 2026-04-12
**Verfasser:** Claude (CL), Um:bruch Rechtsabteilung (RB)
**Typ:** Synthese-Gutachten aller bisherigen Einzelgutachten + Umsetzungs-Audit
**Auftrag:** Lukas Geiger (Projekt-Initiator), 2026-04-12
**Status:** KI-basierte Ersteinschätzung — kein Anwaltsersatz (siehe Kapitel 9)

---

## 1. Executive Summary

Das Projekt VerordnungsAmpel_SOCIAL ist nach vier parallelen Einzelgutachten (MDSW, DSGVO, RUO, Publikation/Lizenz, Haftung) und dem Repo-Audit **rechtlich tragfähig**, wenn es als reines Open-Source-Informationswerk ohne Trägerkonstellation, ohne Pilot-Praxen und ohne Vermarktungsversprechen veröffentlicht wird. Die sechs Ampel-Dimensionen stehen auf **§ 521 BGB Schenkungsprivileg GRÜN, MDR GRÜN–GELB, DSGVO GRÜN, Lizenz/Marke GELB, PLD 2024/2853 GRÜN, UWG/§ 444 BGB GELB**. Die Disclaimer-Architektur (NOTICE, README-Disclaimer-Block, persistenter Erststart-Dialog mit vier Pflicht-Checkboxen + Hash-Chain-Versiegelung, permanente GUI-Statuszeile) ist wirksam umgesetzt und bringt das Projekt in die "kein Medizinprodukt / Nutzung auf eigenes Risiko"-Schutzzone, die die Gutachten verlangen. Die in README, NOTICE, CHANGELOG und ABOUT_TEXT umgesetzte Zweckbestimmungs-Deeskalation ("Regress-Prävention" fallengelassen, ersetzt durch "Risikoindikatoren-Anzeige zu Forschungszwecken") entspricht präzise der MDSW-Empfehlung 3.2.1 und der RUO-Variante C. Als **einziger inhaltlich-kritischer Rest-Widerspruch** verbleibt, dass `src/verordnungsampel/gui/strings_de.py` in `APP_TAGLINE` und `TRAY_TOOLTIP` noch "Regress-Prävention" schreibt, während NOTICE, README und ABOUT_TEXT den Begriff bereits explizit fallengelassen haben — das ist ein Umsetzungs-Fehlschluss, leicht behebbar, aber ein § 5 UWG / § 444 BGB-Angriffsfläche. Release-Readiness: **Privater GitHub-Stand ist heute gegeben; Public-Release ist unter Behebung von drei Restposten (Tagline-Fix, "Um:bruch e.V."-Zeile in DSGVO_KONZEPT.md, LICENSE-Copyright-Zeile) innerhalb von 1–2 Arbeitsstunden erreichbar**; Zenodo-Archivierung sinnvoll erst nach Public-Release; **Pilotierung in echten Praxen ist auf Basis dieser Einschätzung weiterhin NICHT empfohlen** (KONZEPT.md-Revision 2026-04-12 hat die Pilot-Option selbst fallengelassen — das ist eine Stärke, keine Lücke). Top-3-Rest: (a) Tagline und Tray-Tooltip im Code korrigieren, (b) Copyright-Zeile in LICENSE-Kopf auf "Lukas Geiger (c/o Um:bruch Think Tank)" vereinheitlichen und letzte "Um:bruch e.V."-Referenzen in DSGVO_KONZEPT säubern, (c) DPMA-Identitäts-/Ähnlichkeitsrecherche zu "VerordnungsAmpel" in Klassen 09/42/44 vor dem Public-Announcement durchführen.

---

## 2. Konsistenz-Check der Einzelgutachten

Geprüft wurden fünf Einzelgutachten und ein Audit. Alle sind vom 12.04.2026 und vom selben Verfasser (CL), was Konsistenz begünstigt, aber auch Klumpenrisiko birgt (kein interner Gegenzeuge).

### 2.1 Linie der Einzelgutachten

| Gutachten | Kernaussage | Ampel |
|---|---|---|
| `RECHTSGUTACHTEN_MDSW.md` | Bei sauberer Zweckbestimmung kein MDSW nach MDR Art. 2 Nr. 1; Subsumtion via MDCG 2019-11 Rev. 1 und EuGH C-329/16 Snitem (keine patientenspezifischen Daten, reine Table-Lookup-Funktion, sozialrechtlich-administrativer Zweck). | Gesamt: **mittel** → niedrig bei Umsetzung |
| `DSGVO_KONZEPT.md` | Kein Auftragsverarbeiter, kein Verantwortlicher; Verantwortlicher ist der Arzt. Keine personenbezogenen Daten im Tool, nur ICD/ATC (+ optional Pseudonym). Hash-Chain ↔ Art. 17 durch Bulk-Purge gelöst. | **niedrig** |
| `RECHTSGUTACHTEN_RUO.md` | Reine RUO-Kennzeichnung (Variante A) untergräbt Projektziel; empfohlen ist **Variante C** (Informationswerk + "nicht klinisch validiert" + "eigenes Risiko" + optional "Pilot-Phase nur für akkreditierte Praxen"). | **niedrig bis mittel** |
| `RECHTSGUTACHTEN_PUBLIKATION_LIZENZ.md` | Veröffentlichungsfähig auf GitHub. Drei Blocker: (1) LICENSE-Volltext fehlt, (2) Copyright "Um:bruch e.V." existiert nicht, (3) "Therapiefreiheit e.V." ohne Zustimmung genannt. | Blocker-behebbar |
| `RECHTSGUTACHTEN_HAFTUNG.md` | § 521 BGB greift voll, § 823 BGB kein Zugriff auf Vermögensschaden, PLD 2024/2853 OSS-Ausnahme greift bei Nicht-Gewerblichkeit. Voraussetzung: Disclaimer, Erststart-Acknowledgement, keine Zusicherungen. | **GERING** bei Umsetzung |
| `RECHTSAUDIT_ALLE_PROJEKTE.md` | VerordnungsAmpel auf Stufe 4 (Medizin). Muster für andere Stufe-4-Repos. Keine eigenständige neue Aussage zum Projekt. | — |

### 2.2 Widersprüche / Spannungen

**Keine harten inhaltlichen Widersprüche.** Die Gutachten bauen aufeinander auf und ziehen konsistent an einem Strang. Es gibt drei **Spannungen**, die durch die Projekt-Revision vom 12.04.2026 (KONZEPT.md Kopfzeile) aber **bereits aufgelöst** sind:

1. **Pilot-Phase vs. kein Pilot.** RUO-Gutachten Variante C Stufe 1 (S. 7.4) empfiehlt noch "Pilot-Release für akkreditierte Evaluations-Praxen" als Schutz-Narrativ. KONZEPT.md-Revision 2026-04-12 hat die Pilot-Phase **komplett gestrichen** ("ohne Pilot-Praxen, ohne Kooperationsankündigung"). Auflösung: Die RUO-Variante-C-Sprache wird durch eine noch enger gefasste Variante ersetzt — "reines OSS-Forschungs- und Weiterentwicklungs-Nachschlagewerk ohne Träger". Das ist **mindestens gleich, eher besser** aus Haftungssicht, weil keine Pilot-Vereinbarungen benötigt werden.
2. **"Regress-Prävention" als Claim vs. Fallen-gelassen.** MDSW-Gutachten 2.7/3.2 warnte vor therapeutischen Claims; RUO-Gutachten 8.2.6 verlangte neutrale Sprache ("Dokumentationshilfe", "Rechts-Referenz"). README, NOTICE und CHANGELOG (2026-04-12) haben "Regress-Prävention" als Vermarktungsbegriff gestrichen. Spannung ist **konzeptionell aufgelöst**, aber in `strings_de.py` **noch nicht durchgezogen** (siehe Umsetzungs-Matrix, Kap. 3).
3. **"Um:bruch e.V." in LICENSE/Urheber vs. kein e.V. existiert.** Publikations-Gutachten 2.4 adressiert genau diese Inkonsistenz. In NOTICE und README bereits korrigiert ("Lukas Geiger (c/o Um:bruch Think Tank)"), in `DSGVO_KONZEPT.md` Zeile 70 ist die alte Zuschreibung noch als Tabellen-Eintrag vorhanden.

### 2.3 Methodische Anmerkung

Alle Gutachten markieren sich korrekt als **KI-basierte Erstanalyse** und benennen die Grenzen. Die Quellenapparate sind überdurchschnittlich dicht (MDR, MDCG 2019-11 Rev. 1, EuGH C-329/16, BGB-Schenkungsrecht, PLD 2024/2853, ifrOSS). Das entspricht der Policy `RECHTSABTEILUNG.md` Abschnitt 2.

---

## 3. Umsetzungsstatus — Empfehlungs-Matrix

Die Matrix zeigt, welche Empfehlung aus welchem Gutachten im Repository **tatsächlich** umgesetzt ist.

### 3.1 MDSW-Gutachten — Maßnahmen aus 3.2

| # | Empfehlung MDSW 3.2.x | Status | Fundstelle |
|---|---|---|---|
| M1 | Verbindliche Zweckbestimmungs-Formulierung ("Informationswerk ... kein Medizinprodukt ... medizinische Verantwortung beim Arzt") in README, pyproject.toml, Impressum, jeder öffentlichen Kommunikation | **Umgesetzt** | README.md Z. 13–38; NOTICE Z. 10–30 |
| M2 | Kein Patienten-Identifier in UI (keine Felder Name/Geburtsdatum/PID); Alter nur abstrakt | **Umgesetzt** | `strings_de.py` `CHECK_AGE_LABEL` = nur "Alter (optional)", kein Patientenname in GUI-Strings |
| M3 | Keine "Fall-Speicherung" — stateless, Log speichert Events nicht Patienten | **Umgesetzt** | Compliance-Log-Architektur laut DSGVO_KONZEPT 3.2 V3 |
| M4 | Keine Therapie-Vorschläge, keine Alternativen aus Eigenleistung | **Umgesetzt** | GUI-Strings enthalten keine "schlage vor …"-Formulierungen |
| M5 | Ampel-Label neutral halten ("AM-RL Anlage III — verordnungseingeschränkt", nicht "riskant") | **Umgesetzt** (Check-Tab-Hints) | `CHECK_HINT_UNKNOWN`, Ampel-Labels sind Status, nicht Urteil |
| M6 | Begründungstexte = Zitate aus Regelwerk | **Umgesetzt** (Seed-Daten mit `quelle`/`paragraph`) | `data/seed/README.md` + Regel-Seed |
| M7 | Persistent sichtbarer Disclaimer (Fußzeile) | **Umgesetzt** | `STATUS_PERMANENT_DISCLAIMER` = "Pre-Alpha — nicht klinisch validiert — keine Gewährleistung" |
| M8 | Erststart-Acknowledgement (Checkbox, protokolliert) | **Umgesetzt** | `src/verordnungsampel/gui/disclaimer_dialog.py` — 4 Pflicht-Checkboxen, NOTICE-Hash, Hash-Chain-Versiegelung |
| M9 | "Ersetzt keine eigene Prüfung" als inline-Hinweis bei jedem Ampel-Ergebnis | **Teilweise** | NOTICE und permanente Statuszeile vorhanden; inline-Hinweis direkt im Ampel-Output-String in `strings_de.py` nicht als eigene Konstante; vermutlich in Result-Label eingebettet, nicht verifiziert im Audit |
| M10 | Marketing-Blacklist einhalten (kein "Entscheidungsunterstützung", "KI", "Sicherheit", "Diagnose") | **Überwiegend umgesetzt** | README.md: sauber. `strings_de.py`: **"Regress-Prävention" in APP_TAGLINE und TRAY_TOOLTIP noch vorhanden** — Restposten |
| M11 | BfArM-Abgrenzungsantrag (§ 6 MPDG) | Optional, nicht umgesetzt | Empfehlung: erst bei Skalierung, siehe Kap. 6 |

### 3.2 DSGVO-Konzept — Maßnahmen aus 14.2–14.3

| # | Empfehlung DSGVO | Status | Fundstelle |
|---|---|---|---|
| E1 | `export --patient <Pseudonym> --format json` | Nicht verifiziert (CLI-Subcommand-Liste zeigt `init/check/log/verify/justify/workflow/remind` — kein `export`) | CHANGELOG 0.1.0 "CLI-Frontend mit 7 Subcommands"; `export` fehlt |
| E2 | `export --all --format json` | **Nicht umgesetzt** | s. o. |
| E3 | `purge --all` (Chain-Reset) | **Nicht umgesetzt** (kein Subcommand) | s. o. |
| E4 | `purge --older-than` | **Nicht umgesetzt** | s. o. |
| E5 | `purge --patient` | **Nicht umgesetzt** | s. o. |
| E6 | `config set praxis.name …` statt Hardcode | Unklar; `config`-Subcommand nicht gelistet, aber GUI-Workflow-Tab hat Praxisfeld → vermutlich in DB-Settings persistiert | `strings_de.py` WORKFLOW_PRAXIS etc. |
| E7 | Startup-Banner-Hinweis "keine Klartext-Patientendaten, Pseudonyme verwenden" | **Teilweise** (NOTICE + Disclaimer-Dialog erklären Pseudonymisierung nicht explizit) | NOTICE erwähnt Pseudonyme nicht ausdrücklich |
| E8 | SECURITY.md mit Coordinated-Disclosure | **Umgesetzt** | `SECURITY.md` vorhanden (laut Repo-Listing) |

**Bewertung:** Die DSGVO-Betroffenenrechte-CLI (E1–E5) ist die größte offene Lücke. Im aktuellen Zustand ohne Pilot-Praxen ist das **akzeptabel**, weil das Tool niemand in einer echten Praxis produktiv nutzt — und damit keine Betroffenenrechte real anfallen. Sollte jemals doch eine echte Nutzung entstehen (auch ohne Pilot), wären E1+E3 vor 30-Tages-Frist nachzureichen.

### 3.3 RUO-Gutachten — Maßnahmen aus 8.2

| # | Empfehlung RUO 8.2.x | Status |
|---|---|---|
| R1 | README-Block "Status und Zweckbestimmung" mit "Kein Medizinprodukt / Nicht klinisch validiert / Eigenes Risiko" | **Umgesetzt** (README Z. 13–38, sogar prominenter platziert als in 8.2.1 gefordert) |
| R2 | pyproject.toml description "Informations- und Nachschlagewerk … kein Medizinprodukt … nicht klinisch validiert" | **Teilweise** — die Description im `pyproject.toml` Z. 8 lautet "Softwareentwurf — Abgleich … ohne Gewähr, zu Forschungszwecken" — deckt die Essenz, aber nicht den RUO-vorgeschlagenen Wortlaut. Vertretbar, aber die Keyword-Liste enthält `"medizin"` als erstes Keyword, was Classifier `Medical Science Apps.` verstärkt — MDSW-Drift-Risiko niedrig. |
| R3 | CLI-Eingangs-Banner (Erstausführung persistent) | Nicht im Audit verifiziert — Disclaimer-Dialog deckt GUI ab, CLI-Erststart-Banner unklar |
| R4 | GUI-Startscreen Pflicht-Checkbox | **Umgesetzt** (`disclaimer_dialog.py` mit 4 Pflicht-Checkboxen + Enter-erzwungen, NOTICE-Hash-Persistierung) |
| R5 | Persistente Fußzeile "Informationswerk / Kein Medizinprodukt / Keine Therapieempfehlung / Medizinische Verantwortung beim Arzt / Nicht klinisch validiert" | **Teilweise** — `STATUS_PERMANENT_DISCLAIMER` kürzer gefasst. Vertretbar; RUO-Langform wäre sauberer. |
| R6 | Kontextbezogene Hinweise bei jedem GELB/ROT-Ergebnis | Nicht explizit als String-Konstante sichtbar; in der Result-Darstellung vermutlich enthalten, aber nicht verifiziert |
| R7 | Werbe- und Kommunikationsregeln (Blacklist) | **Teilweise** — siehe oben M10 zum "Regress-Prävention"-Restposten |

### 3.4 Publikation/Lizenz-Gutachten — Gate-Items 8.1–8.6

| # | Blocker/Gate | Status |
|---|---|---|
| P1 | LICENSE-Datei GPL-3.0-Volltext (≥90% SPDX) | **Umgesetzt** — 674 Zeilen GPL-Volltext vorhanden |
| P2 | Copyright-Zeile "Lukas Geiger (c/o Um:bruch Think Tank)" statt "Um:bruch e.V." | **Umgesetzt in NOTICE** (Z. 4). In LICENSE-Datei-Kopf: der GPL-3.0-Volltext beginnt mit FSF-Copyright-Kopf, Projekt-Copyright müsste separat vor den GPL-Text gesetzt sein. **Nicht im Audit verifiziert** — nach Publikations-Gutachten 5.1 Vorschlag (Projekt-Disclaimer + GPL-Volltext in einer Datei) vermutlich Grenzfall. |
| P3 | MDSW-Gutachten finalisiert | **Vorhanden** |
| P4 | RUO-Entscheidung dokumentiert, Kennzeichnung im README | **Umgesetzt** |
| P5 | DSGVO-Implementierung E1–E8 | Teilweise (s. 3.2) |
| P6 | DPMA-Recherche "VerordnungsAmpel" (Klassen 09/42/44) | **Nicht umgesetzt** (eigene Lücke — muss vor Public oder spätestens vor Marken-Announcement) |
| P7 | "Therapiefreiheit e.V." im Repo | **Umgesetzt** — in KONZEPT.md durchgestrichen und Revision dokumentiert; in DSGVO_KONZEPT.md Z. 70 aber noch in alter Tabelle als Miterwähnung, siehe 3.5 |
| P8 | Keine "Dr. Müller"-Beispiele → "Dr. med. Musterarzt" / "Musterpraxis" | **Umgesetzt** (README Z. 113) |
| P9 | Keine echten Krankenkassen-Namen in Beispielen | **Umgesetzt** (README Z. 112 "Musterkasse") |
| P10 | `AUFGABEN.txt` nicht committet | Lokal im Projekt-Root vorhanden, per `.gitignore` ausgeschlossen — **verifizierbar nur beim Staging** |
| P11 | `THIRD_PARTY_LICENSES.txt` | **Umgesetzt** (Datei vorhanden) |
| P12 | `LICENSES/` mit SPDX-Volltexten + REUSE-Compliance | **Nicht umgesetzt** (nice-to-have, kein Blocker) |
| P13 | FUNDING.yml, Issue-Templates | Nicht im Audit sichtbar; nach GITHUB-POLICY für SOCIAL-Repos Pflicht |
| P14 | CHANGELOG-Eintrag für aktuelle Version | **Umgesetzt** (Unreleased + 0.1.0 dokumentiert) |

### 3.5 Haftungs-Gutachten — Maßnahmen aus 10.1–10.7

| # | Empfehlung Haftung 10.x | Status |
|---|---|---|
| H1 | README-Disclaimer (10.1) | **Umgesetzt** (sogar prominenter als empfohlen) |
| H2 | GUI-Startscreen-Pflichtdialog (10.2) | **Umgesetzt** über `disclaimer_dialog.py` |
| H3 | Dauerhafte Statuszeile (10.3) | **Umgesetzt** (`STATUS_PERMANENT_DISCLAIMER`) |
| H4 | Ampel-Ausgabe-Fußzeile (10.4) | **Nicht explizit als String-Konstante verifiziert** |
| H5 | LICENSE_DE.md / NOTICE.md mit § 521 BGB-Hinweis (10.5) | **Umgesetzt** — NOTICE Z. 36–45 |
| H6 | Impressum auf Website (10.6) | Außerhalb des Repos — wird bei Go-Live auf um-bruch.org benötigt |
| H7 | Compliance-Log-Erststart-Eintrag mit Disclaimer-Hash (10.7) | **Umgesetzt** — `disclaimer_dialog.record_acceptance()` versiegelt als JSON-Extra in Hash-Chain |
| H8 | Haftpflichtversicherung (11.1) | Empfehlung, nicht zwingend; bei aktueller Nicht-Gewerblichkeit + Nicht-Piloting **nicht akut** |
| H9 | Vereinsgründung e.V. (11.2) | Offene Diskussion; KONZEPT.md Revision hat explizit "keine Rechtsform aktuell" entschieden. § 521 BGB + PLD-OSS-Ausnahme schützt auch natürliche Person (siehe Haftung 6.4). **Tragbar.** |

### 3.6 Kritische Inkonsistenzen im Projektstand

Drei Delta zwischen Gutachten-Empfehlung und Repo-Realität:

1. **Tagline-Widerspruch.** `strings_de.py` Z. 11: `APP_TAGLINE = "Companion-Tool für Vertragsärzte zur Regress-Prävention"` und Z. 14 `TRAY_TOOLTIP = "VerordnungsAmpel — Regress-Prävention"`. CHANGELOG Z. 18 erklärt den Begriff dagegen explizit fallengelassen. Der ABOUT_TEXT (Z. 127) sagt "Keine Regress-Prävention" — GUI widerspricht sich intern. → **Blocker für Public Release** (Rechtssicherheits-Angriffsfläche § 5 UWG / § 444 BGB).
2. **"Um:bruch e.V."-Reste.** `docs/legal/DSGVO_KONZEPT.md` Z. 70 in der Rollentabelle: "Um:bruch e.V. / Therapiefreiheit e.V. (Entwickler/Herausgeber)". Widerspricht KONZEPT.md-Revision und Publikations-Gutachten 2.4. → **Kleiner Blocker** (nicht kritisch, aber Irreführung).
3. **LICENSE-Copyright-Kopf.** Formelle Frage: Vor dem GPL-Volltext sollte eine Projekt-Copyright-Zeile stehen ("Copyright (C) 2026 Lukas Geiger (c/o Um:bruch Think Tank). This program is free software..."). Der GPL-Volltext selbst beginnt mit dem FSF-eigenen Kopf und sagt nichts über das konkrete Werk. Das NOTICE-File trägt den Copyright — das ist die REUSE-/GNU-empfohlene Praxis, ist aber nur dann wasserdicht, wenn LICENSE und NOTICE zusammen ausgeliefert werden. → **Verifizierung empfohlen**, kein harter Blocker, weil NOTICE die Funktion übernimmt.

---

## 4. Restrisiken — Sechs-Dimensionen-Ampel

### 4.1 § 521 BGB Schenkungsprivileg — **GRÜN**

**Begründung:** Tool wird kostenlos unter GPL-3.0 verbreitet, keine Vergütung, keine SaaS, keine gewerbliche Tätigkeit (KONZEPT.md-Revision hat Pilot, Förderantrag, Kooperationen explizit verworfen). Damit greift das Schenkungsrecht; Haftung nur für Vorsatz und grobe Fahrlässigkeit (siehe `RECHTSGUTACHTEN_HAFTUNG.md` Kap. 5). Das Privileg wird **nicht** durch Zusicherungen entwertet, solange NOTICE und README "ohne Gewähr / nicht validiert / Nutzung auf eigenes Risiko" transportieren — was sie tun. Restposten (Tagline) muss behoben werden, damit nicht versehentlich der Zusicherungs-Anschein ("Regress-Prävention" als produktseitiges Versprechen) entsteht; nach Behebung: **GRÜN**.

### 4.2 MDR / MDSW-Grenze — **GRÜN bei sauberer Zweckbestimmung, GELB nur bei Marketing-Drift**

**Begründung:** Subsumtion im MDSW-Gutachten Kap. 2.6 ist solide: Keine patientenspezifischen Daten (Snitem-Kernkriterium verneint), reine Table-Lookup-Funktion (MDCG 2019-11 Step 3 verneint), sozialrechtlich-administrativer Zweck (Art. 2 Nr. 1 MDR verneint). Zweckbestimmung ist in README, NOTICE und ABOUT_TEXT konsistent als "Informationswerk / kein Medizinprodukt" formuliert. **Gelb-Einschlag nur** durch `strings_de.py`-Taglines "Regress-Prävention": Dieser Begriff suggeriert einen **Produktnutzen** ("das Tool verhindert Regresse"), was als therapeutische/administrative Zusicherung gedeutet werden könnte, auch wenn keine medizinische Zweckbestimmung vorliegt. Nach Tagline-Fix: **GRÜN**. Klassifier `Topic :: Scientific/Engineering :: Medical Science Apps.` und Keyword `"medizin"` in pyproject.toml ist bewusst neutral, aber Grenzfall — vertretbar.

### 4.3 DSGVO — **GRÜN**

**Begründung:** Keine Patientenklardaten, optional Pseudonym, ausschließlich lokale SQLite-DB, keine Telemetrie, keine Cloud. Rollenfrage sauber gelöst (Arzt = Verantwortlicher; Entwickler = Werkzeughersteller, weder Auftragsverarbeiter noch Verantwortlicher nach EuGH C-25/17 Zeugen Jehovas + EDSA 07/2020). Rechtsgrundlagen Art. 6(1)(c/f) + Art. 9 Abs. 2 lit. h i.V.m. § 22 BDSG für den Arzt tragfähig. Verarbeitungsverzeichnis-Muster im Konzept geliefert (13.3). Einzige **offene Punkte ohne aktuellen Druck:** Die DSGVO-Betroffenenrechte-CLI (E1–E5: export/purge) fehlt — spielt aber erst bei echter Praxisnutzung eine Rolle. Aktueller Release-Status: **GRÜN**; bei späterer Piloteröffnung dann **GELB** bis E1/E3 nachgereicht sind.

### 4.4 Urheber-/Marken-/Lizenzrecht — **GELB**

**Begründung:** Lizenz GPL-3.0-or-later ist konsistent gewählt und mit Dependencies (PySide6 LGPL-3.0, pytest MIT, PSF) kompatibel (Publikations-Gutachten 5.2). GPL-Volltext vorhanden. AM-RL-Seed-Daten als amtliche Werke (§ 5 UrhG) unproblematisch, PRISCUS 2.0 als Fakteninformation zulässig, ATC nicht-kommerziell korrekt gekennzeichnet, BSG/LSG/SG-/EuGH-Urteile amtliche Werke. THIRD_PARTY_LICENSES.txt vorhanden. **Gelb-Einschlag:** (a) DPMA-Recherche "VerordnungsAmpel" noch nicht durchgeführt (Klassen 09, 42, 44). Name ist für "beschreibend + Unterscheidungskraft" grenzwertig (wie "LebensmittelAmpel", "CO2-Ampel"). (b) "Um:bruch e.V."-Restposten in DSGVO_KONZEPT.md. (c) Projekt-Copyright-Zeile im LICENSE-Header nur indirekt über NOTICE geregelt. Nach DPMA-Check + DSGVO-Säuberung: **GRÜN**.

### 4.5 PLD 2024/2853 (ab 09.12.2026) — **GRÜN**

**Begründung:** Erwägungsgrund 14 PLD 2024 nimmt "Free and Open Source Software, die außerhalb einer gewerblichen Tätigkeit entwickelt oder bereitgestellt wird" explizit aus dem Anwendungsbereich. VerordnungsAmpel erfüllt alle sechs Kriterien der Nicht-Gewerblichkeit (Haftung 6.4): kein Preis, keine Förderung angenommen, keine Personendaten zu Werbezwecken, keine SaaS, keine Wartungsabos, natürliche Person + Repo. Die **Hürde** bleibt, dass die Nicht-Gewerblichkeit **dauerhaft** gewahrt werden muss; sobald irgendein kommerzieller Service dazu käme, kippt der Status. Der deutsche Referentenentwurf zur PLD-Umsetzung (erwartet H2/2026) ist noch nicht bekannt; die OSS-Ausnahme ist in RL-Text aber klar formuliert, sodass nationale Umsetzung hinter ihr nicht zurückbleiben kann.

### 4.6 Wettbewerb / UWG (§ 5, § 444 BGB) — **GELB**

**Begründung:** Der Tagline-Widerspruch "Regress-Prävention" in `strings_de.py` vs. "keine Regress-Prävention" in README/NOTICE/ABOUT_TEXT ist die konkreteste **UWG-Angriffsfläche**: § 5 UWG verbietet irreführende geschäftliche Handlungen. Auch im nicht-kommerziellen Betrieb kann ein Wettbewerber (z. B. PVS-Hersteller, die sich durch das Tool angegriffen fühlen, siehe KONZEPT-Marktanalyse) auf § 5 UWG stützen, wenn innerhalb der Produktkommunikation widersprüchliche Aussagen stehen. § 444 BGB (Zusicherung) greift parallel, wenn "Regress-Prävention" als Zusage einer Wirkung gewertet wird. Nach Tagline-Fix und einheitlicher Sprache **GRÜN**. Bis dahin: **GELB** (ernst zu nehmen, aber klein, weil kein Wettbewerber das Tool aktuell wahrnimmt).

### 4.7 Zusammenfassende Ampel-Tabelle

| Dimension | Aktuell | Nach Top-5-Fix | Begründung (Kurz) |
|---|:---:|:---:|---|
| § 521 BGB Schenkungsprivileg | GRÜN | GRÜN | OSS-Schenkung, keine Gewerblichkeit |
| MDR / MDSW-Grenze | GELB | GRÜN | Tagline-Restposten entwertet sonst saubere Zweckbestimmung |
| DSGVO | GRÜN | GRÜN | Nur ICD/ATC, lokal, Pseudonyme — keine DSFA-Pflicht beim Entwickler |
| Urheber-/Marken-/Lizenzrecht | GELB | GRÜN | DPMA-Recherche + kleine Copyright-Säuberungen ausstehend |
| PLD 2024/2853 | GRÜN | GRÜN | OSS-Ausnahme greift solange nicht-gewerblich |
| UWG / § 444 BGB | GELB | GRÜN | Tagline-Fix ist Schlüssel |

---

## 5. Release-Readiness

### 5.1 Private GitHub-Release (research-line/verordnungsampel, aktueller Zustand)

**Status: GRÜN.** Kein Gate-Item blockiert den aktuellen privaten Stand. Das Repo kann und wird privat genutzt werden; Disclaimer und Lizenz-Hygiene sind auf privatem Stand ausreichend. Einzige offene Punkte sind die internen Restposten, die vor Public behoben werden müssen, nicht davor.

### 5.2 Public GitHub-Release (research-line → public)

**Status: GELB.** Empfehlung: **NICHT heute veröffentlichen**, sondern 3 Blocker-Korrekturen durchziehen (Tagline-Fix, DSGVO_KONZEPT-Zeile 70, LICENSE-Copyright-Header-Check) und optional DPMA-Recherche. Aufwand: 1–3 Arbeitsstunden für die Korrekturen, 20 Minuten für die DPMA-Online-Recherche. Danach **GRÜN**.

### 5.3 Zenodo-DOI-Archivierung

**Status: GELB.** Erst nach Public-Release sinnvoll. Dann direkt empfohlen, weil Zenodo-DOI die Publikation als wissenschaftlichen Open-Source-Beitrag verankert und die Nicht-Gewerblichkeit zusätzlich dokumentiert. Lizenz (GPL-3.0) ist Zenodo-kompatibel, CC-BY-4.0 für die Rechtsgutachten und das DSGVO-Konzept wäre ein Upgrade (Publikations-Gutachten 3.6). Parallel-Ablage des Gesamtprojekts auf Zenodo schafft Versions-Persistenz, die GitHub allein nicht liefert.

### 5.4 Pilotierung in echten Arztpraxen

**Status: ROT (Empfehlung: nicht durchführen).** KONZEPT.md-Revision 2026-04-12 hat den Pilot selbst explizit gestrichen — das ist rechtlich die **sauberste** Entscheidung, weil sie die PLD-2024-OSS-Ausnahme, das § 521 BGB-Schenkungsprivileg und die Nicht-Verantwortlichkeit nach DSGVO konsequent wahrt. Ein Pilot würde zwingend verlangen: Pilot-Vereinbarung (Schriftform), Haftpflichtversicherung (Haftung 11.1), DSGVO-Betroffenenrechte-CLI-Implementierung E1/E3, fachanwaltliche Gegenprüfung, ggf. DSFA. **Falls** später ein Dritter (e.V., Kammer, Uni) den Pilot trägt, geht er **nicht in die Um:bruch-Sphäre** über — die OSS-Bereitstellung bleibt bei LG/Um:bruch, der Pilot ist eine separate, verantwortlich vom Dritten getragene Studie. Diese Trennung ist die empfohlene Konstellation.

---

## 6. Top 5 Restmaßnahmen vor Public Release

| Prio | Maßnahme | Fundstelle Gutachten | Verantwortlich | Aufwand |
|:---:|---|---|---|---|
| 1 | **Tagline und Tray-Tooltip fixen:** `strings_de.py` Z. 11+14 — `APP_TAGLINE` und `TRAY_TOOLTIP` auf neutrale Formulierung umstellen (z. B. `"Informationswerk zu Verordnungsregelwerken (AM-RL, PRISCUS)"` bzw. `"VerordnungsAmpel — Informationswerk"`). Parallel Check, ob Widerspruch auch im README Z. 161f. ("Werkzeug zur Verhinderung künftiger Regresse") steht. Tests der GUI-Anzeige nachprüfen. | MDSW 3.2.3; RUO 8.2.6; Haftung 9.2 Punkt 4; CHANGELOG 2026-04-12 | LG / Dev | 30 min |
| 2 | **"Um:bruch e.V."-Rest in DSGVO_KONZEPT.md Z. 70 säubern.** Tabellenzeile ersetzen durch `Lukas Geiger (c/o Um:bruch Think Tank, nicht als e.V. eingetragen)` — konsistent zu KONZEPT.md und NOTICE. Gleichzeitig LICENSE-Kopf verifizieren: entweder im LICENSE-File vor dem GPL-Volltext eine Projekt-Copyright-Zeile einfügen, oder klarstellen, dass NOTICE die funktional entsprechende Copyright-Notice trägt (REUSE-Praxis ausreichend). | Publikation 2.4 + 5.1 | LG / RB | 20 min |
| 3 | **DPMA-Recherche "VerordnungsAmpel"** online im DPMAregister, Klassen 09 (Software), 42 (SaaS/wissenschaftliche Dienstleistungen), 44 (medizinische Dienstleistungen). Identitäts- und Ähnlichkeitstreffer dokumentieren in `docs/legal/MARKEN_RECHERCHE.md`. Bei Treffern: Namensprüfung + ggf. Entscheidung, ob umbenannt werden muss (oder es sich um einen anderen Markenbereich handelt). Keine Markenanmeldung zwingend. | Publikation 4.1 + 8.1 | LG | 20 min Recherche + 20 min Doku |
| 4 | **Inline-Disclaimer bei jedem Ampel-Result verifizieren**, insbesondere bei GELB/ROT. RUO 8.2.5 fordert einen context-bezogenen Hinweis ("Dieser Hinweis basiert auf AM-RL Anlage III Stand 2026-Q2. Ersetzt keine eigene Prüfung. Kein Medizinprodukt."). Haftung 10.4 dasselbe. Wenn aktuell nur die permanente Statuszeile trägt, eine zusätzliche Result-Fußzeilen-Konstante in `strings_de.py` ergänzen und in der Result-Darstellung einbetten. | RUO 8.2.5; Haftung 10.4; MDSW 3.2.2 Punkt 8 | LG / Dev | 30 min |
| 5 | **GITHUB-POLICY-Pflichtdateien für SOCIAL-Repos:** `.github/FUNDING.yml`, `.github/ISSUE_TEMPLATE/bug_report.md`, `.github/ISSUE_TEMPLATE/feature_request.md`, GitHub-Repository-Description englisch ("Open-source reference tool for German outpatient physicians — information work, not a medical device."), GitHub-Topics (`healthcare`, `germany`, `prescription`, `reference-tool`, `open-source`, `gpl-3`). | Publikation 8.5 + 8.6 | LG | 40 min |

**Gesamtschätzung Top-5-Fix: 2–3 Arbeitsstunden.**

Nachrangig (nicht release-blockierend, aber "good hygiene"): REUSE-Compliance mit `LICENSES/`-Verzeichnis + SPDX-Headern in `src/**/*.py` + `reuse lint`-CI-Workflow; Screenshots für README; Upgrade der Rechtsgutachten-Dateien auf CC-BY-4.0 (SPDX-Header).

---

## 7. Abgegrenzte Anwaltsthemen — wann und wofür Fachanwalt

Die KI-basierte Rechtsabteilung kommt an folgenden Stellen an ihre Grenze:

| Situation | Fachgebiet | Anlass |
|---|---|---|
| **Vor echtem Pilotbetrieb** (falls der Kurs geändert wird) | Medizinrecht + Datenschutzrecht | DSFA, Pilotvereinbarung, Haftpflichtversicherung-Fragebogen, Einbindung DPO der Pilot-Praxis |
| **Vor Markenanmeldung "VerordnungsAmpel" beim DPMA** | Gewerblicher Rechtsschutz | Volltextliche Anmeldung in 3 Klassen, ca. 500–1000 EUR inkl. Recherche — aber nur wenn Markenanmeldung strategisch sinnvoll (aktuell: nein) |
| **Bei Abmahnung, Unterlassungsaufforderung, Anwaltsschreiben Dritter** | Je nach Sachverhalt (Medien-/Urheber-/Wettbewerbs-/Medizinrecht) | Sofortige Eskalation nach Policy `RECHTSABTEILUNG.md` |
| **Vor Umsetzung der PLD 2024 ins deutsche Recht (voraussichtlich H2/2026 Referentenentwurf, 09.12.2026 Umsetzungsfrist)** | Produkthaftungsrecht | Neuprüfung der OSS-Ausnahme im deutschen Umsetzungsrecht; KI-Rechtsabteilung hat hier nur den EU-Text, nicht den deutschen Umsetzungstext |
| **Bei jeder Abwicklung von Spenden/Crowdfunding > Bagatellgrenze** | Steuerrecht + Vereinsrecht | Schwellenüberschreitung in Gewerblichkeits-Nähe, Gemeinnützigkeitsprüfung |
| **Bei tatsächlicher Vereinsgründung e.V./gUG** (falls kommt) | Vereinsrecht | Satzungsentwurf, D&O-Versicherung, Gemeinnützigkeit nach § 52 AO |
| **Bei BfArM-Abgrenzungsantrag** nach § 6 MPDG (falls strategisch gewünscht) | Medizinprodukterecht | Formale Feststellung der Nicht-MDSW-Eigenschaft — nur sinnvoll bei Skalierung mit hohen Rechtsfolgen |
| **Bei Kontaktaufnahme mit "Therapiefreiheit e.V." für Kooperation** (falls kommt) | Vertragsrecht + Kooperationsrecht | Aktuell irrelevant, weil Kooperation verworfen |

Erstberatung je nach Thema RVG 190–400 EUR netto. Bei OSS/IT-Themen: JBB Rechtsanwälte, ifrOSS, iRights.Law. Bei Medizinrecht/MDR: Taylor Wessing, CMS Hasche Sigle, Fieldfisher, Prof. Heckmann (Uni Passau).

---

## 8. Empfohlener Transitionspfad PRI → PUB

**Phasenmodell** (basiert auf Publikation 9.1, angepasst an aktuellen Projektstand und Revision 2026-04-12):

| Phase | Zustand | Ziel | Gate |
|---|---|---|---|
| **P0 – heute** | `research-line/verordnungsampel` PRI, v0.1.0 | Gutachten vollständig, NOTICE+Disclaimer-Dialog+LICENSE umgesetzt | Erreicht |
| **P1 – 1–2 Tage** | PRI | Top-5-Restmaßnahmen (Kap. 6) durchziehen: Tagline-Fix, DSGVO_KONZEPT-Säuberung, DPMA-Recherche, Result-Inline-Disclaimer, GITHUB-POLICY-Pflichtdateien | Alle Top-5 grün |
| **P2 – optional, 1–2 Tage** | PRI | REUSE-Compliance, SPDX-Header, CC-BY-4.0 für Gutachten, Screenshots, CC0-1.0 für Seed-Daten, Fachanwalts-Terminanfrage (optional) | "Good hygiene" |
| **P3 – 1 Tag** | `PUB`, v0.2.0 | Repo auf public + GitHub-Release + kurze Announcement-Notiz (Um:bruch-Blog, RSS). Kein Marketing-Push. Kein Pilot. | Announcement ruhig-technisch formuliert |
| **P4 – nach 1 Woche** | PUB | Zenodo-DOI-Archivierung (inkl. Gutachten als CC-BY-4.0) | DOI vergeben |
| **P5 – 2026 ff.** | PUB | Quartals-Build-Zyklus für AM-RL/PRISCUS-Updates; Bug-Bounty-Kontakt security@um-bruch.org; ggf. Reviewer aus Forschungs-Netzwerk einladen | laufend |
| **P6 – 2027+** | PUB | **Entweder** Um:bruch-Vereinsgründung → Repo-Transfer an e.V., **oder** Weiterführung als LG-Einzelurheber. Bei PLD-2024-Umsetzungsgesetz: Gutachten aktualisieren | Review zum Stichtag 09.12.2026 |

**Entscheidungsweichen:**

- *Soll an einen Dritten (Kammer, Forschungs-e.V.) übergeben werden?* Ja, aber als **Fork**, nicht als Übertragung. Forker übernimmt Verantwortung ab Fork-Zeitpunkt; LG bleibt Urheber des Ausgangs-Werks.
- *Sobald ein Dritter einen Pilot fährt:* Pilot liegt **vollständig** in dessen Verantwortung; LG/Um:bruch hat damit nichts zu tun. Klarstellung in einer separaten "Pilot-Disclaimer"-Notiz im README-Abschnitt "Mitwirken".

---

## 9. Grenzen dieser Einschätzung

Diese Synthese ist eine **KI-basierte Ersteinschätzung** auf Basis der fünf Einzelgutachten vom 12.04.2026 und des Projektstands vom selben Tag. Sie ersetzt **keine anwaltliche Beratung**.

- **Klumpenrisiko:** Alle Einzelgutachten stammen vom selben Verfasser (CL). Ein unabhängiger Gegenzeuge (Gemini oder menschlicher Fachanwalt) wurde für einzelne Teilfragen nicht hinzugezogen. Das ist für einen OSS-Private-Release akzeptabel; für einen Piloteinsatz wäre es nicht akzeptabel.
- **Keine formelle DPMA-Recherche:** Dokumentationsstand der Marke "VerordnungsAmpel" ist nicht verifiziert.
- **Keine source-datei-genaue Verifikation** der Umsetzungs-Matrix (Kap. 3). Die Matrix beruht auf Stichproben aus `strings_de.py`, `disclaimer_dialog.py`, `pyproject.toml`, `NOTICE`, `README.md`, `CHANGELOG.md`, `KONZEPT.md` und `USER-GUIDE.md`. Weitere Source-Dateien (Result-Rendering, CLI-Subcommands, DB-Schema) wurden nicht durchleuchtet — hier können kleinere Abweichungen existieren.
- **PLD-2024-Umsetzung** in Deutschland liegt noch nicht vor; Einschätzung basiert auf EU-Text + Erwägungsgrund 14.
- **Gesetzes- und Rechtsprechungsstand:** April 2026.
- **Kein AUTOFIX_REPORT** gefunden — falls ein Auto-Fix-Lauf parallel läuft, sind dessen Ergebnisse nicht in dieser Synthese erfasst.

Bei Risikoeinschätzung "Hoch" oder "Kritisch" wird die Einschaltung eines Fachanwalts empfohlen. Diese Einschätzung hat das Gesamtrisiko bei Umsetzung der Top-5-Maßnahmen als **niedrig** bewertet.

---

## 10. Quellen

### 10.1 Intern konsultierte Einzelgutachten

- `docs/legal/RECHTSGUTACHTEN_MDSW.md` (2026-04-12, CL)
- `docs/legal/DSGVO_KONZEPT.md` (2026-04-12, CL)
- `docs/legal/RECHTSGUTACHTEN_RUO.md` (2026-04-12, CL)
- `docs/legal/RECHTSGUTACHTEN_PUBLIKATION_LIZENZ.md` (2026-04-12, CL)
- `docs/legal/RECHTSGUTACHTEN_HAFTUNG.md` (2026-04-12, CL)
- `docs/legal/RECHTSAUDIT_ALLE_PROJEKTE.md` (2026-04-12, CL)

### 10.2 Intern konsultierter Projektstand (Stichprobe)

- `README.md` (2026-04-12, Disclaimer-Block Z. 13–38 und Haftungshinweis Z. 170–175)
- `NOTICE` (Projekt-Copyright + Haftungsblock + Schenkungshinweis)
- `LICENSE` (GPL-3.0-Volltext 674 Z.)
- `THIRD_PARTY_LICENSES.txt`
- `pyproject.toml` (Z. 1–56)
- `CHANGELOG.md` (Revision 2026-04-12)
- `KONZEPT.md` (Kopf + Revisions-Hinweis Z. 8 + Durchstreichungen)
- `USER-GUIDE.md` (Kopf + "Was sie ist / NICHT ist")
- `src/verordnungsampel/gui/strings_de.py`
- `src/verordnungsampel/gui/disclaimer_dialog.py`

### 10.3 Policy / Methodische Grundlage

- `C:\Users\User\OneDrive\.UMBRUCH\Policies\RECHTSABTEILUNG.md` (2026-04-02)
- `C:\Users\User\OneDrive\.TOPICS\.SOFTWARE\GITHUB-POLICY.md` (2026-02-22)

### 10.4 Externe Rechtsquellen (kumuliert aus den Einzelgutachten)

MDR (EU) 2017/745, IVDR (EU) 2017/746, MDCG 2019-11 Rev. 1, EuGH C-329/16 Snitem, BGB §§ 241, 280, 305–310, 442, 444, 516–524, 630a, 630f, 823, SGB V §§ 31, 76, 92, 94, 106, MPDG §§ 6, 92, ProdHaftG §§ 1, 3, 14, PLD (EU) 2024/2853, GPL-3.0 Sections 15–17, UrhG §§ 2, 4, 5, 7, 8, 51, 62, 63, 69a, 87a ff., MarkenG §§ 8, 14, 23, UWG §§ 3, 5, BGH "Inkasso-Programm" (I ZR 52/83), BGH I ZR 112/22 (KI-Werke), BGH VI ZR 64/07 (Facharztstandard), BSG B 6 KA 26/13, SG Marburg S 18 KA 96/23, LSG BW 15.11.2023, LG München I 21 O 6123/04 (GPL-Durchsetzbarkeit), BfArM FAQ Abgrenzung, ifrOSS, Spindler 2003, Jaeger/Metzger 2020.

---

**Disclaimer (Schlussklausel):**
Diese Einschätzung ist eine **KI-basierte Erstanalyse** der Um:bruch-Rechtsabteilung (Rolle RB, Besetzung Claude) und **ersetzt keine anwaltliche Beratung**. Die Gesamt-Risikoeinschätzung ist **niedrig** bei Umsetzung der Top-5-Restmaßnahmen. Bei Pilot-Eröffnung, Vereinsgründung oder PLD-Umsetzungsgesetz ist eine Fachanwalts-Gegenprüfung einzuholen.

**Prüfende Stelle:** Um:bruch Think Tank — Rechtsabteilung RB
**Bearbeiter:** Claude (CL)
**Datum:** 2026-04-12
**Ablage:** `docs/legal/GESAMTEINSCHAETZUNG.md`
