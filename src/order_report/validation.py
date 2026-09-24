def validate_columns(data, required):
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Saknade kolumner: {sorted(missing)}")
    