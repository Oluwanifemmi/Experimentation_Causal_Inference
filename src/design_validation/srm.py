from scipy.stats import chisquare
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

data_path = "data/Processed_data/clean_processed_file.csv"

def srm_checks(data_path :str):
    data = pd.read_csv(data_path) 

    observed = data["segment"].value_counts()
    total = len(data)
    expected = [total / 3] * 3

    chi2, p_value = chisquare(f_obs=observed, f_exp=expected)
    return chi2, p_value



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    chi2, p_value = srm_checks(data_path)
    print(f"Chi-square:({chi2})")
    print(f"p-value:({p_value})")    

