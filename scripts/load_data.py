import pandas as pd
import os

def load_data():
    try:
        base_path = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "data/raw/olist_customers_dataset.csv")

        df = pd.read_csv(file_path)
        print("Data loaded successfully")
        print(df.head())
        return df

    except Exception as e:
        print("Error loading data:", e)

if __name__ == "__main__":
    load_data()