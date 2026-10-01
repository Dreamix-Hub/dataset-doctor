"""Class-imbalance diagnosis checks."""
import pandas as pd

from app.diagnosis.schema import (
    Finding,
    FindingType,
    Severity,
)


def detect_class_imbalance(
    dataframe: pd.DataFrame,
    target_column: str | None,
) -> list[Finding]:

    if not target_column:
        return []

    if target_column not in dataframe.columns:
        return []

    target = dataframe[target_column].dropna()

    if target.empty:
        return []

    unique_classes = target.nunique()

    if unique_classes < 2:
        return [
            Finding(
                type=FindingType.TARGET_ISSUE,
                severity=Severity.CRITICAL,
                title="Target has only one class",
                message=(
                    f"Target column '{target_column}' contains "
                    "only one unique class."
                ),
                column=target_column,
                evidence={
                    "unique_classes": unique_classes,
                },
                recommendation=(
                    "Verify that the correct target column "
                    "was selected and that the dataset contains "
                    "multiple target classes."
                ),
            )
        ]

    if unique_classes > 20:
        return []

    value_counts = target.value_counts()

    percentages = (
        target.value_counts(normalize=True) * 100
    )

    smallest_percentage = percentages.min()

    if smallest_percentage >= 20:
        return []

    if smallest_percentage < 5:
        severity = Severity.CRITICAL
    else:
        severity = Severity.WARNING

    distribution = {
        str(class_name): int(count)
        for class_name, count in value_counts.items()
    }

    percentage_distribution = {
        str(class_name): round(float(percentage), 2)
        for class_name, percentage
        in percentages.items()
    }

    return [
        Finding(
            type=FindingType.CLASS_IMBALANCE,
            severity=severity,
            title=f"Class imbalance in '{target_column}'",
            message=(
                f"The target column '{target_column}' has "
                f"{unique_classes} classes, but their frequencies "
                "are substantially uneven."
            ),
            column=target_column,
            evidence={
                "class_count": unique_classes,
                "distribution": distribution,
                "percentage_distribution": percentage_distribution,
                "smallest_class_percentage": round(
                    float(smallest_percentage),
                    2,
                ),
            },
            recommendation=(
                "Evaluate class distribution before training. "
                "Consider appropriate evaluation metrics and "
                "sampling strategies rather than relying only "
                "on accuracy."
            ),
        )
    ]