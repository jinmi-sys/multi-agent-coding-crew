"""Token estimation utilities."""

import math


def estimate_tokens(text: str) -> int:
    """Estimate token count (~4 chars per token for English, ~2 for CJK)."""
    if not text:
        return 0
    ascii_chars = sum(1 for c in text if ord(c) < 128)
    non_ascii = len(text) - ascii_chars
    return math.ceil(ascii_chars / 4 + non_ascii / 2)


def fits_in_context(text: str, max_tokens: int = 1_000_000) -> bool:
    return estimate_tokens(text) <= max_tokens


def context_usage_pct(text: str, max_tokens: int = 1_000_000) -> float:
    if max_tokens <= 0:
        return 0.0
    return round(estimate_tokens(text) / max_tokens * 100, 2)
