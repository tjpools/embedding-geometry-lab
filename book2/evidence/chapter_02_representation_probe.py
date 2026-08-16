#!/usr/bin/env python3

import json
import unicodedata


BASE_VOCABULARY = {
    "<unk>": 0,
    "locked": 1,
    "unlocked": 2,
    "open": 3,
}

PERMUTED_VOCABULARY = {
    "unlocked": 0,
    "open": 1,
    "<unk>": 2,
    "locked": 3,
}

BASE_TABLE = (
    (0.0, 0.0, 0.0),
    (0.8, 0.1, -0.2),
    (0.6, 0.4, 0.3),
    (0.2, 0.9, 0.5),
)

PERMUTED_TABLE = (
    (0.6, 0.4, 0.3),
    (0.2, 0.9, 0.5),
    (0.0, 0.0, 0.0),
    (0.8, 0.1, -0.2),
)


def normalize(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold().strip()


def tokenize(text: str) -> list[str]:
    return normalize(text).split()


def identifier(token: str, vocabulary: dict[str, int]) -> int:
    return vocabulary.get(token, vocabulary["<unk>"])


def one_hot(index: int, dimension: int) -> list[int]:
    return [int(position == index) for position in range(dimension)]


def vector_for(token: str, vocabulary: dict[str, int], table: tuple[tuple[float, ...], ...]) -> tuple[float, ...]:
    return table[identifier(token, vocabulary)]


def run_probe() -> dict:
    source = " OPEN "
    normalized = normalize(source)
    tokens = tokenize(source)
    assert tokens == ["open"]

    token = tokens[0]
    base_id = identifier(token, BASE_VOCABULARY)
    permuted_id = identifier(token, PERMUTED_VOCABULARY)
    base_one_hot = one_hot(base_id, len(BASE_VOCABULARY))
    permuted_one_hot = one_hot(permuted_id, len(PERMUTED_VOCABULARY))
    base_vector = vector_for(token, BASE_VOCABULARY, BASE_TABLE)
    permuted_vector = vector_for(token, PERMUTED_VOCABULARY, PERMUTED_TABLE)

    assert base_id != permuted_id
    assert base_one_hot != permuted_one_hot
    assert base_vector == permuted_vector

    unknown_tokens = ("ajar", "obstructed")
    unknown_ids = [identifier(value, BASE_VOCABULARY) for value in unknown_tokens]
    unknown_vectors = [vector_for(value, BASE_VOCABULARY, BASE_TABLE) for value in unknown_tokens]
    assert len(set(unknown_ids)) == 1
    assert len(set(unknown_vectors)) == 1

    return {
        "input": source,
        "normalized": normalized,
        "tokens": tokens,
        "permutation": {
            "base_id": base_id,
            "permuted_id": permuted_id,
            "base_one_hot": base_one_hot,
            "permuted_one_hot": permuted_one_hot,
            "base_vector": base_vector,
            "permuted_vector": permuted_vector,
            "selected_vector_preserved": base_vector == permuted_vector,
        },
        "information_loss": {
            "distinct_inputs": unknown_tokens,
            "shared_identifier": unknown_ids[0],
            "shared_vector": unknown_vectors[0],
            "distinction_discarded": True,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2))
