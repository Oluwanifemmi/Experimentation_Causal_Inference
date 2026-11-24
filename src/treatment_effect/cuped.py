import numpy as np
import logging 
import pandas as pd

logger = logging.getLogger(__name__)

data_path = "data/Processed_data/clean_processed_file.csv"


def cuped_variance_reduction(data_path:str):
    newdata = pd.read_csv(data_path)
    outcome = "spend"
    covariate = "history"

    #calculate theta
    cov = np.cov(newdata[covariate], newdata[outcome])[0, 1]
    theta = cov / newdata[covariate].var()
  
    #adjusted outcome
    newdata["spend_cuped"] = newdata[outcome] - theta * (newdata[covariate] - newdata[covariate].mean())

    #variance shrink range
    var_before = newdata[outcome].var()
    var_after = newdata["spend_cuped"].var()
    Variance_reduction = round(1 - var_after / var_before, 4)
    return Variance_reduction , theta , newdata



def raw_adjusted_treatment(newdata:pd.DataFrame):
    control = newdata[newdata["segment"] == "No E-Mail"]
    rows = []
    for name in ["Mens E-Mail", "Womens E-Mail"]:
        treatment = newdata[newdata["segment"] == name]

        for label, col in [("Raw", "spend"), ("CUPED", "spend_cuped")]:
            diff = treatment[col].mean() - control[col].mean()
            se = np.sqrt(treatment[col].var() / len(treatment) + control[col].var() / len(control))

            rows.append({
                "treatment": name,
                "method": label,
                "effect": diff,
                "se": se,
                "ci_low": diff - 1.96 * se,
                "ci_high": diff + 1.96 * se,
                "ci_width": 2 * 1.96 * se,
            })

    comparison = pd.DataFrame(rows)
    return comparison.round(4)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Vr , th, newdata = cuped_variance_reduction(data_path)
    print(f"Variance reduction:{Vr}")
    print(f"Theta:{th}")
    treatment_comparison = raw_adjusted_treatment(newdata)
    print(treatment_comparison)