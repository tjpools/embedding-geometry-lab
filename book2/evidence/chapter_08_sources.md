# Chapter 8 Source Ledger — Learned Spaces

**Status:** Source basis established August 13, 2026  
**Scope:** learned vector representations, embedding-space interpretation, metric choice, and geometric limits

## Sources

### S1 — Mikolov et al.

Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg S. Corrado, and Jeff Dean, “Distributed Representations of Words and Phrases and their Compositionality,” *Advances in Neural Information Processing Systems 26*, 2013.

- URL: https://proceedings.neurips.cc/paper/2013/hash/9aa42b31882ec039965f3c4923ce901b-Abstract.html
- Accessed: August 13, 2026
- Authority: primary peer-reviewed machine-learning paper
- Supports: training distributed word and phrase vector representations; observed syntactic and semantic relationships under the paper's models and evaluation tasks; stated limitations involving word order and idiomatic phrases
- Limitation: The Chapter 8 probe does not train Skip-gram, use a corpus, reproduce the paper's evaluations, or treat its illustrative labels as words with learned semantics.

### S2 — Google Machine Learning Crash Course

Google, “Embeddings: Embedding space and static embeddings,” *Machine Learning Crash Course*, updated August 25, 2025.

- URL: https://developers.google.com/machine-learning/crash-course/embeddings/embedding-space
- Accessed: August 13, 2026
- Authority: official technical educational material
- Supports: embeddings as vector representations; mathematical comparison of relative positions; task dependence; high dimensionality; frequent difficulty of interpreting individual dimensions; corpus dependence of static word embeddings
- Limitation: Its food examples are pedagogical illustrations. Relative position is a property of a model's representation and does not by itself establish semantic truth.

### S3 — scikit-learn Cosine Similarity Reference

scikit-learn Developers, “cosine_similarity,” *scikit-learn API Reference*.

- URL: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
- Accessed: August 13, 2026
- Authority: official API reference
- Supports: cosine similarity as the normalized dot product $\langle X,Y\rangle/(\lVert X\rVert\lVert Y\rVert)$
- Limitation: The probe implements the formula with the Python standard library and does not use scikit-learn or establish cosine similarity as the correct measure for every representation.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Models can learn vector representations whose relative positions are analyzed geometrically. | S1, S2 | Learned embeddings are model-, data-, task-, and objective-dependent numerical representations. |
| Learned-space dimensions need not have simple human-readable meanings. | S2 | Geometric relations may be inspectable even when individual axes are not readily interpretable. |
| Cosine similarity is a normalized dot product. | S3 | In the fixture, cosine and Euclidean comparison select different neighbors. |
| A metric determines a neighborhood relation. | S2, S3, probe | The same coordinates require a declared comparison rule before “nearest” is well-defined. |
| Coordinate transformations can preserve or alter selected geometric relations. | derivation, probe | Rotation preserves the recorded Euclidean distances; anisotropic scaling changes the recorded Euclidean neighbor. |

## Prohibited Inferences

The sources and probe do not warrant claims that proximity is meaning, every embedding axis has an interpretable concept, a two-dimensional plot faithfully represents a high-dimensional space, cosine similarity is universally superior, geometric regularity establishes understanding, or learned representation settles semantic interpretation.