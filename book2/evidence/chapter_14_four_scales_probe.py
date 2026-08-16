#!/usr/bin/env python3

import json
from dataclasses import asdict, dataclass
from typing import Any


ARCHITECTURE_ID = "book2.transformer.architecture.01"
ARCHITECTURE_MODULE = "convergence.architecture"
BLOCK_CONTRACT_ID = "transformer.block.v1"


@dataclass(frozen=True)
class Dimensions:
    vocabulary: int
    context: int
    model: int
    heads: int
    head: int
    feed_forward: int
    blocks: int


@dataclass(frozen=True)
class ArchitectureView:
    view_id: str
    architecture_id: str
    scale: str
    selected_object_id: str
    parent_object_id: str | None
    child_object_ids: tuple[str, ...]
    visible_interfaces: tuple[str, ...]


@dataclass(frozen=True)
class ContainmentEdge:
    parent_id: str
    child_id: str


@dataclass(frozen=True)
class DependencyEdge:
    source: str
    target: str


DIMENSIONS = Dimensions(
    vocabulary=32_000,
    context=2_048,
    model=512,
    heads=8,
    head=64,
    feed_forward=2_048,
    blocks=3,
)

BLOCK_INSTANCE_IDS = (
    "architecture.01.stack.main.block.00",
    "architecture.01.stack.main.block.01",
    "architecture.01.stack.main.block.02",
)

BLOCK_INSTANCES = tuple(
    {
        "instance_id": instance_id,
        "position": position,
        "contract_id": BLOCK_CONTRACT_ID,
    }
    for position, instance_id in enumerate(BLOCK_INSTANCE_IDS)
)

VIEWS = (
    ArchitectureView(
        "view.system",
        ARCHITECTURE_ID,
        "system",
        "architecture.01.system",
        None,
        ("architecture.01.stack.main",),
        ("system.token_ids_in", "system.logits_out"),
    ),
    ArchitectureView(
        "view.stack",
        ARCHITECTURE_ID,
        "stack",
        "architecture.01.stack.main",
        "architecture.01.system",
        BLOCK_INSTANCE_IDS,
        ("stack.hidden_rows_in", "stack.hidden_rows_out", "stack.block_contract"),
    ),
    ArchitectureView(
        "view.block.01",
        ARCHITECTURE_ID,
        "block",
        "architecture.01.stack.main.block.01",
        "architecture.01.stack.main",
        (
            "architecture.01.stack.main.block.01.attention",
            "architecture.01.stack.main.block.01.residual_norm.01",
            "architecture.01.stack.main.block.01.feed_forward",
            "architecture.01.stack.main.block.01.residual_norm.02",
        ),
        (
            "block.hidden_rows_in",
            "block.attention_sublayer",
            "block.residual_norm_01",
            "block.feed_forward_sublayer",
            "block.residual_norm_02",
            "block.hidden_rows_out",
        ),
    ),
    ArchitectureView(
        "view.operation.attention",
        ARCHITECTURE_ID,
        "operation",
        "architecture.01.stack.main.block.01.attention",
        "architecture.01.stack.main.block.01",
        (
            "architecture.01.stack.main.block.01.attention.projections",
            "architecture.01.stack.main.block.01.attention.score",
            "architecture.01.stack.main.block.01.attention.softmax",
            "architecture.01.stack.main.block.01.attention.value_combination",
            "architecture.01.stack.main.block.01.attention.output_projection",
        ),
        (
            "attention.hidden_rows_in",
            "attention.qkv_projections",
            "attention.scaled_scores",
            "attention.normalized_rows",
            "attention.value_combination",
            "attention.output_projection",
            "attention.hidden_rows_out",
        ),
    ),
)

CONTAINMENT_EDGES = (
    ContainmentEdge("architecture.01.system", "architecture.01.stack.main"),
    *(ContainmentEdge("architecture.01.stack.main", block_id) for block_id in BLOCK_INSTANCE_IDS),
    ContainmentEdge(BLOCK_INSTANCE_IDS[1], f"{BLOCK_INSTANCE_IDS[1]}.attention"),
    ContainmentEdge(BLOCK_INSTANCE_IDS[1], f"{BLOCK_INSTANCE_IDS[1]}.residual_norm.01"),
    ContainmentEdge(BLOCK_INSTANCE_IDS[1], f"{BLOCK_INSTANCE_IDS[1]}.feed_forward"),
    ContainmentEdge(BLOCK_INSTANCE_IDS[1], f"{BLOCK_INSTANCE_IDS[1]}.residual_norm.02"),
    ContainmentEdge(f"{BLOCK_INSTANCE_IDS[1]}.attention", f"{BLOCK_INSTANCE_IDS[1]}.attention.projections"),
    ContainmentEdge(f"{BLOCK_INSTANCE_IDS[1]}.attention", f"{BLOCK_INSTANCE_IDS[1]}.attention.score"),
    ContainmentEdge(f"{BLOCK_INSTANCE_IDS[1]}.attention", f"{BLOCK_INSTANCE_IDS[1]}.attention.softmax"),
    ContainmentEdge(f"{BLOCK_INSTANCE_IDS[1]}.attention", f"{BLOCK_INSTANCE_IDS[1]}.attention.value_combination"),
    ContainmentEdge(f"{BLOCK_INSTANCE_IDS[1]}.attention", f"{BLOCK_INSTANCE_IDS[1]}.attention.output_projection"),
)

OUTGOING_EDGES = (
    DependencyEdge(ARCHITECTURE_MODULE, "convergence.execution"),
    DependencyEdge(ARCHITECTURE_MODULE, "convergence.limits"),
)

SYSTEM_REQUIRED_INTERFACES = frozenset(("system.token_ids_in", "system.logits_out"))


def has_cycle(edges: tuple[ContainmentEdge, ...]) -> bool:
    children: dict[str, list[str]] = {}
    for edge in edges:
        children.setdefault(edge.parent_id, []).append(edge.child_id)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        if any(visit(child_id) for child_id in children.get(node_id, ())):
            return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    nodes = {edge.parent_id for edge in edges} | {edge.child_id for edge in edges}
    return any(visit(node_id) for node_id in sorted(nodes))


def validate_system_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    interfaces = frozenset(candidate.get("visible_interfaces", ()))
    missing_interfaces = tuple(sorted(SYSTEM_REQUIRED_INTERFACES - interfaces))
    scope_complete = candidate.get("scope") == "system"
    accepted = scope_complete and not missing_interfaces
    return {
        "accepted": accepted,
        "code": "SYSTEM_SCOPE_COMPLETE" if accepted else "INCOMPLETE_SCOPE_MISSING_INTERFACES",
        "scope_complete": scope_complete,
        "missing_interfaces": missing_interfaces,
    }


def build_result() -> dict[str, Any]:
    expected_edges = (
        ContainmentEdge("architecture.01.system", "architecture.01.stack.main"),
        *(ContainmentEdge("architecture.01.stack.main", block_id) for block_id in BLOCK_INSTANCE_IDS),
        ContainmentEdge(BLOCK_INSTANCE_IDS[1], f"{BLOCK_INSTANCE_IDS[1]}.attention"),
        ContainmentEdge(BLOCK_INSTANCE_IDS[1], f"{BLOCK_INSTANCE_IDS[1]}.residual_norm.01"),
        ContainmentEdge(BLOCK_INSTANCE_IDS[1], f"{BLOCK_INSTANCE_IDS[1]}.feed_forward"),
        ContainmentEdge(BLOCK_INSTANCE_IDS[1], f"{BLOCK_INSTANCE_IDS[1]}.residual_norm.02"),
        ContainmentEdge(f"{BLOCK_INSTANCE_IDS[1]}.attention", f"{BLOCK_INSTANCE_IDS[1]}.attention.projections"),
        ContainmentEdge(f"{BLOCK_INSTANCE_IDS[1]}.attention", f"{BLOCK_INSTANCE_IDS[1]}.attention.score"),
        ContainmentEdge(f"{BLOCK_INSTANCE_IDS[1]}.attention", f"{BLOCK_INSTANCE_IDS[1]}.attention.softmax"),
        ContainmentEdge(f"{BLOCK_INSTANCE_IDS[1]}.attention", f"{BLOCK_INSTANCE_IDS[1]}.attention.value_combination"),
        ContainmentEdge(f"{BLOCK_INSTANCE_IDS[1]}.attention", f"{BLOCK_INSTANCE_IDS[1]}.attention.output_projection"),
    )
    attention_row_candidate = {
        "record_id": "attention.row.block.01.head.00.query.07",
        "architecture_id": ARCHITECTURE_ID,
        "scope": "operation_record",
        "visible_interfaces": ("attention.normalized_rows",),
        "row_length": DIMENSIONS.context,
        "interpretation": "one normalized attention row; not a system explanation",
    }
    scope_control = validate_system_candidate(attention_row_candidate)
    owned_interfaces = tuple(view.visible_interfaces for view in VIEWS)
    flattened_interfaces = tuple(interface for interfaces in owned_interfaces for interface in interfaces)

    validation = {
        "one_architecture_id_at_all_scales": {view.architecture_id for view in VIEWS} == {ARCHITECTURE_ID},
        "four_scales_exact": tuple(view.scale for view in VIEWS) == ("system", "stack", "block", "operation"),
        "containment_edges_exact": CONTAINMENT_EDGES == expected_edges,
        "containment_acyclic": not has_cycle(CONTAINMENT_EDGES),
        "selected_path_exact": tuple(view.selected_object_id for view in VIEWS)
        == (
            "architecture.01.system",
            "architecture.01.stack.main",
            "architecture.01.stack.main.block.01",
            "architecture.01.stack.main.block.01.attention",
        ),
        "dimensions_fixed_and_consistent": DIMENSIONS.model == DIMENSIONS.heads * DIMENSIONS.head
        and DIMENSIONS.feed_forward == 4 * DIMENSIONS.model
        and DIMENSIONS.blocks == len(BLOCK_INSTANCES),
        "block_instances_distinct": len({block["instance_id"] for block in BLOCK_INSTANCES}) == DIMENSIONS.blocks,
        "block_contract_shared": {block["contract_id"] for block in BLOCK_INSTANCES} == {BLOCK_CONTRACT_ID},
        "interfaces_owned_by_one_scale": len(flattened_interfaces) == len(set(flattened_interfaces)),
        "containment_not_execution_order": all(
            "execution" not in field
            for edge in CONTAINMENT_EDGES
            for field in (edge.parent_id, edge.child_id)
        ),
        "attention_row_rejected_for_incomplete_scope": not scope_control["accepted"]
        and not scope_control["scope_complete"],
        "attention_row_reports_missing_system_interfaces": scope_control["missing_interfaces"]
        == ("system.logits_out", "system.token_ids_in"),
        "outgoing_edges_exact": OUTGOING_EDGES
        == (
            DependencyEdge("convergence.architecture", "convergence.execution"),
            DependencyEdge("convergence.architecture", "convergence.limits"),
        ),
    }
    assert all(validation.values())

    return {
        "fixture": "deterministic standard-library four-scale architecture elevation",
        "architecture_id": ARCHITECTURE_ID,
        "dimensions": asdict(DIMENSIONS),
        "views": tuple(asdict(view) for view in VIEWS),
        "block_instances": BLOCK_INSTANCES,
        "containment_edges": tuple(asdict(edge) for edge in CONTAINMENT_EDGES),
        "relation_note": (
            "containment records ownership and zoom selection only; it does not declare runtime execution order"
        ),
        "attention_row_scope_substitution_control": {
            "candidate": attention_row_candidate,
            "result": scope_control,
        },
        "outgoing_edges": tuple(asdict(edge) for edge in OUTGOING_EDGES),
        "boundary": (
            "declares architecture only; no tokenization, execution trace, activation values, decoding, "
            "runtime benchmark, limits measurement, attention semantics, or philosophical interpretation"
        ),
        "validation": validation,
    }


def serialized(document: dict[str, Any]) -> str:
    return json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def run_probe() -> dict[str, Any]:
    result = build_result()
    rerun = build_result()
    deterministic_rerun = serialized(result) == serialized(rerun)
    assert deterministic_rerun
    return {**result, "deterministic_rerun": deterministic_rerun}


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2, sort_keys=True, ensure_ascii=True))