"""i18n-Infrastruktur für VerordnungsAmpel (DE/EN).

Lädt JSON-basierte Übersetzungen aus ``data/translations/<lang>.json`` und
stellt eine schlanke API zum Abrufen lokalisierter Strings bereit:

- :func:`t` — primäre Lookup-Funktion mit ``str.format``-kompatibler
  Variablen-Ersetzung.
- :func:`set_language` / :func:`get_language` — Aktive Sprache umschalten.
- :func:`available_languages` — Liste der gefundenen Sprach-Codes.
- :func:`reload` — Übersetzungs-Cache leeren (z.B. für Tests).

Das Modul ist bewusst frei von externen Abhängigkeiten und liest direkt
aus dem mitgelieferten Daten-Verzeichnis (``utils.paths.project_data_dir``).
Das Translations-Schema ist an Geiger 2026 (DOI 10.5281/zenodo.18736725,
MIT) angelehnt und unter GPL-3.0 re-lizenziert.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Iterable

from verordnungsampel.utils.paths import project_data_dir


_DEFAULT_LANGUAGE = "de"
_FALLBACK_LANGUAGE = "de"

_lock = threading.RLock()
_current_language: str = _DEFAULT_LANGUAGE
_translations: dict[str, dict[str, str]] = {}
_loaded: bool = False


class TranslationError(KeyError):
    """Wird ausgelöst, wenn ein Key in keiner Sprache gefunden wird."""


def _translations_dir() -> Path:
    return project_data_dir() / "translations"


def _load_language_file(path: Path) -> dict[str, str]:
    """Lade eine einzelne Sprach-Datei und filtere Meta-Keys (führendes ``_``)."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Ungültige JSON-Übersetzungsdatei {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"Translation file {path} muss ein JSON-Objekt sein")
    return {k: v for k, v in raw.items() if not k.startswith("_") and isinstance(v, str)}


def _ensure_loaded() -> None:
    """Lazy-Load aller verfügbaren Sprach-Dateien (idempotent)."""
    global _loaded
    if _loaded:
        return
    with _lock:
        if _loaded:
            return
        directory = _translations_dir()
        if not directory.is_dir():
            raise FileNotFoundError(
                f"Translations-Ordner fehlt: {directory}. "
                "Erwartet werden Dateien wie data/translations/de.json."
            )
        loaded: dict[str, dict[str, str]] = {}
        for json_path in sorted(directory.glob("*.json")):
            lang = json_path.stem
            loaded[lang] = _load_language_file(json_path)
        if _DEFAULT_LANGUAGE not in loaded:
            raise FileNotFoundError(
                f"Default-Sprache '{_DEFAULT_LANGUAGE}' fehlt in {directory}"
            )
        _translations.clear()
        _translations.update(loaded)
        _loaded = True


def reload() -> None:
    """Cache leeren (Tests, Hot-Reload). Sprache bleibt erhalten."""
    global _loaded
    with _lock:
        _loaded = False
        _translations.clear()


def available_languages() -> list[str]:
    """Liste der verfügbaren Sprach-Codes (sortiert)."""
    _ensure_loaded()
    return sorted(_translations.keys())


def get_language() -> str:
    """Aktive Sprache zurückgeben."""
    return _current_language


def set_language(lang: str) -> None:
    """Aktive Sprache wechseln. Wirft ``ValueError`` bei unbekannter Sprache."""
    _ensure_loaded()
    if lang not in _translations:
        raise ValueError(
            f"Unbekannte Sprache '{lang}'. Verfügbar: {available_languages()}"
        )
    global _current_language
    with _lock:
        _current_language = lang


def t(key: str, *, lang: str | None = None, **fmt: object) -> str:
    """Lokalisierten String für ``key`` zurückgeben.

    Lookup-Reihenfolge:
        1. Aktive (oder per ``lang=`` überschriebene) Sprache
        2. Fallback-Sprache (Default: ``de``)

    ``fmt``-Argumente werden via ``str.format`` substituiert. Fehlende
    Format-Felder lassen den Platzhalter unverändert (kein Crash).

    Args:
        key: Lookup-Schlüssel (z.B. ``"APP_TITLE"``).
        lang: Optionaler Override der aktiven Sprache.
        **fmt: Format-Variablen für ``str.format``.

    Raises:
        TranslationError: Wenn der Key in keiner Sprache existiert.
    """
    _ensure_loaded()
    target_lang = lang or _current_language
    # Bugsweep (2026-06-23): isinstance-Guard. Mappt eine Sprache in der geladenen
    # Übersetzungsdatei auf null (statt auf ein Objekt), liefert .get(lang, {}) das
    # None und das verkettete .get(key) crashte mit AttributeError.
    _lang_dict = _translations.get(target_lang)
    raw: str | None = _lang_dict.get(key) if isinstance(_lang_dict, dict) else None
    if raw is None and target_lang != _FALLBACK_LANGUAGE:
        _fb_dict = _translations.get(_FALLBACK_LANGUAGE)
        raw = _fb_dict.get(key) if isinstance(_fb_dict, dict) else None
    if raw is None:
        raise TranslationError(
            f"Key '{key}' fehlt in Sprache '{target_lang}' und Fallback "
            f"'{_FALLBACK_LANGUAGE}'."
        )
    if not fmt:
        return raw
    try:
        return raw.format(**fmt)
    except (KeyError, IndexError):
        # Fehlende Platzhalter ignorieren statt crashen.
        return raw


def keys(lang: str | None = None) -> Iterable[str]:
    """Iterator über alle bekannten Keys einer Sprache (Default: aktive)."""
    _ensure_loaded()
    target_lang = lang or _current_language
    return iter(_translations.get(target_lang, {}).keys())


def has_key(key: str, *, lang: str | None = None) -> bool:
    """True, wenn ``key`` in der angegebenen oder aktiven Sprache vorhanden ist."""
    _ensure_loaded()
    target_lang = lang or _current_language
    return key in _translations.get(target_lang, {})


__all__ = [
    "TranslationError",
    "available_languages",
    "get_language",
    "has_key",
    "keys",
    "reload",
    "set_language",
    "t",
]
