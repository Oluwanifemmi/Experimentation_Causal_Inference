import numpy as np
import pandas as pd
import pytest

from src.analysis.cuped import cuped_variance_reduction, raw_adjusted_treatment


# ---------- helpers ----------

def write_csv(df, tmp_path):
    path = tmp_path / "data.csv"
    df.to_csv(path, index=False)
    return str(path)


def simulated_experiment(corr_with_history=True, n=30_000, seed=0):
    """Three equal groups. True effects: men +1.0, women +0.5."""
    rng = np.random.default_rng(seed)
    segments = np.repeat(["No E-Mail", "Mens E-Mail", "Womens E-Mail"], n)
    history = rng.normal(100, 20, 3 * n)
    effect = np.where(segments == "Mens E-Mail", 1.0,
             np.where(segments == "Womens E-Mail", 0.5, 0.0))
    slope = 0.2 if corr_with_history else 0.0
    spend = slope * history + rng.normal(0, 2, 3 * n) + effect
    return pd.DataFrame({"segment": segments, "history": history, "spend": spend})


# ---------- cuped_variance_reduction ----------

def test_theta_and_reduction_hand_computed(tmp_path):
    # theta = 8/10 = 0.8 ; corr = 8/10 = 0.8 ; variance reduction = corr^2 = 0.64
    df = pd.DataFrame({"history": [1, 2, 3, 4, 5], "spend": [1, 3, 2, 5, 4]})
    vr, theta, _ = cuped_variance_reduction(write_csv(df, tmp_path))
    assert theta == pytest.approx(0.8)
    assert vr == pytest.approx(0.64)


def test_perfect_linear_relationship(tmp_path):
    df = pd.DataFrame({"history": [1, 2, 3, 4, 5], "spend": [2, 4, 6, 8, 10]})
    vr, theta, out = cuped_variance_reduction(write_csv(df, tmp_path))
    assert theta == pytest.approx(2.0)
    assert vr == pytest.approx(1.0)
    assert out["spend_cuped"].tolist() == pytest.approx([6, 6, 6, 6, 6])


def test_adjustment_preserves_mean_and_original_spend(tmp_path):
    df = simulated_experiment(n=2000)
    _, _, out = cuped_variance_reduction(write_csv(df, tmp_path))
    assert out["spend_cuped"].mean() == pytest.approx(df["spend"].mean())
    assert out["spend"].tolist() == pytest.approx(df["spend"].tolist())


def test_returns_dataframe_with_new_column(tmp_path):
    df = simulated_experiment(n=500)
    _, _, out = cuped_variance_reduction(write_csv(df, tmp_path))
    assert isinstance(out, pd.DataFrame)
    assert "spend_cuped" in out.columns
    assert len(out) == len(df)


def test_uncorrelated_history_gives_about_zero_reduction(tmp_path):
    df = simulated_experiment(corr_with_history=False)
    vr, theta, _ = cuped_variance_reduction(write_csv(df, tmp_path))
    assert abs(theta) < 0.02
    assert vr == pytest.approx(0.0, abs=0.001)      # like your Hillstrom 0.0002


def test_reduction_equals_squared_correlation(tmp_path):
    df = simulated_experiment()
    vr, _, _ = cuped_variance_reduction(write_csv(df, tmp_path))
    expected = df["history"].corr(df["spend"]) ** 2
    assert vr == pytest.approx(expected, abs=1e-4)  # function rounds to 4 decimals


# ---------- raw_adjusted_treatment ----------

def test_output_shape_and_columns(tmp_path):
    df = simulated_experiment(n=1000)
    _, _, out = cuped_variance_reduction(write_csv(df, tmp_path))
    result = raw_adjusted_treatment(out)

    assert len(result) == 4                          # 2 treatments x 2 methods
    assert set(result["method"]) == {"Raw", "CUPED"}
    assert set(result["treatment"]) == {"Mens E-Mail", "Womens E-Mail"}
    assert {"effect", "se", "ci_low", "ci_high", "ci_width"} <= set(result.columns)


def test_raw_effect_equals_difference_in_means(tmp_path):
    df = simulated_experiment(n=2000)
    _, _, out = cuped_variance_reduction(write_csv(df, tmp_path))
    result = raw_adjusted_treatment(out)

    control_mean = df.loc[df["segment"] == "No E-Mail", "spend"].mean()
    men_mean = df.loc[df["segment"] == "Mens E-Mail", "spend"].mean()
    row = result[(result["treatment"] == "Mens E-Mail") & (result["method"] == "Raw")].iloc[0]
    assert row["effect"] == pytest.approx(men_mean - control_mean, abs=1e-4)


def test_ci_is_consistent_with_effect_and_se(tmp_path):
    df = simulated_experiment(n=2000)
    _, _, out = cuped_variance_reduction(write_csv(df, tmp_path))
    result = raw_adjusted_treatment(out)

    assert (result["ci_low"] < result["effect"]).all()
    assert (result["effect"] < result["ci_high"]).all()
    assert result["ci_width"].tolist() == pytest.approx((2 * 1.96 * result["se"]).tolist(), abs=1e-3)


def test_cuped_keeps_effect_unbiased_and_narrows_ci(tmp_path):
    df = simulated_experiment(corr_with_history=True)
    _, _, out = cuped_variance_reduction(write_csv(df, tmp_path))
    result = raw_adjusted_treatment(out)

    truth = {"Mens E-Mail": 1.0, "Womens E-Mail": 0.5}
    for name, true_effect in truth.items():
        raw = result[(result["treatment"] == name) & (result["method"] == "Raw")].iloc[0]
        cup = result[(result["treatment"] == name) & (result["method"] == "CUPED")].iloc[0]

        assert cup["effect"] == pytest.approx(true_effect, abs=4 * cup["se"])
        assert cup["se"] < raw["se"]
        assert cup["ci_width"]