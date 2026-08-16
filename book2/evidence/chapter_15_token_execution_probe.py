#!/usr/bin/env python3

import hashlib
import json
import math
from typing import Any, Sequence


VOCABULARY = ("<unk>", "small", "models", "run", "clear", "steps")
TOKEN_TO_ID = {token: token_id for token_id, token in enumerate(VOCABULARY)}
REQUEST = "small models run"
POSITIONS = 3
MODEL_WIDTH = 4
FEED_FORWARD_WIDTH = 5
EPSILON = 1e-9

EMBEDDINGS = (
    (0.00, 0.00, 0.00, 0.00),
    (0.20, -0.10, 0.40, 0.30),
    (-0.30, 0.50, 0.10, -0.20),
    (0.40, 0.20, -0.20, 0.10),
    (-0.10, 0.30, 0.20, 0.50),
    (0.30, -0.20, 0.50, -0.40),
)
POSITION_ROWS = (
    (0.00, 0.10, 0.00, 0.10),
    (0.10, 0.00, 0.10, 0.00),
    (0.00, -0.10, 0.10, 0.00),
)
W_Q = (
    (0.4, -0.2, 0.1, 0.3),
    (0.1, 0.5, -0.3, 0.2),
    (-0.2, 0.1, 0.6, -0.1),
    (0.3, 0.2, 0.1, 0.4),
)
W_K = (
    (0.2, 0.3, -0.2, 0.1),
    (-0.4, 0.2, 0.5, 0.0),
    (0.1, -0.3, 0.2, 0.6),
    (0.3, 0.1, 0.4, -0.2),
)
W_V = (
    (0.5, -0.1, 0.2, 0.0),
    (0.2, 0.4, -0.2, 0.3),
    (-0.3, 0.2, 0.5, 0.1),
    (0.1, 0.0, 0.3, 0.6),
)
W_O = (
    (0.3, -0.2, 0.1, 0.0),
    (0.1, 0.4, -0.1, 0.2),
    (-0.2, 0.1, 0.3, 0.5),
    (0.2, 0.0, 0.4, -0.3),
)
W_FF_1 = (
    (0.4, -0.1, 0.3, 0.2, -0.2),
    (-0.2, 0.5, 0.1, -0.3, 0.2),
    (0.3, 0.2, -0.4, 0.1, 0.5),
    (0.1, -0.3, 0.2, 0.6, -0.2),
)
B_FF_1 = (0.05, -0.02, 0.03, 0.00, -0.01)
W_FF_2 = (
    (0.3, -0.2, 0.1, 0.4),
    (-0.1, 0.2, 0.5, -0.3),
    (0.4, 0.1, -0.2, 0.2),
    (0.2, -0.4, 0.3, 0.1),
    (-0.3, 0.3, 0.2, -0.1),
)
B_FF_2 = (0.02, -0.03, 0.01, 0.00)
W_VOCABULARY = (
    (0.2, -0.1, 0.3, 0.0, -0.2, 0.1),
    (-0.3, 0.4, 0.1, -0.2, 0.2, 0.5),
    (0.1, 0.2, -0.4, 0.3, 0.5, -0.1),
    (0.4, -0.2, 0.2, 0.5, -0.3, 0.1),
)


def canonical(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 9)
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    if isinstance(value, dict):
        return {key: canonical(item) for key, item in value.items()}
    return value


def serialized(value: Any) -> str:
    return json.dumps(canonical(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value: Any) -> str:
    return hashlib.sha256(serialized(value).encode("ascii")).hexdigest()


def shape(value: Any) -> list[int]:
    dimensions = []
    current = value
    while isinstance(current, (list, tuple)):
        dimensions.append(len(current))
        current = current[0] if current else None
    return dimensions


def element_count(value: Any) -> int:
    dimensions = shape(value)
    return math.prod(dimensions) if dimensions else 1


def stage(
    order: int,
    name: str,
    input_value: Any,
    output_value: Any,
    expected_input_shape: Sequence[int],
    expected_output_shape: Sequence[int],
    category: str,
    work: dict[str, int],
    include_values: bool = True,
) -> dict[str, Any]:
    input_shape = shape(input_value)
    output_shape = shape(output_value)
    valid = input_shape == list(expected_input_shape) and output_shape == list(expected_output_shape)
    assert valid, f"{name} shape validation failed"
    record = {
        "order": order,
        "stage": name,
        "status": "executed",
        "input_shape": input_shape,
        "expected_input_shape": list(expected_input_shape),
        "output_shape": output_shape,
        "expected_output_shape": list(expected_output_shape),
        "shape_validated": valid,
        "operation_category": category,
        "allocated_output_elements": element_count(output_value),
        "work_count": work,
        "output_sha256": digest(output_value),
    }
    if include_values:
        record["output_values"] = canonical(output_value)
    return record


def row_times_matrix(row: Sequence[float], matrix: Sequence[Sequence[float]]) -> tuple[float, ...]:
    assert len(row) == len(matrix)
    return tuple(sum(row[index] * matrix[index][column] for index in range(len(row))) for column in range(len(matrix[0])))


def linear(rows: Sequence[Sequence[float]], matrix: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    return tuple(row_times_matrix(row, matrix) for row in rows)


def add_rows(left: Sequence[Sequence[float]], right: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row, strict=True))
        for left_row, right_row in zip(left, right, strict=True)
    )


def softmax(row: Sequence[float]) -> tuple[float, ...]:
    maximum = max(row)
    exponentials = tuple(math.exp(value - maximum) for value in row)
    total = sum(exponentials)
    return tuple(value / total for value in exponentials)


def layer_norm(rows: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    output = []
    for row in rows:
        mean = sum(row) / len(row)
        variance = sum((value - mean) ** 2 for value in row) / len(row)
        denominator = math.sqrt(variance + EPSILON)
        output.append(tuple((value - mean) / denominator for value in row))
    return tuple(output)


def run_attention(rows: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    queries = linear(rows, W_Q)
    keys = linear(rows, W_K)
    values = linear(rows, W_V)
    scores = tuple(
        tuple(sum(a * b for a, b in zip(query, key, strict=True)) / math.sqrt(MODEL_WIDTH) for key in keys)
        for query in queries
    )
    weights = tuple(softmax(row) for row in scores)
    combined = tuple(
        tuple(sum(weights[position][source] * values[source][axis] for source in range(POSITIONS)) for axis in range(MODEL_WIDTH))
        for position in range(POSITIONS)
    )
    return linear(combined, W_O)


def feed_forward(rows: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    hidden_linear = tuple(
        tuple(value + bias for value, bias in zip(row_times_matrix(row, W_FF_1), B_FF_1, strict=True))
        for row in rows
    )
    hidden_relu = tuple(tuple(max(0.0, value) for value in row) for row in hidden_linear)
    return tuple(
        tuple(value + bias for value, bias in zip(row_times_matrix(row, W_FF_2), B_FF_2, strict=True))
        for row in hidden_relu
    )


def validate_block_input(rows: Sequence[Sequence[float]]) -> dict[str, Any]:
    actual_shape = shape(rows)
    accepted = actual_shape == [POSITIONS, MODEL_WIDTH]
    return {
        "accepted": accepted,
        "code": "BLOCK_INPUT_SHAPE_VALID" if accepted else "BLOCK_INPUT_WIDTH_MISMATCH",
        "expected_shape": [POSITIONS, MODEL_WIDTH],
        "actual_shape": actual_shape,
    }


def execute_fixture() -> dict[str, Any]:
    stages = []
    tokens = tuple(REQUEST.lower().split())
    stages.append(stage(1, "tokenize", REQUEST, tokens, (), (POSITIONS,), "representation", {"character_scans": len(REQUEST)}))

    token_ids = tuple(TOKEN_TO_ID.get(token, 0) for token in tokens)
    stages.append(stage(2, "token_ids", tokens, token_ids, (POSITIONS,), (POSITIONS,), "lookup", {"vocabulary_lookups": POSITIONS}))

    embedding_rows = tuple(
        tuple(value + position for value, position in zip(EMBEDDINGS[token_id], POSITION_ROWS[index], strict=True))
        for index, token_id in enumerate(token_ids)
    )
    stages.append(stage(3, "embedding_plus_position", token_ids, embedding_rows, (POSITIONS,), (POSITIONS, MODEL_WIDTH), "representation", {"embedding_lookups": POSITIONS, "additions": POSITIONS * MODEL_WIDTH}))

    block_gate = validate_block_input(embedding_rows)
    assert block_gate["accepted"]
    stages.append(stage(4, "block_input_validation", embedding_rows, embedding_rows, (POSITIONS, MODEL_WIDTH), (POSITIONS, MODEL_WIDTH), "validation", {"dimension_comparisons": 2}, include_values=False))

    attention_output = run_attention(embedding_rows)
    attention_work = {
        "multiplications": 4 * POSITIONS * MODEL_WIDTH * MODEL_WIDTH + POSITIONS * POSITIONS * MODEL_WIDTH + POSITIONS * POSITIONS * MODEL_WIDTH,
        "additions": 4 * POSITIONS * MODEL_WIDTH * (MODEL_WIDTH - 1) + POSITIONS * POSITIONS * (MODEL_WIDTH - 1) + POSITIONS * MODEL_WIDTH * (POSITIONS - 1),
        "exponentials": POSITIONS * POSITIONS,
    }
    stages.append(stage(5, "attention", embedding_rows, attention_output, (POSITIONS, MODEL_WIDTH), (POSITIONS, MODEL_WIDTH), "attention", attention_work))

    residual_1 = add_rows(embedding_rows, attention_output)
    norm_1 = layer_norm(residual_1)
    stages.append(stage(6, "residual_norm_1", (embedding_rows, attention_output), norm_1, (2, POSITIONS, MODEL_WIDTH), (POSITIONS, MODEL_WIDTH), "constraint", {"residual_additions": POSITIONS * MODEL_WIDTH, "normalization_elements": POSITIONS * MODEL_WIDTH}))

    ff_output = feed_forward(norm_1)
    stages.append(stage(7, "feed_forward", norm_1, ff_output, (POSITIONS, MODEL_WIDTH), (POSITIONS, MODEL_WIDTH), "computation", {"multiplications": POSITIONS * MODEL_WIDTH * FEED_FORWARD_WIDTH + POSITIONS * FEED_FORWARD_WIDTH * MODEL_WIDTH, "bias_additions": POSITIONS * (FEED_FORWARD_WIDTH + MODEL_WIDTH), "relu_comparisons": POSITIONS * FEED_FORWARD_WIDTH}))

    residual_2 = add_rows(norm_1, ff_output)
    norm_2 = layer_norm(residual_2)
    stages.append(stage(8, "residual_norm_2", (norm_1, ff_output), norm_2, (2, POSITIONS, MODEL_WIDTH), (POSITIONS, MODEL_WIDTH), "constraint", {"residual_additions": POSITIONS * MODEL_WIDTH, "normalization_elements": POSITIONS * MODEL_WIDTH}))

    final_hidden = norm_2[-1]
    stages.append(stage(9, "final_position_hidden", norm_2, final_hidden, (POSITIONS, MODEL_WIDTH), (MODEL_WIDTH,), "selection", {"row_selections": 1}))

    logits = row_times_matrix(final_hidden, W_VOCABULARY)
    stages.append(stage(10, "vocabulary_projection", final_hidden, logits, (MODEL_WIDTH,), (len(VOCABULARY),), "projection", {"multiplications": MODEL_WIDTH * len(VOCABULARY), "additions": (MODEL_WIDTH - 1) * len(VOCABULARY)}))

    selected_id = min(index for index, value in enumerate(logits) if value == max(logits))
    stages.append(stage(11, "argmax", logits, selected_id, (len(VOCABULARY),), (), "selection", {"comparisons": len(VOCABULARY) - 1, "tie_rule_operations": 1}))

    decoded_token = VOCABULARY[selected_id]
    stages.append(stage(12, "decode", selected_id, decoded_token, (), (), "lookup", {"vocabulary_lookups": 1}))

    return {
        "request": REQUEST,
        "unknown_token_rule": "tokens absent from the fixed vocabulary map to ID 0 (<unk>)",
        "argmax_tie_rule": "choose the lowest token ID among equal maximum logits",
        "dimensions": {"positions": POSITIONS, "model_width": MODEL_WIDTH, "feed_forward_width": FEED_FORWARD_WIDTH, "vocabulary": len(VOCABULARY)},
        "vocabulary": VOCABULARY,
        "stages": stages,
        "selected_token_id": selected_id,
        "decoded_token": decoded_token,
    }


def run_control() -> dict[str, Any]:
    token_ids = tuple(TOKEN_TO_ID.get(token, 0) for token in REQUEST.lower().split())
    corrupted_rows = tuple(
        tuple(value + position for value, position in zip(EMBEDDINGS[token_id], POSITION_ROWS[index], strict=True)) + (0.0,)
        for index, token_id in enumerate(token_ids)
    )
    result = validate_block_input(corrupted_rows)
    assert result == {
        "accepted": False,
        "code": "BLOCK_INPUT_WIDTH_MISMATCH",
        "expected_shape": [POSITIONS, MODEL_WIDTH],
        "actual_shape": [POSITIONS, MODEL_WIDTH + 1],
    }
    later_stages = ("attention", "residual_norm_1", "feed_forward", "residual_norm_2", "final_position_hidden", "vocabulary_projection", "argmax", "decode")
    return {
        "change": "append one zero coordinate to each embedding-plus-position row",
        "first_failed_stage": "block_input_validation",
        "failure": result,
        "stage_statuses": {
            "tokenize": "executed",
            "token_ids": "executed",
            "embedding_plus_position": "executed_corrupted_width",
            "block_input_validation": "failed",
            **{name: "unexecuted" for name in later_stages},
        },
        "corrupted_rows_sha256": digest(corrupted_rows),
    }


def build_result() -> dict[str, Any]:
    trace = execute_fixture()
    control = run_control()
    stages = trace["stages"]
    dependency_edges = {
        "incoming": (("convergence.architecture", "convergence.execution"), ("programming.runtimes", "convergence.execution")),
        "outgoing": (("convergence.execution", "convergence.limits"),),
    }
    validation = {
        "fixed_request_has_three_tokens": len(REQUEST.split()) == POSITIONS,
        "all_request_tokens_are_known": all(token in TOKEN_TO_ID for token in REQUEST.split()),
        "stage_order_is_exact": tuple(record["stage"] for record in stages) == ("tokenize", "token_ids", "embedding_plus_position", "block_input_validation", "attention", "residual_norm_1", "feed_forward", "residual_norm_2", "final_position_hidden", "vocabulary_projection", "argmax", "decode"),
        "every_executed_stage_validates_shapes": all(record["shape_validated"] for record in stages),
        "every_stage_records_category": all(record["operation_category"] for record in stages),
        "every_stage_records_allocated_elements": all(record["allocated_output_elements"] >= 1 for record in stages),
        "every_stage_records_work": all(record["work_count"] and all(value >= 0 for value in record["work_count"].values()) for record in stages),
        "every_stage_records_value_or_digest": all("output_values" in record or "output_sha256" in record for record in stages),
        "attention_rows_have_declared_shape": stages[4]["output_shape"] == [POSITIONS, MODEL_WIDTH],
        "first_norm_rows_have_declared_shape": stages[5]["output_shape"] == [POSITIONS, MODEL_WIDTH],
        "feed_forward_rows_have_declared_shape": stages[6]["output_shape"] == [POSITIONS, MODEL_WIDTH],
        "second_norm_rows_have_declared_shape": stages[7]["output_shape"] == [POSITIONS, MODEL_WIDTH],
        "final_row_is_last_block_row": stages[8]["output_values"] == stages[7]["output_values"][-1],
        "logit_count_equals_vocabulary": len(stages[9]["output_values"]) == len(VOCABULARY),
        "argmax_obeys_lowest_id_tie_rule": trace["selected_token_id"] == min(index for index, value in enumerate(stages[9]["output_values"]) if value == max(stages[9]["output_values"])),
        "decode_matches_selected_id": trace["decoded_token"] == VOCABULARY[trace["selected_token_id"]],
        "control_fails_first_at_block_gate": control["first_failed_stage"] == "block_input_validation" and control["failure"]["code"] == "BLOCK_INPUT_WIDTH_MISMATCH",
        "control_leaves_all_downstream_stages_unexecuted": all(status == "unexecuted" for name, status in control["stage_statuses"].items() if name in {"attention", "residual_norm_1", "feed_forward", "residual_norm_2", "final_position_hidden", "vocabulary_projection", "argmax", "decode"}),
        "dependency_edges_exact": dependency_edges == {
            "incoming": (("convergence.architecture", "convergence.execution"), ("programming.runtimes", "convergence.execution")),
            "outgoing": (("convergence.execution", "convergence.limits"),),
        },
    }
    assert all(validation.values())
    return {
        "fixture": "deterministic standard-library token execution trace",
        "trace": trace,
        "width_corruption_control": control,
        "dependency_edges": dependency_edges,
        "count_note": "allocated-element and arithmetic/work counts are deterministic fixture counts, not elapsed time, latency, throughput, or a runtime benchmark",
        "boundary": "one fixed fixture path; no training, sampling, cache, batching, production equivalence, quality claim, semantic inference, parameter sweep, or philosophical interpretation",
        "validation": validation,
    }


def run_probe() -> dict[str, Any]:
    result = build_result()
    rerun = build_result()
    deterministic_rerun = serialized(result) == serialized(rerun)
    assert deterministic_rerun
    return {**result, "validation_count": len(result["validation"]), "deterministic_rerun": deterministic_rerun}


if __name__ == "__main__":
    print(json.dumps(canonical(run_probe()), indent=2, sort_keys=True, ensure_ascii=True))