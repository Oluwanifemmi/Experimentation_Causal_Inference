import numpy as np
import logging
import pandas as pd 

logger = logging.getLogger(__name__)


data_path = "data/Processed_data/clean_processed_file.csv"

def confidence_interval(data_path:str):
    data = pd.read_csv(data_path)
    #import numpy as np

    control = data[data["segment"] == "No E-Mail"]["spend"]

    for name in ["Mens E-Mail", "Womens E-Mail"]:
        treatment = data[data["segment"] == name]["spend"]

        diff = treatment.mean() - control.mean()
        se = np.sqrt(treatment.var() / len(treatment) + control.var() / len(control))

        low = diff - 1.96 * se
        high = diff + 1.96 * se
        return name, low , high , diff



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    name, low , high, diff = confidence_interval(data_path)
    print(name)
    print("  Difference:", round(diff, 4))
    print("  95% CI:", round(low, 4), "to", round(high, 4))