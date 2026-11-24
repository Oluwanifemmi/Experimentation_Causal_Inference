import numpy as np
import pandas as pd 
import logging 
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest


logger = logging.getLogger()
Business_problem = "Does sending marketing emails improve customer spending and conversion?"
Null_hypothesis = "Sending marketing emails has no effect on customer spending and conversion"
Alternate_hypothesis = "Sending marketing emails changes customer spending and conversion"
significance_level = 0.05
power = 0.80
data_path = "data/Processed_data/clean_processed_file.csv"

def testing_hypo(datapath:str):
    df = pd.read_csv(datapath)
    control = df[df["segment"] == "No E-Mail"]["spend"]
    results = []
    for name in ["Mens E-Mail", "Womens E-Mail"]:
        treat = df[df["segment"] == name]["spend"]

        diff = treat.mean() - control.mean()
        se = np.sqrt(treat.var(ddof=1) / len(treat) + control.var(ddof=1) / len(control))
        ci_low, ci_high = diff - 1.96 * se, diff + 1.96 * se
        t_stat, p_value = stats.ttest_ind(treat, control, equal_var=False)
        results.append((name, diff, p_value, ci_low, ci_high))

    return results
   


def testing_hypo_conversion(datapath: str):
    df = pd.read_csv(datapath)
    control = df[df["segment"] == "No E-Mail"]["conversion"]

    results = []
    for name in ["Mens E-Mail", "Womens E-Mail"]:
        treat = df[df["segment"] == name]["conversion"]

        # difference in conversion rates
        p_treat, p_control = treat.mean(), control.mean()
        diff = p_treat - p_control

        # z-test: counts of conversions and group sizes
        count = [treat.sum(), control.sum()]
        nobs = [len(treat), len(control)]
        z_stat, p_value = proportions_ztest(count, nobs)

        # 95% CI for the difference in proportions
        se = np.sqrt(p_treat * (1 - p_treat) / len(treat) + p_control * (1 - p_control) / len(control))
        ci_low, ci_high = diff - 1.96 * se, diff + 1.96 * se

        results.append((name, diff, p_value, ci_low, ci_high))

    return results





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    #results = testing_hypo(data_path)

    #for name, diff, p_value, ci_low, ci_high in results:
    #    print(f"{name}: diff = {diff:.4f}, p_value = {p_value:.2e}, ci_low = {ci_low:.4f}, ci_high = {ci_high:.4f}")

    results = testing_hypo_conversion(data_path)
    for name, diff, p_value, ci_low, ci_high in results:
            print(f"{name}: diff = {diff:.4f}, p_value = {p_value:.2e}, ci_low = {ci_low:.4f}, ci_high = {ci_high:.4f}")
    
    