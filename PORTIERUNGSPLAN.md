# Portierungsplan VerordnungsAmpel

Stand: 2026-05-28

## Ergebnis der Bedingungsprüfung

Vor diesem Check gab es keinen eigenen Portierungsplan. Dieses Dokument legt daher nach Pfad B die Plattformstrategie für die VerordnungsAmpel fest.

## Zweck und Grenze

Die VerordnungsAmpel ist ein Open-Source-Softwareentwurf zur Anzeige bekannter Regress-Risikoindikatoren aus öffentlichen Regelwerken. Sie ist kein Medizinprodukt, keine klinische Entscheidungsunterstützung, keine Rechtsberatung und kein produktives Praxisverwaltungssystem.

Die Plattformstrategie muss diese Grenze schützen: lokale Verarbeitung, keine Telemetrie, keine Cloud-Synchronisierung, keine öffentlichen Upload-Flows für Falldaten und keine Store-Vermarktung mit Wirkversprechen.

## Features

- ICD-10-GM- und ATC-Kombination gegen AM-RL-Anlagen, PRISCUS- und Praxisbesonderheiten-Daten prüfen.
- Ampelergebnis mit Quellenhinweis und nachvollziehbarer Begründung ausgeben.
- Strukturierte Begründung über eine Hierarchical State Machine erfassen.
- Container-sensitive Vorab-Klärungs- oder Stellungnahme-Workflows als Text erzeugen.
- Praxisbesonderheiten im Quartal erkennen und Reminder ausgeben.
- Compliance-Log lokal als Hash-Chain prüfen und verifizieren.
- Regelwerksquellen und Seed-Stand über CLI, GUI und Web-Prototyp sichtbar machen.
- Regelwerksabdeckung für pseudonymisierte Falllisten methodisch auswerten.

## Usecase-Settings

### Setting 1: Praxisnahe lokale Nutzung

Nutzer: Ärztinnen, Ärzte und Praxisteams, die eine Verordnung vor oder während der Dokumentation gegen öffentliche Regelwerke plausibilisieren wollen.

Usecases:

- Schneller ICD-/ATC-Check am Arbeitsplatz.
- Begründung für auffällige Verordnungen strukturiert erfassen.
- Vorab-Antrags- oder Stellungnahme-Text vorbereiten.
- Quartalsweise Praxisbesonderheiten prüfen.
- Lokale Hash-Chain für Nachvollziehbarkeit verifizieren.

Plattformfolge: Windows-Desktop und lokale Browser-Oberfläche sind primär. macOS und Linux sind sinnvolle Source-Smoke-Ziele. Mobile Geräte sind hier nur als PWA-Companion für Nachschlagen, Vorbereitung oder Demonstration sinnvoll, nicht als native Voll-App.

### Setting 2: Regelwerks- und Forschungsarbeit

Nutzer: Entwickler, Forschungsteams, Ärzteverbände oder andere Dritte, die Regelwerke pflegen, Coverage-Analysen durchführen oder das Projekt evaluieren.

Usecases:

- Seed-Daten aktualisieren und prüfen.
- Regelwerksquellen transparent dokumentieren.
- Pseudonymisierte Falllisten auswerten.
- Forks oder Pilotvarianten methodisch vorbereiten.

Plattformfolge: GitHub, CLI und reproduzierbare JSON-Dateien sind wichtiger als App-Store-Distribution. Linux/macOS-Smokes sind für Forschungsteams nützlich; mobile Stores sind hier kein Ziel.

### Setting 3: Mobile Demonstration und Nachschlagen

Nutzer: dieselben Fachnutzer wie in Setting 1, aber unterwegs, in Schulungssituationen oder bei Besprechungen.

Usecases:

- Regelwerksstatus und Beispielchecks nachschlagen.
- Pseudonymisierte, nicht produktive Demo-Fälle prüfen.
- Exportierte Fallbündel oder Regelwerks-Snapshots anzeigen.

Plattformfolge: Web/PWA ist der passende gemeinsame Pfad für Android, iOS und Browser. Native Android- oder iOS-Apps sind erst dann sinnvoll, wenn ein Dritter einen eigenständigen, validierten Mobile-Usecase verantwortet.

## Plattformentscheidungen

| Plattform | Entscheidung | Begründung |
|---|---|---|
| Windows | Vollversion beibehalten | Aktueller Entwicklungs- und Praxisarbeitsplatz; PySide6-Tray, CLI und lokaler Web-Prototyp passen zum Companion-Modus. |
| macOS | Source-Smoke planen | Forschungsteams und ärztliche Einzelpraxen können macOS nutzen; keine eigene Paketierung vor stabilem Datenschutz-/Release-Konzept. |
| Linux | Source-Smoke planen | Relevant für Forschung, Server-nahe Tests und OSS-Weiterentwicklung; keine primäre Endnutzer-Distribution. |
| Web/PWA | Lokale PWA als Hauptlinie ausbauen | Niedrige Zugangshürde, gleiche Fachlogik, gute mobile Reichweite; weiterhin lokal/offline-first und ohne Cloud-Datenfluss. |
| Android | Keine native App; PWA-Smoke | Der mobile Usecase ist Nachschlagen/Demo, nicht produktive Verordnungsdokumentation. |
| iOS | Keine native App; PWA-Smoke | Gleiche Begründung wie Android; App-Store-Distribution wäre rechtlich und fachlich zu früh. |
| Windows Store | Kein aktiver Zielkanal | Gesundheits- und Rechtskontext, GPL-3.0, fehlende klinische Validierung und klare Forschungszweckbestimmung sprechen gegen Store-Onboarding. |

## Austausch- und Synchronisationsmodell

Keine direkte Synchronisation zwischen Desktop, Web/PWA und mobilen Geräten. Direkte Synchronisation wäre ein eigener Companion-Usecase und müsste vorab datenschutzrechtlich, medizinprodukterechtlich und fachlich neu geprüft werden.

Stattdessen wird ein dateibasierter Austausch geplant:

- `verordnungsampel-casebundle-v1.json` für pseudonymisierte Checks, Begründungen, Workflow-Ausgaben und Audit-Metadaten.
- `verordnungsampel-ruleset-v1.json` für versionierte Regelwerks-Snapshots mit Quellen- und Checksum-Metadaten.

Die Formate werden in `EXPORTFORMAT.md` beschrieben. Klartext-Patientendaten, PVS-Zugangsdaten, Credentials, lokale absolute Pfade und Telemetriedaten gehören nicht in diese Exporte.

## Umsetzungsplan

### P0: Plattformgrenzen und Datenformat festlegen

- `EXPORTFORMAT.md` als Spezifikation für Fallbündel und Regelwerks-Snapshots führen.
- Web-MVP-Doku mit dieser Plattformentscheidung synchronisieren.
- Windows Store in der Root-Pipeline als derzeit ausgeschlossen markieren.

### P1: Lokale Web/PWA-Linie ausbauen

- Browser-Masken für `justify` und `workflow` ergänzen.
- PWA-Manifest, Service Worker und Offline-Fallback ohne Third-Party-CDN ergänzen.
- Browser-Speicherung nur lokal und sichtbar machen; keine Cloud-Anbindung.

### P2: Desktop- und Source-Smokes

- Windows-EXE-Smoke für den PyInstaller-Build dokumentieren.
- macOS- und Linux-Source-Smoke für CLI, GUI-Import und Web-Start vorbereiten.
- Pfad-, Encoding- und Datenverzeichniszugriffe plattformneutral prüfen.

### P3: Mobile PWA-Smokes

- Android- und iOS-Browser-Smoke für Check-, Quellen- und Export-Import-Ansicht durchführen.
- Keine nativen Store-Artefakte erstellen, solange kein eigenständiger Mobile-Usecase validiert ist.

## Nicht-Ziele

- Keine öffentliche Upload-Webapp für Falldaten.
- Keine App-eigene Cloud-Synchronisierung.
- Keine native Android-/iOS-App im aktuellen Projektzuschnitt.
- Keine Windows-Store-Einreichung mit Gesundheits- oder Wirksamkeitsversprechen.
- Keine PVS-Integration ohne neues Datenschutz-, Haftungs- und Medizinprodukte-Konzept.
