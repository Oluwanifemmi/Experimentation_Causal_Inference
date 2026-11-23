import logging 
import pandas as pd

logger = logging.getLogger(__name__)


data_path = "data/Processed_data/clean_processed_file.csv"

def difference_naive(data_path :str):
    data = pd.read_csv(data_path) 
    #average outcome per segment
    means = data.groupby("segment")[["spend", "conversion", "visit"]].mean()

    #naive difference = treatment mean - control mean
    control = means.loc["No E-Mail"]
    naive_mens = means.loc["Mens E-Mail"] - control
    naive_womens = means.loc["Womens E-Mail"] - control
    return naive_mens , naive_womens




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    naive_mens , naive_womens = difference_naive(data_path)
    print(f"The men: {naive_mens}")
    print(f"The woman: {naive_womens}")