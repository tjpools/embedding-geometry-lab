# Chapter 8 Visual — Neighborhoods in a Learned Space

**Status:** Verified August 13, 2026  
**Canonical source:** [chapter_08_learned_space.svg](chapter_08_learned_space.svg)  
**Generator:** [chapter_08_learned_space.py](chapter_08_learned_space.py)  
**Data source:** [../evidence/chapter_08_learned_space_probe.py](../evidence/chapter_08_learned_space_probe.py)

**Production exports:**

- [full-size color PNG](chapter_08_learned_space.png)
- [full-size grayscale PNG](chapter_08_learned_space_grayscale.png)
- [100-pixel thumbnail](chapter_08_learned_space_thumbnail.png)

## Structural Reveal

A neighborhood belongs to coordinates, a comparison rule, and transformations that preserve or alter that rule. It is not attached intrinsically to a label.

## Caption

For four illustrative coordinates, Euclidean distance selects `north` while cosine similarity selects `east`. A 37-degree rotation preserves the Euclidean neighborhood and all pairwise distances within floating-point tolerance. Invertible scaling by $(0.2,3.0)$ changes the Euclidean neighbor to `east`. The coordinates are not learned by this probe, and the changed neighborhood is not a semantic conclusion.

## Alternative Text

Three coordinate plots contain points named anchor, east, north, and west. In the base plot, a solid line joins anchor to north for Euclidean nearest distance, while a dashed line joins anchor toward east for greatest cosine similarity. In the rotated plot, the points turn 37 degrees and the solid anchor-to-north relation remains. In the scaled plot, the horizontal coordinates are compressed and vertical coordinates expanded; the solid nearest relation changes from north to east. A summary band reports Euclidean north, cosine east, rotation error 4.44 times ten to the minus 16, and after scaling east. A footer states that the coordinates are illustrative, not learned by the probe, and support no semantic conclusion.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 13, 2026
- Originality: original programmatic composition generated from the verified Chapter 8 probe
- External assets: none
- Typeface: DejaVu Sans
- Format: SVG, 1200 × 760 view box
- Deterministic SVG SHA-256: `b7e6c537e0097b43c74aca2132c0403517a7ffb8c9f0ab5a7e054f6eac587ebf`

## Required Tests

| Test | Result |
|---|---|
| coordinates, neighbors, transformations, and error derive from the verified probe | pass |
| SVG parses and rasterizes | pass |
| 1200 × 760 color export is nonblank | pass |
| 1200 × 760 grayscale export is nonblank | pass |
| base, rotated, and scaled relations remain recognizable at 100 pixels wide | pass |
| labels, solid relation, dashed relation, and panel order do not rely on color alone | pass |
| full-size points, labels, axes, and summary values do not clip or overlap | pass |
| changed neighborhood remains visible without implying changed semantics | pass |
| exactly one Chapter 8 anchor remains in the production package | pass |

The first probe fixture made the control point `west` unintentionally nearest after anisotropic scaling. Its declared coordinate was corrected before visual production so the counterexample isolates the intended `north`-to-`east` neighborhood change.