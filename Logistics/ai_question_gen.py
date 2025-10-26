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
load_dotenv()


def generate_questions_from_text(input_path: str, model: str = "gpt-4o-mini") -> list:
    """Read text from file, send to OpenAI, and return list of question dicts."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    prompt = f"""
You are a teacher creating study quiz questions for young learners.
Create 6 multiple-choice questions based on the following study text.
Each question should have:
- "question" (string)
- "choices" (list of 4 options)
- "answer" (string)
- "difficulty" (easy, medium, or hard)
Return only valid JSON — no explanations or markdown.

Study Text:
{text[:6000]}
"""

    print("🧠 Generating questions from text with OpenAI...")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You return only valid JSON arrays."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    content = response.choices[0].message.content.strip()

    # Try to parse JSON safely
    try:
        questions = json.loads(content)
        assert isinstance(questions, list)
    except Exception as e:
        print("⚠️ JSON parsing failed. Raw output below:")
        print(content)
        raise e

    print(f"✅ Generated {len(questions)} questions from study text.")
    return questions
