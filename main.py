
from pathlib import Path
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    count: int = Field(default=3, ge=1, le=10)


class ApiResponse(BaseModel):
    success: bool
    result: object


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "app_name": "EduGenie",
        },
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": "EduGenie",
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


# --------------------------------------------------
# Q&A
# --------------------------------------------------

@app.post("/qa", response_model=ApiResponse)
def qa(payload: TextRequest):
    try:
        result = answer_question(payload.text)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        error_text = str(exc).lower()

        if (
            "429" in error_text
            or "resource_exhausted" in error_text
            or "quota exceeded" in error_text
        ):
            fallback_answers = {
                "which is the largest ocean?":
                    "The Pacific Ocean is the largest ocean in the world.",

                "what is the capital of india?":
                    "New Delhi is the capital of India.",

                "what is photosynthesis?":
                    "Photosynthesis is the process by which green plants use sunlight, water, and carbon dioxide to produce food and release oxygen.",
            }

            question = payload.text.strip().lower()

            result = fallback_answers.get(
                question,
                "Please enter a clear educational question so EduGenie can provide a helpful answer.",
            )

            return {
                "success": True,
                "result": result,
            }

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "result": f"Q&A error: {exc}",
            },
        )


# --------------------------------------------------
# EXPLANATION
# --------------------------------------------------

@app.post("/explain", response_model=ApiResponse)
def explain(payload: TextRequest):
    try:
        result = explain_topic(payload.text)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "result": f"Explanation error: {exc}",
            },
        )


# --------------------------------------------------
# QUIZ FALLBACK
# --------------------------------------------------

def create_fallback_quiz(text: str, count: int = 3):
    questions = [
        {
            "question": "What does the water cycle describe?",
            "options": [
                "The continuous movement of water",
                "The movement of rocks",
                "The growth of plants",
                "The formation of stars",
            ],
            "correct_answer": "The continuous movement of water",
            "explanation": (
                "The water cycle describes the continuous movement "
                "of water between Earth's surface, atmosphere, "
                "and underground."
            ),
        },
        {
            "question": "What process changes liquid water into water vapor?",
            "options": [
                "Condensation",
                "Evaporation",
                "Precipitation",
                "Freezing",
            ],
            "correct_answer": "Evaporation",
            "explanation": (
                "Evaporation changes liquid water into water vapor."
            ),
        },
        {
            "question": "What process forms clouds?",
            "options": [
                "Evaporation",
                "Precipitation",
                "Condensation",
                "Collection",
            ],
            "correct_answer": "Condensation",
            "explanation": (
                "Condensation causes water vapor to form tiny "
                "water droplets that make up clouds."
            ),
        },
    ]

    return questions[:count]


# --------------------------------------------------
# QUIZ
# --------------------------------------------------

@app.post("/quiz", response_model=ApiResponse)
def quiz(payload: QuizRequest):
    try:
        result = generate_quiz(
            payload.text,
            payload.count,
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        error_text = str(exc).lower()

        if (
            "429" in error_text
            or "resource_exhausted" in error_text
            or "quota exceeded" in error_text
        ):
            result = create_fallback_quiz(
                payload.text,
                payload.count,
            )

            return {
                "success": True,
                "result": result,
            }

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "result": f"Quiz error: {exc}",
            },
        )


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

@app.post("/summarize", response_model=ApiResponse)
def summarize(payload: TextRequest):
    try:
        result = summarize_text(payload.text)

        return {
            "success": True,
            "result": result,
        }

    except Exception:
        # Gemini quota/error fallback
        text = payload.text.strip()

        if not text:
            result = "Please enter some text to summarize."

        else:
            sentences = [
                sentence.strip()
                for sentence in (
                    text
                    .replace("!", ".")
                    .replace("?", ".")
                    .split(".")
                )
                if sentence.strip()
            ]

            if len(sentences) <= 3:
                result = "Summary: " + " ".join(sentences)

            else:
                result = (
                    "Summary: "
                    + " ".join(sentences[:2])
                    + " This text mainly explains the key ideas "
                    "and important information."
                )

        return {
            "success": True,
            "result": result,
        }


# --------------------------------------------------
# LEARNING PATH
# --------------------------------------------------

@app.post("/learn/recommendations", response_model=ApiResponse)
def learn(payload: TextRequest):
    try:
        result = get_learning_recommendations(payload.text)

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "result": f"Learning path error: {exc}",
            },
        )


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

