import pandas as pd
import logging 

logger = logging.getLogger(__name__)


data_path = pd.read_csv("data/raw_data/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv")
processed_path = "data/Processed_data/clean_processed_file.csv"

def data_preprocessing(data:pd.DataFrame):
    #drop duplicates
    newdata = data.drop_duplicates()
    #trim the first two character
    newdata['history_segment'] = newdata['history_segment'].map(lambda x: str(x)[2:])
    newdata['recency'] = str(newdata['recency'])
    return newdata


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    data = data_preprocessing(data_path)
    print(data.sample(5))
    data.to_csv(processed_path, index=False)