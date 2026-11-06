"""Test cryptographic integrity and trial pre-registration specifications."""

from dads.verify import verify_benchmark_integrity
from dads import PROMPT_SET_SHA256, PRE_REGISTERED_DATE, TOTAL_EVALUATION_TURNS, load_turns, load_benchmark_data


def test_trial_verification():
    res = verify_benchmark_integrity()
    assert res["verified"] is True
    assert len(res["errors"]) == 0
    assert len(res["checks"]) >= 5


def test_metadata_constants():
    assert PROMPT_SET_SHA256 == "e66f70eafd7ce902813a99d7ba49a244e0abcf137cc70b6f6c4a5b248b985e8e"
    assert PRE_REGISTERED_DATE == "2026-07-26"
    assert TOTAL_EVALUATION_TURNS == 11000


def test_turns_structure():
    turns = load_turns()
    assert len(turns) == 11
    for t in turns:
        assert "id" in t
        assert "number" in t
        assert "prompt" in t
        assert "criteria" in t
        assert "unrailed_pass_pct" in t
        assert "railed_pass_pct" in t


def test_models_structure():
    data = load_benchmark_data()
    models = data.get("models", [])
    assert len(models) == 6
    for m in models:
        assert "id" in m
        assert "name" in m
        assert "unrailed_overall" in m
        assert "railed_overall" in m
        # Assert treatment beats control across every model
        assert m["railed_overall"] > m["unrailed_overall"]

