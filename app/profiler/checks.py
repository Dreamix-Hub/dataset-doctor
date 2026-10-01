"""Dataset quality checks."""

import pandas as pd


def calculate_missing_percentage(
    missing_count: int,
    total_count: int,
) -> float:
    """
    Calculate the percentage of missing values.
    """

    if total_count == 0:
        return 0.0

    return round((missing_count / total_count) * 100, 2)


def calculate_unique_percentage(
    unique_count: int,
    total_count: int,
) -> float:
    """
    Calculate the percentage of unique values.
    """

    if total_count == 0:
        return 0.0

    return round((unique_count / total_count) * 100, 2)


def is_constant_column(series: pd.Series) -> bool:
    """
    A column is constant when it contains
    only one unique value.
    """

    return series.nunique(dropna=False) <= 1


def is_high_cardinality(
    series: pd.Series,
    threshold: float = 0.90,
) -> bool:
    """
    Detect columns where at least 90% of
    non-missing values are unique.

    These columns may represent things such
    as IDs or other high-cardinality fields.
    """

    if len(series) == 0:
        return False

    non_missing = series.dropna()

    if len(non_missing) == 0:
        return False

    unique_ratio = non_missing.nunique() / len(non_missing)

    return unique_ratio >= threshold


def count_duplicate_rows(dataframe: pd.DataFrame) -> int:
    """
    Count completely duplicated rows.
    """

    return int(dataframe.duplicated().sum())


def calculate_duplicate_percentage(
    duplicate_count: int,
    total_rows: int,
) -> float:
    """
    Calculate the percentage of duplicate rows.
    """

    if total_rows == 0:
        return 0.0

    return round((duplicate_count / total_rows) * 100, 2)