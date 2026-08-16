# Chapter 15 Source Ledger — A Token Through the Machine

**Status:** Source basis established August 14, 2026  
**Scope:** ordered representation handoffs, one fixed Transformer block, deterministic next-token selection, runtime work records, and first-failure control  
**Chapter brief:** [../chapter_briefs/chapter_15.md](../chapter_briefs/chapter_15.md)

## Source Standard

The verified Chapter 15 probe is authoritative for all fixture text, vocabulary IDs, numerical rows, logits, work counts, stage statuses, control behavior, and checksums. Repository architecture and runtime evidence support only their named incoming interfaces. The primary Transformer paper supports bounded component terminology, not the fixture's numerical result.

## Repository Sources

### R1 — Canonical dependency graph

- Artifacts: [../dependencies.tsv](../dependencies.tsv) and [../dependency_map.md](../dependency_map.md)
- Supports: exact incoming edges `convergence.architecture -> convergence.execution` and `programming.runtimes -> convergence.execution`; exact outgoing edge `convergence.execution -> convergence.limits`
- Limitation: edges declare handoffs, not measured causation or performance.

### R2 — Four-scale architecture evidence

- Artifact: [chapter_14_four_scales_probe.md](chapter_14_four_scales_probe.md)
- Supports: the block boundary contains attention, residual/normalization, feed-forward, and second residual/normalization interfaces; architecture containment is distinct from execution order
- Limitation: Chapter 14 supplies interfaces but no runtime values.

### R3 — Transformer block evidence

- Artifact: [chapter_11_transformer_block_probe.md](chapter_11_transformer_block_probe.md)
- Supports: actual arithmetic for attention, residual paths, normalization, and positionwise feed-forward computation in a bounded standard-library fixture
- Limitation: Chapter 15 uses its own smaller weights and extends the path through tokenization, vocabulary projection, selection, and decoding.

### R4 — Runtime-record precedent

- Artifacts: [chapter_09_recurrent_runtime_probe.md](chapter_09_recurrent_runtime_probe.md) and [../chapters/chapter_09.md](../chapters/chapter_09.md)
- Supports: ordered operation records and structural read/write/work counts can be reported without converting them into elapsed-time or byte-traffic claims
- Limitation: recurrent dependencies are not the Chapter 15 Transformer execution path.

### R5 — Token execution probe

- Artifact: [chapter_15_token_execution_probe.md](chapter_15_token_execution_probe.md)
- Supports: all exact stage values, shapes, operation categories, work and allocation counts, argmax/decode result, deterministic rerun, and width-control statuses
- Limitation: one tiny untrained fixture is not production evidence.

## External Source

### S1 — Attention Is All You Need

Ashish Vaswani et al., “Attention Is All You Need,” *Advances in Neural Information Processing Systems 30*, 2017.

- URL: https://arxiv.org/abs/1706.03762
- Accessed: August 14, 2026
- Authority: primary peer-reviewed Transformer architecture paper
- Supports: embedding plus positional information, attention, residual connections, layer normalization, positionwise feed-forward networks, and learned output projection followed by next-token probability machinery as canonical Transformer components
- Limitation: it does not define this vocabulary, weights, post-normalization fixture, work counts, failure code, logits, or decoded token.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Execution is an ordered chain of validated representation handoffs in this fixture. | R2, R4, R5 | The trace orders 12 stages and validates every executed shape before use. |
| The fixed block performs actual attention, residual/normalization, and feed-forward arithmetic. | R3, R5, S1 | Numerical outputs are computed from declared fixed matrices rather than fabricated records. |
| ID 2 is selected and decodes to `models`. | R5 | The maximum fixture logit is at ID 2; the fixed vocabulary maps ID 2 to `models`. |
| Width corruption prevents later execution. | R5 | Shape `[3,5]` is rejected where `[3,4]` is required, and all later stages are unexecuted. |
| Work counts are not performance measurements. | R4, R5 | Counts inventory bounded fixture operations and allocations only. |

## Prohibited Inferences

These sources do not warrant claims about production model equivalence, latency, throughput, hardware utilization, training, sampling quality, semantic understanding, causal interpretation, universal Transformer behavior, effects of parameter sweeps, or philosophical conclusions about intelligence.