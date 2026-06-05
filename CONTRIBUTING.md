# Beitragsrichtlinie / Contributing Guide

## Deutsch

Vielen Dank für Ihr Interesse, zu diesem Projekt beizutragen!

### Wie Sie beitragen können

1. **Bug melden:** Erstellen Sie ein Issue mit dem Label `bug`
2. **Feature vorschlagen:** Erstellen Sie ein Issue mit dem Label `enhancement`
3. **Regelwerk pflegen:** AM-RL-Anlagen ändern sich quartalsweise — Aktualisierungen der
   JSON-Seed-Dateien sind besonders willkommen (Quellen angeben!)
4. **Rechtsprechung ergänzen:** Neue BSG/SG/LSG-Urteile zu Wirtschaftlichkeitsprüfung →
   als Issue mit Label `rechtsprechung`
5. **Code beitragen:** Pull Request erstellen

### Pull Requests

1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch: `git checkout -b feature/mein-feature`
3. Committen Sie Ihre Änderungen: `git commit --signoff -m "Beschreibung der Änderung"`
4. Pushen Sie den Branch: `git push origin feature/mein-feature`
5. Erstellen Sie einen Pull Request

### Developer Certificate of Origin (DCO)

Dieses Projekt verwendet den [Developer Certificate of Origin (DCO)](https://developercertificate.org/).
Bitte signieren Sie jeden Commit mit `--signoff`:

    git commit --signoff -m "Beschreibung der Änderung"

Damit bestätigen Sie, dass Sie das Recht haben, den Code unter der Projektlizenz (GPL-3.0-or-later) einzureichen.

### Code-Richtlinien

- Python: PEP 8 Stil
- Encoding: UTF-8 für alle Dateien
- Sprache: Code, Docstrings und Kommentare auf Deutsch oder Englisch (konsistent pro Modul)
- Deutsche Umlaute (ä ö ü ß) in Dokumentation und User-facing-Strings — NICHT ae/oe/ue
- Keine hardcoded Pfade oder API-Keys
- Neue Regelwerke IMMER mit Quellen-Referenz (Paragraph, Urteil, G-BA-Beschluss)

### Tests

Alle PRs müssen die bestehende Test-Suite bestehen:

```bash
PYTHONPATH=src python -m pytest tests/ -q
```

Neue Features erfordern begleitende Tests.

### Erste Schritte

```bash
git clone https://github.com/um-bruch/verordnungsampel.git
cd verordnungsampel
pip install -r requirements.txt
pip install -e ".[dev]"
python -m verordnungsampel.cli.main init
```

Für GUI-Entwicklung zusätzlich:

```bash
pip install -e ".[gui]"
python -m verordnungsampel.cli.main gui
```

---

## English

Thank you for your interest in contributing to this project!

### How to Contribute

1. **Report bugs:** Create an issue with the `bug` label
2. **Suggest features:** Create an issue with the `enhancement` label
3. **Maintain rule sets:** AM-RL annexes change quarterly — updates of JSON seed files are
   especially welcome (cite sources!)
4. **Add case law:** New BSG/SG/LSG rulings on economic-efficiency review → file an issue
   with label `rechtsprechung`
5. **Contribute code:** Create a Pull Request

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit --signoff -m "Description of change"`
4. Push the branch: `git push origin feature/my-feature`
5. Create a Pull Request

### Developer Certificate of Origin (DCO)

This project uses the [Developer Certificate of Origin (DCO)](https://developercertificate.org/).
Please sign off every commit with `--signoff`:

    git commit --signoff -m "Description of change"

This certifies that you have the right to submit the code under the project license (GPL-3.0-or-later).

### Code Guidelines

- Python: PEP 8 style
- Encoding: UTF-8 for all files
- Language: Code, docstrings and comments in German or English (consistent per module)
- German umlauts (ä ö ü ß) in documentation and user-facing strings — NOT ae/oe/ue
- No hardcoded paths or API keys
- New rule sets ALWAYS with source references (paragraph, ruling, G-BA decision)

### Tests

All PRs must pass the existing test suite:

```bash
PYTHONPATH=src python -m pytest tests/ -q
```

New features require accompanying tests.

### Getting Started

```bash
git clone https://github.com/um-bruch/verordnungsampel.git
cd verordnungsampel
pip install -r requirements.txt
pip install -e ".[dev]"
python -m verordnungsampel.cli.main init
```

For GUI development also:

```bash
pip install -e ".[gui]"
python -m verordnungsampel.cli.main gui
```
