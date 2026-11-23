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

    mde = 0.003           
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


def statistic_power(data_path:str):
    newdata = pd.read_csv(data_path)
    alpha = 0.05
    target_power = 0.80

    control = newdata[newdata["segment"] == "No E-Mail"]
    n_control = len(control)

    baseline_conv = control["conversion"].mean()
    std_spend = control["spend"].std()

    return n_control, baseline_conv , std_spend



def observed_powerlist(data_path:str):
    newdata = pd.read_csv(data_path)
    alpha = 0.05
    target_power = 0.80
    rows = []
    for name in ["Mens E-Mail", "Womens E-Mail"]:
        control = newdata[newdata["segment"] == "No E-Mail"]
        n_control = len(control)
                
        baseline_conv = control["conversion"].mean()
        std_spend = control["spend"].std()
        treat = newdata[newdata["segment"] == name]
        n_treat = len(treat)
        ratio = n_control / n_treat   

        #Conversion
        lift = treat["conversion"].mean() - baseline_conv
        es = proportion_effectsize(baseline_conv + lift, baseline_conv)
        power_conv = NormalIndPower().power(effect_size=es, nobs1=n_treat, alpha= alpha, ratio=ratio)

        #Spend
        diff = treat["spend"].mean() - control["spend"].mean()
        d = diff / std_spend
        power_spend = TTestIndPower().power(effect_size=d, nobs1=n_treat, alpha=alpha, ratio=ratio)

        rows.append({"treatment": name,
                    "conv_lift": lift, "conv_power": power_conv,
                    "spend_diff": diff, "spend_power": power_spend})
        row_fixed = pd.DataFrame(rows).round(4)
    return row_fixed

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    #nn_per_group, baseline = sample_size(data_path)
   #print("Sample size per group:", int(round(nn_per_group)))
    #print("Baseline conversion rate:", round(baseline, 5))
    #n_control , baseline_conv, std_spend = statistic_power(data_path)
    #print("Control size:", n_control)
    #print("Baseline conversion:", round(baseline_conv, 5))
    #print("Std of spend:", round(std_spend, 4))
    row = observed_powerlist(data_path)
    print(row)