import pandas as pd

from order_report.processing import summarise_by

# Liten, manuell testdata f;r snabbt test
def test_summarise_by_groups_and_calculates_return_rate():
    data = pd.DataFrame({
        "order_id": [1, 2, 3, 4],
        "product_category": ["A", "A", "B", "B"],
        "discounted_value": [100.0, 200.0, 50.0, 50.0],
        "returned": [True, False, False, False],
    })

    result = summarise_by(data, "product_category")

    # Kategori A: två ordrar (1 och 2) blir totalt 100 + 200 = 300
    # och 1 av 2 ordrar returnerad -> return_rate 0.5.

    row_a = result[result["product_category"] == "A"].iloc[0]
    assert row_a["order_count"] == 2
    assert row_a["total_sales"] == 300.0
    assert row_a["return_rate"] == 0.5