from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following passage for a student.

Requirements:
- Preserve the important facts and ideas.
- Remove repetition and unnecessary detail.
- Use simple language.
- Use a short heading and bullet points when appropriate.
- Do not add information that is not supported by the passage.

Passage:
{text}
"""
    return generate_text(prompt, max_output_tokens=1000)
