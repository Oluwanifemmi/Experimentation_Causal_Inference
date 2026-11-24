import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import argparse
import matplotlib
matplotlib.use("Agg") 
import os 



logger = logging.getLogger(__name__)

data_path = data_path = "data/Processed_data/clean_processed_file.csv"


NUMERIC = ["recency", "history", "spend"]
BINARY = ["visit", "conversion", "newbie", "mens", "womens"]
CATEGORICAL = ["segment", "zip_code", "channel", "history_segment"]
SEGMENT_ORDER = ["No E-Mail", "Mens E-Mail", "Womens E-Mail"]


def descriptive_analysis(datapath:str):
    df = pd.read_csv(datapath)
    num_cols = [c for c in NUMERIC if c in df.columns]
    bin_cols = [c for c in BINARY if c in df.columns]
    cat_cols = [c for c in CATEGORICAL if c in df.columns]
    data_describe = df[num_cols].describe(percentiles=[0.25, 0.5, 0.75, 0.95, 0.99]).round(2)
    data_skewness = df[num_cols].skew().round(2)
    data_binary_variable = df[bin_cols].mean().round(4)
    rows = []
    for c in num_cols:
        s = df[c].dropna()
        if c == "spend":
            s = s[s > 0]
            label = "spend (buyers only)"
        else:
            label = c
        low, high, n_out = iqr_outliers(s)
        rows.append({
            "variable": label, "n": len(s), "lower_fence": round(low, 2),
            "upper_fence": round(high, 2), "n_outliers": n_out,
            "outlier_%": round(n_out / len(s) * 100, 2), "max": round(s.max(), 2),
        })
    outlier_variables = pd.DataFrame(rows).to_string(index=False)

    return  outlier_variables, data_skewness, data_binary_variable, data_describe




def iqr_outliers(s):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_out = ((s < low) | (s > high)).sum()
    return low, high, n_out


def data_plot(datapath):
# Load data and make a folder for the graphs
    df = pd.read_csv(datapath).drop_duplicates()
    os.makedirs("figures", exist_ok=True)

    # 1. History and recency: raw vs log scale
    for col in ["history", "recency"]:
        plt.figure(figsize=(10, 4))

        plt.subplot(1, 2, 1)
        plt.hist(df[col], bins=50)
        plt.title(col)

        plt.subplot(1, 2, 2)
        plt.hist(np.log1p(df[col]), bins=50)
        plt.title(col + " (log scale)")

        plt.savefig("figures/" + col + "_distribution.png")
        plt.close()


    # 2. Spend: most customers spent 0, so also plot buyers only
    zero_share = (df["spend"] == 0).mean() * 100
    print("Customers with zero spend:", round(zero_share, 2), "%")

    buyers = df[df["spend"] > 0]

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.hist(df["spend"], bins=50)
    plt.title("Spend: all customers")

    plt.subplot(1, 2, 2)
    plt.hist(buyers["spend"], bins=40)
    plt.title("Spend: buyers only")

    plt.savefig("figures/spend_distribution.png")
    plt.close()


    # 3. Counts for binary and categorical columns
    for col in ["visit", "conversion", "newbie", "zip_code", "channel", "segment"]:
        df[col].value_counts().plot(kind="bar", title=col)
        plt.tight_layout()
        plt.savefig("figures/" + col + "_counts.png")
        plt.close()


    # 4. Boxplots by experiment group
    for col in ["history", "recency"]:
        df.boxplot(column=col, by="segment")
        plt.suptitle("")
        plt.title(col + " by group")
        plt.savefig("figures/" + col + "_boxplot.png")
        plt.close()

    buyers.boxplot(column="spend", by="segment")
    plt.suptitle("")
    plt.title("Spend by group (buyers only)")
    plt.savefig("figures/spend_boxplot.png")
    plt.close()


    # 5. Correlation heatmap
    cols = ["recency", "history", "spend", "visit", "conversion"]
    corr = df[cols].corr()
    print(corr.round(3))

    plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar()
    plt.xticks(range(len(cols)), cols, rotation=45)
    plt.yticks(range(len(cols)), cols)
    plt.title("Correlation matrix")
    plt.tight_layout()
    plt.savefig("figures/correlation_heatmap.png")
    plt.close()

    print("Graphs saved in the figures folder")





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    outlier_variables, data_skewness, data_binary_variable, data_describe = descriptive_analysis(data_path)
    print(f"outlier variable: {outlier_variables}")
    print(f"data skewness: {data_skewness}")
    print(f"Binary Variable: {data_binary_variable}")
    print(f"data describe : {data_describe}")
    data_plotly = data_plot(data_path)
    print(data_plotly)