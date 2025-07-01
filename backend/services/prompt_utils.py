# backend/services/prompt_utils.py

import os


def load_prompt(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
