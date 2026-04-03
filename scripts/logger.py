import logging
import os


def setup_logger():
    base_path = os.path.dirname(os.path.dirname(__file__))
    log_path = os.path.join(base_path, "logs")

    os.makedirs(log_path, exist_ok=True)

    log_file = os.path.join(log_path, "data_quality.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def log_errors(errors):
    for err in errors:
        logging.error(err)