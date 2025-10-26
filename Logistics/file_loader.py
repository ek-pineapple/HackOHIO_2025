"""
file_loader.py
---------------
Extracts text from PDF or TXT files,
splits it into chunks, and writes the output to a .txt file
for use with LLMs (e.g., question generation).

Dependencies:
    pip install PyMuPDF
"""

import os
import re
from typing import List

# --- Safe imports (so game won't crash if not installed) ---
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


# ------------------------------------------------------------
# PDF Extraction
# ------------------------------------------------------------
def extract_text_from_pdf(path: str) -> str:
    if not fitz:
        raise ImportError("❌ PyMuPDF not installed. Run: pip install PyMuPDF")

    text = []
    with fitz.open(path) as doc:
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


# ------------------------------------------------------------
# TXT Extraction
# ------------------------------------------------------------
def extract_text_from_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------
# File Router
# ------------------------------------------------------------
def get_text_from_file(path: str) -> str:
    """Detect file type and extract text accordingly."""
    path_lower = path.lower()

    if path_lower.endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path_lower.endswith(".txt"):
        return extract_text_from_txt(path)
    else:
        raise ValueError("Unsupported file type. Use .pdf or .txt")


# ------------------------------------------------------------
# Text Chunking Helper
# ------------------------------------------------------------
def chunk_text(text: str, max_chars: int = 3000) -> List[str]:
    """Split text into paragraph-based chunks of approximately max_chars length."""
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current = []
    cur_len = 0

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue

        if cur_len + len(p) + 1 <= max_chars:
            current.append(p)
            cur_len += len(p) + 1
        else:
            if current:
                chunks.append("\n\n".join(current))
            current = [p]
            cur_len = len(p) + 1

    if current:
        chunks.append("\n\n".join(current))

    return chunks


# ------------------------------------------------------------
# 🧠 Write extracted text to a file
# ------------------------------------------------------------
def save_extracted_text(input_path: str, output_path: str = "assets/processed_upload.txt") -> str:
    """Extracts and cleans text from a supported file type, then saves to a .txt file."""
    print(f"📂 Extracting from: {input_path}")

    text = get_text_from_file(input_path)
    chunks = chunk_text(text)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n--- CHUNK SPLIT ---\n\n".join(chunks))

    print(f"✅ Saved extracted text to: {output_path}")
    print(f"🧩 Total chunks: {len(chunks)}")
    print(f"📄 Approx. total characters: {len(text):,}")

    return output_path
