import pandas as pd

def parse_csv(file_path):
    df = pd.read_csv(file_path)

    # Basic cleaning
    df["amount"] = df["amount"].astype(float)
    df["category"] = df["category"].astype(str)
    df["merchant"] = df["merchant"].astype(str)

    return df