import numpy as np
import pandas as pd
import pytest
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

from src.analysis.mde import mde_run

Z_SUM = 1.959964 + 0.841621   # z_(alpha/2) + z_(power), for alpha 0.05 and power 0.80


# ---------- helpers ----------

def make_data(n_control=1000, n_mens=1000, n_womens=1000, seed=0):
    """Control conversion is exactly 10%. Spend is random with std of about 2."""
    rng = np.random.default_rng(seed)

    def group(name, n, conv_rate):
        conversion = np.zeros(n, dtype=int)
        conversion[: int(n * conv_rate)] = 1
        return pd.DataFrame({"segment": name, "conversion": conversion,
                             "spend": rng.normal(5, 2, n)})

    return pd.concat([
        group("No E-Mail", n_control, 0.10),
        group("Mens E-Mail", n_mens, 0.10),
        group("Womens E-Mail", n_womens, 0.10),
    ], ignore_index=True)


def write_csv(df, tmp_path):
    path = tmp_path / "data.csv"
    df.to_csv(path, index=False)
    return str(path)


def conversion_mde_by_hand(baseline, n_control, n_treat):
    """Normal approximation in Cohen's h, converted back to a rate difference."""
    h = Z_SUM * np.sqrt(1 / n_treat + 1 / n_control)
    p2 = np.sin((h + 2 * np.arcsin(np.sqrt(baseline))) / 2) ** 2
    return p2 - baseline


# ---------- structure ----------

def test_returns_a_row_per_treatment(tmp_path):
    result = mde_run(write_csv(make_data(), tmp_path))
    assert len(result) == 2
    assert set(result["treatment"]) == {"Mens E-Mail", "Womens E-Mail"}


def test_has_expected_columns(tmp_path):
    result = mde_run(write_csv(make_data(), tmp_path))
    assert {"treatment", "n_treat", "mde_conversion",
            "mde_conversion_relative_%", "mde_spend_$"} <= set(result.columns)


def test_n_treat_matches_group_sizes(tmp_path):
    df = make_data(n_control=1000, n_mens=1500, n_womens=800)
    result = mde_run(write_csv(df, tmp_path)).set_index("treatment")
    assert result.loc["Mens E-Mail", "n_treat"] == 1500
    assert result.loc["Womens E-Mail", "n_treat"] == 800


# ---------- MDE against hand calculations ----------

def test_conversion_mde_matches_hand_formula(tmp_path):
    df = make_data(n_control=1000, n_mens=1000, n_womens=1000)
    result = mde_run(write_csv(df, tmp_path))

    expected = conversion_mde_by_hand(baseline=0.10, n_control=1000, n_treat=1000)
    assert result["mde_conversion"].tolist() == pytest.approx([expected] * 2, abs=1e-3)


def test_spend_mde_matches_hand_formula(tmp_path):
    # MDE = (z_alpha + z_beta) * std * sqrt(1/n_treat + 1/n_control)
    # The function uses the t-distribution, so allow a small gap from the normal formula.
    df = make_data(n_control=1000, n_mens=1000, n_womens=1000)
    result = mde_run(write_csv(df, tmp_path))

    std = df.loc[df["segment"] == "No E-Mail", "spend"].std()
    expected = Z_SUM * std * np.sqrt(1 / 1000 + 1 / 1000)
    assert result["mde_spend_$"].tolist() == pytest.approx([expected] * 2, rel=0.01)


def test_unequal_group_sizes_are_handled(tmp_path):
    # Control 1000, men 4000, women 500: the ratio argument must be used correctly
    df = make_data(n_control=1000, n_mens=4000, n_womens=500)
    result = mde_run(write_csv(df, tmp_path)).set_index("treatment")

    for name, n_treat in [("Mens E-Mail", 4000), ("Womens E-Mail", 500)]:
        expected = conversion_mde_by_hand(0.10, n_control=1000, n_treat=n_treat)
        assert result.loc[name, "mde_conversion"] == pytest.approx(expected, abs=1e-3)


# ---------- consistency checks ----------

def test_power_at_the_conversion_mde_is_80_percent(tmp_path):
    df = make_data(n_control=2000, n_mens=2000, n_womens=2000)
    result = mde_run(write_csv(df, tmp_path))

    for mde in result["mde_conversion"]:
        es = proportion_effectsize(0.10 + mde, 0.10)
        power = NormalIndPower().power(effect_size=es, nobs1=2000, alpha=0.05, ratio=1)
        assert power == pytest.approx(0.80, abs=0.01)    # MDE is rounded to 4 decimals


def test_relative_mde_is_consistent_with_absolute_mde(tmp_path):
    result = mde_run(write_csv(make_data(), tmp_path))
    expected = result["mde_conversion"] / 0.10 * 100
    assert result["mde_conversion_relative_%"].tolist() == pytest.approx(expected.tolist(), abs=0.05)


def test_mde_is_positive(tmp_path):
    result = mde_run(write_csv(make_data(), tmp_path))
    assert (result["mde_conversion"] > 0).all()
    assert (result["mde_spend_$"] > 0).all()


def test_larger_samples_give_smaller_mde(tmp_path):
    small = mde_run(write_csv(make_data(500, 500, 500), tmp_path))
    large = mde_run(write_csv(make_data(4000, 4000, 4000), tmp_path))
    assert large["mde_conversion"].iloc[0] < small["mde_conversion"].iloc[0]
    assert large["mde_spend_$"].iloc[0] < small["mde_spend_$"].iloc[0]


def test_quadrupling_the_sample_halves_the_mde(tmp_path):
    # MDE is proportional to 1/sqrt(n), so 4x the customers -> about half the MDE
    base = mde_run(write_csv(make_data(1000, 1000, 1000), tmp_path))
    big = mde_run(write_csv(make_data(4000, 4000, 4000), tmp_path))
    ratio = big["mde_conversion"].iloc[0] / base["mde_conversion"].iloc[0]
    assert ratio == pytest.approx(0.5, abs=0.03)