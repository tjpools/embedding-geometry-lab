import re
from typing import Dict, Sequence

from engine.markdown_strip import count_paragraphs, extract_words, sentence_word_counts


def estimate_syllables(word: str) -> int:
    value = re.sub(r"[^a-z]", "", word.lower())
    if not value:
        return 0
    groups = len(re.findall(r"[aeiouy]+", value))
    if value.endswith("e") and not value.endswith(("le", "ye")) and groups > 1:
        groups -= 1
    return max(1, groups)


def reading_ease(word_list: Sequence[str], sentence_count: int) -> float:
    if not word_list or sentence_count == 0:
        return 0.0
    syllables = sum(estimate_syllables(word) for word in word_list)
    score = 206.835 - 1.015 * (len(word_list) / sentence_count) - 84.6 * (syllables / len(word_list))
    return round(score, 1)


def measure(text: str) -> Dict[str, float]:
    word_list = extract_words(text)
    sentence_lengths = sentence_word_counts(text)
    sentences = len(sentence_lengths)
    paragraphs = count_paragraphs(text)
    long_sentences = sum(length > 30 for length in sentence_lengths)
    return {
        "sentences": sentences,
        "paragraphs": paragraphs,
        "average_sentence_words": round(sum(sentence_lengths) / sentences, 1) if sentences else 0.0,
        "long_sentence_percent": round(long_sentences / sentences * 100, 1) if sentences else 0.0,
        "cci": round(sentences / paragraphs, 2) if paragraphs else 0.0,
        "reading_ease_estimate": reading_ease(word_list, sentences),
    }
