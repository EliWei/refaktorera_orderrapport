import logging

from .config import INPUT_FILE, OUTPUT_FOLDER
from .loading import load_data
from .processing import clean_data, calculate_metrics
from .reporting import save_results


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

def main():
    logger.info("Startar orderrapport")
    try:
        data = load_data(INPUT_FILE)
        data = clean_data(data)
        overview, sales_by_category, sales_by_region, returns_by_category = calculate_metrics(data)
        save_results(overview, sales_by_category, sales_by_region, returns_by_category, OUTPUT_FOLDER)
        logger.info("Klart")

    # Fångar kända fel: fil saknas eller data är ogiltig.
    except FileNotFoundError as error:
        logger.error("Hittade inte filen: %s", error)
    except ValueError as error:
        logger.error("Fel i datan: %s", error)

if __name__ == "__main__":
    main()