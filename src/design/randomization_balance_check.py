import numpy as np
import pandas as pd 
import logging 

logger = logging.getLogger(__name__)

processed_data_path = "data/Processed_data/clean_processed_file.csv"


def balance_check(data:pd.Dataframe):
    data = pd.read_csv(data)
    result = (data.groupby("segment")[["history","newbie"]]
              .agg(["sum", "mean", "max", "min", "median", "std"]))
    return result




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    data = balance_check(processed_data_path)
    print(data)
    

