# Web-MVP der VerordnungsAmpel

Stand: 2026-05-23

## Ziel dieses Schritts

Die geplante Browser-/PWA-Linie hat jetzt einen ersten lokalen Prototypen, ohne
eine zweite Fachlogik aufzubauen. Der Web-Stack nutzt dieselben Python-Module wie
CLI und PySide6-GUI:

- `evaluate()` für die Ampelentscheidung
- `find_matching()` für Praxisbesonderheiten
- `load_seed_data()` für das initiale Regelwerks-Bootstrapping

## Enthaltener Umfang

- Lokale Flask-App unter `src/verordnungsampel/web/app.py`
- HTML-Form für ICD, ATC und optionales Alter
- JSON-Endpunkt `POST /api/check`
- Health-Endpunkt `GET /health`
- Seed-Autoinit beim ersten Web-Zugriff auf eine leere Datenbank

## Starten

```powershell
cd verordnungsampel
python -m pip install -e ".[web]"
python -m verordnungsampel.cli.main web
```

Danach im Browser öffnen:

- `http://127.0.0.1:5000/`
- API-Test: `POST http://127.0.0.1:5000/api/check`

## Noch bewusst offen

- strukturierte Begründung im Browser
- Workflow-Textgenerator als Web-Maske
- PWA-Metadaten, Offline-Cache und Installierbarkeit
- getrennte Eingabemaske für Pilotpraxen
- datensparsame Export-/Import-Flüsse für spätere Praxisintegration

## Einordnung im Portierungsplan

Der Web-MVP ist die bevorzugte Linie für Web, Android und iOS, aber nur als lokale
PWA bzw. Companion-Oberfläche. Eine native Android- oder iOS-App ist aktuell kein
Ziel. Auch eine Cloud-Synchronisierung ist kein Ziel, weil direkte Synchronisation
in diesem Gesundheits- und Rechtskontext ein neues Datenschutz-, Haftungs- und
Medizinprodukte-Konzept erfordern würde.

Der geplante Austausch läuft dateibasiert über die in `EXPORTFORMAT.md`
beschriebenen Formate `verordnungsampel-casebundle-v1.json` und
`verordnungsampel-ruleset-v1.json`.

## Nächste sinnvolle Schritte

1. Web-Maske für `justify` und `workflow` ergänzen
2. Eingaben im Browser lokal zwischenspeichern, aber ohne Voll-Sync
3. PWA-Basis ergänzen: Manifest, Service Worker, Offline-Fallback
