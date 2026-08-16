# Chapter 8 Probe — Neighborhoods in a Learned Space

**Status:** Verified August 13, 2026  
**Implementation:** [chapter_08_learned_space_probe.py](chapter_08_learned_space_probe.py)  
**Dependencies:** Python standard library only

## Claims Under Test

1. Euclidean distance and cosine similarity can select different neighbors for the same coordinates.
2. A rigid rotation can preserve pairwise Euclidean distances and the Euclidean neighborhood.
3. An invertible anisotropic scaling can change the Euclidean neighborhood.

## Coordinate Status

The four points are declared illustrative coordinates:

| Label | Coordinate |
|---|---:|
| `anchor` | $(1,0)$ |
| `east` | $(2,0.2)$ |
| `north` | $(1.05,1)$ |
| `west` | $(-1,1)$ |

They are not learned by this probe and do not carry intrinsic semantic labels. The fixture tests geometric analysis rules that can later be applied to learned representations whose source is separately documented.

## Two Comparison Rules

Euclidean distance is

$$
d(u,v)=\sqrt{(u_1-v_1)^2+(u_2-v_2)^2}.
$$

Cosine similarity is

$$
s(u,v)=\frac{u\cdot v}{\lVert u\rVert\lVert v\rVert}.
$$

From `anchor`, the recorded comparisons are:

| Candidate | Euclidean distance | Cosine similarity |
|---|---:|---:|
| `east` | $1.0198039$ | $0.9950372$ |
| `north` | $1.0012492$ | $0.7241379$ |
| `west` | $2.2360680$ | $-0.7071068$ |

Euclidean distance selects `north`; cosine similarity selects `east`.

## Rotation Control

The probe rotates every point by 37 degrees around the origin. The maximum absolute change across all six pairwise Euclidean distances is approximately

$$
4.44\times10^{-16}.
$$

The Euclidean nearest neighbor remains `north`. This finite-precision result is consistent with rigid rotation preserving Euclidean distance.

## Anisotropic-Scaling Counterexample

The probe applies

$$
(x,y)\mapsto(0.2x,3y).
$$

Both scale factors are nonzero, so the map is invertible. It does not preserve Euclidean distance. After scaling, `east` becomes the Euclidean nearest neighbor of `anchor`, replacing `north`.

The counterexample separates two properties: a transformation can retain enough information to be inverted while changing the geometry selected for neighborhood analysis.

## Validation Gates

- Euclidean and cosine nearest neighbors differ in the base fixture
- rotation preserves pairwise Euclidean distances within $10^{-12}$
- rotation preserves the Euclidean nearest neighbor
- anisotropic scaling changes the Euclidean nearest neighbor from `north` to `east`
- both anisotropic scale factors are nonzero
- rerunning the probe produces identical structured output

All gates pass.

## Evidence Boundary

The probe establishes metric and transformation behavior for four fixed two-dimensional coordinates, one rotation, and one anisotropic scaling.

It does not establish:

- that the coordinates were learned
- semantic similarity, meaning, causation, or truth
- behavior of a real high-dimensional embedding model
- validity of a two-dimensional projection
- clustering quality or category boundaries
- that cosine or Euclidean comparison is universally appropriate
- that every invertible transformation preserves a useful interpretation
- that geometric analysis alone explains a model's behavior