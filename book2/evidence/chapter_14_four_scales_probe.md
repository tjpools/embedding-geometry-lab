# Chapter 14 Probe — One Architecture at Four Scales

**Status:** Verified August 14, 2026  
**Implementation:** [chapter_14_four_scales_probe.py](chapter_14_four_scales_probe.py)  
**Dependencies:** Python standard library only  
**Chapter brief:** [../chapter_briefs/chapter_14.md](../chapter_briefs/chapter_14.md)

## Claim Under Test

One architecture can be inspected at system, stack, block, and operation scales while preserving one architecture identity and exact parent-child containment. Each scale owns a distinct visible interface set. Selecting deeper detail does not turn containment into runtime order, and one attention row cannot substitute for the whole system.

## Structured Fixture

The fixed architecture identifier is `book2.transformer.architecture.01`. Its declared dimensions are:

| Dimension | Value |
|---|---:|
| vocabulary | 32,000 |
| context | 2,048 |
| model | 512 |
| heads | 8 |
| head | 64 |
| feed-forward | 2,048 |
| repeated blocks | 3 |

The dimension checks require $8 \times 64 = 512$ and $4 \times 512 = 2{,}048$. These are fixture declarations, not measured capacity or performance results.

## Four Views

| Scale | Selected object | Owned visible interfaces |
|---|---|---|
| system | `architecture.01.system` | token IDs in; logits out |
| stack | `architecture.01.stack.main` | hidden rows in/out; block contract |
| block | `architecture.01.stack.main.block.01` | attention; two residual/normalization boundaries; feed-forward; hidden rows in/out |
| operation | `architecture.01.stack.main.block.01.attention` | Q/K/V projections; scaled scores; normalized rows; value combination; output projection; hidden rows in/out |

All four records carry the same architecture ID. Their interface identifiers are unique across scales, so a system interface cannot silently appear as an operation-owned interface.

## Exact Containment

The system has exactly one stack child. The stack has exactly three block children. Block 01 has exactly attention, first residual/normalization, feed-forward, and second residual/normalization children. Its attention child has exactly projection, score, softmax, value-combination, and output-projection children.

The probe compares the complete edge tuple with an independently declared expected tuple and traverses the resulting graph to reject cycles. The selected inspection path is exactly:

```text
architecture.01.system
  contains architecture.01.stack.main
  contains architecture.01.stack.main.block.01
  contains architecture.01.stack.main.block.01.attention
```

This path records ownership and selection. It is explicitly not an execution trace.

## Repetition Without Identity Collapse

The repeated stack contains instance IDs `block.00`, `block.01`, and `block.02`. The three identifiers are distinct, their positions are distinct, and all share contract `transformer.block.v1`. Repetition therefore means several instances satisfy one structural contract; it does not mean one block record has been reused as three identities.

## Scope-Substitution Control

The control presents `attention.row.block.01.head.00.query.07` as a whole-system candidate. It carries architecture identity and one visible interface, `attention.normalized_rows`, but its declared scope is `operation_record`.

System validation returns:

```text
INCOMPLETE_SCOPE_MISSING_INTERFACES
```

The explicit missing interfaces are `system.token_ids_in` and `system.logits_out`. The result rejects the candidate both because its scope is incomplete and because it lacks the whole-system boundary. It does not infer semantics, causal explanation, or system behavior from the row.

## Dependency Boundary

The exact outgoing edges are:

```text
convergence.architecture -> convergence.execution
convergence.architecture -> convergence.limits
```

No other outgoing edge is admitted. The probe declares architecture for those later modules without tracing a request or measuring a constraint.

## Validation Gates

- one architecture ID is preserved at all four exact scales
- containment edges equal the declared edge tuple and are acyclic
- the selected system-to-attention containment path is exact
- dimensions are fixed and internally consistent
- three block instances are distinct and share one contract
- visible interfaces are owned by one scale each
- containment records contain no execution relation
- the attention row is rejected for incomplete scope and missing interfaces
- outgoing edges are exactly execution and limits
- independently recomputed records serialize identically

All embedded assertions pass. Two complete command-line runs produced identical JSON with SHA-256 `d096c45e27cf083e3af1d7344c8629476711cb038ca940257e1ef28ce2abd8cf`.

## Evidence Boundary

The fixture is a deterministic architecture declaration. It does not tokenize, execute a request, record activation values, decode output, benchmark runtime, measure context/compute/data constraints, infer meaning from attention, or make philosophical claims.