import pandas as pd
import logging

logger = logging.getLogger(__name__)

from .validation import validate_columns

# read_csv
def load_data(file_path):
   
    data = pd.read_csv(file_path)

    required = {
        "order_id",
        "order_date",
        "customer_id",
        "region",
        "product_category",
        "quantity",
        "unit_price",
        "discount",
        "returned",
    }

    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Saknade kolumner: {sorted(missing)}")

    logger.info("Läste in %d rader", len(data))

    return data