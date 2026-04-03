import pandas as pd
import os
import shutil
from logger import setup_logger, log_errors
from alert import send_alert
import logging


def get_paths():
    base_path = os.path.dirname(os.path.dirname(__file__))

    return {
        "raw": os.path.join(base_path, "data/raw/olist_customers_dataset.csv"),
        "validated": os.path.join(base_path, "data/validated/clean_customers.csv"),
        "quarantine": os.path.join(base_path, "data/quarantine/olist_customers_dataset.csv"),
    }


def load_data(file_path):
    try:
        df = pd.read_csv(file_path, dtype={"customer_zip_code_prefix": str})
        logging.info("✅ Data loaded successfully")
        return df
    except Exception as e:
        logging.error(f"❌ Error loading data: {e}")
        return None


def validate_data(df):
    errors = []

    logging.info(f"📊 Total records: {len(df)}")

    if df['customer_id'].isnull().sum() > 0:
        errors.append("customer_id contains null values")

    if df['customer_unique_id'].isnull().sum() > 0:
        errors.append("customer_unique_id contains null values")

    if df['customer_id'].duplicated().sum() > 0:
        errors.append("customer_id contains duplicates")

    if df['customer_zip_code_prefix'].isnull().sum() > 0:
        errors.append("zip code contains null values")

    invalid_zip = df['customer_zip_code_prefix'].dropna().apply(lambda x: not str(x).isdigit()).sum()
    if invalid_zip > 0:
        errors.append("zip code contains non-numeric values")

    invalid_states = df['customer_state'].dropna().apply(lambda x: len(str(x)) != 2).sum()
    if invalid_states > 0:
        errors.append("invalid state codes found")

    return errors


def clean_data(df):
    logging.info("🧹 Cleaning data...")

    df = df.dropna(subset=[
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix"
    ])

    df = df.drop_duplicates(subset=["customer_id"])

    df["customer_zip_code_prefix"] = df["customer_zip_code_prefix"].astype(str)

    df = df[df["customer_zip_code_prefix"].str.isdigit()]

    df = df[df["customer_state"].astype(str).str.len() == 2]

    logging.info(f"✅ Records after cleaning: {len(df)}")

    return df


def save_clean_data(df, path):
    df.to_csv(path, index=False)
    logging.info(f"✅ Clean data saved to: {path}")


def move_file(source, destination):
    shutil.move(source, destination)
    logging.info(f"📁 File moved to: {destination}")


if __name__ == "__main__":
    setup_logger()

    paths = get_paths()

    df = load_data(paths["raw"])

    if df is None:
        exit()

    errors = validate_data(df)

    if errors:
        logging.error("❌ Initial Validation FAILED")
        log_errors(errors)

        df = clean_data(df)

        logging.info("🔁 Re-validating cleaned data...")
        errors = validate_data(df)

        if errors:
            logging.error("❌ Still failing after cleaning")
            send_alert(errors)
            move_file(paths["raw"], paths["quarantine"])
            exit()

    logging.info("✅ Data cleaned and validated successfully")
    save_clean_data(df, paths["validated"])