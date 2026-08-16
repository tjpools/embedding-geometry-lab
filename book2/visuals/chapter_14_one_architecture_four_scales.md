# Chapter 14 Visual — One Architecture, Four Scales

**Status:** Verified August 14, 2026  
**Canonical source:** [chapter_14_one_architecture_four_scales.svg](chapter_14_one_architecture_four_scales.svg)  
**Generator:** [chapter_14_one_architecture_four_scales.py](chapter_14_one_architecture_four_scales.py)  
**Data source:** [../evidence/chapter_14_four_scales_probe.py](../evidence/chapter_14_four_scales_probe.py)

**Production exports:**

- [full-size color PNG](chapter_14_one_architecture_four_scales.png)
- [full-size grayscale PNG](chapter_14_one_architecture_four_scales_grayscale.png)
- [100-pixel thumbnail](chapter_14_one_architecture_four_scales_thumbnail.png)

## Structural Reveal

System, stack, block, and attention-operation views select increasingly local interfaces while preserving one architecture identity and one containment path. Repetition shares a contract without collapsing block instances, and one attention row remains visibly insufficient at system scope.

## Caption

Four aligned elevations carry `book2.transformer.architecture.01` from the system boundary through its repeated stack, one selected block, and that block's attention operation. Dashed connectors mean containment and selected zoom, not runtime order. Three distinct block IDs share one contract; each scale exposes only its owned interfaces. The lower control rejects one normalized attention row as a whole system because its scope is incomplete and it lacks token-input and logits-output interfaces.

## Alternative Text

A 1200 by 760 structural diagram titled One Architecture, Four Scales contains four double-bordered panels. Every panel displays architecture ID book2.transformer.architecture.01. The system panel shows token IDs entering a repeated three-block stack and logits leaving. The stack panel shows block 00, block 01, and block 02 as distinct instances sharing transformer.block.v1. The block panel selects block 01 and shows attention, first residual plus normalization, feed-forward, and second residual plus normalization. The operation panel selects block 01 attention and shows Q/K/V projections, scaled scores, softmax rows, value combination, and output projection. Dashed unarrowed connectors above the panels are labeled contains and selected zoom. A dashed lower control presents one attention row as a system and rejects it for incomplete scope and missing system token-input and logits-output interfaces. A footer states that containment and zoom are not runtime order.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 14, 2026
- Originality: original programmatic composition generated from the verified Chapter 14 probe
- External assets: none
- Typeface: DejaVu Sans
- Palette: locked values from [../VISUAL_LANGUAGE.md](../VISUAL_LANGUAGE.md)
- Format: SVG, 1200 × 760 view box
- Generator library: Python standard-library `xml.etree.ElementTree`
- Rasterizer: ImageMagick `convert`
- Deterministic SVG SHA-256: `b96576733a310b72f21b687f6d6f502ec153eb1caf02818d5feb0f706e011f00`

## Required Tests

| Test | Result |
|---|---|
| architecture ID, dimensions, instances, interfaces, and control derive from the verified probe | pass |
| SVG regenerates twice with identical SHA-256 | pass |
| SVG parses and declares a 1200 × 760 canvas and exact title | pass |
| color, grayscale, and 100-pixel exports rasterize and remain nonblank | pass |
| four scales, repeated stack, block interfaces, attention operation, and rejection control remain legible | pass |
| containment connectors are unarrowed and explicitly distinguished from runtime order | pass |
| figure remains structurally recognizable at 100 pixels wide | pass |
| distinctions do not rely on color and alternative text communicates the complete result | pass |
| exactly one Chapter 14 visual anchor exists | pass |