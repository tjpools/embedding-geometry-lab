# Chapter 13 Probe — Three-Lineage Alignment

**Status:** Verified August 14, 2026  
**Implementation:** [chapter_13_lineage_alignment_probe.py](chapter_13_lineage_alignment_probe.py)  
**Dependencies:** Python standard library only  
**Chapter brief:** [../chapter_briefs/chapter_13.md](../chapter_briefs/chapter_13.md)

## Claim Under Test

The completed AI, mathematical, and programming lineages become operational together only when a canonical dependency edge and an exact typed export contract satisfy each destination requirement. Successful alignment preserves source identity; shared vocabulary does not establish compatibility or equivalence.

## Structured Fixture

The fixture declares three immutable lineage records, three dependency edges, three exports, and three requirements. Matching uses this exact key:

```text
(source_module, capability_id, interface_id)
```

No substring, token, fuzzy, or vocabulary comparison participates in acceptance.

| Requirement | Accepted source | Required capability | Required interface |
|---|---|---|---|
| `requirement.architecture` | `ai.transformer` | `component_architecture.ordered_relations` | `alignment.architecture.v1` |
| `requirement.geometry` | `math.geometry` | `representation.declared_transform_compare` | `alignment.geometry.v1` |
| `requirement.implementation` | `programming.tools` | `implementation.validated_callable_contracts` | `alignment.implementation.v1` |

The canonical incoming edges are exactly:

```text
ai.transformer -> convergence.alignment
math.geometry -> convergence.alignment
programming.tools -> convergence.alignment
```

The only outgoing edge is:

```text
convergence.alignment -> convergence.architecture
```

## Valid Alignment

Every requirement receives exactly one matching export. The accepted records retain the original lineage identifiers `ai`, `mathematics`, and `programming`, as well as their exact source modules. The assembled record is complete only when there are no unsatisfied or duplicate requirements.

## Missing-Programming Control

The control removes only the edge `programming.tools -> convergence.alignment` while retaining the programming export record. An export without its declared dependency edge cannot enter alignment. The architecture and geometry requirements remain satisfied; exactly one requirement remains unsatisfied:

```text
requirement.implementation
```

## Vocabulary-Only False Equivalence

The false candidate comes from `math.geometry`, uses capability `representation.transform_label`, and exposes `alignment.geometry.v1`. It attempts to satisfy `requirement.architecture`. Both the candidate and the valid AI export contain the vocabulary term `transform`, but exact validation rejects the candidate with `TYPED_CONTRACT_MISMATCH` because source module, capability identifier, and interface identifier all differ from the architecture requirement.

The control establishes only that vocabulary overlap is excluded from this matcher. It does not claim that all conceptual analogies are useless.

## Validation Gates

- canonical incoming edges equal the repository dependency graph exactly
- valid alignment is complete
- all three requirements are satisfied exactly once
- all three source lineage identities are preserved
- removing the programming edge leaves exactly the implementation requirement unsatisfied
- the false-equivalence candidate shares the term `transform`
- the false-equivalence candidate is rejected for exact source, capability, and interface mismatches
- the outgoing edge is exactly `convergence.alignment -> convergence.architecture`
- independently recomputed valid and control records are equal

All embedded assertions pass.

## Evidence Boundary

The fixture verifies one local typed alignment model. It does not claim that the three disciplines are identical, that mathematical transformations are Transformer components, or that an architecture specification is executable without programming contracts. It does not inspect Chapter 14 multi-scale architecture, trace Chapter 15 inference, measure Chapter 16 limits, or interpret the technical result through Book Three philosophy.