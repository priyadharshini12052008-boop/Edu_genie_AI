from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qa_endpoint():
    with patch("main.answer_question", return_value="AI is a field of computer science."):
        response = client.post("/qa", json={"text": "What is AI?"})

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "AI" in response.json()["result"]


def test_quiz_endpoint():
    quiz = [
        {
            "question": "2 + 2?",
            "options": ["1", "2", "3", "4"],
            "correct_answer": "4",
            "explanation": "2 + 2 is 4.",
        }
    ]

    with patch("main.generate_quiz", return_value=quiz):
        response = client.post(
            "/quiz",
            json={"text": "Addition", "count": 1},
        )

    assert response.status_code == 200
    assert response.json()["result"][0]["correct_answer"] == "4"
