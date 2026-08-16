#!/usr/bin/env python3

import json
import math
from collections.abc import Sequence


QUERIES = ((1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (-1.0, 1.0), (0.5, -0.5))
KEYS = ((1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (-1.0, 0.0), (0.5, -0.5))
VALUES = ((1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (-1.0, 1.0), (0.5, -1.0))
VALUE_PERTURBATION = (0.4, -0.2)
DIMENSION = 2
SCALE = math.sqrt(DIMENSION)
TOLERANCE = 1e-12


def dot(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != DIMENSION or len(right) != DIMENSION:
        raise ValueError("vectors must have dimension two")
    return sum(a * b for a, b in zip(left, right, strict=True))


def add(left: Sequence[float], right: Sequence[float]) -> tuple[float, float]:
    if len(left) != DIMENSION or len(right) != DIMENSION:
        raise ValueError("vectors must have dimension two")
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale_vector(scalar: float, vector: Sequence[float]) -> tuple[float, float]:
    if len(vector) != DIMENSION:
        raise ValueError("vectors must have dimension two")
    return tuple(scalar * value for value in vector)


def softmax(scores: Sequence[float]) -> tuple[float, ...]:
    if not scores:
        raise ValueError("softmax requires at least one admitted score")
    maximum = max(scores)
    exponentials = [math.exp(score - maximum) for score in scores]
    denominator = sum(exponentials)
    return tuple(value / denominator for value in exponentials)


def attention(values: Sequence[Sequence[float]], causal: bool) -> dict:
    if len(QUERIES) != len(KEYS) or len(KEYS) != len(values):
        raise ValueError("queries, keys, and values must have equal position counts")

    score_rows = []
    weight_rows = []
    contribution_rows = []
    outputs = []
    admitted_rows = []
    for query_index, query in enumerate(QUERIES):
        scores = tuple(dot(query, key) / SCALE for key in KEYS)
        admitted = tuple(
            key_index
            for key_index in range(len(KEYS))
            if not causal or key_index <= query_index
        )
        admitted_weights = softmax(tuple(scores[index] for index in admitted))
        weights = [0.0] * len(KEYS)
        for key_index, weight in zip(admitted, admitted_weights, strict=True):
            weights[key_index] = weight
        contributions = [
            scale_vector(weight, value)
            for weight, value in zip(weights, values, strict=True)
        ]
        output = (0.0, 0.0)
        for contribution in contributions:
            output = add(output, contribution)

        score_rows.append(scores)
        admitted_rows.append(admitted)
        weight_rows.append(tuple(weights))
        contribution_rows.append(contributions)
        outputs.append(output)

    return {
        "scores": score_rows,
        "admitted_key_positions_zero_based": admitted_rows,
        "weights": weight_rows,
        "contributions": contribution_rows,
        "outputs": outputs,
    }


def close_vectors(left: Sequence[float], right: Sequence[float]) -> bool:
    return all(
        math.isclose(a, b, rel_tol=0.0, abs_tol=TOLERANCE)
        for a, b in zip(left, right, strict=True)
    )


def run_probe() -> dict:
    full = attention(VALUES, causal=False)
    causal = attention(VALUES, causal=True)

    changed_values = list(VALUES)
    changed_values[0] = add(changed_values[0], VALUE_PERTURBATION)
    controlled = attention(changed_values, causal=False)

    observed_differences = [
        add(changed, scale_vector(-1.0, original))
        for original, changed in zip(full["outputs"], controlled["outputs"], strict=True)
    ]
    expected_differences = [
        scale_vector(weights[0], VALUE_PERTURBATION)
        for weights in full["weights"]
    ]

    validation = {
        "all_vectors_have_declared_dimension": all(
            len(vector) == DIMENSION
            for vector in (
                *QUERIES,
                *KEYS,
                *VALUES,
                *full["outputs"],
                *(item for row in full["contributions"] for item in row),
            )
        ),
        "full_weights_normalized": all(
            math.isclose(sum(row), 1.0, rel_tol=0.0, abs_tol=TOLERANCE)
            for row in full["weights"]
        ),
        "causal_weights_normalized": all(
            math.isclose(sum(row), 1.0, rel_tol=0.0, abs_tol=TOLERANCE)
            for row in causal["weights"]
        ),
        "causal_future_weights_are_zero": all(
            causal["weights"][query_index][key_index] == 0.0
            for query_index in range(len(QUERIES))
            for key_index in range(query_index + 1, len(KEYS))
        ),
        "outputs_equal_recorded_contribution_sums": all(
            close_vectors(
                output,
                tuple(sum(contribution[axis] for contribution in row) for axis in range(DIMENSION)),
            )
            for output, row in zip(full["outputs"], full["contributions"], strict=True)
        ),
        "value_change_preserves_scores": controlled["scores"] == full["scores"],
        "value_change_preserves_weights": controlled["weights"] == full["weights"],
        "value_change_matches_weighted_delta": all(
            close_vectors(observed, expected)
            for observed, expected in zip(
                observed_differences, expected_differences, strict=True
            )
        ),
    }
    assert all(validation.values())

    return {
        "operation": "single-head scaled dot-product attention",
        "dimension": DIMENSION,
        "scale": SCALE,
        "queries": QUERIES,
        "keys": KEYS,
        "values": VALUES,
        "full_attention": full,
        "causal_attention": causal,
        "value_only_control": {
            "value_1_delta": VALUE_PERTURBATION,
            "changed_values": changed_values,
            "scores_unchanged": controlled["scores"] == full["scores"],
            "weights_unchanged": controlled["weights"] == full["weights"],
            "outputs": controlled["outputs"],
            "observed_output_differences": observed_differences,
            "expected_weighted_differences": expected_differences,
        },
        "structural_path_comparison": {
            "recurrent_graph": "x1 -> h1 -> h2 -> h3 -> h4 -> h5",
            "recurrent_edge_count": 5,
            "attention_contribution_graph": "v1 -> o5",
            "attention_edge_count": 1,
            "measurement_boundary": "abstract graph edges; not runtime measurements",
        },
        "validation": validation,
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2))