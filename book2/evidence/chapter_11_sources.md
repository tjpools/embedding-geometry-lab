# Chapter 11 Source Ledger — The Transformer

**Status:** Source basis established August 14, 2026  
**Scope:** transformer block assembly, multi-head attention context, residual interfaces, and layer normalization boundaries  
**Chapter brief:** [../chapter_briefs/chapter_11.md](../chapter_briefs/chapter_11.md)

## Source Standard

The Chapter 11 probe is the authority for all fixture tensors, equations, intermediate rows, and controls. Primary architecture papers define the canonical component interfaces and historical rationale. Source claims remain bounded to what the papers and probe directly support.

## Sources

### S1 — Attention Is All You Need

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin, “Attention Is All You Need,” *Advances in Neural Information Processing Systems 30*, 2017.

- URL: https://arxiv.org/abs/1706.03762
- Accessed: August 14, 2026
- Authority: primary peer-reviewed Transformer architecture paper
- Supports: scaled dot-product attention, multi-head attention, output projection after head concatenation, residual connections around sublayers, layer normalization placement in the original formulation, and positionwise feed-forward sublayers
- Limitation: Chapter 11 uses a fixed deterministic fixture with no training loop and no benchmark replication.

### S2 — Layer Normalization

Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E. Hinton, “Layer Normalization,” arXiv preprint, 2016.

- URL: https://arxiv.org/abs/1607.06450
- Accessed: August 14, 2026
- Authority: primary normalization method paper
- Supports: per-example normalization over hidden units with mean and variance in a layer-normalization formulation
- Limitation: The chapter uses the simplified fixed-parameter form with scale and shift set to identity and zero; it does not reproduce training experiments.

### S3 — Deep Residual Learning for Image Recognition

Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun, “Deep Residual Learning for Image Recognition,” *Proceedings of CVPR*, 2016.

- URL: https://arxiv.org/abs/1512.03385
- Accessed: August 14, 2026
- Authority: primary residual-learning architecture paper
- Supports: residual pathway principle that transformed outputs can be composed with identity paths across layers
- Limitation: The chapter does not claim Transformer residual interfaces are identical to image-model residual stacks or that ResNet results transfer directly.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| A Transformer block is a composition of interfaces, not attention alone. | S1, probe | Multi-head attention is one sublayer assembled with residual paths, normalization, and a feed-forward sublayer. |
| Multi-head rows normalize per query and may differ by head. | S1, probe | Each head computes its own normalized row; distinct heads can produce distinct distributions in the same fixture. |
| Residual equations are explicit architectural interfaces. | S1, S3, probe | Declared branch outputs are combined with identity paths before subsequent transformations. |
| Layer normalization can be checked by row mean/variance under a declared formula. | S2, probe | The probe verifies near-zero means and near-unit variances using the declared epsilon-stabilized formula. |
| A component-removal control can expose local contribution without proving global causal semantics. | probe | Zeroing projected attention changes block outputs in this fixture while leaving other declared components fixed. |

## Prohibited Inferences

These sources and this probe do not warrant claims that:

- this fixed fixture is trained or production-equivalent
- one block output establishes language understanding or semantic correctness
- a no-attention control here proves universal causal attribution rules for all Transformer models
- this chapter reproduces full token-through-machine execution (Chapter 15 scope)
- this chapter establishes the architecture-limits boundary (Chapter 16 scope)
- this chapter's deterministic fixture implies benchmark performance, throughput, or latency on any hardware