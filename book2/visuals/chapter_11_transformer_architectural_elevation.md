# Chapter 11 Visual — Transformer Architectural Elevation

**Status:** Verified August 14, 2026  
**Canonical source:** [chapter_11_transformer_architectural_elevation.svg](chapter_11_transformer_architectural_elevation.svg)  
**Generator:** [chapter_11_transformer_architectural_elevation.py](chapter_11_transformer_architectural_elevation.py)  
**Data source:** [../evidence/chapter_11_transformer_block_probe.py](../evidence/chapter_11_transformer_block_probe.py)

**Production exports:**

- [full-size color PNG](chapter_11_transformer_architectural_elevation.png)
- [full-size grayscale PNG](chapter_11_transformer_architectural_elevation_grayscale.png)
- [100-pixel thumbnail](chapter_11_transformer_architectural_elevation_thumbnail.png)

## Structural Reveal

Attention is one component interface inside a larger ordered assembly. The transformer block is formed by the composition boundaries between projections, multi-head attention, residual pathways, normalization, and feed-forward transformation.

## Caption

The elevation traces one deterministic four-row transformer block fixture from representation-plus-position entry through fixed Q/K/V projections, two distinct normalized heads, concatenation and output projection, first residual-plus-normalization, positionwise feed-forward transformation, and second residual-plus-normalization. A no-attention control sets the projected multi-head branch to zero before the first residual and changes final outputs at every row. The figure demonstrates interface composition, not training quality, runtime performance, or end-to-end model behavior.

## Alternative Text

A horizontal pipeline begins with input token rows and positional rows, combines them, projects Q K V, runs two attention heads, concatenates and projects, then applies residual plus normalization. A left panel shows query row four weights for head one and head two, both summing to one but with different values. A right panel reports projected attention row four and notes that row means are near zero and row variances near one after normalization. A lower lane shows positionwise feed-forward followed by the second residual plus normalization and a final row four output. A control band states that setting projected attention to zero changes final outputs and lists per-row difference norms. A footer states that attention alone is not the transformer and the fixture is deterministic, fixed, and not production-equivalent.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 14, 2026
- Originality: original programmatic composition generated from the verified Chapter 11 probe
- External assets: none
- Typeface: DejaVu Sans
- Format: SVG, 1200 × 760 view box
- Deterministic SVG SHA-256: `6e1ab3d631b29066bfbd77bb0dddf23ec30f0395eb073bfc2fe902f3f793ab25`

## Required Tests

| Test | Result |
|---|---|
| head weights, projected attention, final row, and control deltas derive from the verified probe | pass |
| SVG parses and rasterizes | pass |
| 1200 × 760 color export is nonblank | pass |
| 1200 × 760 grayscale export is nonblank | pass |
| pipeline stages and head-distinction panel remain recognizable at 100 pixels wide | pass |
| stage boundaries, arrows, and control distinctions do not rely on color alone | pass |
| full-size labels, panels, equations, and control values do not clip or overlap | pass |
| visual states that attention alone is not the transformer and avoids runtime/quality claims | pass |
| exactly one Chapter 11 anchor remains in the production package | pass |