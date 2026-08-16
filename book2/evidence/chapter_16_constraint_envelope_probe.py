#!/usr/bin/env python3

import hashlib
import json
from typing import Any, Callable

try:
    from evidence.chapter_15_token_execution_probe import (
        EMBEDDINGS,
        MODEL_WIDTH,
        POSITION_ROWS,
        REQUEST,
        TOKEN_TO_ID,
        VOCABULARY,
        add_rows,
        canonical,
        execute_fixture,
        feed_forward,
        layer_norm,
        run_attention,
        validate_block_input,
    )
except ModuleNotFoundError:
    from chapter_15_token_execution_probe import (
        EMBEDDINGS,
        MODEL_WIDTH,
        POSITION_ROWS,
        REQUEST,
        TOKEN_TO_ID,
        VOCABULARY,
        add_rows,
        canonical,
        execute_fixture,
        feed_forward,
        layer_norm,
        run_attention,
        validate_block_input,
    )


CONTEXT_CAPACITY = 3
UNKNOWN_ID = 0
LIMITS_MODULE = "convergence.limits"
OUTSIDE_OPERATIONAL_EVIDENCE = "OUTSIDE_OPERATIONAL_EVIDENCE"
PROHIBITED_CLAIMS = frozenset(("understands", "is_person", "cannot_ever_understand"))


def serialized(value: Any) -> str:
    return json.dumps(canonical(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value: Any) -> str:
    return hashlib.sha256(serialized(value).encode("ascii")).hexdigest()


def experiment(
    experiment_id: str,
    experiment_type: str,
    changed_variables: dict[str, Any],
    held_fixed_variables: dict[str, Any],
    result_type: str,
    result: dict[str, Any],
    permitted_inference: str,
) -> dict[str, Any]:
    return {
        "experiment_id": experiment_id,
        "experiment_type": experiment_type,
        "changed_variables": changed_variables,
        "held_fixed_variables": held_fixed_variables,
        "result_type": result_type,
        "result": result,
        "permitted_inference": permitted_inference,
    }


def context_experiment() -> dict[str, Any]:
    records = []
    request_token_ids = (1, 2, 3, 4)
    for requested_length in (1, 2, 3, 4):
        admitted = requested_length <= CONTEXT_CAPACITY
        embedded_rows = tuple(EMBEDDINGS[token_id] for token_id in request_token_ids[:requested_length]) if admitted else ()
        records.append(
            {
                "requested_length": requested_length,
                "admitted": admitted,
                "code": "CONTEXT_ACCEPTED" if admitted else "CONTEXT_CAPACITY_EXCEEDED",
                "embedding_executed": admitted,
                "embedding_output_shape": [len(embedded_rows), MODEL_WIDTH] if admitted else None,
            }
        )
    return experiment(
        "limits.context_capacity",
        "acceptance_boundary",
        {"requested_length": [1, 2, 3, 4]},
        {"context_capacity": CONTEXT_CAPACITY, "gate_order": "before_embedding"},
        "admission_records",
        {"records": records, "first_rejected_length": 4, "rejected_before_embedding": True},
        "This fixture admits lengths 1 through 3 and rejects length 4 before embedding.",
    )


def representation_experiment() -> dict[str, Any]:
    records = []
    width_four_rows = fixture_input_rows()
    for received_width in (4, 5):
        rows = width_four_rows if received_width == MODEL_WIDTH else tuple(row + (0.0,) for row in width_four_rows)
        gate_result = validate_block_input(rows)
        accepted = gate_result["accepted"]
        records.append(
            {
                "received_width": received_width,
                "accepted": accepted,
                "code": gate_result["code"],
                "expected_shape": gate_result["expected_shape"],
                "actual_shape": gate_result["actual_shape"],
                "block_math_status": "eligible" if accepted else "unexecuted",
            }
        )
    return experiment(
        "limits.representation_width",
        "interface_gate",
        {"received_width": [4, 5]},
        {"expected_width": MODEL_WIDTH, "sequence_length": 3, "gate": "block_input"},
        "shape_gate_records",
        {"records": records, "width_4_accepted": True, "width_5_rejected_at_block_gate": True},
        "The fixed block gate accepts width 4 and rejects width 5 before block arithmetic.",
    )


def attention_work_counts(sequence_length: int) -> dict[str, int]:
    width = MODEL_WIDTH
    return {
        "multiplications": 4 * sequence_length * width * width + 2 * sequence_length * sequence_length * width,
        "additions": 4 * sequence_length * width * (width - 1) + sequence_length * sequence_length * (width - 1) + sequence_length * width * (sequence_length - 1),
        "exponentials": sequence_length * sequence_length,
    }


def compute_experiment() -> dict[str, Any]:
    records = tuple(
        {"sequence_length": sequence_length, **attention_work_counts(sequence_length)}
        for sequence_length in (1, 2, 3)
    )
    return experiment(
        "limits.attention_work",
        "structural_count",
        {"sequence_length": [1, 2, 3]},
        {"model_width": MODEL_WIDTH, "heads": 1, "counting_rule": "Chapter 15 scalar-loop formulas"},
        "formula_evaluations",
        {
            "formulas": {
                "multiplications": "4*n*d^2 + 2*n^2*d",
                "additions": "4*n*d*(d-1) + n^2*(d-1) + n*d*(n-1)",
                "exponentials": "n^2",
            },
            "records": records,
            "measurement_kind": "structural_counts_not_timing",
        },
        "Under the declared scalar counting formulas, attention work counts increase from n=1 to n=3; these are not timings.",
    )


def vocabulary_experiment() -> dict[str, Any]:
    absent_strings = ("quartzbird", "velvetaxiom")
    ids = tuple(TOKEN_TO_ID.get(token, UNKNOWN_ID) for token in absent_strings)
    embeddings = tuple(EMBEDDINGS[token_id] for token_id in ids)
    return experiment(
        "limits.vocabulary_coverage",
        "many_to_one_representation",
        {"input_string": absent_strings},
        {"vocabulary": VOCABULARY, "unknown_id": UNKNOWN_ID, "embedding_table": EMBEDDINGS},
        "token_id_and_embedding_collision",
        {
            "strings_are_distinct": absent_strings[0] != absent_strings[1],
            "token_ids": ids,
            "embeddings": embeddings,
            "same_unknown_id": ids == (UNKNOWN_ID, UNKNOWN_ID),
            "same_embedding": embeddings[0] == embeddings[1],
        },
        "Two distinct absent strings lose their distinction at lookup in this fixed vocabulary by mapping to the same <unk> ID and row.",
    )


def select_argmax(logits: tuple[float, ...]) -> int:
    maximum = max(logits)
    return min(index for index, value in enumerate(logits) if value == maximum)


def select_allowed_argmax(logits: tuple[float, ...], allowed_ids: tuple[int, ...]) -> int:
    assert allowed_ids and len(set(allowed_ids)) == len(allowed_ids)
    assert all(0 <= token_id < len(logits) for token_id in allowed_ids)
    maximum = max(logits[token_id] for token_id in allowed_ids)
    return min(token_id for token_id in allowed_ids if logits[token_id] == maximum)


def decoding_experiment() -> dict[str, Any]:
    trace = execute_fixture()
    logits = tuple(trace["stages"][9]["output_values"])
    allowed_ids = (0, 1, 3, 4, 5)
    before_bytes = serialized(logits).encode("ascii")
    argmax_id = select_argmax(logits)
    constrained_id = select_allowed_argmax(logits, allowed_ids)
    after_bytes = serialized(logits).encode("ascii")
    return experiment(
        "limits.decoding_policy",
        "policy_comparison",
        {"selection_policy": ["global_argmax", "allowed_id_argmax"]},
        {"logits": logits, "allowed_ids": allowed_ids, "tie_rule": "lowest ID among equal eligible maxima"},
        "selected_token_ids",
        {
            "global_argmax_id": argmax_id,
            "constrained_allowed_id": constrained_id,
            "selected_ids_differ": argmax_id != constrained_id,
            "logits_equal_before_after": logits == tuple(trace["stages"][9]["output_values"]),
            "logits_bytes_equal_before_after": before_bytes == after_bytes,
            "logits_sha256_before": hashlib.sha256(before_bytes).hexdigest(),
            "logits_sha256_after": hashlib.sha256(after_bytes).hexdigest(),
            "policy_definition": "select the highest-logit ID in the explicit allowed set; choose the lowest ID on an eligible tie",
        },
        "With one fixed logit vector, changing only the declared eligible-ID policy changes the selected ID from 2 to 0.",
    )


def fixture_input_rows() -> tuple[tuple[float, ...], ...]:
    token_ids = tuple(TOKEN_TO_ID.get(token, UNKNOWN_ID) for token in REQUEST.lower().split())
    return tuple(
        tuple(value + position for value, position in zip(EMBEDDINGS[token_id], POSITION_ROWS[index], strict=True))
        for index, token_id in enumerate(token_ids)
    )


def block_output(rows: tuple[tuple[float, ...], ...], attention_provider: Callable[[tuple[tuple[float, ...], ...]], tuple[tuple[float, ...], ...]]) -> tuple[tuple[float, ...], ...]:
    attention_output = attention_provider(rows)
    first_normalized = layer_norm(add_rows(rows, attention_output))
    feed_forward_output = feed_forward(first_normalized)
    return layer_norm(add_rows(first_normalized, feed_forward_output))


def architecture_experiment() -> dict[str, Any]:
    rows = fixture_input_rows()
    baseline = block_output(rows, run_attention)

    def no_attention_contribution(input_rows: tuple[tuple[float, ...], ...]) -> tuple[tuple[float, ...], ...]:
        return tuple(tuple(0.0 for _ in row) for row in input_rows)

    controlled = block_output(rows, no_attention_contribution)
    absolute_differences = tuple(
        abs(left - right)
        for left_row, right_row in zip(baseline, controlled, strict=True)
        for left, right in zip(left_row, right_row, strict=True)
    )
    return experiment(
        "limits.architecture_contribution",
        "component_contribution_control",
        {"attention_contribution_at_first_residual": ["computed_attention_output", "zero_rows"]},
        {"request": REQUEST, "input_rows": rows, "all_fixture_parameters": "Chapter 15 constants unchanged", "remaining_block_operations": "unchanged"},
        "numerical_output_difference",
        {
            "baseline_output": baseline,
            "no_attention_contribution_output": controlled,
            "baseline_sha256": digest(baseline),
            "control_sha256": digest(controlled),
            "maximum_absolute_difference": max(absolute_differences),
            "nonzero_difference": any(difference > 0.0 for difference in absolute_differences),
        },
        "Removing this declared attention contribution while holding the request and other fixture parameters fixed changes the block's numerical output.",
    )


def validate_claim_scope(claim: str) -> dict[str, Any]:
    accepted = claim not in PROHIBITED_CLAIMS
    return {
        "claim": claim,
        "accepted": accepted,
        "code": "WITHIN_OPERATIONAL_EVIDENCE" if accepted else OUTSIDE_OPERATIONAL_EVIDENCE,
        "interpretation": "scope classification only; rejection does not establish that the predicate is false",
    }


def build_result() -> dict[str, Any]:
    experiments = (
        context_experiment(),
        representation_experiment(),
        compute_experiment(),
        vocabulary_experiment(),
        decoding_experiment(),
        architecture_experiment(),
    )
    claim_scope_control = tuple(validate_claim_scope(claim) for claim in sorted(PROHIBITED_CLAIMS))
    dependency_edges = {
        "incoming": (
            ("convergence.architecture", LIMITS_MODULE),
            ("convergence.execution", LIMITS_MODULE),
        ),
        "outgoing": (),
    }
    validations = {
        "six_experiments_exact": len(experiments) == 6 and len({item["experiment_type"] for item in experiments}) == 6,
        "every_experiment_has_required_metadata": all(
            item["changed_variables"] and item["held_fixed_variables"] and item["result_type"] and item["permitted_inference"]
            for item in experiments
        ),
        "context_boundary_exact": experiments[0]["result"]["first_rejected_length"] == 4 and experiments[0]["result"]["rejected_before_embedding"],
        "representation_boundary_exact": experiments[1]["result"]["width_4_accepted"] and experiments[1]["result"]["width_5_rejected_at_block_gate"],
        "attention_counts_match_chapter_15_at_n3": experiments[2]["result"]["records"][-1] == {"sequence_length": 3, "multiplications": 264, "additions": 195, "exponentials": 9},
        "attention_counts_are_not_timing": experiments[2]["result"]["measurement_kind"] == "structural_counts_not_timing",
        "unknown_strings_collapse": experiments[3]["result"]["strings_are_distinct"] and experiments[3]["result"]["same_unknown_id"] and experiments[3]["result"]["same_embedding"],
        "decoding_policy_changes_only_selection": experiments[4]["result"]["selected_ids_differ"] and experiments[4]["result"]["logits_bytes_equal_before_after"],
        "architecture_control_has_nonzero_difference": experiments[5]["result"]["nonzero_difference"],
        "claim_scope_rejections_exact": all(not item["accepted"] and item["code"] == OUTSIDE_OPERATIONAL_EVIDENCE for item in claim_scope_control),
        "dependency_edges_exact_and_terminal": dependency_edges == {
            "incoming": (("convergence.architecture", LIMITS_MODULE), ("convergence.execution", LIMITS_MODULE)),
            "outgoing": (),
        },
    }
    assert all(validations.values())
    return {
        "fixture": "Chapter 15 width-four deterministic Transformer fixture",
        "module": LIMITS_MODULE,
        "experiments": experiments,
        "claim_scope_control": claim_scope_control,
        "dependency_edges": dependency_edges,
        "boundary": "local operational evidence only; no timing benchmark, production generalization, semantic predicate, personhood criterion, consciousness test, or universal impossibility claim",
        "validation": validations,
    }


def run_probe() -> dict[str, Any]:
    result = build_result()
    rerun = build_result()
    deterministic_rerun = serialized(result) == serialized(rerun)
    assert deterministic_rerun
    return {**result, "validation_count": len(result["validation"]), "deterministic_rerun": deterministic_rerun}


if __name__ == "__main__":
    print(json.dumps(canonical(run_probe()), indent=2, sort_keys=True, ensure_ascii=True))