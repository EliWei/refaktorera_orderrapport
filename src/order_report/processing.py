import pandas as pd

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
