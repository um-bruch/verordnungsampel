# Exportformat VerordnungsAmpel

Stand: 2026-05-28

Dieses Dokument beschreibt die geplanten dateibasierten Austauschformate für die plattformübergreifende Nutzung. Es ist noch keine Implementierungszusage; es legt die Grenzen für spätere CLI-, Desktop- und PWA-Funktionen fest.

## Grundregeln

- Exporte enthalten keine Klartext-Patientendaten.
- Patientenbezüge werden nur als vom Nutzer gesetzte Pseudonyme geführt.
- Keine Credentials, Tokens, lokalen absoluten Pfade, PVS-Zugangsdaten oder Telemetriedaten.
- Dateien werden bewusst durch Nutzer exportiert und importiert. Es gibt keine automatische Synchronisierung.
- UTF-8 ohne BOM, JSON, stabile `schema_version`.

## `verordnungsampel-casebundle-v1.json`

Zweck: Ein pseudonymisiertes Fallbündel zwischen Desktop, lokaler Web/PWA und Forschungs-/Review-Workflows austauschen.

Mindeststruktur:

```json
{
  "schema_version": "verordnungsampel-casebundle-v1",
  "created_at": "2026-05-28T00:00:00Z",
  "created_by_app": {
    "name": "VerordnungsAmpel",
    "version": "0.1.0"
  },
  "privacy": {
    "contains_clear_patient_data": false,
    "pseudonymized": true,
    "notes": "Keine Namen, Geburtsdaten, Versichertennummern oder Praxisgeheimnisse."
  },
  "cases": [
    {
      "case_ref": "case-001",
      "patient_ref": "P-4711",
      "icd": "F41",
      "atc": "N05BA01",
      "age_years": 72,
      "checked_at": "2026-05-28T00:00:00Z",
      "result": {
        "traffic_light": "rot",
        "matched_rules": [],
        "source_refs": []
      },
      "justification": {
        "status": "draft|complete|not_applicable",
        "steps": []
      },
      "workflow": {
        "type": "pflicht_antrag|verboten_hinweis|stellungnahme|keine_aktion",
        "text": null
      }
    }
  ],
  "audit": {
    "hash_chain_exported": false,
    "entries": []
  }
}
```

Importregeln:

- Unbekannte Felder tolerant ignorieren, bekannte Felder streng validieren.
- `contains_clear_patient_data=true` muss Import in normalen PWA-/Demo-Flows blockieren.
- `patient_ref` darf leer sein; Klartextnamen dürfen nicht akzeptiert werden.
- Workflow-Texte sind Nutzer-Ausgaben und dürfen beim Import als unverifiziert markiert werden.

## `verordnungsampel-ruleset-v1.json`

Zweck: Regelwerks-Snapshots mit Quellenstand, Checksummen und materialisierten Code-Relationen zwischen Entwicklungs-, Review- und PWA-Umgebungen austauschen.

Mindeststruktur:

```json
{
  "schema_version": "verordnungsampel-ruleset-v1",
  "created_at": "2026-05-28T00:00:00Z",
  "source_state": {
    "amrl_iii": "2025-10-09",
    "amrl_v": "2026-03-24",
    "amrl_vi": "2025-05-07"
  },
  "checksums": {
    "algorithm": "sha256",
    "files": []
  },
  "rules": [],
  "icd10": [],
  "atc": [],
  "praxisbesonderheiten": [],
  "relations": []
}
```

Importregeln:

- Regelwerks-Snapshots dürfen bestehende lokale Daten nur nach expliziter Nutzerbestätigung ersetzen.
- Quelle, Datum und Prüfsumme müssen sichtbar bleiben.
- Ein importierter Snapshot ersetzt keine medizinische oder rechtliche Validierung.

## Nicht enthalten

- PVS-Patientenakte oder PVS-IDs.
- Arztsignaturen, Zertifikate oder KV-/Kassen-Zugangsdaten.
- Vollständige lokale SQLite-Datenbank als Rohdump.
- Netzwerk- oder Sync-Konfiguration.
