import os

from gemini_client import generate_text

LOCAL_MODEL = os.getenv("LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M")


def _local_explain(topic: str) -> str:
    # Imported only when local mode is enabled so the normal installation
    # remains lightweight.
    from transformers import pipeline

    generator = pipeline(
        "text2text-generation",
        model=LOCAL_MODEL,
        tokenizer=LOCAL_MODEL,
        device=-1,
    )
    prompt = (
        "Explain the following topic to a beginner. "
        "Use simple language, one small example, and key points.\n\n"
        f"Topic: {topic}"
    )
    result = generator(prompt, max_new_tokens=300, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    if os.getenv("USE_LOCAL_EXPLANATION", "false").lower() == "true":
        try:
            return _local_explain(topic)
        except Exception as exc:
            # A cloud fallback keeps the application usable if the local
            # model is not installed or cannot run on the current machine.
            fallback_note = (
                f"The local explanation model could not be loaded ({exc}). "
                "Using Gemini instead.\n\n"
            )
            return fallback_note + _gemini_explain(topic)

    return _gemini_explain(topic)


def _gemini_explain(topic: str) -> str:
    prompt = f"""
You are EduGenie, an educational tutor.

Explain this topic to a beginner:
{topic}

Requirements:
1. Start with a simple definition.
2. Explain the idea step by step.
3. Give one easy example.
4. End with 3 key points to remember.
5. Keep the language clear and not overly technical.
"""
    return generate_text(prompt, max_output_tokens=1200)
