"""Test hardware microbenchmark functionality."""

from dads.benchmark import run_state_microbenchmarks


def test_microbenchmarks():
    res = run_state_microbenchmarks(iterations=500)
    assert res["struct_bytes"] == 32
    assert res["json_bytes"] > 100
    assert res["struct_avg_us"] > 0
    assert res["json_avg_us"] > 0
    assert res["speedup"] > 1.0
    assert res["token_savings_pct"] > 90.0

