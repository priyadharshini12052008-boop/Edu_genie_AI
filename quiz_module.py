import json
import re

from gemini_client import generate_json


QUIZ_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "question": {"type": "string"},
            "options": {
                "type": "array",
                "items": {"type": "string"},
            },
            "correct_answer": {"type": "string"},
            "explanation": {"type": "string"},
        },
        "required": [
            "question",
            "options",
            "correct_answer",
            "explanation",
        ],
    },
}


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _validate_quiz(data, count: int):
    if not isinstance(data, list):
        raise ValueError("Quiz response is not a list.")

    if len(data) != count:
        raise ValueError(f"Expected {count} questions, received {len(data)}.")

    cleaned = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Question {index} is not an object.")

        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        correct = str(item.get("correct_answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Question {index} must have exactly 4 options.")
        if correct not in options:
            raise ValueError(
                f"Question {index} has a correct answer not present in options."
            )

        cleaned.append(
            {
                "question": question,
                "options": [str(option).strip() for option in options],
                "correct_answer": correct,
                "explanation": explanation,
            }
        )

    return cleaned


def generate_quiz(text: str, count: int = 3):
    prompt = f"""
Create exactly {count} multiple-choice questions from the educational text below.

Rules:
- Each question must have exactly four options.
- Only one option is correct.
- The correct_answer field must exactly match one option.
- Include a short explanation for the correct answer.
- Questions must be answerable from the supplied text/topic.
- Return only the requested JSON structure.

Educational text/topic:
{text}
"""
    raw = generate_json(prompt, QUIZ_SCHEMA, max_output_tokens=1800)
    data = json.loads(clean_json_block(raw))
    return _validate_quiz(data, count)
