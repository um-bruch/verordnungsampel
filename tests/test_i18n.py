"""Tests fuer das i18n-System (DE/EN-Translation, strings_de-Bridge).

Deckt ab:
- Lazy-Load der JSON-Translations
- t() liefert deutsch und englisch je nach aktiver Sprache
- Format-Substitution mit ``str.format``
- Fallback auf DE bei fehlendem Key in EN
- TranslationError bei voellig unbekanntem Key
- set_language()-Wechsel und Validierung
- Backwards-Compatible Bridge: ``from gui import strings_de as S`` plus
  Modul-Level ``S.APP_TITLE`` reagieren auf Sprachwechsel
"""

from __future__ import annotations

import json

import pytest

from verordnungsampel import i18n


@pytest.fixture(autouse=True)
def reset_i18n():
    """Vor jedem Test: Cache leeren und Sprache auf de zuruecksetzen."""
    i18n.reload()
    i18n.set_language("de")
    yield
    i18n.reload()
    i18n.set_language("de")


# ---------------------------------------------------------------------------
# Loader / Schema
# ---------------------------------------------------------------------------


def test_available_languages_contains_de_and_en():
    langs = i18n.available_languages()
    assert "de" in langs
    assert "en" in langs


def test_default_language_is_de():
    # Nach reload + set_language("de") in der Fixture
    assert i18n.get_language() == "de"


def test_translations_are_strings_only():
    # Meta-Eintraege (mit fuehrendem _) und Nicht-Strings duerfen nicht
    # in den geladenen Cache wandern.
    for key in i18n.keys("de"):
        assert isinstance(key, str)
        assert not key.startswith("_")


def test_translations_have_no_meta_key_leak():
    assert not i18n.has_key("_meta")


# ---------------------------------------------------------------------------
# t() — Lookup, Format, Fallback
# ---------------------------------------------------------------------------


def test_t_returns_german_by_default():
    assert i18n.t("APP_TITLE") == "VerordnungsAmpel"
    assert i18n.t("AMPEL_GRUEN") == "GRÜN"
    assert i18n.t("BTN_CANCEL") == "Abbrechen"


def test_t_with_lang_override_returns_english():
    assert i18n.t("AMPEL_GRUEN", lang="en") == "GREEN"
    assert i18n.t("BTN_CANCEL", lang="en") == "Cancel"


def test_t_after_set_language_en():
    i18n.set_language("en")
    assert i18n.get_language() == "en"
    assert i18n.t("AMPEL_GRUEN") == "GREEN"
    assert i18n.t("LOG_VERIFY_FAIL") == "WARNING: Hash chain is BROKEN!"


def test_t_format_substitution():
    rendered = i18n.t("WORKFLOW_SAVED", path="/tmp/x.txt")
    assert "/tmp/x.txt" in rendered


def test_t_format_missing_placeholder_does_not_crash():
    # Wenn keine kwargs uebergeben werden, bleiben Platzhalter erhalten.
    raw = i18n.t("CHECK_ERROR_GENERIC")
    assert "{msg}" in raw


def test_t_format_with_irrelevant_kwarg():
    # Extra-Kwargs werden ignoriert, weil ``str.format(**kwargs)`` nicht
    # genutzte Keys einfach uebergeht.
    rendered = i18n.t("APP_TITLE", foo="bar")
    assert rendered == "VerordnungsAmpel"


def test_t_format_unknown_placeholder_falls_back_to_raw():
    # Wenn ein Platzhalter im Template ist, der nicht in kwargs liegt,
    # soll der Roh-Text zurueckkommen statt zu crashen.
    rendered = i18n.t("CHECK_ERROR_GENERIC")  # erwartet {msg}
    assert "{msg}" in rendered


def test_t_unknown_key_raises_translation_error():
    with pytest.raises(i18n.TranslationError):
        i18n.t("DEFINITELY_NOT_A_REAL_KEY")


# ---------------------------------------------------------------------------
# Sprachwechsel
# ---------------------------------------------------------------------------


def test_set_language_unknown_raises_value_error():
    with pytest.raises(ValueError):
        i18n.set_language("xx")


def test_set_language_round_trip():
    i18n.set_language("en")
    assert i18n.get_language() == "en"
    i18n.set_language("de")
    assert i18n.get_language() == "de"


def test_has_key():
    assert i18n.has_key("APP_TITLE")
    assert not i18n.has_key("NONEXISTENT_KEY")


# ---------------------------------------------------------------------------
# Fallback DE bei luecken in EN
# ---------------------------------------------------------------------------


def test_fallback_to_de_when_en_misses_key(tmp_path, monkeypatch):
    """EN-Datei mit luecke -> Fallback auf DE."""
    # Wir simulieren temporaer ein Translations-Verzeichnis mit einer
    # absichtlich unvollstaendigen EN-Datei.
    fake_dir = tmp_path / "translations"
    fake_dir.mkdir()
    (fake_dir / "de.json").write_text(
        json.dumps({"FOO": "deutscher_foo", "BAR": "deutscher_bar"}),
        encoding="utf-8",
    )
    (fake_dir / "en.json").write_text(
        json.dumps({"FOO": "english_foo"}),  # BAR fehlt
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "verordnungsampel.i18n.project_data_dir", lambda: tmp_path
    )
    i18n.reload()
    i18n.set_language("en")
    assert i18n.t("FOO") == "english_foo"
    assert i18n.t("BAR") == "deutscher_bar"  # Fallback


# ---------------------------------------------------------------------------
# strings_de-Bridge
# ---------------------------------------------------------------------------


def test_strings_de_bridge_returns_german_strings():
    from verordnungsampel.gui import strings_de as S

    assert S.APP_TITLE == "VerordnungsAmpel"
    assert S.AMPEL_GRUEN == "GRÜN"
    assert S.BTN_CANCEL == "Abbrechen"


def test_strings_de_bridge_reacts_to_language_switch():
    from verordnungsampel.gui import strings_de as S

    assert S.AMPEL_GRUEN == "GRÜN"
    i18n.set_language("en")
    assert S.AMPEL_GRUEN == "GREEN"
    i18n.set_language("de")
    assert S.AMPEL_GRUEN == "GRÜN"


def test_strings_de_bridge_unknown_attribute_raises():
    from verordnungsampel.gui import strings_de as S

    with pytest.raises(AttributeError):
        _ = S.NOT_A_REAL_STRING


def test_strings_de_bridge_dunder_attributes_not_routed():
    """Schutz vor versehentlichem Routing von Python-Internals."""
    from verordnungsampel.gui import strings_de as S

    # ``__name__`` etc. duerfen nicht ueber __getattr__ laufen
    assert S.__name__ == "verordnungsampel.gui.strings_de"


def test_strings_de_dir_lists_known_keys():
    from verordnungsampel.gui import strings_de as S

    listed = dir(S)
    assert "APP_TITLE" in listed
    assert "AMPEL_GRUEN" in listed
    assert "DISCLAIMER_BTN_ACCEPT" in listed


# ---------------------------------------------------------------------------
# Konsistenz DE <-> EN
# ---------------------------------------------------------------------------


def test_de_and_en_keys_match():
    """Sicherheitsnetz: DE und EN sollen denselben Keyset haben.

    Falls EN eine Luecke hat, faellt t() zwar auf DE zurueck, aber wir
    wollen explizit wissen, wenn ein neuer Key in DE landet ohne EN-
    Pendant.
    """
    de_keys = set(i18n.keys("de"))
    en_keys = set(i18n.keys("en"))
    only_in_de = de_keys - en_keys
    only_in_en = en_keys - de_keys
    assert not only_in_de, f"DE-Keys ohne EN-Uebersetzung: {sorted(only_in_de)}"
    assert not only_in_en, f"EN-Keys ohne DE-Pendant: {sorted(only_in_en)}"


def test_about_text_has_version_placeholder_in_both_languages():
    de_text = i18n.t("ABOUT_TEXT", lang="de")
    en_text = i18n.t("ABOUT_TEXT", lang="en")
    assert "{version}" in de_text
    assert "{version}" in en_text


def test_about_text_format_works():
    rendered_de = i18n.t("ABOUT_TEXT", version="1.0")
    assert "1.0" in rendered_de
    assert "{version}" not in rendered_de
