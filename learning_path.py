from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are EduGenie, a personalized learning-path mentor.

Create a structured learning path for:
{topic}

Organize it from beginner to advanced.

Include:
1. Prerequisites.
2. Beginner topics.
3. Intermediate topics.
4. Advanced topics.
5. A suggested timeline.
6. Practice/project ideas.
7. Suggested resource types such as videos, articles, documentation, or books.
8. A simple weekly study routine.

Keep the plan realistic for a student and explain why each stage matters.
Do not invent specific links. Name reliable resource types or well-known
documentation/resource names only when you are confident.
"""
    return generate_text(prompt, max_output_tokens=1600)
