# Chapter 2 Visual — From Token to Coordinate

**Status:** Verified August 12, 2026  
**Canonical source:** [chapter_02_from_token_to_coordinate.svg](chapter_02_from_token_to_coordinate.svg)  
**Generator:** [chapter_02_from_token_to_coordinate.py](chapter_02_from_token_to_coordinate.py)  
**Data source:** [../evidence/chapter_02_representation_probe.py](../evidence/chapter_02_representation_probe.py)

**Production exports:**

- [full-size color PNG](chapter_02_from_token_to_coordinate.png)
- [full-size grayscale PNG](chapter_02_from_token_to_coordinate_grayscale.png)
- [100-pixel thumbnail](chapter_02_from_token_to_coordinate_thumbnail.png)

## Structural Reveal

A token becomes computable through several distinct mappings; no identifier, coordinate, or vector is the token's intrinsic meaning.

## Caption

Vocabulary assignment determines an identifier and one-hot coordinate, while a lookup table selects the vector used by later computation. Consistent renumbering changes `open` from identifier 3 and coordinate $[0,0,0,1]$ to identifier 1 and coordinate $[0,1,0,0]$ without changing the selected vector $(0.2,0.9,0.5)$.

## Alternative Text

A left-to-right structural diagram begins with source text containing a leading space, `OPEN`, and a trailing space. NFC normalization, case folding, and trimming produce `open`; whitespace splitting selects the token `open`. Two aligned lanes compare representation systems. In the base assignment, `open` maps to identifier 3, one-hot coordinate $[0,0,0,1]$ in dimension 4, and lookup vector $(0.2,0.9,0.5)$. Under a consistently permuted vocabulary and lookup table, `open` maps to identifier 1 and coordinate $[0,1,0,0]$ but selects the same vector $(0.2,0.9,0.5)$. A subordinate annotation states that, under the declared toy unknown policy, the distinct inputs `ajar` and `obstructed` both map to identifier 0 and vector $(0,0,0)$, so that distinction is discarded.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 12, 2026
- Originality: Original programmatic composition generated from the verified Chapter 2 probe
- External assets: None
- Typeface: DejaVu Sans
- Palette: Locked Book Two functional colors from [../VISUAL_LANGUAGE.md](../VISUAL_LANGUAGE.md)
- Format: SVG, 1200 × 760 view box
- Deterministic SVG SHA-256: `db11c4e022939db14d23e4f1b1b2037c970b6ab0a749c1f6e65abf4fb9bbba48`

## Required Tests

| Test | Result |
|---|---|
| source values equal the verified probe output | pass |
| deterministic regeneration preserves the SVG hash | pass |
| SVG parses without error | pass |
| 1200 × 760 raster export is nonblank | pass |
| primary structure remains present at 100 pixels wide | pass |
| grayscale retains structural contrast | pass |
| labels and arrows do not rely on color alone | pass |
| exactly one Chapter 2 SVG anchor remains in the production package | pass |

The first raster pass exposed a clipped permutation label and arrow markers that did not survive the available SVG renderer. The label was split and the markers were replaced with explicit arrowheads before this record was promoted.