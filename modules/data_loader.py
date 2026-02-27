import pandas as pd

def load_transactions(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print("Error loading data:", e)
        return None