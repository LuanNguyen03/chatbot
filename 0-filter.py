"""
Sensitive Data Filter: Nhận diện & xử lý dữ liệu nhạy cảm
"""
import re

SENSITIVE_PATTERNS = {
    "account_number": r"\b\d{9,14}\b",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "id_card": r"\b\d{9,12}\b",
    "phone": r"(\+84|0)\d{9,10}"
}

def detect_sensitive(text: str):
    matches = {}
    for key, pattern in SENSITIVE_PATTERNS.items():
        found = re.findall(pattern, text)
        if found:
            matches[key] = found
    return matches

def mask_sensitive(text: str, mapping: dict):
    for key, pattern in SENSITIVE_PATTERNS.items():
        found = re.findall(pattern, text)
        for f in found:
            token = f"<{key.upper()}_{len(mapping)+1}>"
            mapping[token] = f
            text = text.replace(f, token)
    return text, mapping

def restore_sensitive(text: str, mapping: dict):
    for token, original in mapping.items():
        text = text.replace(token, original)
    return text
