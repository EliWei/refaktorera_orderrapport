import os
import pandas as pd

INPUT_FILE = "data/orders.csv"
OUTPUT_FOLDER = "output"

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

    if not required.issubset(data.columns):
        raise Exception("Fel data")

    print("Läste in", len(data), "rader")

    return data

# region, product_category, quantity, unit_price, discount, returned
def clean_data(data):
    data["region"] = data["region"].fillna("Unknown").astype(str).str.strip().str.title()
    data["product_category"] = (
        data["product_category"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )
    
    data["quantity"] = pd.to_numeric(
            data["quantity"], errors="coerce"
        ).fillna(1)
    
    data["unit_price"] = pd.to_numeric(
            data["unit_price"], errors="coerce"
        )
    data["unit_price"] = data["unit_price"].fillna(
            data["unit_price"].median()
        )
    
    data["discount"] = pd.to_numeric(
            data["discount"], errors="coerce"
        ).fillna(0)
    
    data["returned"] = (
            data["returned"]
            .fillna("false")
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["true", "yes", "1", "ja"])
        )
    
    return data

def summarise_by(data, column):
    summary = (
            data.groupby(
                column,
                as_index=False,
            )
            .agg(
                order_count=("order_id", "nunique"),
                total_sales=("discounted_value", "sum"),
                returns=("returned", "sum"),
            )
        )
    summary["total_sales"] = summary["total_sales"].round(2)

    summary["return_rate"] = (summary["returns"] / summary["order_count"]).round(3)

    summary = (summary.sort_values("total_sales", ascending=False).reset_index(drop=True))

    return summary
               


# order_value, discounted_value, overview, sales_by_category, sales_by_region, returns_by_category
def calculate_metrics(data):
    data["order_value"] = (
            data["quantity"] * data["unit_price"]
        )
    
    data["discounted_value"] = (
            data["order_value"] * (1 - data["discount"])
        )
    
    total_sales = round(
            data["discounted_value"].sum(),
            2,
        )
    
    number_of_orders = data["order_id"].nunique()
    number_of_returns = int(data["returned"].sum())
    
    overview = pd.DataFrame(
            {
                "metric": [
                    "total_sales",
                    "order_count",
                    "return_count",
                ],
                "value": [
                    total_sales,
                    number_of_orders,
                    number_of_returns,
                ],
            }
        )

    sales_by_category = summarise_by(data, "product_category")
    sales_by_region = summarise_by(data, "region")

    #återanvänder sales_by_category och väljer ut kolumnerna som behövs för returns_by_category
    returns_by_category = (
        sales_by_category[["product_category", "order_count", "returns", "return_rate"]]
        .sort_values("return_rate", ascending=False)
        .reset_index(drop=True)
    )
    
    return overview, sales_by_category, sales_by_region, returns_by_category

def save_results(overview, sales_by_category, sales_by_region, returns_by_category, output_folder):
    overview.to_csv(
                os.path.join(
                    output_folder,
                    "overview.csv",
                ),
                index=False,
            )
        
    print("Sparade overview.csv")
    
    sales_by_category.to_csv(
                    os.path.join(
                        output_folder,
                        "sales_by_category.csv",
                    ),
                    index=False,
                )
    print("Sparade sales_by_category.csv")
    
    sales_by_region.to_csv(
                os.path.join(
                    output_folder,
                    "sales_by_region.csv",
                ),
                index=False,
            )
        
    print("Sparade sales_by_region.csv")
    
    returns_by_category.to_csv(
            os.path.join(
                output_folder,
                "returns_by_category.csv",
            ),
            index=False,
        )
    
    print("Sparade returns_by_category.csv")

def main():
    print("Startar orderrapport")
    try:
        data = load_data(INPUT_FILE)
        data = clean_data(data)
        overview, sales_by_category, sales_by_region, returns_by_category = calculate_metrics(data)
        save_results(overview, sales_by_category, sales_by_region, returns_by_category, OUTPUT_FOLDER)
        print("Klart")
    except Exception as error:
        print("Något gick fel:", error)

if __name__ == "__main__":
    main()


    
  

