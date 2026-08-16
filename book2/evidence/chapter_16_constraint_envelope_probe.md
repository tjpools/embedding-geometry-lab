# Chapter 16 Probe — The Constraint Envelope

**Status:** Verified August 14, 2026  
**Implementation:** [chapter_16_constraint_envelope_probe.py](chapter_16_constraint_envelope_probe.py)  
**Dependencies:** Python standard library plus direct reuse of the standard-library Chapter 15 fixture  
**Chapter brief:** [../chapter_briefs/chapter_16.md](../chapter_briefs/chapter_16.md)

## Claim Under Test

The fixed width-four Transformer fixture operates inside a typed constraint envelope. Context, representation, structural work, vocabulary coverage, decoding policy, and architectural contribution can be varied separately and reported as local operational evidence without converting those records into timing, semantic, personhood, or universal impossibility claims.

## Typed Experiment Contract

Each of the six experiment records contains `changed_variables`, `held_fixed_variables`, `result_type`, a structured `result`, and one `permitted_inference`. Their result types are deliberately different. Acceptance boundaries, shape gates, formula counts, representation collisions, policy selections, and numerical differences do not share a scale or unit.

## Exact Results

| Type | Changed variable | Held fixed | Result | Permitted inference |
|---|---|---|---|---|
| context acceptance boundary | requested length 1, 2, 3, 4 | capacity 3; gate before embedding | lengths 1–3 accepted; 4 returns `CONTEXT_CAPACITY_EXCEEDED`; embedding unexecuted for 4 | this fixture rejects the first over-capacity request before embedding |
| representation interface gate | received width 4, 5 | expected width 4; length 3; block-input gate | 4 accepted; 5 returns `BLOCK_INPUT_WIDTH_MISMATCH`; block math unexecuted for 5 | this block interface enforces width 4 before arithmetic |
| structural count | sequence length 1, 2, 3 | width 4; one head; Chapter 15 scalar formulas | multiplication/addition/exponential counts are `72/51/1`, `160/116/4`, and `264/195/9` | declared work grows across these lengths; counts are not timing |
| vocabulary coverage | `quartzbird`, `velvetaxiom` | six-entry vocabulary; unknown ID 0; embedding table | both map to ID 0 and embedding `[0,0,0,0]` | this fixed lookup loses the distinction between these absent strings |
| decoding policy | global argmax vs allowed-ID argmax | Chapter 15 logits; allowed IDs `{0,1,3,4,5}`; lowest-ID tie rule | global ID 2; constrained ID 0; logit bytes unchanged at SHA-256 `af6666aa2915977123572c90a8f2a41fda50e830c57bd0da128481f070bd48ce` | policy alone can change the selected ID for fixed logits |
| architecture contribution | computed attention output vs zero contribution at first residual | request, input rows, fixture parameters, and remaining block operations | maximum absolute output difference `0.138179224`; baseline and control digests differ | this declared contribution changes this fixture's numerical output |

The constrained decoding rule is exact: among the explicit allowed IDs, select the highest logit and choose the lowest ID on an eligible tie. ID 2 is intentionally absent from that allowed set. ID 0 has the largest eligible logit, so the different selection follows from the rule rather than from mutated logits.

The architecture control reuses Chapter 15's actual embedding, position, attention, residual, normalization, and feed-forward functions and constants. It replaces only the attention output presented to the first residual addition with zero rows. The baseline output digest is `e241693a9373cd7586485ffd3bbe80467862c77678223d8feded9f88b0dc18af`; the control digest is `12646e35923002aa765247f5803e7b5ff81f68e42569310bf87c8902e23f6518`.

## Claim-Scope Control

The validator rejects `understands`, `is_person`, and `cannot_ever_understand` with:

```text
OUTSIDE_OPERATIONAL_EVIDENCE
```

The code classifies claim scope. It does not test those predicates and does not establish that any rejected predicate is false.

## Dependency Boundary

The exact incoming edges are:

```text
convergence.architecture -> convergence.limits
convergence.execution -> convergence.limits
```

The module declares no outgoing Book Two edge.

## Validation Gates

- exactly six distinct experiment types exist
- every experiment records changed variables, held-fixed variables, result type, and permitted inference
- context length 4 and width 5 stop before invalid downstream work
- the $n=3$ work record reproduces Chapter 15's `264/195/9` counts
- structural counts are explicitly not timing
- two distinct absent strings collide at both ID and embedding
- decoding changes selection while canonical logit bytes remain identical
- the architecture control produces a nonzero numerical difference
- all three unsupported claims receive the exact scope code
- incoming edges are exact and outgoing edges are empty
- two complete constructions and two command-line runs are byte-identical

Eleven embedded validations pass. Two command-line runs produced identical JSON with SHA-256 `f0eff86f8826caee1af09ba508ed170a568374b4bf898963e69f230281c460fa`.

## Evidence Boundary

These are local deterministic fixture records. They are not a performance benchmark, production evaluation, corpus judgment, universal scaling law, safety evaluation, semantic test, consciousness test, personhood criterion, proof of understanding, or proof that understanding is impossible.