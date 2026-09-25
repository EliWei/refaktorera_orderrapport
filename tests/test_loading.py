import pytest

from order_report.validation import validate_columns
import pandas as pd

# Testar felscenario, saknade kolumner, direkt mot validate_columns

def test_validate_columns_raises_valueerror_when_column_missing():
    # Data som saknar flera obligatoriska kolumner
    data = pd.DataFrame({"order_id": [1]})
    required = {"order_id", "region", "quantity"}

    # Vi förväntar oss att funktionen get ValueError,
    # inte ett generellt Exception
    with pytest.raises(ValueError):
        validate_columns(data, required)