# Chapter 15 Visual — A Token Through the Machine

**Status:** Verified August 14, 2026  
**Canonical source:** [chapter_15_token_through_machine.svg](chapter_15_token_through_machine.svg)  
**Generator:** [chapter_15_token_through_machine.py](chapter_15_token_through_machine.py)  
**Data source:** [../evidence/chapter_15_token_execution_probe.py](../evidence/chapter_15_token_execution_probe.py)

**Production exports:**

- [full-size color PNG](chapter_15_token_through_machine.png)
- [full-size grayscale PNG](chapter_15_token_through_machine_grayscale.png)
- [100-pixel thumbnail](chapter_15_token_through_machine_thumbnail.png)

## Structural Reveal

Concrete values become different representations in runtime order while shape gates regulate each handoff. The subordinate control makes non-execution visible: a width-five row reaches the block gate, fails, and produces no block, projection, selection, or decode records.

## Caption

The fixed text `small models run` becomes IDs `[1,2,3]`, three width-four embedding-plus-position rows, one block output, the final hidden row `[1.591,-0.369,-1.152,-0.071]`, six logits, selected ID 2, and decoded token `models`. Each box distinguishes shape, value or digest, and bounded fixture work. The lower lane changes embedding width to five; `BLOCK_INPUT_WIDTH_MISMATCH` stops every downstream stage. Counts are not latency or a runtime benchmark.

## Alternative Text

A 1200 by 760 execution diagram titled A Token Through the Machine has three main horizontal bands connected by arrows. The first carries the text small models run to tokens, IDs 1 2 3, three by four embedding-plus-position rows, and an accepted block gate. The second, double-bordered band contains attention, first residual plus normalization, feed-forward, and second residual plus normalization, with output digest prefixes and work counts. The third carries the final-position hidden row through six vocabulary logits to argmax ID 2 and decoded token models. A dashed lower control appends a zero coordinate to create shape three by five. Block input validation expects three by four, reports BLOCK_INPUT_WIDTH_MISMATCH, and points to a dashed unexecuted box listing block math, projection, argmax, and decode. A footer says the counts are fixture records, not a benchmark.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 14, 2026
- Originality: original programmatic composition generated from the verified Chapter 15 probe
- External assets: none
- Typeface: DejaVu Sans
- Palette: locked values from [../VISUAL_LANGUAGE.md](../VISUAL_LANGUAGE.md)
- Format: SVG, 1200 × 760 view box
- Generator library: Python standard-library `xml.etree.ElementTree`
- Rasterizer: ImageMagick `convert`
- Deterministic SVG SHA-256: `6a0116714f84b6d9def07a9b833e016989b764d1dfacf5b610f7f2548ad893ac`

## Required Tests

| Test | Result |
|---|---|
| exact title, request, IDs, shapes, values, digest prefixes, result, and control derive from the verified probe | pass |
| SVG regenerates twice with identical SHA-256 | pass |
| SVG parses and declares a 1200 × 760 canvas and exact title | pass |
| color and grayscale exports are 1200 × 760, nonblank, and legible | pass |
| thumbnail is 100 pixels wide and preserves the three main bands plus failure lane | pass |
| arrows establish runtime order and the failure lane visibly terminates at the block gate | pass |
| labels and distinctions remain coherent without color | pass |
| alternative text communicates values, sequence, failure, and non-execution | pass |
| exactly one Chapter 15 visual anchor exists | pass |