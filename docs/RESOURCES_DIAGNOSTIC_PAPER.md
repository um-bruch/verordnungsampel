# Ressourcen aus dem Diagnostic-Paper (Geiger 2026)

> **Quelle:** Lukas Geiger (2026). *An Integrated Multiaxial Model for Computer-Assisted Psychiatric Diagnosis*.
> **DOI:** [10.5281/zenodo.18736725](https://doi.org/10.5281/zenodo.18736725)
> **Lokaler Spiegel:** `_codebases/REF_Diagnostic_Paper/`
> **Lizenz:** MIT (Code) — kompatibel mit VerordnungsAmpel GPL-3.0
> **Erfasst:** 2026-04-08

## Kontext

Lukas' eigenes vorheriges Forschungsprojekt — ein *Multiaxial Diagnostic Expert System*, veröffentlicht im März 2026 auf Zenodo. Trotz des thematischen Unterschieds (Psychiatrische Diagnostik vs. Verordnungsprüfung) liefert das Projekt auf **zwei Ebenen** direkt nutzbare Bausteine:

- **A) Ressourcen für die Software (VerordnungsAmpel)**
- **B) Ressourcen für das Begleitpaper (Um:bruch ST-001)**

---

## A) Ressourcen für die Software (VerordnungsAmpel)

### A.1 Code-Database-Builder — **höchster Wert**

**Datei:** `_codebases/REF_Diagnostic_Paper/build_code_database.py` (801 Zeilen)

Direkt wiederverwendbar als Vorlage für das ICD-10-GM-Datenmodell. Die erzeugte `diagnostic_codes.db` zeigt das fertige Schema:

| Tabelle | Einträge | Spalten |
|---|---|---|
| `icd11` | 173 | `code`, `title_de`, `title_en`, `chapter`, `block` |
| `dsm5` | 127 | `icd10cm_code`, `title_de`, `title_en`, `dsm5_category` |
| `icf` | 85 | `code`, `title_de`, `title_en`, `component` |
| `code_mapping` | 89 | `source_system`, `source_code`, `target_system`, `target_code`, `mapping_quality` |
| `metadata` | 7 | `key`, `value` |

**Direkt nutzbar für VerordnungsAmpel:**

1. **Schema-Pattern für die ICD-10-GM-Datenbank** — exakt dieselbe Struktur (`code`, `title_de`, `title_en`, `chapter`, `block`) übertragbar auf ICD-10-GM
2. **Cross-System-Mapping mit Qualitätsbewertung** — exakt was wir für ICD↔Wirkstoff-Zuordnungen brauchen (Feld `mapping_quality`)
3. **Bilinguale Titel als Spalten** — einfacher als separater Translation-Layer bei statischen Terminologien
4. **89 ICD-DSM-Mappings als Test-Beispiele** für die Mapping-Logik

> **Nächster konkreter Schritt:** Python-Script `src/verordnungsampel/db/build_icd10gm.py` nach diesem Vorbild schreiben, das eine separate `icd10gm.db` aus offiziellen BfArM-Daten erzeugt.

### A.2 Translations-System — i18n-Infrastruktur

**Datei:** `_codebases/REF_Diagnostic_Paper/translations.json` (1469 Zeilen, 584 Keys)

Vollständige DE/EN-Infrastruktur, direkt portabel. Schema:

```json
{
  "de": { "key": "deutscher Text", ... },
  "en": { "key": "english text", ... }
}
```

> **Nächster konkreter Schritt:** `src/verordnungsampel/i18n.py` mit Lader für dieses Format anlegen, wenn das CLI/Backend mehrsprachig wird. Vorerst nur Hinweis — MVP bleibt deutsch.

### A.3 Testcenter — Flask + SQLite + REST-API

**Ordner:** `_codebases/REF_Diagnostic_Paper/testcenter/`

Ein vollständiges, laufendes Flask-Backend. Schlüsselpatterns:

| Pattern | Datei | Für VerordnungsAmpel nutzbar als |
|---|---|---|
| `@app.before_request` Auto-DB-Initialisierung | `app.py` Z. 40–76 | Saubere Erstinitialisierung des Regelwerks |
| Sessions + Batteries (Multi-Test-Bündel) | `app.py` Z. 47–70 | Multi-Verordnungs-Sessions pro Arzt |
| Token-basiertes Link-Sharing (UUID) | `app.py` (Session-Create) | Anonyme Nutzungs-Sessions ohne Login |
| Print-friendly Output | `templates/` | Compliance-Log-Export (Sozialgericht-ready) |
| REST-API (`/api/tests`, `/api/results/`, `/api/score`) | `app.py` | Strukturierte API für spätere PWA-Anbindung |
| Critical-Item-Alerts (PHQ-9 Item 9, C-SSRS) | `app.py` + `scoring.py` | Pattern für Regress-Risiko-Alerts in der Ampel-Engine |
| 16 validierte Instrumente mit automatischem Scoring | `scoring.py` | Pattern für Regel-Evaluator |

**Architektur-Übernahme für VerordnungsAmpel:**

- **Flask-Backend statt PHP/Node** — bewährt, läuft, Code existiert
- **SQLite mit `before_request` Auto-Init** — keine Setup-Skripte nötig
- **Token-URLs für anonyme Praxis-Sessions** — DSGVO-Vorteil, keine Benutzer-Accounts
- **Print-Templates für Compliance-Export** — direkt anpassbar

> **Nächster konkreter Schritt:** Wenn VerordnungsAmpel von CLI auf Browser-PWA erweitert wird, `testcenter/app.py` als Ausgangspunkt nehmen. Route-Struktur adaptieren: `/check` statt `/test`, `/compliance-log` statt `/session`.

### A.4 Hierarchical State Machine — Decision-Engine-Pattern

**Quelle:** Paper Section 9 *Technical Architecture of the Python Implementation* (Volltext im Spiegel unter `_codebases/REF_Diagnostic_Paper/paper/Review_Multiaxiale_Diagnostik_v2_en.tex`, Zeile 852 ff.)

Die Architektur **"Hierarchical State Machines as Decision Engine"** ist ein methodisch fundiertes Pattern für Plausibilitätsprüfungen über mehrere Schritte. Das deckt sich exakt mit der strukturierten Begründungspflicht in VerordnungsAmpel:

```
Diagnose → Vorbehandlung → Therapieversagen → BSG-Off-Label-Kriterien → Praxisbesonderheit
```

Jeder Zustand ist ein eigener HSM-State mit definierten Übergängen. Das macht die Begründungslogik deterministisch, testbar und vor Sozialgericht verteidigbar.

> **Nächster konkreter Schritt:** Für die MVP-Erweiterung um "strukturierte Begründungs-Templates" (KONZEPT.md Funktion 2) diese HSM-Architektur adaptieren. Kandidat: neues Modul `src/verordnungsampel/engine/justification_fsm.py`.

---

## B) Ressourcen für das Begleitpaper (ST-001)

Das Paper *"An Integrated Multiaxial Model for Computer-Assisted Psychiatric Diagnosis"* ist strukturell ein **Methods and Design Paper** — exakt das Format, in das ST-001 wachsen könnte. Die folgenden Sektionen sind als Vorlage direkt übertragbar:

### B.1 Paper-Struktur als Vorlage

| ST-001 könnte übernehmen | Aus Diagnostic-Paper Section |
|---|---|
| Methodisches Vorgehen schärfen | Section 1: *Methods* (Z. 87) |
| DSGVO-Sektion erweitern | Section 12 (Teil): *Data Protection and GDPR* (Z. 972) |
| Liability-Diskussion | Section 12 (Teil): *Liability and Medico-Legal Responsibility* |
| Algorithmische Bias | Section 12 (Teil): *Algorithmic Bias and Validation Populations* |
| Interoperabilität (HL7 FHIR) | Section 14: *Interoperability and Health IT Standards* (Z. 1072) |
| Validation Strategy | Section 13: *Validation Strategy* (Z. 1031) |
| Methodische Coverage-Analyse | Section 7: *The Coverage Analysis* (Z. 692) |

### B.2 Coverage-Analysis als methodischer Vorläufer

Die Coverage-Analysis aus dem Paper:

> **C(S) = |explained| / |total symptoms|**

ist ein **direkter Vorläufer unseres Verhältnis-Modells** (Schaden zu Einnahme). Beide arbeiten mit **set-basierter Metrik**. Wir können unsere Verhältnisrechnung als *"Coverage-Analyse für Folgekostenbeitrag"* methodisch fundieren — und auf das Paper verweisen.

> **Nächster konkreter Schritt:** In ST-001 Methodenteil eine Subsection "Coverage-Analyse für Regress-Risiko" anlegen, die auf Geiger (2026) verweist und die Formel auf unser Problem adaptiert.

### B.3 Zenodo-Veröffentlichungs-Workflow

Das Paper ist bereits auf Zenodo (DOI: 10.5281/zenodo.18736725). Wir können **denselben Workflow für ST-001 v1.0** nutzen — Lukas hat den Prozess schon aufgesetzt (siehe `ZENODO_CREDENTIALS.md` im Original-Projekt).

### B.4 ORCID + bibliographische Konvention

Das Paper nutzt LaTeX mit `diagnostic_references.bib`. Für ST-001 v1.0 kann derselbe BibTeX-Workflow übernommen werden — `paper/Review_Multiaxiale_Diagnostik_v2_en.tex` als LaTeX-Template-Vorbild.

---

## C) Konkrete Empfehlungen

### Sofort umsetzbar (für VerordnungsAmpel)

- [x] **`build_code_database.py`** als Template kopiert → `_codebases/REF_Diagnostic_Paper/build_code_database.py`
- [x] **`translations.json`** kopiert → `_codebases/REF_Diagnostic_Paper/translations.json`
- [x] **`testcenter/app.py`** als Flask-Backend-Vorlage kopiert → `_codebases/REF_Diagnostic_Paper/testcenter/app.py`
- [ ] ICD-10-GM-Builder-Script (`src/verordnungsampel/db/build_icd10gm.py`) nach Vorbild `build_code_database.py` schreiben
- [ ] i18n-Modul vorbereiten, wenn DE/EN-Anforderung konkret wird
- [ ] Flask-Backend-Prototyp aufsetzen, wenn von CLI auf PWA erweitert wird

### Mittelfristig (für ST-001)

- [ ] **DSGVO-Section** aus Paper-Section 12 lesen und eine kompakte Version in PP-003 + ST-001 einarbeiten (ergänzend zur DSGVO-Matrix)
- [ ] **Coverage-Analysis-Methodik** aus Section 7 auf unsere Verhältnisrechnung übertragen — methodisch fundieren statt nur abschätzen
- [ ] **Validation-Strategy** aus Section 13 als Vorbild für *"Was wäre eine empirische Prüfung der Hochrechnung?"* nehmen

### Strategisch

- [ ] **Inhaltlicher Bezug:** Das Diagnostic-Paper kann in ST-001 als Verweis dienen:

  > *"Eine ähnliche methodische Schichtung wurde für die psychiatrische Diagnostik bereits durchgeführt (Geiger 2026, Zenodo: 10.5281/zenodo.18736725)."*

  Das positioniert ST-001 als **zweiten Stein in einer methodischen Familie** — nicht als Einzelbeitrag, sondern als Fortführung einer bereits publizierten Methoden-Linie. Strategisch wertvoll für Reviewer-Wahrnehmung und Fördermittel.

---

## Lizenz-Klarheit

| Asset | Original-Lizenz | Nutzung in VerordnungsAmpel |
|---|---|---|
| `build_code_database.py` | MIT (Geiger 2026) | Direkt adaptierbar, GPL-3.0-Header beim Übernehmen setzen |
| `translations.json` | MIT (Geiger 2026) | Direkt adaptierbar |
| `testcenter/app.py`, `scoring.py`, `config.py` | MIT (Geiger 2026) | Direkt adaptierbar |
| `testcenter/tests/` (Instrument-Inhalte) | jeweils eigene Lizenzen, s. `testcenter/NOTICE.md` | **Nicht übernommen** — domänenfremd, Lizenzen nicht relevant |
| Paper-Volltext (`paper/*.tex`, `*.pdf`) | CC-BY-4.0 (Scientific Papers) | Zitieren per DOI, keine Direkt-Kopie ins Repo |

Da Lukas Geiger sowohl Autor der Diagnostic-Paper-Codebase als auch der VerordnungsAmpel ist, ist die Re-Lizenzierung MIT → GPL-3.0 rechtlich unproblematisch. Der Herkunftshinweis bleibt trotzdem als wissenschaftliche Zitation und aus Transparenzgründen:

```python
# Adapted from Diagnostic Testcenter (MIT, Geiger 2026,
# DOI 10.5281/zenodo.18736725). Re-licensed under GPL-3.0
# as part of VerordnungsAmpel.
```

---

## Verweise

- **Original-Projekt:** `C:\Users\User\OneDrive\.TOPICS\.RESEARCH\.CLOSED\!!!PP__Diagnostic\`
- **Lokaler Spiegel (diese Referenz):** `_codebases/REF_Diagnostic_Paper/`
- **VerordnungsAmpel-Konzept:** `../KONZEPT.md`
- **Code-Audit der anderen Referenzen:** `CODE_AUDIT.md` (MediPlaner, Foerderplaner)
- **Um:bruch ST-001:** `C:\Users\User\OneDrive\.UMBRUCH\Publikationen\Positionspapier\ST-001_Das_Angstsystem.tex`
