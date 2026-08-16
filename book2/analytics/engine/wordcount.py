from typing import Dict

from engine.markdown_strip import extract_words


def measure(text: str) -> Dict[str, int]:
    word_list = extract_words(text)
    return {
        "words": len(word_list),
        "unique_words": len({word.lower() for word in word_list}),
        "characters": len(text),
        "characters_no_spaces": sum(not character.isspace() for character in text),
    }
