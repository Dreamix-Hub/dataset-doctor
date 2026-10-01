import os
from pathlib import Path

from dotenv import load_dotenv

from google import genai
from google.genai import types

from app.ai.schema import FindingExplanation


load_dotenv(
    Path(__file__).resolve().parents[2] / ".env"
)


class GemmaModel:
    """
    Client for communicating with Gemma through
    the Gemini API.
    """

    def __init__(
        self,
        api_key: str | None = None,
    ):
        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
        )

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.model_id = os.getenv(
            "GEMMA_MODEL_ID",
            "gemma-4-26b-a4b-it",
        )

        self.max_output_tokens = int(
            os.getenv(
                "GEMMA_MAX_OUTPUT_TOKENS",
                "200",
            )
        )

        self.temperature = float(
            os.getenv(
                "GEMMA_TEMPERATURE",
                "0.1",
            )
        )

        self.client = genai.Client(
            api_key=self.api_key,
        )

    def explain(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> FindingExplanation:

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
                response_mime_type="application/json",
                response_schema=FindingExplanation,
            ),
        )

        if response.parsed is not None:
            return response.parsed

        if response.text:
            try:
                return FindingExplanation.model_validate_json(
                    response.text
                )
            except Exception as exc:
                raise ValueError(
                    "Gemma returned invalid JSON."
                ) from exc

        raise ValueError(
            "Gemma returned no usable response."
        )