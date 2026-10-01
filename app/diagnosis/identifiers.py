import pandas as pd

from app.diagnosis.schema import (
    Finding,
    FindingType,
    Severity,
)


def detect_suspicious_identifiers(
    dataframe: pd.DataFrame,
) -> list[Finding]:

    findings = []

    for column in dataframe.columns:

        series = dataframe[column]

        if len(series) == 0:
            continue

        unique_ratio = (
            series.nunique(dropna=False)
            / len(series)
        )

        column_lower = column.lower()

        name_suggests_identifier = (
            column_lower == "id"
            or column_lower.endswith("_id")
            or column_lower.endswith("id")
            or "identifier" in column_lower
            or "uuid" in column_lower
        )

        # A column is considered a suspicious identifier
        # only when BOTH conditions are true:
        #
        # 1. Every value is unique
        # 2. The column name strongly suggests an ID
        #
        # This prevents legitimate columns such as
        # age, income, or credit_score from being
        # incorrectly classified as identifiers.
        if (
            unique_ratio == 1.0
            and name_suggests_identifier
        ):
            findings.append(
                Finding(
                    type=FindingType.SUSPICIOUS_IDENTIFIER,
                    severity=Severity.WARNING,
                    title=(
                        f"Potential identifier column "
                        f"'{column}'"
                    ),
                    message=(
                        f"Column '{column}' appears to behave "
                        f"like an identifier. It has "
                        f"{unique_ratio:.2%} unique values."
                    ),
                    column=column,
                    evidence={
                        "unique_ratio": unique_ratio,
                        "unique_percentage": (
                            unique_ratio * 100
                        ),
                        "name_suggests_identifier": True,
                        "numeric": (
                            pd.api.types.is_numeric_dtype(
                                series
                            )
                        ),
                    },
                    recommendation=(
                        "Check whether this column identifies "
                        "individual records rather than "
                        "representing a meaningful predictive "
                        "feature. Identifier columns are often "
                        "excluded from model training."
                    ),
                )
            )

    return findings