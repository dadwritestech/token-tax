"""Pure metric math. Everything here is unit-tested; nothing touches the network.

Conventions
- `tokens` is a count for one language's copy of the parallel corpus.
- "English-equivalent words" = words in the English copy of the same corpus. Because
  FLORES sentences are translations of each other, dividing any language's token count
  by the English word count gives tokens per unit of *content*, which sidesteps the
  fact that Chinese/Japanese/Thai/Burmese don't put spaces between words.
"""
from __future__ import annotations

import math
import re
import unicodedata

_QUOTE_RUN = re.compile(r'"{2,}')


def clean(text: str) -> str:
    """Undo FLORES-200's CSV-escaping artifact (runs of doubled quotes) and NFC-normalise."""
    return unicodedata.normalize("NFC", _QUOTE_RUN.sub('"', text))


def count_words(text: str) -> int:
    return len(text.split())


def count_chars(text: str) -> int:
    """Unicode code points, whitespace excluded (NFC)."""
    return sum(1 for ch in unicodedata.normalize("NFC", text) if not ch.isspace())


def premium(tokens: int, en_tokens: int) -> float:
    """How many times more tokens the same content needs than in English."""
    if en_tokens <= 0:
        raise ValueError("English token count must be positive")
    return tokens / en_tokens


def per_unit(tokens: int, units: int) -> float | None:
    return tokens / units if units else None


def cost_per_m_en_words(tokens: int, en_words: int, usd_per_mtok: float) -> float:
    """USD to process content equal to 1M English words, written in this language."""
    if en_words <= 0:
        raise ValueError("English word count must be positive")
    tokens_per_en_word = tokens / en_words
    return tokens_per_en_word * 1_000_000 * usd_per_mtok / 1_000_000


def context_words(context_tokens: int, tokens: int, words: int) -> float:
    """How many words fit in a context window, given this corpus' tokens-per-word.

    Pass English word count to get English-equivalent words of content."""
    if tokens <= 0:
        raise ValueError("token count must be positive")
    return context_tokens * words / tokens


def geomean(xs) -> float:
    xs = list(xs)
    if not xs:
        raise ValueError("geomean of empty sequence")
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


def paragraph_cost(prem: float, base: float = 1.0) -> float:
    """If an English paragraph costs `base`, the same paragraph in this language costs this."""
    return base * prem
