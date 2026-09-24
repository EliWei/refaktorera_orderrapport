import os
import logging

logger = logging.getLogger(__name__)

def save_results(overview, sales_by_category, sales_by_region, returns_by_category, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    overview.to_csv(
                os.path.join(
                    output_folder,
                    "overview.csv",
                ),
                index=False,
            )
        
    logger.info("Sparade overview.csv")
    
    sales_by_category.to_csv(
                    os.path.join(
                        output_folder,
                        "sales_by_category.csv",
                    ),
                    index=False,
                )
    logger.info("Sparade sales_by_category.csv")
    
    sales_by_region.to_csv(
                os.path.join(
                    output_folder,
                    "sales_by_region.csv",
                ),
                index=False,
            )
        
    logger.info("Sparade sales_by_region.csv")
    
    returns_by_category.to_csv(
            os.path.join(
                output_folder,
                "returns_by_category.csv",
            ),
            index=False,
        )
    
    logger.info("Sparade returns_by_category.csv")
