# Gesamteinschätzung — Publikationsstand

> **Stand:** 2026-04-13 (Public-Release-Version)
> **Vorgängerdokument:** Interne Vollversion mit Defekt-Matrix wird nicht öffentlich geführt.
> **Methodische Grundlage:** Vier projektbezogene Rechtsgutachten (MDSW, DSGVO, RUO, Publikation/Lizenz, Haftung) und ein Repo-Audit, dokumentiert in den Einzelgutachten in diesem Ordner.

## Kurzbefund

Das Projekt VerordnungsAmpel ist nach einer Serie paralleler Einzelgutachten und einem Repo-Audit **rechtlich tragfähig**, solange es als reines Open-Source-Informationswerk ohne Trägerorganisation, ohne klinische Pilotierung und ohne Vermarktungsversprechen veröffentlicht wird.

## Sechs Ampel-Dimensionen

| Dimension | Ampel | Gutachten |
|---|---|---|
| § 521 BGB Schenkungsprivileg (Haftung) | 🟢 | RECHTSGUTACHTEN_HAFTUNG |
| MDR — kein Medizinprodukt | 🟢 | RECHTSGUTACHTEN_MDSW |
| DSGVO (Arzt = Verantwortlicher, lokale Verarbeitung) | 🟢 | DSGVO_KONZEPT |
| Lizenz / Marke | 🟡 | RECHTSGUTACHTEN_PUBLIKATION_LIZENZ, MARKEN_RECHERCHE |
| PLD 2024/2853 (Produkthaftung) | 🟢 | RECHTSGUTACHTEN_HAFTUNG |
| UWG / § 444 BGB (Zweckbestimmung) | 🟡 | RECHTSGUTACHTEN_RUO |

## Disclaimer-Architektur (umgesetzt)

- NOTICE mit Projekt-Copyright und Haftungsausschluss
- README-Disclaimer-Block (Top, prominent)
- Persistenter Erststart-Dialog mit vier Pflicht-Checkboxen, versiegelt per Hash-Chain im Compliance-Log
- Permanente GUI-Statuszeile „kein Medizinprodukt / Nutzung auf eigenes Risiko"

## Kern-Entscheidungen

1. **Open Source ohne Trägerorganisation.** Keine Gründung eines Um:bruch e.V. nur zum Zweck der § 521 BGB-Optimierung. Urheber bleibt Lukas Geiger als natürliche Person (c/o Um:bruch Think Tank).
2. **Zweckbestimmungs-Deeskalation.** Der Begriff „Regress-Prävention" wurde fallengelassen und durch „Risikoindikatoren-Anzeige ohne Gewähr, zu Forschungs- und Weiterentwicklungszwecken" ersetzt (MDSW-Empfehlung 3.2.1, RUO-Variante C).
3. **Keine Pilotierung in Praxen.** Der Softwareentwurf wird ausdrücklich für Forschungs- und Weiterentwicklungszwecke publiziert, nicht für den produktiven Einsatz am Patienten (KONZEPT.md-Revision 2026-04-12).

## Release-Readiness

Das Projekt ist public-release-ready. Zenodo-Archivierung ist nach Public-Release sinnvoll. Eine klinische Pilotierung in Praxen ist auf Basis dieser Einschätzung **nicht empfohlen** — die Software adressiert Forschungs- und Methoden-Fragen, nicht die direkte Versorgung.

## Grenzen dieser Einschätzung

Dies ist eine KI-gestützte Erstanalyse. Sie ersetzt keine anwaltliche Beratung. Wer die Software fortführt, sollte für konkrete Weiterentwicklungen (insb. geplante Pilotierung, Kommerzialisierung, Integration in Praxissysteme) eigenständige Rechtsberatung einholen.

---

*Companion-Projekt zu Um:bruch PP-003 / ST-001 (Regress-Transparenzportal).*
