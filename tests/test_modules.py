import json
from unittest.mock import patch

from quiz_module import clean_json_block, generate_quiz
from summary_module import summarize_text
from qna import answer_question
from learning_path import get_learning_recommendations


def test_clean_json_block():
    raw = '```json\n[{"question":"Q"}]\n```'
    assert clean_json_block(raw) == '[{"question":"Q"}]'


def test_quiz_generation():
    payload = [
        {
            "question": "2 + 2 = ?",
            "options": ["1", "2", "3", "4"],
            "correct_answer": "4",
            "explanation": "Adding two and two gives four.",
        },
        {
            "question": "Capital of France?",
            "options": ["Paris", "Rome", "Delhi", "Tokyo"],
            "correct_answer": "Paris",
            "explanation": "Paris is the capital of France.",
        },
        {
            "question": "Sun is a?",
            "options": ["Planet", "Star", "Moon", "Comet"],
            "correct_answer": "Star",
            "explanation": "The Sun is a star.",
        },
    ]

    with patch("quiz_module.generate_json", return_value=json.dumps(payload)):
        result = generate_quiz("Basic general knowledge", 3)

    assert len(result) == 3
    assert result[0]["correct_answer"] == "4"


def test_text_modules_use_gemini_helper():
    with patch("qna.generate_text", return_value="answer"):
        assert answer_question("What is AI?") == "answer"

    with patch("summary_module.generate_text", return_value="summary"):
        assert summarize_text("Long text") == "summary"

    with patch("learning_path.generate_text", return_value="path"):
        assert get_learning_recommendations("SQL") == "path"
