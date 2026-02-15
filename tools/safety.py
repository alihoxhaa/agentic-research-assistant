import re

# Light heuristic patterns: enough for a demo + rubric requirement
_PATTERNS = [
    r"ignore (all|any) (previous|prior) instructions",
    r"reveal (hidden|system) (prompt|instructions|secrets)",
    r"you are now (an? )?assistant",
    r"override .* instructions",
    r"do not follow .* rules",
    r"always answer with made[- ]up facts",
]

def strip_prompt_injection(text: str) -> str:
    cleaned = text
    for pat in _PATTERNS:
        cleaned = re.sub(pat, "[REMOVED_INSTRUCTION_LIKE_TEXT]", cleaned, flags=re.IGNORECASE)
    return cleaned
