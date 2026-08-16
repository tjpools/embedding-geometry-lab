# Chapter 7 Visual — Tensor Work on Parallel Lanes

**Status:** Verified August 13, 2026  
**Canonical source:** [chapter_07_tensor_parallel.svg](chapter_07_tensor_parallel.svg)  
**Generator:** [chapter_07_tensor_parallel.py](chapter_07_tensor_parallel.py)  
**Data source:** [../evidence/chapter_07_tensor_parallel_probe.py](../evidence/chapter_07_tensor_parallel_probe.py)

**Production exports:**

- [full-size color PNG](chapter_07_tensor_parallel.png)
- [full-size grayscale PNG](chapter_07_tensor_parallel_grayscale.png)
- [100-pixel thumbnail](chapter_07_tensor_parallel_thumbnail.png)

## Structural Reveal

The tensor operation contains eight independently indexed output tasks. A four-lane work partition preserves the declared result only when every output coordinate is assigned exactly once.

## Caption

Two batched input tensors with shapes $(2,2,3)$ and $(2,3,2)$ expose eight output coordinates containing three scalar product terms each. Four abstract lanes assign every coordinate once and assemble the same $(2,2,2)$ tensor as the serial reference. Removing coordinate $(1,1,1)$ leaves one empty cell and breaks equivalence. The lanes show a work decomposition, not measured GPU execution or speedup.

## Alternative Text

A left-to-right structural diagram begins with tensors A and B, each shown as two matrix batches with shapes 2 by 2 by 3 and 2 by 3 by 2. The center contains four horizontal lanes. Each lane receives two distinct output coordinates and their computed values, covering eight coordinates total. The right contains the assembled output tensor C with shape 2 by 2 by 2 and states that it equals the serial reference. A dashed control band below removes coordinate 1,1,1 from lane 3 and shows the final output cell as empty and unequal to the reference. A footer states that the lanes are abstract and no GPU execution or timing was measured.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 13, 2026
- Originality: original programmatic composition generated from the verified Chapter 7 probe
- External assets: none
- Typeface: DejaVu Sans
- Format: SVG, 1200 × 760 view box
- Deterministic SVG SHA-256: `004b6042aba47cec63a9b77104e2ef097d9e0204754b1cc59b188c10af024dc1`

## Required Tests

| Test | Result |
|---|---|
| input shapes, lane assignments, cell values, and control derive from the verified probe | pass |
| SVG parses and rasterizes | pass |
| 1200 × 760 color export is nonblank | pass |
| 1200 × 760 grayscale export is nonblank | pass |
| input, four-lane partition, result, and control remain recognizable at 100 pixels wide | pass |
| labels, borders, flow lines, and dashed control do not rely on color alone | pass |
| full-size labels, tensor values, lane assignments, and control do not clip or overlap | pass |
| omitted-work control remains visible and unequal to the reference | pass |
| exactly one Chapter 7 anchor remains in the production package | pass |

The first generator run exposed that the probe's structured output omitted its declared input tensors. The probe contract was completed before raster production so every displayed input and result derives from the same verified output.