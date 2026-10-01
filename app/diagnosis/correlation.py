"""Correlation diagnosis checks."""
import pandas as pd

from app.diagnosis.schema import (
    Finding,
    FindingType,
    Severity,
)


def detect_high_correlations(
    dataframe: pd.DataFrame,
    threshold: float = 0.90,
) -> list[Finding]:

    numerical_data = dataframe.select_dtypes(
        include="number"
    )

    if numerical_data.shape[1] < 2:
        return []

    correlation_matrix = numerical_data.corr()

    findings: list[Finding] = []

    columns = correlation_matrix.columns

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):

            column_a = columns[i]
            column_b = columns[j]

            correlation = correlation_matrix.loc[
                column_a,
                column_b,
            ]

            if pd.isna(correlation):
                continue

            if abs(correlation) < threshold:
                continue

            findings.append(
                Finding(
                    type=FindingType.HIGH_CORRELATION,
                    severity=Severity.WARNING,
                    title=(
                        f"High correlation between "
                        f"'{column_a}' and '{column_b}'"
                    ),
                    message=(
                        f"'{column_a}' and '{column_b}' have "
                        f"a correlation of "
                        f"{correlation:.3f}."
                    ),
                    columns=[
                        column_a,
                        column_b,
                    ],
                    evidence={
                        "correlation": round(
                            float(correlation),
                            4,
                        ),
                        "absolute_correlation": round(
                            abs(float(correlation)),
                            4,
                        ),
                        "threshold": threshold,
                    },
                    recommendation=(
                        "Investigate whether both features "
                        "provide distinct information. Highly "
                        "correlated features may introduce "
                        "redundancy for some models."
                    ),
                )
            )

    return findings