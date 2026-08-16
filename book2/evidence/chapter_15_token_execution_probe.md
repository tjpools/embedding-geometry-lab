# Chapter 15 Probe — A Token Through the Machine

**Status:** Verified August 14, 2026  
**Implementation:** [chapter_15_token_execution_probe.py](chapter_15_token_execution_probe.py)  
**Dependencies:** Python standard library only  
**Chapter brief:** [../chapter_briefs/chapter_15.md](../chapter_briefs/chapter_15.md)

## Claim Under Test

One fixed request can pass through an ordered sequence of validated representations from text to a decoded token. Every executed stage records input and output shape, an operation category, allocated output elements, bounded work counts, and concrete values or a deterministic digest. A malformed embedding width must stop execution at the first block-input gate.

## Fixed Fixture

The request is `small models run`. The vocabulary is `(<unk>, small, models, run, clear, steps)`, with IDs assigned by tuple position. Any absent token maps to ID 0, `<unk>`. The request therefore tokenizes to `(small, models, run)` and maps to IDs `[1, 2, 3]`.

The fixture has three positions, model width four, feed-forward width five, one attention head, fixed embedding and position rows, fixed block matrices, and a fixed $4\times6$ vocabulary projection. It is not trained and has no external tokenizer or weights.

## Ordered Trace

| Order | Stage | Output shape | Concrete result or digest | Recorded work |
|---:|---|---|---|---|
| 1 | tokenize | `[3]` | `small`, `models`, `run` | 15 character scans |
| 2 | token IDs | `[3]` | `[1, 2, 3]` | 3 vocabulary lookups |
| 3 | embedding + position | `[3,4]` | rows below | 3 lookups, 12 additions |
| 4 | block-input validation | `[3,4]` | accepted; SHA prefix `3d60dbf4a2` | 2 dimension comparisons |
| 5 | attention | `[3,4]` | SHA prefix `a217a4333f` | 264 multiplications, 195 additions, 9 exponentials |
| 6 | residual + norm 1 | `[3,4]` | SHA prefix `dff2601203` | 12 residual additions, 12 normalized elements |
| 7 | feed-forward | `[3,4]` | SHA prefix `8514b58921` | 120 multiplications, 27 bias additions, 15 ReLU comparisons |
| 8 | residual + norm 2 | `[3,4]` | SHA prefix `e241693a93` | 12 residual additions, 12 normalized elements |
| 9 | final-position hidden | `[4]` | `[1.591346871, -0.368589077, -1.151836533, -0.070921261]` | 1 row selection |
| 10 | vocabulary projection | `[6]` | logits below | 24 multiplications, 18 additions |
| 11 | argmax | scalar | ID 2 | 5 comparisons, 1 tie-rule operation |
| 12 | decode | scalar | `models` | 1 vocabulary lookup |

The embedding-plus-position rows are:

```text
[[ 0.2, 0.0,  0.4, 0.4],
 [-0.2, 0.5,  0.2,-0.2],
 [ 0.4, 0.1, -0.1, 0.1]]
```

The vocabulary logits in ID order are:

```text
[0.285293940, -0.522753373, 0.887095515,
 -0.307293775, -0.946629078, 0.082931676]
```

The unique maximum is `0.887095515` at ID 2. The declared tie rule is to choose the lowest ID among equal maxima, so the rule remains deterministic even though this result is not tied. ID 2 decodes to `models`.

Allocated-element and work counts describe this fixture's constructed outputs and declared arithmetic. They are not elapsed time, latency, throughput, hardware utilization, memory-byte traffic, or a runtime benchmark.

## Width-Corruption Control

The control changes only the embedding output width by appending one zero coordinate to every row. Tokenization and ID lookup execute, and the corrupted embedding stage produces shape `[3,5]`. The first block-input validation expects `[3,4]` and returns:

```text
BLOCK_INPUT_WIDTH_MISMATCH
```

The first failed stage is `block_input_validation`. Attention, both residual/normalization stages, feed-forward computation, final-row selection, vocabulary projection, argmax, and decode are all recorded as `unexecuted`. No result record is fabricated for any skipped operation.

## Validation Gates

Nineteen assertions verify the fixed request, known-token mapping, exact 12-stage order, every shape handoff, category/work/allocation metadata, value-or-digest coverage, block component shapes, final-row selection, vocabulary-sized logits, lowest-ID argmax rule, decode lookup, exact dependency edges, first-failure code, and complete downstream non-execution.

Two complete command-line runs produced byte-identical JSON. SHA-256: `484c4438d6a61629d718f4bb769c4f42b6a94e4213bbf98b707ba24be0c82b83`.

## Evidence Boundary

The trace establishes one deterministic fixture path only. It does not establish production model behavior, measured performance, model quality, semantic understanding, training behavior, sampling behavior, hardware efficiency, or the effects of varying constraints.