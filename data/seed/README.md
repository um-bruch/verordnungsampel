# Seed-Daten für VerordnungsAmpel

Dieses Verzeichnis enthält **JSON-Stammdaten**, die beim ersten Start
in die SQLite-Datenbank geladen werden. Alle Daten sind öffentlich
oder explizit unter freier Lizenz.

## Wichtig: Regelwerks-Snapshot, keine medizinische Validierung

Die AM-RL-Anlagen III, V und VI liegen als strukturierter Snapshot mit
Stand-Datum, Quell-URL und Extraktionsmetadaten vor. Sie bleiben dennoch
ein **Software- und Forschungsdatensatz**: Vor produktiver oder fachlicher
Nutzung müssen neue oder geänderte Einträge juristisch-medizinisch geprüft
werden.

## Dateien

| Datei | Zweck | Ziel-Tabelle |
|---|---|---|
| `quellen.json` | Quellenverweise (AM-RL, BSG, PRISCUS, GKV-SV) | `quelle` |
| `icd10.json` | Beispiel-ICD-10-GM-Codes | `icd10` |
| `atc.json` | Beispiel-ATC-Codes (WHO) | `atc` |
| `amrl_anlagen.json` | Legacy-Sammeldatei AM-RL (MVP, kann leer sein) | `amrl_anlage` |
| `amrl_anlage_III.json` | AM-RL Anlage III (Verordnungseinschränkungen/-ausschlüsse, Stand 2025-10-09) | `amrl_anlage` |
| `amrl_anlage_V.json` | AM-RL Anlage V (verordnungsfähige Medizinprodukte, Stand 2026-03-24) | `amrl_anlage` |
| `amrl_anlage_VI_A.json` | AM-RL Anlage VI Teil A (anerkannter Off-Label-Use, Stand 2025-05-07) | `amrl_anlage` |
| `amrl_anlage_VI_B.json` | AM-RL Anlage VI Teil B (nicht anerkannter Off-Label-Use, Stand 2025-05-07) | `amrl_anlage` |
| `praxisbesonderheiten.json` | Beispiel-Praxisbesonderheiten | `praxisbesonderheit` |
| `regeln.json` | Generische Ampel-Regeln (PRISCUS, Container, etc.) | `regel` |

## ATC-Pattern-Notation

Die `atc_pattern`-Felder nutzen SQL-LIKE-Syntax:

- `A02BC%` matched alle PPI (Pantoprazol, Omeprazol, ...)
- `R06AD%` matched die alten H1-Antihistaminika (Promethazin etc.)
- `_09AA%` matched alles in der ATC-Position 2 mit `09AA` (selten genutzt)

## Quellenpflege

Jede Regel sollte einen `quelle`-Verweis (Kürzel) tragen. Wenn die Quelle
in `quellen.json` existiert, wird die Regel beim Seed-Laden mit der
korrekten `quelle_id` verknüpft.

## Normalisierte Code-Relationen

Seit Schema-Version 2 erzeugt der Seed-Loader zusätzliche Relationstabellen:

- `amrl_anlage_atc`
- `praxisbesonderheit_atc`
- `praxisbesonderheit_icd10`
- `regel_atc`
- `regel_icd10`

Diese Tabellen materialisieren explizite `atc_pattern`- und `icd_pattern`-Treffer
gegen die bekannten Seed-Codes. Die Ampel-Engine nutzt weiter die Pattern-Logik;
die Relationen dienen UI-Abfragen, Coverage-Analysen und späteren Backend-Views.
`NULL`-Patterns werden bewusst nicht als Kreuztabelle materialisiert, weil sie
"keine Einschränkung" bedeuten.

## Versionierung und Updates

Seit Seed-Version 1.0.0 (2026-04-12) haben die AM-RL-Anlagen-Dateien
einen `_meta`-Header mit Stand-Datum, Quell-URL, Extraktionsmethode und
Version. Der Loader (`src/verordnungsampel/db/seed.py`) unterstützt
beide Formate (neu + Legacy-Liste).

Für das **Aktualisierungsverfahren** siehe **`UPDATE_METHODE.md`** in
diesem Verzeichnis. Archivierte Stände liegen in `_archiv/<DATUM>/`,
Rohtext-Extrakte in `_raw/`.

CLI:

```
python -m verordnungsampel.cli.main sources              # Übersicht
python -m verordnungsampel.cli.main sources --json       # JSON-Export
python -m verordnungsampel.cli.main rules --anlage III   # einzelne Anlage
python scripts/update_amrl.py diff --anlage III --url <G-BA-URL>  # Maintainer
```
