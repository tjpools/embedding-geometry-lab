# Chapter 8 Brief — Learned Spaces

**Status:** Verified; Part II integrated  
**Part:** II — Learning Systems  
**Module:** `math.geometry`  
**Visual anchor:** **Neighborhoods in a Learned Space**

## Reader Entry

Chapters 2, 4, 6, and 7 established vectors, transformations, adjustment, and shaped computation. The reader may still treat proximity as intrinsic meaning, assume every similarity measure produces the same neighborhood, or infer that a visually coherent plot explains what a model has learned.

## Intended Exit

The reader can distinguish:

- a learned representation from an illustrative analysis fixture
- coordinates from the item represented
- a declared metric from an intrinsic relationship
- Euclidean distance from cosine similarity
- direction from displacement
- a rigid coordinate change from a geometry-changing transformation
- invertibility from distance preservation
- a neighborhood from a semantic conclusion
- a two-dimensional visual slice from a high-dimensional representation
- geometric evidence from interpretation

## Central Question

What must be declared before distances, directions, and neighborhoods in a learned representation become inspectable claims?

## Chapter Claim

Geometric analysis of learned representations requires a declared coordinate source, comparison rule, and transformation. Neighborhoods can differ across metrics and can change under an invertible transformation that does not preserve the selected metric. Geometry makes relations inspectable inside those choices; it does not make their semantic interpretation intrinsic or self-validating.

The [verified learned-space probe](../evidence/chapter_08_learned_space_probe.md) supports the metric and transformation claims. The [source ledger](../evidence/chapter_08_sources.md) grounds learned embedding and cosine-similarity claims.

## Chapter Result

For four declared two-dimensional coordinates, Euclidean distance makes `north` the nearest neighbor of `anchor`, while cosine similarity selects `east`. A 37-degree rotation preserves every pairwise Euclidean distance within $4.45\times10^{-16}$ and leaves the Euclidean neighbor unchanged. Invertible scaling by $(0.2,3.0)$ changes the Euclidean nearest neighbor from `north` to `east`. The probe demonstrates dependence on metric and transformation, not learned semantics.

## Dependency Alignment

**Incoming edges:**

| Source | Target | Inherited requirement |
|---|---|---|
| `math.matrices` | `math.geometry` | Linear maps provide explicit coordinate transformations. |
| `math.calculus` | `math.geometry` | Local change supports trajectories and sensitivity analysis in represented spaces. |
| `math.tensors` | `math.geometry` | Multi-axis numerical representations provide slices and points for declared geometric analysis. |

**Outgoing edge:**

| Source | Target | Destination | Handoff |
|---|---|---:|---|
| `math.geometry` | `convergence.alignment` | 13 | Geometric language becomes one interface through which the mathematical lineage is compared with AI and programming evidence. |

## Reader Movement

1. Define a learned representation as vectors produced under a model, task, data, and objective.
2. Separate learned vectors from the probe's illustrative coordinates.
3. Declare Euclidean distance and cosine similarity.
4. Compare the anchor's neighbors under both rules.
5. Rotate every point and test Euclidean invariance.
6. Apply invertible anisotropic scaling and observe a changed neighborhood.
7. Distinguish invertibility from metric preservation.
8. Bound what a low-dimensional plot can reveal.
9. Separate geometric regularity from semantic warrant.
10. Hand geometric assumptions toward later convergence analysis.

## Visual Anchor

**Neighborhoods in a Learned Space** is one geometric plot containing:

- the four declared base coordinates
- a solid Euclidean-neighbor relation from `anchor` to `north`
- a dashed cosine-neighbor relation from `anchor` toward `east`
- a rotated panel with the Euclidean neighborhood preserved
- an anisotropically scaled panel with `east` becoming Euclidean-nearest

**Structural reveal:** a neighborhood belongs to coordinates, a comparison rule, and transformations that preserve or alter that rule; it is not attached intrinsically to a label.

The figure must label its coordinates as illustrative and must not depict them as measured semantic truth.

## Verification Questions

- Is the coordinate source declared before geometric interpretation?
- Are Euclidean distance and cosine similarity defined separately?
- Do the two comparison rules select different neighbors in the base fixture?
- Does rigid rotation preserve every pairwise Euclidean distance?
- Is anisotropic scaling identified as invertible but not distance-preserving?
- Is the changed neighbor shown without claiming that an item's meaning changed?
- Are task, corpus, model, and objective retained as embedding context?
- Is a two-dimensional plot kept distinct from a full learned space?
- Are geometric relations kept distinct from semantic conclusions?
- Does the chapter avoid using geometry as an ontology of meaning or intelligence?

## Explicit Exclusions

This chapter does not train an embedding model, project a real high-dimensional embedding into two dimensions, run a clustering algorithm, establish causal or semantic truth from proximity, or claim that every learned dimension is interpretable. It does not treat invertibility as meaning preservation or define people by coordinate geometry.

## Narrative Transition

Chapter 8 completes the mathematical path into learned-space analysis. Chapter 9 returns to execution by adding ordered state, kernels, scheduling, and memory movement. Chapter 13 later uses the bounded geometric account at the three-lineage alignment interface.

## Drafting Gate

Prose began only after the probe, source ledger, and deterministic visual production package passed validation. The completed chapter preserves the brief's claim boundary and has passed probe, visual, link, analytics, source, and manuscript checks.