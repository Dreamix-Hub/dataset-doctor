"""Dataset profiling logic."""
import pandas as pd

from app.profiler.checks import (
    calculate_duplicate_percentage,
    calculate_missing_percentage,
    calculate_unique_percentage,
    count_duplicate_rows,
    is_constant_column,
    is_high_cardinality,
)
from app.profiler.schema import ColumnProfile, DatasetProfile
from app.utils.helpers import infer_column_type, round_float


class DatasetProfiler:
    """
    Performs basic dataset profiling.

    Phase 1 checks:

    - Dataset dimensions
    - Column data types
    - Missing values
    - Unique values
    - Constant columns
    - High-cardinality columns
    - Duplicate rows
    - Basic numerical statistics
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        filename: str = "dataset.csv",
    ):
        self.dataframe = dataframe
        self.filename = filename

    def profile(self) -> DatasetProfile:
        """
        Generate a complete dataset profile.
        """

        rows = len(self.dataframe)
        column_count = len(self.dataframe.columns)

        numerical_columns: list[str] = []
        categorical_columns: list[str] = []
        datetime_columns: list[str] = []

        column_profiles: list[ColumnProfile] = []

        for column in self.dataframe.columns:
            series = self.dataframe[column]

            inferred_type = infer_column_type(series)

            if inferred_type == "numerical":
                numerical_columns.append(column)

            elif inferred_type == "categorical":
                categorical_columns.append(column)

            elif inferred_type == "datetime":
                datetime_columns.append(column)

            column_profile = self._profile_column(
                column=column,
                series=series,
            )

            column_profiles.append(column_profile)

        duplicate_rows = count_duplicate_rows(
            self.dataframe
        )

        duplicate_percentage = calculate_duplicate_percentage(
            duplicate_count=duplicate_rows,
            total_rows=rows,
        )

        warnings = self._generate_warnings(
            duplicate_rows=duplicate_rows,
            duplicate_percentage=duplicate_percentage,
            column_profiles=column_profiles,
        )

        memory_usage_mb = (
            self.dataframe.memory_usage(deep=True).sum()
            / (1024 * 1024)
        )

        return DatasetProfile(
            filename=self.filename,
            rows=rows,
            columns=column_count,
            memory_usage_mb=round_float(
                memory_usage_mb,
                4,
            ),
            numerical_columns=numerical_columns,
            categorical_columns=categorical_columns,
            datetime_columns=datetime_columns,
            duplicate_rows=duplicate_rows,
            duplicate_percentage=duplicate_percentage,
            column_profiles=column_profiles,
            warnings=warnings,
        )

    def _profile_column(
        self,
        column: str,
        series: pd.Series,
    ) -> ColumnProfile:
        """
        Generate a profile for one column.
        """

        total_values = len(series)

        missing_values = int(
            series.isna().sum()
        )

        missing_percentage = calculate_missing_percentage(
            missing_count=missing_values,
            total_count=total_values,
        )

        unique_values = int(
            series.nunique(dropna=True)
        )

        unique_percentage = calculate_unique_percentage(
            unique_count=unique_values,
            total_count=total_values,
        )

        constant = is_constant_column(series)

        high_cardinality = is_high_cardinality(series)

        statistics = self._calculate_statistics(
            series=series,
        )

        return ColumnProfile(
            name=column,
            data_type=str(series.dtype),
            inferred_type=infer_column_type(series),
            total_values=total_values,
            missing_values=missing_values,
            missing_percentage=missing_percentage,
            unique_values=unique_values,
            unique_percentage=unique_percentage,
            is_constant=constant,
            is_high_cardinality=high_cardinality,
            statistics=statistics,
        )

    def _calculate_statistics(
        self,
        series: pd.Series,
    ) -> dict:
        """
        Calculate basic statistics for numerical columns.
        """

        if not pd.api.types.is_numeric_dtype(series):
            return {}

        clean_series = series.dropna()

        if clean_series.empty:
            return {}

        return {
            "mean": round_float(
                clean_series.mean()
            ),
            "median": round_float(
                clean_series.median()
            ),
            "std": round_float(
                clean_series.std()
            ),
            "min": round_float(
                clean_series.min()
            ),
            "max": round_float(
                clean_series.max()
            ),
            "q1": round_float(
                clean_series.quantile(0.25)
            ),
            "q3": round_float(
                clean_series.quantile(0.75)
            ),
        }

    def _generate_warnings(
        self,
        duplicate_rows: int,
        duplicate_percentage: float,
        column_profiles: list[ColumnProfile],
    ) -> list[str]:
        """
        Generate simple human-readable warnings.
        """

        warnings: list[str] = []

        if duplicate_rows > 0:
            warnings.append(
                f"Dataset contains {duplicate_rows} "
                f"duplicate rows "
                f"({duplicate_percentage}% of all rows)."
            )

        for column in column_profiles:

            if column.missing_percentage > 0:
                warnings.append(
                    f"Column '{column.name}' contains "
                    f"{column.missing_values} missing values "
                    f"({column.missing_percentage}%)."
                )

            if column.is_constant:
                warnings.append(
                    f"Column '{column.name}' is constant "
                    f"and contains only one unique value."
                )

            if column.is_high_cardinality:
                warnings.append(
                    f"Column '{column.name}' has high "
                    f"cardinality "
                    f"({column.unique_percentage}% unique values)."
                )

        return warnings