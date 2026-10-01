"""Shared application helpers."""
import numpy as np
import pandas as pd


def round_float(
    value: float,
    digits: int = 2,
) -> float:
    """
    Safely round a numerical value.
    """

    if pd.isna(value):
        return 0.0

    return round(float(value), digits)


def infer_column_type(series: pd.Series) -> str:
    """
    Infer a human-friendly column type.
    """

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "numerical"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    return "categorical"


def safe_json_value(value):
    """
    Convert NumPy/Pandas values into
    JSON-compatible Python values.
    """

    if pd.isna(value):
        return None

    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        return float(value)

    if isinstance(value, np.bool_):
        return bool(value)

    return value