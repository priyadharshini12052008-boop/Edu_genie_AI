from gemini_client import generate_text

SYSTEM_STYLE = """
You are EduGenie, a friendly educational assistant.
Answer for a student in clear, accurate language.
Prefer concise explanations, short paragraphs, and bullet points when useful.
If the question is ambiguous, state the reasonable interpretation you are using.
Do not pretend to know facts you are uncertain about.
"""

def answer_question(question: str) -> str:
    prompt = f"""
{SYSTEM_STYLE}

Student question:
{question}

Give a direct answer first, then a short explanation if needed.
"""
    return generate_text(prompt, max_output_tokens=1000)
