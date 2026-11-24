import pandas as pd
import numpy as np
import logging 
from statsmodels.stats.power import NormalIndPower, TTestIndPower
from statsmodels.stats.proportion import proportion_effectsize

logger = logging.getLogger(__name__)
data_path =  "data/Processed_data/clean_processed_file.csv"


def mde_run(data_path:str):
    newdata = pd.read_csv(data_path)
    rows = []
    alpha = 0.05
    for name in ["Mens E-Mail", "Womens E-Mail"]:
        target_power = 0.80
        control = newdata[newdata["segment"] == "No E-Mail"]
        n_control = len(control)
                        
        baseline_conv = control["conversion"].mean()
        std_spend = control["spend"].std()
        treat = newdata[newdata["segment"] == name]
        n_treat = len(treat)
        n_treat = len(newdata[newdata["segment"] == name])
        ratio = n_control / n_treat

        # Conversion MDE (Cohen's h), then convert back to a rate difference
        h = NormalIndPower().solve_power(effect_size=None, nobs1=n_treat, alpha=alpha,
                                        power=target_power, ratio=ratio)
        p2 = np.sin((h + 2 * np.arcsin(np.sqrt(baseline_conv))) / 2) ** 2
        mde_conv = p2 - baseline_conv

        # Spend MDE (Cohen's d), then convert to dollars
        d = TTestIndPower().solve_power(effect_size=None, nobs1=n_treat, alpha=alpha,
                                        power=target_power, ratio=ratio)
        mde_spend = d * std_spend

        rows.append({"treatment": name,
                    "n_treat": n_treat,
                    "mde_conversion": mde_conv,
                    "mde_conversion_relative_%": mde_conv / baseline_conv * 100,
                    "mde_spend_$": mde_spend})
        new_row = pd.DataFrame(rows).round(4)
    return new_row




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    row = mde_run(data_path)
    print(row)