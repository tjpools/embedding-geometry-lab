# Chapter 4 Visual — A Map and Its Local Change

**Status:** Verified August 13, 2026  
**Canonical source:** [chapter_04_map_and_local_change.svg](chapter_04_map_and_local_change.svg)  
**Generator:** [chapter_04_map_and_local_change.py](chapter_04_map_and_local_change.py)  
**Data source:** [../evidence/chapter_04_map_and_local_change_probe.py](../evidence/chapter_04_map_and_local_change_probe.py)

**Production exports:**

- [full-size color PNG](chapter_04_map_and_local_change.png)
- [full-size grayscale PNG](chapter_04_map_and_local_change_grayscale.png)
- [100-pixel thumbnail](chapter_04_map_and_local_change_thumbnail.png)

## Structural Reveal

A matrix can describe a complete linear transformation, while a Jacobian describes first-order change only near its declared evaluation point.

## Caption

The fixed matrix transforms the complete coordinate field on the left. On the right, the nonlinear map's actual displacement near $p=(0.6,-0.8)$ nearly coincides with the directional change predicted by $J_f(p)$; the agreement is local, not a claim that the nonlinear map equals its Jacobian globally.

## Alternative Text

A vertical divider separates two uses of matrices. On the left, a square coordinate grid is transformed into a slanted grid by the matrix with rows $(1,0.5)$ and $(-0.25,1)$, illustrating one global linear map. On the right, a highlighted neighborhood surrounds the mapped point $f(p)$ for $p=(0.6,-0.8)$. A thick solid arrow shows the nonlinear map's actual short displacement in direction $(0.3,-0.2)$, while a dashed arrow shows the displacement predicted by the Jacobian at $p$; their endpoints nearly coincide. Text states that local agreement is not global identity.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 13, 2026
- Originality: original programmatic composition generated from the verified Chapter 4 probe
- External assets: none
- Typeface: DejaVu Sans
- Format: SVG, 1200 × 760 view box
- Deterministic SVG SHA-256: `fe1f5ddd5adf3e08da313cfe35f704eba34e8f0c95c9560247d7243c62ad667c`

## Required Tests

| Test | Result |
|---|---|
| source values equal the verified probe output | pass |
| SVG parses and rasterizes | pass |
| 1200 × 760 color export is nonblank | pass |
| 1200 × 760 grayscale export is nonblank | pass |
| primary two-part distinction remains present at 100 pixels wide | pass |
| labels and line styles do not rely on color alone | pass |
| no clipping or incoherent overlap in full-size visual inspection | pass |
| exactly one Chapter 4 anchor remains in the production package | pass |
