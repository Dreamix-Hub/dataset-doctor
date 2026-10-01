"""Outlier diagnosis checks."""
import pandas as pd

from app.diagnosis.schema import (
    Finding,
    FindingType,
    Severity,
)


def detect_outliers(
    dataframe: pd.DataFrame,
) -> list[Finding]:
    findings: list[Finding] = []

    numerical_columns = dataframe.select_dtypes(
        include="number"
    ).columns

    for column in numerical_columns:

        series = dataframe[column].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outliers = series[
            (series < lower_bound)
            | (series > upper_bound)
        ]

        outlier_count = len(outliers)

        if outlier_count == 0:
            continue

        outlier_percentage = (
            outlier_count / len(series)
        ) * 100

        if outlier_percentage >= 10:
            severity = Severity.WARNING
        else:
            severity = Severity.INFO

        findings.append(
            Finding(
                type=FindingType.OUTLIERS,
                severity=severity,
                title=f"Potential outliers in '{column}'",
                message=(
                    f"'{column}' contains approximately "
                    f"{outlier_count} potential outliers "
                    f"({outlier_percentage:.2f}% of "
                    f"non-missing values) using the IQR method."
                ),
                column=column,
                evidence={
                    "outlier_count": outlier_count,
                    "outlier_percentage": round(
                        outlier_percentage,
                        2,
                    ),
                    "q1": round(float(q1), 4),
                    "q3": round(float(q3), 4),
                    "iqr": round(float(iqr), 4),
                    "lower_bound": round(
                        float(lower_bound),
                        4,
                    ),
                    "upper_bound": round(
                        float(upper_bound),
                        4,
                    ),
                },
                recommendation=(
                    "Investigate these observations before "
                    "removing them. Extreme values may be "
                    "valid observations rather than errors."
                ),
            )
        )

    return findings