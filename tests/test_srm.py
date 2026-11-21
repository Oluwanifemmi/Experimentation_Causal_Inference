import numpy as np
import pandas as pd
import pytest

from src.monitoring.srm import srm_checks


def write_csv(counts, tmp_path):
    """counts: dict of segment -> number of rows."""
    segments = []
    for name, n in counts.items():
        segments += [name] * n
    path = tmp_path / "data.csv"
    pd.DataFrame({"segment": segments}).to_csv(path, index=False)
    return str(path)


def test_perfectly_equal_split(tmp_path):
    path = write_csv({"No E-Mail": 100, "Mens E-Mail": 100, "Womens E-Mail": 100}, tmp_path)
    chi2, p = srm_checks(path)
    assert chi2 == pytest.approx(0.0)
    assert p == pytest.approx(1.0)


def test_hand_computed_chi_square(tmp_path):
    # Observed 10, 20, 30 and expected 20 each:
    # chi2 = (100 + 0 + 100) / 20 = 10
    # With 2 degrees of freedom, p = exp(-chi2 / 2) = exp(-5) = 0.006738
    path = write_csv({"No E-Mail": 10, "Mens E-Mail": 20, "Womens E-Mail": 30}, tmp_path)
    chi2, p = srm_checks(path)
    assert chi2 == pytest.approx(10.0)
    assert p == pytest.approx(np.exp(-5), rel=1e-6)


def test_your_hillstrom_group_sizes_show_no_srm(tmp_path):
    # chi2 = (37^2 + 28^2 + 65^2) / 19146 = about 0.333, p = exp(-chi2/2) = about 0.85
    path = write_csv({"Mens E-Mail": 19183, "Womens E-Mail": 19174, "No E-Mail": 19081}, tmp_path)
    chi2, p = srm_checks(path)
    assert chi2 == pytest.approx(0.3331, abs=1e-3)
    assert p == pytest.approx(np.exp(-chi2 / 2), rel=1e-6)
    assert p > 0.001                      # no SRM at the usual threshold


def test_clear_imbalance_is_flagged(tmp_path):
    path = write_csv({"No E-Mail": 500, "Mens E-Mail": 300, "Womens E-Mail": 200}, tmp_path)
    chi2, p = srm_checks(path)
    assert p < 0.001                      # SRM detected


def test_result_does_not_depend_on_row_order(tmp_path):
    counts = {"No E-Mail": 120, "Mens E-Mail": 100, "Womens E-Mail": 90}
    path = write_csv(counts, tmp_path)
    original = srm_checks(path)

    shuffled = pd.read_csv(path).sample(frac=1, random_state=0)
    shuffled.to_csv(path, index=False)
    assert srm_checks(path) == pytest.approx(original)


def test_which_group_is_larger_does_not_matter(tmp_path):
    # Equal expected counts, so swapping the labels gives the same statistic
    a = srm_checks(write_csv({"No E-Mail": 150, "Mens E-Mail": 100, "Womens E-Mail": 100}, tmp_path))
    b = srm_checks(write_csv({"No E-Mail": 100, "Mens E-Mail": 150, "Womens E-Mail": 100}, tmp_path))
    assert a == pytest.approx(b)


def test_p_value_is_a_valid_probability(tmp_path):
    path = write_csv({"No E-Mail": 95, "Mens E-Mail": 110, "Womens E-Mail": 105}, tmp_path)
    chi2, p = srm_checks(path)
    assert chi2 >= 0
    assert 0 <= p <= 1