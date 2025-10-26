"""
upload_manager.py
-----------------
Handles file upload, text extraction, and LLM-based question generation.
Outputs both a generated JSON file and a simple status message.
"""

import os
import json
from Logistics.file_loader import save_extracted_text
from Logistics.ai_question_gen import generate_questions_from_text


def handle_file_upload(file_path: str, sidebar) -> str:
    """
    Extracts text, generates questions via LLM, saves JSON next to main.py,
    and updates the game's sidebar question list.

    Args:
        file_path (str): Path to the uploaded file.
        sidebar: Sidebar instance for question storage.

    Returns:
        str: Status message for UI display.
    """
    if not os.path.exists(file_path):
        return "⚠️ Invalid path or file not found."

    try:
        # 1️⃣ Extract and save processed text
        uploaded_file_path = save_extracted_text(file_path)
        print(f"✅ Uploaded and processed file: {uploaded_file_path}")

        # 2️⃣ Generate AI questions
        ai_questions = generate_questions_from_text(uploaded_file_path)

        # 3️⃣ Save JSON next to main.py
        output_json_path = os.path.join(os.path.dirname(__file__), "..", "generated_questions.json")
        output_json_path = os.path.abspath(output_json_path)

        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(ai_questions, f, indent=2)

        # 4️⃣ Update sidebar
        sidebar.questions = ai_questions

        # 5️⃣ User message
        filename = os.path.basename(file_path)
        print(f"🧩 {len(ai_questions)} AI-generated questions saved to {output_json_path}")
        return f"✅ Questions generated from this file: {filename}"

    except Exception as e:
        print(f"⚠️ Upload or LLM error: {e}")
        return f"⚠️ Error: {e}"
