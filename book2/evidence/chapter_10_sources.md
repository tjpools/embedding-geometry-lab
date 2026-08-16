# Chapter 10 Source Ledger — Attention Changes the Path

**Status:** Source basis established August 14, 2026  
**Scope:** learned alignment, scaled dot-product self-attention, masking, path length, and interpretation limits  
**Chapter brief:** [../chapter_briefs/chapter_10.md](../chapter_briefs/chapter_10.md)

## Source Standard

The executable probe is the authority for all fixture scores, weights, contributions, outputs, controls, and abstract graph counts. Historical papers ground the development and implementation of attention. Interpretation studies bound claims made from attention weights but do not establish one universal verdict for every architecture and use.

## Sources

### S1 — Jointly Learning to Align and Translate

Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio, “Neural Machine Translation by Jointly Learning to Align and Translate,” *International Conference on Learning Representations*, 2015.

- URL: https://arxiv.org/abs/1409.0473
- Accessed: August 14, 2026
- Authority: primary peer-reviewed architecture and evaluation paper
- Supports: learned soft alignment over source positions as an alternative to encoding a complete source sentence into one fixed-length vector for the paper's recurrent translation system
- Limitation: Its alignment mechanism is not identical to Transformer self-attention, and its translation results do not establish that attention weights are general semantic or causal explanations.

### S2 — Attention Is All You Need

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin, “Attention Is All You Need,” *Advances in Neural Information Processing Systems 30*, 2017.

- URL: https://arxiv.org/abs/1706.03762
- Accessed: August 14, 2026
- Authority: primary peer-reviewed Transformer architecture paper
- Supports: scaled dot-product attention, multi-head attention, masking in decoder self-attention, comparison of maximum path lengths, and the reported machine-translation experiments
- Limitation: Chapter 10 implements one fixed head without learned projections or training. The paper's benchmark results remain attached to its models, tasks, hardware, and training setup.

### S3 — Attention Is Not Explanation

Sarthak Jain and Byron C. Wallace, “Attention Is Not Explanation,” *Proceedings of NAACL-HLT*, 2019.

- URL: https://arxiv.org/abs/1902.10186
- Accessed: August 14, 2026
- Authority: primary peer-reviewed empirical interpretation study
- Supports: experiments finding weak or inconsistent relationships between learned attention weights and several feature-importance measures, including materially different attention distributions with similar predictions in studied models
- Limitation: The findings belong to the evaluated tasks and architectures. They do not prove that every attention visualization is useless or settle every definition of explanation.

### S4 — Is Attention Interpretable?

Sofia Serrano and Noah A. Smith, “Is Attention Interpretable?” *Proceedings of ACL*, 2019.

- URL: https://arxiv.org/abs/1906.03731
- Accessed: August 14, 2026
- Authority: primary peer-reviewed intervention study
- Supports: attention magnitude was not a fail-safe indicator of input importance in the studied text-classification models; perturbation effects can differ from rankings by raw weight
- Limitation: The study does not imply that weights never correlate with effects, and Chapter 10's value-only control is an arithmetic fixture rather than a reproduction of its model interventions.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Attention introduced learned weighting over sequence positions before the Transformer. | S1 | Learned soft alignment let the studied recurrent decoder combine source annotations instead of relying only on one fixed-length source vector. |
| Transformer attention computes normalized weighted value combinations. | S2, probe | Scaled query-key scores produce weights; those weights scale values that are summed into outputs. |
| Self-attention shortens abstract dependency paths between positions. | S2, probe | In the declared graphs, $v_1$ contributes directly to $o_5$ while recurrent $x_1$ reaches $h_5$ through intervening states. |
| Weight magnitude alone is not a sufficient causal explanation. | S3, S4, probe | Interpretation requires evidence beyond displaying a normalized attention row. |
| Masking is an architectural exclusion rule. | S2, probe | A causal mask removes future positions from the admitted score set before normalization. |

## Prohibited Inferences

The sources and probe do not warrant claims that attention weights are posterior probabilities, a highest-weight token caused an output, attention is always interpretable or never useful for interpretation, direct graph paths guarantee lower latency, masking is learned irrelevance, one head represents a complete Transformer, or the paper's translation benchmarks generalize to every model and workload.