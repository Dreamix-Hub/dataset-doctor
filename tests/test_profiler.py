"""Tests for the dataset profiler."""
import pandas as pd

from app.profiler.profiler import DatasetProfiler


def create_test_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "age": [20, 25, 30, None, 25],
            "salary": [
                30000,
                40000,
                50000,
                60000,
                40000,
            ],
            "department": [
                "IT",
                "HR",
                "IT",
                "Finance",
                "HR",
            ],
        }
    )


def test_dataset_dimensions():
    dataframe = create_test_dataframe()

    profiler = DatasetProfiler(dataframe)

    result = profiler.profile()

    assert result.rows == 5
    assert result.columns == 3


def test_missing_values():
    dataframe = create_test_dataframe()

    profiler = DatasetProfiler(dataframe)

    result = profiler.profile()

    age_column = next(
        column
        for column in result.column_profiles
        if column.name == "age"
    )

    assert age_column.missing_values == 1
    assert age_column.missing_percentage == 20.0


def test_duplicate_rows():
    dataframe = create_test_dataframe()

    profiler = DatasetProfiler(dataframe)

    result = profiler.profile()

    assert result.duplicate_rows == 1


def test_column_types():
    dataframe = create_test_dataframe()

    profiler = DatasetProfiler(dataframe)

    result = profiler.profile()

    assert "age" in result.numerical_columns
    assert "salary" in result.numerical_columns
    assert "department" in result.categorical_columns