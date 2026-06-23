# -*- coding: utf-8 -*-
"""Regressionstests Bugsweep 2026-06-23 (Desktop, /bugsweep paced Loop).

Geprüfte echte Bugs (VerordnungsAmpel Desktop-Erst-Sweep; medizinisch → do-no-harm,
nur Code-Robustheit, keine klinische Logik geändert):
  #1 cli.cmd_check: _load_answers_file wirft ValueError/OSError (ungültige/fehlende
     --answers-Datei), cmd_check fing nur JustificationError → roher Traceback.
  #2 cli.cmd_workflow: out_path.write_text ohne OSError-Guard → Traceback bei
     PermissionError/fehlendem Verzeichnis.
  #3 i18n.t(): verkettetes _translations.get(lang, {}).get(key) → AttributeError, wenn
     eine Sprache in der Übersetzungsdatei auf null mappt. isinstance-Guard.
  #4 gui/check_tab: GUI-Nutzereingaben icd/atc flossen ungeescaped in setHtml
     (<img src=...> würde remote laden) → html.escape.

FALSE POSITIVES (verifiziert, NICHT geändert; s. AUFGABEN): compliance_log-Append ist
atomar (INSERT+UPDATE in EINER Transaktion); seed.py f-string-SQL nutzt hardcodierte
Tabellen; praxisbesonderheit None-Guard moot (seq=PK, ampel NOT NULL); app.py QMenu
wird via self.menu referenziert (kein GC); coverage.py int(alter) ist im CLI-Caller
cmd_coverage bereits per except ValueError abgesichert.
"""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "verordnungsampel"


# --- Bug #3: i18n None-Sprach-Dict (behavioral) ---------------------------

def test_i18n_none_language_dict_no_attributeerror(monkeypatch):
    from verordnungsampel import i18n

    # _ensure_loaded neutralisieren, damit die injizierte Struktur erhalten bleibt.
    monkeypatch.setattr(i18n, "_ensure_loaded", lambda: None)
    monkeypatch.setattr(i18n, "_translations", {i18n._FALLBACK_LANGUAGE: None})

    # Vor dem Fix: AttributeError ('NoneType' object has no attribute 'get').
    # Nach dem Fix: sauberer TranslationError (Key nicht auffindbar).
    with pytest.raises(i18n.TranslationError):
        i18n.t("EIN_NICHT_EXISTENTER_KEY", lang=i18n._FALLBACK_LANGUAGE)


# --- Bug #1/#2/#4: Quelltext-Assertionen ----------------------------------

def test_cmd_check_catches_answers_load_errors():
    src = (SRC / "cli" / "main.py").read_text(encoding="utf-8")
    # cmd_check muss ValueError/OSError der Antwortdatei abfangen (nicht nur JustificationError).
    assert "except (ValueError, OSError)" in src


def test_cmd_workflow_guards_file_write():
    src = (SRC / "cli" / "main.py").read_text(encoding="utf-8")
    # out_path.write_text muss in try/except OSError stehen.
    assert "Workflow-Datei konnte nicht geschrieben werden" in src
    assert "except OSError" in src


def test_check_tab_escapes_user_icd_atc():
    src = (SRC / "gui" / "tabs" / "check_tab.py").read_text(encoding="utf-8")
    assert "html.escape(ergebnis.icd)" in src
    assert "html.escape(ergebnis.atc)" in src
