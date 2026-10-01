import pandas as pd

from app.ai.schema import (
    AIAnalysis,
    FindingExplanation,
)
from app.ai.service import GemmaService
from app.diagnosis.engine import DiagnosisEngine


class FakeGemmaModel:

    def explain(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> FindingExplanation:

        return FindingExplanation(
            explanation=(
                "This finding may affect the quality "
                "of the dataset."
            ),
            action=(
                "Review the affected feature before "
                "training the model."
            ),
        )


def create_test_dataframe() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "customer_id": [
                1,
                2,
                3,
                4,
            ],
            "age": [
                20,
                25,
                None,
                30,
            ],
            "income": [
                30000,
                40000,
                50000,
                60000,
            ],
            "churn": [
                "yes",
                "no",
                "yes",
                "no",
            ],
        }
    )


def test_gemma_service():

    dataframe = create_test_dataframe()

    diagnosis = DiagnosisEngine(
        dataframe=dataframe,
        filename="test.csv",
        target_column="churn",
    ).diagnose()

    service = GemmaService(
        model=FakeGemmaModel()
    )

    result = service.analyze(
        diagnosis
    )

    assert isinstance(
        result,
        AIAnalysis,
    )

    assert result.summary

    assert isinstance(
        result.findings,
        list,
    )

    assert isinstance(
        result.next_steps,
        list,
    )

    for finding in result.findings:

        assert finding.type
        assert finding.title
        assert finding.severity
        assert finding.explanation
        assert finding.action