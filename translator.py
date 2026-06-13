# translator.py
# No longer used for verse display — Tamil verses come directly from
# the local TAMOVR-BibleWorks.txt file (authentic, no translation errors).
# This file is kept to avoid import errors if referenced elsewhere.

def detect_language_code(text: str) -> str:
    return "ta" if any('\u0B80' <= c <= '\u0BFF' for c in text) else "en"