"""
ai_question_gen.py
------------------
Reads processed text from a file and uses OpenAI GPT
to generate JSON-formatted quiz questions.

Output format:
[
  {
    "question": "What is the color of the sky?",
    "choices": ["Blue", "Red", "Green", "Yellow"],
    "answer": "Blue",
    "difficulty": "easy"
  },
  ...
]
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env if available
load_dotenv()


def generate_questions_from_text(input_path: str, model: str = "gpt-4o-mini") -> list:
    """Read text from file, send to OpenAI, and return list of question dicts."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    prompt = f"""
You are a teacher creating quiz questions for learners.
Based on the provided study text, generate **exactly 30 multiple-choice questions** in JSON format.

Distribute them evenly:
- 10 questions labeled "easy"
- 10 questions labeled "medium"
- 10 questions labeled "hard"

Each question object must have:
- "question": a clear question string
- "choices": list of 4 answer options
- "answer": the correct choice string
- "difficulty": one of "easy", "medium", or "hard"

Ensure the JSON is valid and the list has exactly 30 items.

Return **only valid JSON**, no markdown, no commentary.

Study Text:
{text[:8000]}
"""

    print("🧠 Generating 30 quiz questions from text with OpenAI...")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You must return only valid JSON arrays of objects."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    content = response.choices[0].message.content.strip()

    # --- JSON Parse ---
    try:
        questions = json.loads(content)
        assert isinstance(questions, list)
    except Exception as e:
        print("⚠️ JSON parsing failed, raw output below:\n")
        print(content)
        raise e

    print(f"✅ Generated {len(questions)} questions from study text.")
    return questions
