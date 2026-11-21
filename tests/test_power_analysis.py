import math

import numpy as np
import pandas as pd
import pytest

from src.design.power_analysis import sample_size, statistic_power, observed_powerlist


# ---------- helpers ----------

def make_data(n=1000, treat_conv_rate=0.10, treat_spend_shift=0.0, seed=0):
    """Control plus two treatment groups of equal size.
    Control conversion is exactly 10%. Both treatments get the same
    conversion rate and spend shift, so the tests are easy to reason about."""
    rng = np.random.default_rng(seed)
    base_spend = rng.normal(5, 2, n)

    def group(name, conv_rate, shift):
        conversion = np.zeros(n, dtype=int)
        conversion[: int(n * conv_rate)] = 1
        return pd.DataFrame({"segment": name, "conversion": conversion,
                             "spend": base_spend + shift})

    return pd.concat([
        group("No E-Mail", 0.10, 0.0),
        group("Mens E-Mail", treat_conv_rate, treat_spend_shift),
        group("Womens E-Mail", treat_conv_rate, treat_spend_shift),
    ], ignore_index=True)


def write_csv(df, tmp_path):
    path = tmp_path / "data.csv"
    df.to_csv(path, index=False)
    return str(path)


# ---------- sample_size ----------

def test_baseline_comes_from_the_control_group(tmp_path):
    df = make_data()
    _, baseline = sample_size(write_csv(df, tmp_path))
    assert baseline == pytest.approx(0.10)


def test_sample_size_matches_hand_formula(tmp_path):
    # Two-sample proportions: n = 2 * ((z_alpha + z_beta) / h)^2, h = Cohen's h
    # Baseline 0.10 and the hard-coded MDE of 0.003 -> 0.10 vs 0.103
    df = make_data()
    n, baseline = sample_size(write_csv(df, tmp_path))

    z_alpha, z_beta = 1.959964, 0.841621
    h = 2 * math.asin(math.sqrt(baseline + 0.003)) - 2 * math.asin(math.sqrt(baseline))
    expected = 2 * ((z_alpha + z_beta) / h) ** 2
    assert n == pytest.approx(expected, rel=0.001)


def test_sample_size_is_large_for_a_small_lift(tmp_path):
    # A 0.3 point lift on a 10% baseline needs tens of thousands per group
    n, _ = sample_size(write_csv(make_data(), tmp_path))
    assert 30_000 < n < 50_000


# ---------- statistic_power ----------

def test_statistic_power_returns_control_summaries(tmp_path):
    df = make_data()
    n_control, baseline, std_spend = statistic_power(write_csv(df, tmp_path))

    control = df[df["segment"] == "No E-Mail"]
    assert n_control == len(control)
    assert baseline == pytest.approx(control["conversion"].mean())
    assert std_spend == pytest.approx(control["spend"].std())


# ---------- observed_powerlist ----------

def test_returns_a_row_per_treatment(tmp_path):
    result = observed_powerlist(write_csv(make_data(), tmp_path))
    assert len(result) == 2
    assert set(result["treatment"]) == {"Mens E-Mail", "Womens E-Mail"}


def test_has_expected_columns(tmp_path):
    result = observed_powerlist(write_csv(make_data(), tmp_path))
    assert {"treatment", "conv_lift", "conv_power",
            "spend_diff", "spend_power"} <= set(result.columns)


def test_power_equals_alpha_when_there_is_no_effect(tmp_path):
    # Treatment identical to control: lift = 0, diff = 0 -> power = alpha = 0.05
    df = make_data(treat_conv_rate=0.10, treat_spend_shift=0.0)
    result = observed_powerlist(write_csv(df, tmp_path))
    assert result["conv_power"].tolist() == pytest.approx([0.05] * len(result), abs=1e-3)
    assert result["spend_power"].tolist() == pytest.approx([0.05] * len(result), abs=1e-3)


def test_power_is_near_one_for_a_large_effect(tmp_path):
    # +10 points of conversion and +3 dollars of spend with 1,000 per group
    df = make_data(treat_conv_rate=0.20, treat_spend_shift=3.0)
    result = observed_powerlist(write_csv(df, tmp_path))
    assert (result["conv_power"] > 0.95).all()
    assert (result["spend_power"] > 0.99).all()


def test_lift_and_diff_equal_the_difference_in_means(tmp_path):
    df = make_data(treat_conv_rate=0.15, treat_spend_shift=1.0)
    result = observed_powerlist(write_csv(df, tmp_path))
    row = result[result["treatment"] == "Mens E-Mail"].iloc[0]

    assert row["conv_lift"] == pytest.approx(0.05, abs=1e-4)
    assert row["spend_diff"] == pytest.approx(1.0, abs=1e-4)


def test_power_is_a_valid_probability(tmp_path):
    df = make_data(treat_conv_rate=0.12, treat_spend_shift=0.3)
    result = observed_powerlist(write_csv(df, tmp_path))
    for col in ["conv_power", "spend_power"]:
        assert ((result[col] >= 0) & (result[col] <= 1)).all()


def test_more_effect_means_more_power(tmp_path):
    small = observed_powerlist(write_csv(make_data(treat_spend_shift=0.2), tmp_path))
    large = observed_powerlist(write_csv(make_data(treat_spend_shift=0.8), tmp_path))
    assert large["spend_power"].iloc[0] > small["spend_power"].iloc[0]