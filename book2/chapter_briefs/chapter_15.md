# Chapter 15 Brief — A Token Through the Machine

**Status:** Verified; Part IV integrated  
**Part:** IV — One Executable Architecture  
**Module:** `convergence.execution`  
**Visual anchor:** **A Token Through the Machine**

## Central Question

What concrete representations and runtime work records appear when one fixed request passes through a small Transformer fixture from text to decoded output?

## Chapter Claim

Execution is an ordered chain of validated representation handoffs. A deterministic fixture tokenizes a fixed request, maps IDs to embedding-plus-position rows, executes one declared Transformer block, projects the final row to vocabulary logits, selects one token ID by a declared rule, and decodes it. Every stage records shape, value or digest, and bounded runtime-work metadata. A corrupted embedding-width control is rejected at the first block-input gate, so downstream stages do not execute. The trace demonstrates one fixture path, not production model behavior, measured performance, semantic understanding, or model quality.

## Dependency Alignment

**Incoming edges:**

- `convergence.architecture -> convergence.execution` supplies the declared object and interfaces.
- `programming.runtimes -> convergence.execution` supplies execution, allocation, and operation-record concepts.

**Outgoing edge:** `convergence.execution -> convergence.limits` supplies an observed trace whose declared constraints Chapter 16 can vary and measure.

## Required Trace

1. Fixed input text and deterministic vocabulary tokenization.
2. Token IDs with explicit unknown-token behavior.
3. Fixed embeddings plus positional rows.
4. One small, fixed Transformer block with attention, residual/normalization, feed-forward, and second residual/normalization.
5. Final-position hidden row.
6. Fixed vocabulary projection logits.
7. Deterministic argmax selection with declared tie rule.
8. ID-to-token decoding and complete stage order.
9. Per-stage shape, digest/value, operation category, and allocated-element counts; these are not timing measurements.
10. Deterministic rerun equality.
11. Width-corruption control rejected at block input, with projection/selection/decode marked unexecuted.

## Visual Anchor

The execution trace must show the fixed text, IDs, numerical rows, block stages, logits, selected ID, and decoded token in runtime order. A subordinate failure lane must terminate visibly at the first invalid handoff. The diagram must distinguish values, shapes, and work records and state that counts are not latency.

## Explicit Exclusions

No external tokenizer or weights, training, sampling, beam search, cache, batching, hardware benchmark, production equivalence, quality claim, semantic inference, Chapter 16 parameter sweep, or Book Three philosophical interpretation.

## Verification Questions

- Is execution order distinct from Chapter 14 containment?
- Are all handoff shapes validated before use?
- Are concrete intermediate values or deterministic digests recorded?
- Does the selected token follow exactly from logits and tie rule?
- Are work counts kept distinct from elapsed time?
- Does corruption stop at the first invalid stage with later stages unexecuted?
- Is rerun output identical?

## Narrative Transition

Chapter 15 executes one bounded path. Chapter 16 will vary declared constraints around that path and report what changes without turning technical limits into an ontology.

## Drafting Gate

Prose begins only after the complete deterministic trace, first-failure control, bounded source ledger, and visual production package pass focused validation.
