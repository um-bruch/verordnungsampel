# Update-Methode: AM-RL-Seed-Daten

Dieses Dokument beschreibt **verbindlich**, wie die AM-RL-Regelwerke der
VerordnungsAmpel gepflegt, aktualisiert und versioniert werden. Es
richtet sich an Maintainer und Reviewer — nicht an Endnutzer.

**Stand dieses Dokuments:** 2026-04-12

---

## 1. Wo liegen die Regelwerke?

```
data/seed/
├── _archiv/                              # Historische Snapshots (pro Update-Datum)
│   └── 2026-04-12/
│       ├── amrl_anlage_III.json
│       ├── amrl_anlage_V.json
│       ├── amrl_anlage_VI_A.json
│       └── amrl_anlage_VI_B.json
├── _raw/                                 # Rohtext-Extrakte aus den G-BA-PDFs
│   ├── amrl_III_2025-10-09.txt
│   ├── amrl_V_2026-03-24.txt
│   └── amrl_VI_2025-05-07.txt
├── amrl_anlage_III.json                  # AKTUELL geladenes Regelwerk (Anlage III)
├── amrl_anlage_V.json                    # AKTUELL Anlage V (Medizinprodukte)
├── amrl_anlage_VI_A.json                 # AKTUELL Anlage VI Teil A (Off-Label anerkannt)
├── amrl_anlage_VI_B.json                 # AKTUELL Anlage VI Teil B (Off-Label nicht anerkannt)
├── quellen.json                          # Quellen-Register (URL, Titel, Stand)
├── README.md                             # Allgemeine Beschreibung
└── UPDATE_METHODE.md                     # Dieses Dokument
```

### Dateiformat (Schema)

Jede Anlage-JSON hat seit Seed-Version 1.0.0 einen **Header-Block** `_meta`
und eine Eintragsliste `eintraege`:

```json
{
  "_meta": {
    "anlage": "III",
    "titel": "Arzneimittel-Richtlinie Anlage III - Verordnungseinschraenkungen",
    "stand": "2025-10-09",
    "quelle_kuerzel": "AMRL_III",
    "quelle_url": "https://www.g-ba.de/downloads/83-691-1036/AM-RL-III-Verordnungseinschraenkungen_2025-10-09.pdf",
    "quelle_datei": "AM-RL-III-Verordnungseinschraenkungen_2025-10-09.pdf",
    "raw_datei": "_raw/amrl_III_2025-10-09.txt",
    "extraktion_datum": "2026-04-12",
    "extraktion_methode": "PyMuPDF (fitz) ...",
    "extraktion_version": "1.0.0",
    "eintraege_anzahl": 56,
    "lizenz": "Oeffentliche G-BA-Richtlinie, gemeinfreies amtliches Werk (§ 5 UrhG)."
  },
  "eintraege": [
    { "anlage": "III", "nr": "1", "atc_pattern": "A02B%", "bedingung": "...",
      "ampel": "rot", "begruendung": "...", "quelle": "AMRL_III" },
    ...
  ]
}
```

Der Seed-Loader (`src/verordnungsampel/db/seed.py`) unterstuetzt zusaetzlich
das **Legacy-Format** (flache Liste ohne `_meta`), damit externe/ aeltere
Seed-Dateien weiter eingelesen werden koennen.

---

## 2. Quellen (G-BA)

Die AM-RL-Anlagen werden vom **Gemeinsamen Bundesausschuss (G-BA)**
veroeffentlicht. Einstiegspunkt:

- Hauptseite AM-Richtlinie: https://www.g-ba.de/richtlinien/1/
- Download-Bereich: https://www.g-ba.de/downloads/83-691-<id>/<dateiname>.pdf

### Bekannte URL-Struktur

| Anlage | Download-ID | Aktuelle Datei (Stand 2026-04-12) |
|---|---|---|
| III (Verordnungsausschluesse) | `83-691-1036` | `AM-RL-III-Verordnungseinschraenkungen_2025-10-09.pdf` |
| V (Medizinprodukte) | `83-691-1078` | `AM-RL-V_2026-03-24.pdf` |
| VI (Off-Label Teil A+B) | `83-691-1009` | `AM-RL-VI-Off-label-2025-05-07.pdf` |

Die Download-IDs haben sich historisch geaendert und koennen ohne
Vorankuendigung wechseln. Bei Ausfall einer URL: direkt auf
`https://www.g-ba.de/richtlinien/1/` navigieren und die aktuelle Anlage
manuell ausfindig machen.

PRISCUS 2.0 und GKV-SV-Praxisbesonderheiten werden separat gepflegt
(`regeln.json`, `praxisbesonderheiten.json`) — nicht aus AM-RL-PDFs.

---

## 3. Extraktions-Pipeline

### 3.1 Werkzeuge

- **PyMuPDF** (`import fitz`, Paket `pymupdf`) — PDF-Text-Extraktion.
- **Python-Stdlib** (`json`, `re`, `pathlib`) — Strukturierung.
- **Manuelle Verifikation** — jeder Eintrag wird gegen die PDF-Seitenzahlen
  geprueft (Stichprobe: 100 %, vollstaendig bei juristisch sensiblen Nummern).

### 3.2 Heuristiken

Der Rohtext aus `_raw/*.txt` wird nach folgendem Muster zerlegt:

- Nummern-Erkennung per Regex: `^\s*(\d+)\.?\s+(.+)` (Anlage III nummeriert
  von 1 an, teilweise mit Luecken).
- ATC-Pattern: aus der Stichwort-Erkennung (z.B. "Acida" -> ATC `A02B%`),
  manuell gepflegt. Fuer neue Eintraege gilt: wenn kein ATC eindeutig ist,
  wird ein **Platzhalter** (z.B. `"_TODO_"`) gesetzt und im Review nachgereicht.
- Ampel-Farbe (`rot`/`gelb`/`gruen`): abgeleitet aus der Formulierung
  ("Verordnungsausschluss" -> rot, "Verordnungseinschraenkung" -> gelb,
  "verordnungsfaehig" -> gruen).

### 3.3 Manuelle Validierung

Vor jedem Release:
1. Jede neue oder geaenderte Nummer mindestens 1x vom medizinischen
   Reviewer (Therapiefreiheit e.V. / aerztlicher Partner) bestaetigen.
2. ATC-Pattern gegen WHO-ATC-Index pruefen (https://www.whocc.no/atc_ddd_index/).
3. Mindestens drei Stichproben-Checks pro Anlage: "Text in PDF finden und
   Wortlaut vergleichen".

---

## 4. Aktualisierungsverfahren (Schritt-fuer-Schritt)

Wenn der G-BA eine neue Fassung publiziert:

1. **PDF laden**
   - Neue PDF in `data/seed/_raw/` als `amrl_<nr>_<YYYY-MM-DD>.pdf` ablegen.
   - Rohtext extrahieren und als `amrl_<nr>_<YYYY-MM-DD>.txt` speichern:
     ```bash
     PYTHONIOENCODING=utf-8 python -c "import fitz; \
       doc=fitz.open('data/seed/_raw/amrl_III_NEU.pdf'); \
       open('data/seed/_raw/amrl_III_NEU.txt','w',encoding='utf-8').write( \
         '\n'.join(p.get_text() for p in doc))"
     ```

2. **Diff gegen alten Rohtext** (optional via `scripts/update_amrl.py`):
   ```bash
   PYTHONIOENCODING=utf-8 PYTHONPATH=src python scripts/update_amrl.py \
       --anlage III --new data/seed/_raw/amrl_III_NEU.txt
   ```
   Das Skript listet neue/geloeschte/geaenderte Nummern — **nimmt aber
   keine automatische Uebernahme vor** (Haftungsgrund).

3. **JSON manuell anpassen**
   - Fuer jede Aenderung einen Eintrag in `amrl_anlage_<III|V|VI_A|VI_B>.json`
     einfuegen, aendern oder entfernen.
   - `_meta.stand`, `_meta.quelle_url`, `_meta.quelle_datei`,
     `_meta.raw_datei`, `_meta.extraktion_datum`, `_meta.eintraege_anzahl`
     aktualisieren.
   - `_meta.extraktion_version` hochzaehlen (siehe Abschnitt 5).

4. **Archivieren**
   - Alten Stand nach `data/seed/_archiv/<DATUM>/amrl_anlage_<...>.json`
     kopieren (manuelle Kopie oder `scripts/update_amrl.py --archive`).

5. **quellen.json aktualisieren**
   - Neues `stand`-Datum im passenden Eintrag eintragen.

6. **Tests laufen lassen**
   ```bash
   PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m pytest tests/ -q
   ```
   Insbesondere Idempotenz- und Loader-Tests muessen gruen bleiben.

7. **Verifikation**
   ```bash
   PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m verordnungsampel.cli.main init
   PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m verordnungsampel.cli.main sources
   ```
   Stand-Datum und Eintragszahl muessen stimmen.

8. **Commit**
   - Commit-Message: `feat(seed): Update AM-RL Anlage III auf Stand YYYY-MM-DD`
   - CHANGELOG.md: Einen Abschnitt unter "Regelwerks-Updates" einfuegen.

---

## 5. Versionierung der Seeds (Semantic Versioning)

Das Feld `_meta.extraktion_version` folgt `major.minor.patch`:

| Bump | Anlass |
|---|---|
| **major** (`1.0.0` -> `2.0.0`) | Schema-Bruch: neue Pflichtfelder, alte Felder entfallen, Loader-Inkompatibilitaet |
| **minor** (`1.0.0` -> `1.1.0`) | Neue Eintraege oder groessere inhaltliche Aenderungen (z.B. G-BA-Update) |
| **patch** (`1.0.0` -> `1.0.1`) | Tippfehler-Korrekturen, ATC-Pattern-Feintuning, keine inhaltliche Veraenderung |

Beim Schema-Bump **major** MUSS der Loader (`db/seed.py`) getestet und
angepasst werden. Fallback auf altes Format bleibt bestehen fuer
Archiv-Dateien.

---

## 6. Rollback

Frueherer Stand wiederherstellen:

```bash
cp data/seed/_archiv/<DATUM>/amrl_anlage_III.json data/seed/amrl_anlage_III.json
PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m verordnungsampel.cli.main init
```

Der `init`-Befehl ist **idempotent**: `amrl_anlage` und
`praxisbesonderheit` werden vor jedem Insert geleert, danach frisch
geladen. Kein manueller DB-Cleanup noetig.

Wenn das Archiv-Verzeichnis nicht existiert: Rollback ueber Git
(`git checkout <commit> -- data/seed/amrl_anlage_III.json`).

---

## 7. Automatisierungs-Potenzial (Roadmap)

Aktuell: **manueller Prozess** wegen Haftungsrisiko (siehe Abschnitt 3.3).

Mittelfristig denkbar:

1. **GitHub Action `amrl-diff`**
   - Cron (woechentlich) laedt die aktuell bei `g-ba.de/richtlinien/1/`
     verlinkten PDFs, fuehrt `scripts/update_amrl.py` aus und oeffnet
     bei Diff ein Issue "AM-RL Anlage III: mutmassliche Aenderung seit <datum>".
   - Kein Auto-Commit! Nur Hinweis fuer den Maintainer.

2. **E-Mail-Alarm bei URL-Aenderung**
   - Hetzner-Cronjob: `HEAD`-Request auf die bekannten Download-IDs.
     404 / Location-Header-Aenderung -> Mail an Maintainer.

3. **Watchdog auf G-BA-Pressemitteilungen**
   - Feed `https://www.g-ba.de/presse/rss/` auf Stichworte
     "Arzneimittel-Richtlinie", "Anlage III/V/VI" matchen.

Keine Automatisierung der **Uebernahme** — die manuelle juristische
Pruefung bleibt Pflicht.

---

## 8. Verantwortlichkeit

**Stand 2026-04-12:** Verantwortung offen.

- **Code/Loader/Tests:** Projekt-Maintainer (derzeit: Lukas Geiger)
- **Medizinisch-juristisches Review:** Therapiefreiheit e.V. (angefragt)
- **Langfristig:** Open-Source-Community + gefoerderte Traegerschaft
  (siehe `KONZEPT.md`).

Bis zur Klaerung gilt:
- Keine stille Uebernahme von G-BA-Aenderungen ohne Review.
- Jede Regelwerks-Aenderung erhaelt einen Git-Commit mit Autor und Review-Flag.
- Fuer haftungssensible Nummern (ROT-Ausschluesse, Cannabis, Off-Label):
  **Vier-Augen-Prinzip** Pflicht.

---

## Anhang: CLI-Kurzreferenz

```bash
# Regelwerk initialisieren / neu laden
PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m verordnungsampel.cli.main init

# Uebersicht: welche Regelwerke sind geladen, Stand-Datum, Eintraege
PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m verordnungsampel.cli.main sources
PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m verordnungsampel.cli.main sources --verbose
PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m verordnungsampel.cli.main sources --json

# Regeln einer Anlage auflisten (Filter: --atc, --ampel, --output)
PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m verordnungsampel.cli.main rules --anlage III
PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m verordnungsampel.cli.main rules --anlage III --ampel ROT
PYTHONIOENCODING=utf-8 PYTHONPATH=src python -m verordnungsampel.cli.main rules --anlage VI_A --atc A10 --output json

# Zukuenftiges Update-Check-Skript (Maintainer-Tool)
PYTHONIOENCODING=utf-8 PYTHONPATH=src python scripts/update_amrl.py --help
```
