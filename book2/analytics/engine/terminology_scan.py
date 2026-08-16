from collections import Counter
from typing import Dict, Iterable, Sequence

from engine.markdown_strip import extract_words


DEFAULT_TERMS = (
    "architecture",
    "constraint",
    "execution",
    "geometry",
    "interface",
    "representation",
    "structure",
    "transformer",
)


def scan(text: str, terms: Sequence[str] = DEFAULT_TERMS) -> Dict[str, object]:
    normalized = [word.lower() for word in extract_words(text)]
    counts = Counter(normalized)
    term_counts = {term: counts[term.lower()] for term in terms}
    total = len(normalized)
    return {
        "term_counts": term_counts,
        "terminology_density": round(sum(term_counts.values()) / total * 1000, 1) if total else 0.0,
    }


def aggregate(scans: Iterable[Dict[str, object]], terms: Sequence[str] = DEFAULT_TERMS) -> Dict[str, int]:
    totals = Counter()
    for result in scans:
        totals.update(result["term_counts"])
    return {term: totals[term] for term in terms}
