"""Tests fuer das LIKE-Pattern-Matching der Engine."""

from verordnungsampel.engine.rules import pattern_matches


def test_none_pattern_matches_any_value():
    assert pattern_matches(None, "C09AA02") is True
    assert pattern_matches(None, "") is True
    assert pattern_matches(None, None) is True


def test_empty_string_pattern_matches_any_value():
    assert pattern_matches("", "C09AA02") is True


def test_concrete_pattern_matches_exact():
    assert pattern_matches("C09AA02", "C09AA02") is True
    assert pattern_matches("C09AA02", "C09AA05") is False


def test_percent_wildcard_at_end():
    assert pattern_matches("C09AA%", "C09AA02") is True
    assert pattern_matches("C09AA%", "C09AA05") is True
    assert pattern_matches("C09AA%", "C09BA02") is False


def test_percent_wildcard_in_middle():
    assert pattern_matches("C09%02", "C09AA02") is True
    assert pattern_matches("C09%02", "C09BB02") is True
    assert pattern_matches("C09%02", "C09BB05") is False


def test_underscore_wildcard():
    assert pattern_matches("C09AA_2", "C09AA02") is True
    assert pattern_matches("C09AA_2", "C09AA12") is True
    assert pattern_matches("C09AA_2", "C09AA002") is False


def test_pattern_with_no_value_returns_false():
    assert pattern_matches("C09AA%", None) is False
    assert pattern_matches("C09AA%", "") is False


def test_case_insensitive():
    assert pattern_matches("c09aa%", "C09AA02") is True
    assert pattern_matches("C09AA%", "c09aa02") is True
