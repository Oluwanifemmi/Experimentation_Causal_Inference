import numpy as np
import pandas as pd
import logging 
from statsmodels.stats.power import NormalIndPower, TTestIndPower
from statsmodels.stats.proportion import proportion_effectsize




logger = logging.getLogger(__name__)

data_path = "data/Processed_data/clean_processed_file.csv"

def sample_size(data_path:str):
    newdata = pd.read_csv(data_path)
    #baseline conversion rate
    control = newdata[newdata["segment"] == "No E-Mail"]
    baseline = control["conversion"].mean()

    mde = 0.02           
    alpha = 0.05
    power = 0.80

    #sample size per group
    effect_size = proportion_effectsize(baseline + mde, baseline)

    n_per_group = NormalIndPower().solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        ratio=1,
        alternative="two-sided",
    )
    return n_per_group , baseline



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    nn_per_group, baseline = sample_size(data_path)
    print("Sample size per group:", int(round(nn_per_group)))
    print("Baseline conversion rate:", round(baseline, 5))