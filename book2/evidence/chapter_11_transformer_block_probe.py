#!/usr/bin/env python3

import json
import math
from collections.abc import Sequence


MODEL_DIMENSION = 4
HEADS = 2
HEAD_DIMENSION = 2
FEED_FORWARD_DIMENSION = 6
EPSILON = 1e-9
TOLERANCE = 1e-12

TOKENS = (
    (0.60, -0.20, 0.10, 0.30),
    (-0.10, 0.50, 0.20, -0.40),
    (0.30, 0.10, -0.50, 0.20),
    (0.00, -0.30, 0.40, 0.10),
)

POSITIONAL = (
    (0.00, 1.00, 0.00, 1.00),
    (0.84, 0.54, 0.01, 1.00),
    (0.91, -0.42, 0.02, 1.00),
    (0.14, -0.99, 0.03, 1.00),
)

W_Q = (
    (0.40, -0.20, 0.10, 0.30),
    (0.10, 0.50, -0.30, 0.20),
    (-0.20, 0.10, 0.60, -0.10),
    (0.30, 0.20, 0.10, 0.40),
)

W_K = (
    (0.20, 0.30, -0.20, 0.10),
    (-0.40, 0.20, 0.50, 0.00),
    (0.10, -0.30, 0.20, 0.60),
    (0.30, 0.10, 0.40, -0.20),
)

W_V = (
    (0.50, -0.10, 0.20, 0.00),
    (0.20, 0.40, -0.20, 0.30),
    (-0.30, 0.20, 0.50, 0.10),
    (0.10, 0.00, 0.30, 0.60),
)

W_O = (
    (0.30, -0.20, 0.10, 0.00),
    (0.10, 0.40, -0.10, 0.20),
    (-0.20, 0.10, 0.30, 0.50),
    (0.20, 0.00, 0.40, -0.30),
)

W_FF_1 = (
    (0.40, -0.10, 0.30, 0.20, -0.20, 0.10),
    (-0.20, 0.50, 0.10, -0.30, 0.20, 0.40),
    (0.30, 0.20, -0.40, 0.10, 0.50, -0.10),
    (0.10, -0.30, 0.20, 0.60, -0.20, 0.30),
)

B_FF_1 = (0.05, -0.02, 0.03, 0.00, -0.01, 0.04)

W_FF_2 = (
    (0.30, -0.20, 0.10, 0.40),
    (-0.10, 0.20, 0.50, -0.30),
    (0.40, 0.10, -0.20, 0.20),
    (0.20, -0.40, 0.30, 0.10),
    (-0.30, 0.30, 0.20, -0.10),
    (0.10, 0.20, -0.10, 0.30),
)

B_FF_2 = (0.02, -0.03, 0.01, 0.00)


def check_vector(vector: Sequence[float], expected: int, name: str) -> None:
    if len(vector) != expected:
        raise ValueError(f"{name} must have dimension {expected}")


def dot(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("dot product requires equal dimensions")
    return sum(a * b for a, b in zip(left, right, strict=True))


def add_vectors(left: Sequence[float], right: Sequence[float]) -> tuple[float, ...]:
    if len(left) != len(right):
        raise ValueError("vector addition requires equal dimensions")
    return tuple(a + b for a, b in zip(left, right, strict=True))


def subtract_vectors(left: Sequence[float], right: Sequence[float]) -> tuple[float, ...]:
    if len(left) != len(right):
        raise ValueError("vector subtraction requires equal dimensions")
    return tuple(a - b for a, b in zip(left, right, strict=True))


def matrix_row_times_matrix(row: Sequence[float], matrix: Sequence[Sequence[float]]) -> tuple[float, ...]:
    check_vector(row, len(matrix), "row")
    columns = len(matrix[0])
    return tuple(
        sum(row[i] * matrix[i][j] for i in range(len(row)))
        for j in range(columns)
    )


def apply_linear(rows: Sequence[Sequence[float]], matrix: Sequence[Sequence[float]], bias: Sequence[float] | None = None) -> tuple[tuple[float, ...], ...]:
    projected = []
    for row in rows:
        transformed = matrix_row_times_matrix(row, matrix)
        if bias is not None:
            transformed = add_vectors(transformed, bias)
        projected.append(transformed)
    return tuple(projected)


def softmax(values: Sequence[float]) -> tuple[float, ...]:
    maximum = max(values)
    exponentials = [math.exp(value - maximum) for value in values]
    denominator = sum(exponentials)
    return tuple(entry / denominator for entry in exponentials)


def split_heads(rows: Sequence[Sequence[float]]) -> tuple[tuple[tuple[float, ...], ...], ...]:
    split = []
    for row in rows:
        check_vector(row, MODEL_DIMENSION, "projected row")
        split.append(
            tuple(
                tuple(row[head * HEAD_DIMENSION + offset] for offset in range(HEAD_DIMENSION))
                for head in range(HEADS)
            )
        )
    return tuple(split)


def gather_head(split: Sequence[Sequence[Sequence[float]]], head: int) -> tuple[tuple[float, ...], ...]:
    return tuple(tuple(row[head]) for row in split)


def attention_head(queries: Sequence[Sequence[float]], keys: Sequence[Sequence[float]], values: Sequence[Sequence[float]]) -> dict:
    scale = math.sqrt(HEAD_DIMENSION)
    score_rows = []
    weight_rows = []
    output_rows = []
    contribution_rows = []
    for query in queries:
        scores = tuple(dot(query, key) / scale for key in keys)
        weights = softmax(scores)
        output = [0.0] * HEAD_DIMENSION
        contributions = []
        for weight, value in zip(weights, values, strict=True):
            weighted = tuple(weight * coordinate for coordinate in value)
            contributions.append(weighted)
            for axis in range(HEAD_DIMENSION):
                output[axis] += weighted[axis]
        score_rows.append(scores)
        weight_rows.append(weights)
        output_rows.append(tuple(output))
        contribution_rows.append(tuple(contributions))
    return {
        "scores": tuple(score_rows),
        "weights": tuple(weight_rows),
        "outputs": tuple(output_rows),
        "contributions": tuple(contribution_rows),
    }


def concatenate_heads(head_outputs: Sequence[Sequence[Sequence[float]]]) -> tuple[tuple[float, ...], ...]:
    rows = []
    positions = len(head_outputs[0])
    for position in range(positions):
        combined = []
        for head in range(HEADS):
            combined.extend(head_outputs[head][position])
        rows.append(tuple(combined))
    return tuple(rows)


def layer_norm_rows(rows: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    normalized = []
    for row in rows:
        check_vector(row, MODEL_DIMENSION, "layer norm row")
        mean = sum(row) / MODEL_DIMENSION
        variance = sum((value - mean) ** 2 for value in row) / MODEL_DIMENSION
        denominator = math.sqrt(variance + EPSILON)
        normalized.append(tuple((value - mean) / denominator for value in row))
    return tuple(normalized)


def relu_rows(rows: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    return tuple(tuple(max(0.0, value) for value in row) for row in rows)


def build_block(include_attention: bool) -> dict:
    inputs = tuple(add_vectors(token, position) for token, position in zip(TOKENS, POSITIONAL, strict=True))
    queries = apply_linear(inputs, W_Q)
    keys = apply_linear(inputs, W_K)
    values = apply_linear(inputs, W_V)

    split_q = split_heads(queries)
    split_k = split_heads(keys)
    split_v = split_heads(values)

    head_results = []
    for head in range(HEADS):
        head_results.append(
            attention_head(
                gather_head(split_q, head),
                gather_head(split_k, head),
                gather_head(split_v, head),
            )
        )

    merged_heads = concatenate_heads(tuple(result["outputs"] for result in head_results))
    projected_attention = apply_linear(merged_heads, W_O)
    if not include_attention:
        projected_attention = tuple((0.0, 0.0, 0.0, 0.0) for _ in projected_attention)

    residual_1 = tuple(
        add_vectors(input_row, projected_row)
        for input_row, projected_row in zip(inputs, projected_attention, strict=True)
    )
    norm_1 = layer_norm_rows(residual_1)

    ff_hidden_linear = apply_linear(norm_1, W_FF_1, B_FF_1)
    ff_hidden = relu_rows(ff_hidden_linear)
    ff_output = apply_linear(ff_hidden, W_FF_2, B_FF_2)

    residual_2 = tuple(
        add_vectors(norm_row, ff_row)
        for norm_row, ff_row in zip(norm_1, ff_output, strict=True)
    )
    norm_2 = layer_norm_rows(residual_2)

    return {
        "inputs": inputs,
        "queries": queries,
        "keys": keys,
        "values": values,
        "heads": tuple(head_results),
        "concatenated_heads": merged_heads,
        "projected_attention": projected_attention,
        "residual_1": residual_1,
        "norm_1": norm_1,
        "ff_hidden_linear": ff_hidden_linear,
        "ff_hidden_relu": ff_hidden,
        "ff_output": ff_output,
        "residual_2": residual_2,
        "norm_2": norm_2,
    }


def rows_close(left: Sequence[Sequence[float]], right: Sequence[Sequence[float]]) -> bool:
    return all(
        all(math.isclose(a, b, rel_tol=0.0, abs_tol=TOLERANCE) for a, b in zip(row_l, row_r, strict=True))
        for row_l, row_r in zip(left, right, strict=True)
    )


def run_probe() -> dict:
    full = build_block(include_attention=True)
    no_attention = build_block(include_attention=False)
    rerun = build_block(include_attention=True)

    per_head_row_sums = tuple(
        tuple(sum(row) for row in head["weights"])
        for head in full["heads"]
    )

    norm_1_means = tuple(sum(row) / MODEL_DIMENSION for row in full["norm_1"])
    norm_1_variances = tuple(sum(value * value for value in row) / MODEL_DIMENSION for row in full["norm_1"])
    norm_2_means = tuple(sum(row) / MODEL_DIMENSION for row in full["norm_2"])
    norm_2_variances = tuple(sum(value * value for value in row) / MODEL_DIMENSION for row in full["norm_2"])

    control_differences = tuple(
        subtract_vectors(full_row, control_row)
        for full_row, control_row in zip(full["norm_2"], no_attention["norm_2"], strict=True)
    )
    control_l2 = tuple(math.sqrt(sum(value * value for value in row)) for row in control_differences)

    validation = {
        "dimensions_match_declared_shapes": (
            len(TOKENS) == len(POSITIONAL)
            and all(len(row) == MODEL_DIMENSION for row in full["inputs"])
            and all(len(row) == MODEL_DIMENSION for row in full["queries"])
            and all(len(row) == MODEL_DIMENSION for row in full["keys"])
            and all(len(row) == MODEL_DIMENSION for row in full["values"])
            and all(len(row) == MODEL_DIMENSION for row in full["concatenated_heads"])
            and all(len(row) == MODEL_DIMENSION for row in full["projected_attention"])
            and all(len(row) == MODEL_DIMENSION for row in full["norm_2"])
        ),
        "attention_rows_normalize_to_one": all(
            math.isclose(total, 1.0, rel_tol=0.0, abs_tol=TOLERANCE)
            for head_rows in per_head_row_sums
            for total in head_rows
        ),
        "heads_are_distinct": any(
            any(
                not math.isclose(a, b, rel_tol=0.0, abs_tol=1e-6)
                for a, b in zip(row_a, row_b, strict=True)
            )
            for row_a, row_b in zip(full["heads"][0]["weights"], full["heads"][1]["weights"], strict=True)
        ),
        "first_residual_equation_holds": rows_close(
            full["residual_1"],
            tuple(
                add_vectors(input_row, projected_row)
                for input_row, projected_row in zip(full["inputs"], full["projected_attention"], strict=True)
            ),
        ),
        "second_residual_equation_holds": rows_close(
            full["residual_2"],
            tuple(
                add_vectors(norm_row, ff_row)
                for norm_row, ff_row in zip(full["norm_1"], full["ff_output"], strict=True)
            ),
        ),
        "layer_norm_one_means_near_zero": all(abs(mean) < 1e-9 for mean in norm_1_means),
        "layer_norm_two_means_near_zero": all(abs(mean) < 1e-9 for mean in norm_2_means),
        "layer_norm_one_unit_variance": all(abs(variance - 1.0) < 1e-6 for variance in norm_1_variances),
        "layer_norm_two_unit_variance": all(abs(variance - 1.0) < 1e-6 for variance in norm_2_variances),
        "deterministic_rerun": rows_close(full["norm_2"], rerun["norm_2"]),
        "control_changes_output": any(norm > 1e-6 for norm in control_l2),
    }
    assert all(validation.values())

    return {
        "operation": "minimal_transformer_encoder_block_fixture",
        "disclaimer": "fixed deterministic fixture; not trained and not production-equivalent",
        "dimensions": {
            "positions": len(TOKENS),
            "model": MODEL_DIMENSION,
            "heads": HEADS,
            "head_dimension": HEAD_DIMENSION,
            "ff_dimension": FEED_FORWARD_DIMENSION,
        },
        "normalization_formula": "layer_norm(x) = (x - mean(x)) / sqrt(var(x) + epsilon)",
        "epsilon": EPSILON,
        "tokens": TOKENS,
        "positional_information": POSITIONAL,
        "weights": {
            "W_Q": W_Q,
            "W_K": W_K,
            "W_V": W_V,
            "W_O": W_O,
            "W_FF_1": W_FF_1,
            "B_FF_1": B_FF_1,
            "W_FF_2": W_FF_2,
            "B_FF_2": B_FF_2,
        },
        "full_block": full,
        "control_no_attention": {
            "projected_attention_is_zero": all(
                row == (0.0, 0.0, 0.0, 0.0)
                for row in no_attention["projected_attention"]
            ),
            "norm_2": no_attention["norm_2"],
            "difference_from_full": control_differences,
            "difference_l2_per_position": control_l2,
        },
        "summary": {
            "head_1_query_4_weights": full["heads"][0]["weights"][3],
            "head_2_query_4_weights": full["heads"][1]["weights"][3],
            "projected_attention_query_4": full["projected_attention"][3],
            "final_norm_query_4": full["norm_2"][3],
            "control_difference_query_4": control_differences[3],
        },
        "validation": validation,
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2))