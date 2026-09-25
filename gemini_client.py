import os
import time
from functools import lru_cache

from google import genai
from google.genai import types


class GeminiConfigurationError(RuntimeError):
    """Raised when the Gemini API key is not configured."""


@lru_cache(maxsize=1)
def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is missing. Add it to the .env file."
        )
    return genai.Client(api_key=api_key)


def get_model_name() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

def generate_text(prompt: str, *, max_output_tokens: int = 1500) -> str:
    client = get_client()

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=get_model_name(),
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_output_tokens,
                ),
            )

            text = response.text
            if not text:
                raise RuntimeError("Gemini returned an empty response.")

            return text.strip()

        except Exception as exc:
            error_text = str(exc)
            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                raise RuntimeError(
                    "Gemini API quota exceeded. Please try again later."
            ) from exc

            if "503" not in error_text and "UNAVAILABLE" not in error_text:
                raise

            if attempt == 2:
                raise

            time.sleep(2 ** attempt)


def generate_json(prompt: str, schema: dict, *, max_output_tokens: int = 1600) -> str:
    client = get_client()

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=get_model_name(),
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_output_tokens,
                    response_mime_type="application/json",
                    response_schema=schema,
                ),
            )

            text = response.text
            if not text:
                raise RuntimeError("Gemini returned an empty JSON response.")

            return text.strip()

        except Exception as exc:
            error_text = str(exc)

            if "503" not in error_text and "UNAVAILABLE" not in error_text:
                raise

            if attempt == 2:
                raise

            time.sleep(2 ** attempt)