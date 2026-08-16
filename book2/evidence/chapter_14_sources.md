# Chapter 14 Source Ledger — Architecture in Full

**Status:** Source basis established August 14, 2026  
**Scope:** multi-scale architecture identity, exact containment, repeated block contracts, interface ownership, and bounded Transformer terminology  
**Chapter brief:** [../chapter_briefs/chapter_14.md](../chapter_briefs/chapter_14.md)

## Source Standard

The canonical dependency graph and verified repository probes are authoritative for module edges, fixture identifiers, dimensions, containment records, controls, and validation results. The primary Transformer paper supports only bounded architectural terminology. It does not define this repository's four-scale fixture or prove that an attention record explains a complete system.

## Repository Sources

### R1 — Canonical dependency graph

- Artifacts: [../dependencies.tsv](../dependencies.tsv) and [../dependency_map.md](../dependency_map.md)
- Supports: the incoming edge from `convergence.alignment` and the exact outgoing edges to `convergence.execution` and `convergence.limits`
- Limitation: dependency edges declare module handoffs, not runtime sequence, measured cost, or causation.

### R2 — Transformer block evidence

- Artifact: [chapter_11_transformer_block_probe.md](chapter_11_transformer_block_probe.md)
- Supports: attention, projection, residual/normalization, and feed-forward interfaces remain distinct inside a Transformer block
- Limitation: Chapter 14 inherits interface names but does not repeat Chapter 11 arithmetic or treat its single block as a complete system.

### R3 — Three-lineage alignment evidence

- Artifact: [chapter_13_lineage_alignment_probe.md](chapter_13_lineage_alignment_probe.md)
- Supports: `convergence.alignment` hands validated architecture, mathematical, and implementation contracts to `convergence.architecture`
- Limitation: alignment does not itself establish multi-scale containment.

### R4 — Four-scale architecture probe

- Artifact: [chapter_14_four_scales_probe.md](chapter_14_four_scales_probe.md)
- Supports: fixed identity and dimensions, exact acyclic containment, distinct repeated instances sharing one contract, scale-owned interfaces, deterministic equality, explicit scope rejection, and exact outgoing edges
- Limitation: the records declare structure only; they do not execute the architecture or measure its limits.

## External Source

### S1 — Attention Is All You Need

Ashish Vaswani et al., “Attention Is All You Need,” *Advances in Neural Information Processing Systems 30*, 2017.

- URL: https://arxiv.org/abs/1706.03762
- Accessed: August 14, 2026
- Authority: primary peer-reviewed Transformer architecture paper
- Supports: the Transformer uses repeated layers containing multi-head attention, positionwise feed-forward networks, residual connections, normalization, projections, and system-level input/output machinery
- Limitation: the paper does not define the fixture IDs, selected four-scale path, control code, or repository dependency graph.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| One architecture can be selected at four scales without changing identity. | R4 | The fixture preserves one architecture ID across system, stack, block, and operation views. |
| A repeated stack contains distinct instances satisfying one block contract. | R4, S1 | Repetition preserves contract identity while instance identifiers remain distinct. |
| Attention is contained within a larger block and system. | R2, R4, S1 | An attention operation is selected detail, not the whole architecture. |
| Containment is not execution order. | R1, R4 | Parent-child edges record ownership and zoom selection only. |
| One attention row is incomplete at system scope. | R4 | The control lacks system scope and both required system interfaces. |

## Prohibited Inferences

These sources do not warrant claims that inspection order is runtime order; that one attention row explains model reasoning, semantics, causation, or system behavior; that the fixed dimensions describe a production model; that architectural declaration performs inference; that outgoing edges measure constraints; or that technical structure settles questions of meaning, understanding, personhood, or intelligence.