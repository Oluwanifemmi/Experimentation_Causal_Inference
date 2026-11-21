import pandas as pd
import pytest

from src.design.randomization_balance_check import balance_check


def make_csv(tmp_path):
    """Small dataset whose statistics can be checked on paper."""
    df = pd.DataFrame({
        "segment": ["No E-Mail"] * 3 + ["Mens E-Mail"] * 3 + ["Womens E-Mail"] * 3,
        "history": [10, 20, 30,   10, 20, 60,   5, 5, 5],
        "newbie":  [0, 0, 1,      1, 1, 0,      1, 0, 1],
        "spend":   [0, 0, 0,      0, 0, 0,      0, 0, 0],   # should be ignored
    })
    path = tmp_path / "data.csv"
    df.to_csv(path, index=False)
    return str(path)


def test_one_row_per_segment(tmp_path):
    result = balance_check(make_csv(tmp_path))
    assert set(result.index) == {"No E-Mail", "Mens E-Mail", "Womens E-Mail"}
    assert len(result) == 3


def test_columns_are_history_and_newbie_with_six_statistics(tmp_path):
    result = balance_check(make_csv(tmp_path))
    assert set(result.columns.get_level_values(0)) == {"history", "newbie"}
    assert list(result["history"].columns) == ["sum", "mean", "max", "min", "median", "std"]
    assert result.shape == (3, 12)
    assert "spend" not in result.columns.get_level_values(0)


def test_history_statistics_for_control(tmp_path):
    h = balance_check(make_csv(tmp_path)).loc["No E-Mail", "history"]
    assert h["sum"] == 60
    assert h["mean"] == pytest.approx(20)
    assert h["max"] == 30
    assert h["min"] == 10
    assert h["median"] == 20
    assert h["std"] == pytest.approx(10)          # sqrt(200 / 2)


def test_history_statistics_for_mens(tmp_path):
    h = balance_check(make_csv(tmp_path)).loc["Mens E-Mail", "history"]
    assert h["sum"] == 90
    assert h["mean"] == pytest.approx(30)
    assert h["median"] == 20
    assert h["std"] == pytest.approx(26.4575, abs=1e-3)   # sqrt(1400 / 2)


def test_constant_group_has_zero_std(tmp_path):
    h = balance_check(make_csv(tmp_path)).loc["Womens E-Mail", "history"]
    assert h["std"] == pytest.approx(0)
    assert h["min"] == h["max"] == 5


def test_newbie_statistics(tmp_path):
    n = balance_check(make_csv(tmp_path)).loc["No E-Mail", "newbie"]
    assert n["sum"] == 1
    assert n["mean"] == pytest.approx(1 / 3)
    assert n["std"] == pytest.approx(0.57735, abs=1e-4)   # sqrt(1/3)


def test_mean_of_a_flag_is_a_proportion_between_0_and_1(tmp_path):
    result = balance_check(make_csv(tmp_path))
    assert ((result[("newbie", "mean")] >= 0) & (result[("newbie", "mean")] <= 1)).all()