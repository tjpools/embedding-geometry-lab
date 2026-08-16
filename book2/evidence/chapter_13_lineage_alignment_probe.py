#!/usr/bin/env python3

import json
from dataclasses import asdict, dataclass
from typing import Any


ALIGNMENT_MODULE = "convergence.alignment"
ARCHITECTURE_MODULE = "convergence.architecture"


@dataclass(frozen=True)
class Lineage:
    lineage_id: str
    source_module: str
    role: str


@dataclass(frozen=True)
class DependencyEdge:
    source: str
    target: str


@dataclass(frozen=True)
class Export:
    export_id: str
    lineage_id: str
    source_module: str
    capability_id: str
    interface_id: str
    vocabulary: tuple[str, ...]


@dataclass(frozen=True)
class Requirement:
    requirement_id: str
    accepted_source_module: str
    required_capability_id: str
    required_interface_id: str


@dataclass(frozen=True)
class AcceptedMatch:
    requirement_id: str
    export_id: str
    lineage_id: str
    source_module: str
    capability_id: str
    interface_id: str


LINEAGES = (
    Lineage("ai", "ai.transformer", "declared component architecture"),
    Lineage("mathematics", "math.geometry", "numerical representation and transformation rules"),
    Lineage("programming", "programming.tools", "validated executable contracts"),
)

CANONICAL_INCOMING_EDGES = (
    DependencyEdge("ai.transformer", ALIGNMENT_MODULE),
    DependencyEdge("math.geometry", ALIGNMENT_MODULE),
    DependencyEdge("programming.tools", ALIGNMENT_MODULE),
)

OUTGOING_EDGE = DependencyEdge(ALIGNMENT_MODULE, ARCHITECTURE_MODULE)

EXPORTS = (
    Export(
        "ai.transformer.architecture",
        "ai",
        "ai.transformer",
        "component_architecture.ordered_relations",
        "alignment.architecture.v1",
        ("component", "transform", "relation"),
    ),
    Export(
        "math.geometry.rules",
        "mathematics",
        "math.geometry",
        "representation.declared_transform_compare",
        "alignment.geometry.v1",
        ("representation", "transform", "comparison"),
    ),
    Export(
        "programming.tools.contracts",
        "programming",
        "programming.tools",
        "implementation.validated_callable_contracts",
        "alignment.implementation.v1",
        ("implementation", "runtime", "callable"),
    ),
)

REQUIREMENTS = (
    Requirement(
        "requirement.architecture",
        "ai.transformer",
        "component_architecture.ordered_relations",
        "alignment.architecture.v1",
    ),
    Requirement(
        "requirement.geometry",
        "math.geometry",
        "representation.declared_transform_compare",
        "alignment.geometry.v1",
    ),
    Requirement(
        "requirement.implementation",
        "programming.tools",
        "implementation.validated_callable_contracts",
        "alignment.implementation.v1",
    ),
)


def typed_key(export: Export) -> tuple[str, str, str]:
    return export.source_module, export.capability_id, export.interface_id


def requirement_key(requirement: Requirement) -> tuple[str, str, str]:
    return (
        requirement.accepted_source_module,
        requirement.required_capability_id,
        requirement.required_interface_id,
    )


def align(
    edges: tuple[DependencyEdge, ...],
    exports: tuple[Export, ...],
    requirements: tuple[Requirement, ...] = REQUIREMENTS,
) -> dict[str, Any]:
    edge_sources = {edge.source for edge in edges if edge.target == ALIGNMENT_MODULE}
    accepted: list[AcceptedMatch] = []
    unsatisfied: list[str] = []
    duplicate_requirements: list[str] = []

    for requirement in requirements:
        matches = [
            export
            for export in exports
            if export.source_module in edge_sources
            and typed_key(export) == requirement_key(requirement)
        ]
        if len(matches) == 0:
            unsatisfied.append(requirement.requirement_id)
        elif len(matches) > 1:
            duplicate_requirements.append(requirement.requirement_id)
        else:
            export = matches[0]
            accepted.append(
                AcceptedMatch(
                    requirement.requirement_id,
                    export.export_id,
                    export.lineage_id,
                    export.source_module,
                    export.capability_id,
                    export.interface_id,
                )
            )

    accepted.sort(key=lambda match: match.requirement_id)
    return {
        "complete": not unsatisfied and not duplicate_requirements and len(accepted) == len(requirements),
        "accepted_matches": tuple(accepted),
        "unsatisfied_requirements": tuple(sorted(unsatisfied)),
        "duplicate_requirements": tuple(sorted(duplicate_requirements)),
        "preserved_lineage_ids": tuple(sorted(match.lineage_id for match in accepted)),
        "edge_sources": tuple(sorted(edge_sources)),
    }


def mismatch_reason(candidate: Export, requirement: Requirement) -> dict[str, Any]:
    checks = {
        "source_module_exact": candidate.source_module == requirement.accepted_source_module,
        "capability_id_exact": candidate.capability_id == requirement.required_capability_id,
        "interface_id_exact": candidate.interface_id == requirement.required_interface_id,
    }
    failed_fields = tuple(field for field, passed in checks.items() if not passed)
    return {
        "accepted": all(checks.values()),
        "code": "TYPED_CONTRACT_MISMATCH" if failed_fields else "TYPED_CONTRACT_MATCH",
        "checks": checks,
        "failed_fields": failed_fields,
    }


def serialized(document: dict[str, Any]) -> str:
    return json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def run_probe() -> dict[str, Any]:
    valid_alignment = align(CANONICAL_INCOMING_EDGES, EXPORTS)

    missing_programming_edges = tuple(
        edge for edge in CANONICAL_INCOMING_EDGES if edge.source != "programming.tools"
    )
    missing_programming = align(missing_programming_edges, EXPORTS)

    false_equivalence_export = Export(
        "math.geometry.architecture-label",
        "mathematics",
        "math.geometry",
        "representation.transform_label",
        "alignment.geometry.v1",
        ("transform", "architecture"),
    )
    architecture_requirement = next(
        requirement for requirement in REQUIREMENTS if requirement.requirement_id == "requirement.architecture"
    )
    false_equivalence = mismatch_reason(false_equivalence_export, architecture_requirement)
    shared_vocabulary = tuple(
        sorted(set(false_equivalence_export.vocabulary) & set(EXPORTS[0].vocabulary))
    )

    result = {
        "fixture": "deterministic standard-library three-lineage typed alignment",
        "boundary": (
            "aligns Chapter 13 interfaces only; no multi-scale architecture, inference trace, "
            "limits measurement, or philosophical interpretation"
        ),
        "lineages": tuple(asdict(lineage) for lineage in LINEAGES),
        "exports": tuple(asdict(export) for export in EXPORTS),
        "requirements": tuple(asdict(requirement) for requirement in REQUIREMENTS),
        "canonical_incoming_edges": tuple(asdict(edge) for edge in CANONICAL_INCOMING_EDGES),
        "valid_alignment": {
            **valid_alignment,
            "accepted_matches": tuple(asdict(match) for match in valid_alignment["accepted_matches"]),
        },
        "missing_programming_edge_control": {
            "incoming_edges": tuple(asdict(edge) for edge in missing_programming_edges),
            **missing_programming,
            "accepted_matches": tuple(asdict(match) for match in missing_programming["accepted_matches"]),
        },
        "vocabulary_only_false_equivalence_control": {
            "candidate_export": asdict(false_equivalence_export),
            "attempted_requirement": asdict(architecture_requirement),
            "shared_vocabulary": shared_vocabulary,
            "validation": false_equivalence,
        },
        "outgoing_edge": asdict(OUTGOING_EDGE),
    }

    rerun_valid_alignment = align(CANONICAL_INCOMING_EDGES, EXPORTS)
    rerun_missing_programming = align(missing_programming_edges, EXPORTS)
    rerun_false_equivalence = mismatch_reason(false_equivalence_export, architecture_requirement)
    validation = {
        "canonical_edges_exact": CANONICAL_INCOMING_EDGES == (
            DependencyEdge("ai.transformer", "convergence.alignment"),
            DependencyEdge("math.geometry", "convergence.alignment"),
            DependencyEdge("programming.tools", "convergence.alignment"),
        ),
        "valid_alignment_complete": valid_alignment["complete"],
        "requirements_satisfied_exactly_once": len(valid_alignment["accepted_matches"]) == 3
        and not valid_alignment["duplicate_requirements"],
        "source_lineage_identity_preserved": valid_alignment["preserved_lineage_ids"]
        == ("ai", "mathematics", "programming"),
        "missing_programming_leaves_one_requirement": missing_programming["unsatisfied_requirements"]
        == ("requirement.implementation",),
        "false_equivalence_shares_transform": "transform" in shared_vocabulary,
        "false_equivalence_rejected": not false_equivalence["accepted"],
        "false_equivalence_specific_mismatch": false_equivalence["failed_fields"]
        == ("source_module_exact", "capability_id_exact", "interface_id_exact"),
        "outgoing_edge_exact": OUTGOING_EDGE
        == DependencyEdge("convergence.alignment", "convergence.architecture"),
        "deterministic_rerun_equality": (
            valid_alignment == rerun_valid_alignment
            and missing_programming == rerun_missing_programming
            and false_equivalence == rerun_false_equivalence
        ),
    }
    assert all(validation.values()), validation
    result["validation"] = validation
    return result


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2, sort_keys=True))