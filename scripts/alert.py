import logging


def send_alert(errors):
    logging.warning("🚨 ALERT: Data Quality Issues Detected!")

    for err in errors:
        logging.warning(f"-> {err}")
