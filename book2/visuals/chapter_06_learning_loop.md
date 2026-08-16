# Chapter 6 Visual — The Learning Loop

**Status:** Verified August 13, 2026  
**Canonical source:** [chapter_06_learning_loop.svg](chapter_06_learning_loop.svg)  
**Generator:** [chapter_06_learning_loop.py](chapter_06_learning_loop.py)  
**Data source:** [../evidence/chapter_06_learning_loop_probe.py](../evidence/chapter_06_learning_loop_probe.py)

**Production exports:**

- [full-size color PNG](chapter_06_learning_loop.png)
- [full-size grayscale PNG](chapter_06_learning_loop_grayscale.png)
- [100-pixel thumbnail](chapter_06_learning_loop_thumbnail.png)

## Structural Reveal

Learning in the worked system is repeated, objective-directed parameter adjustment. Gradient direction and update size jointly determine the observed trajectory.

## Caption

For one affine unit trained on four equally weighted examples, learning rate $0.2$ decreases the declared training loss across 12 updates while the parameters move toward $(2,1)$. Holding the model, data, objective, initialization, and step count fixed but increasing the rate to $1.2$ raises final loss to approximately $197.53$. The loop is inspectable, but gradient information alone does not guarantee that every update size improves the objective.

## Alternative Text

The upper-left plot shows training loss falling from 4.5 toward zero over 12 updates with learning rate 0.2. A dashed control arrow leaves the plot above its 4.5 limit; its label reports learning rate 1.2 and final loss 197.53. The upper-right plot shows weight and bias moving from zero toward the declared relation at weight 2 and bias 1. Along the bottom, four boxes labeled Predict, Loss, Gradient, and Update connect left to right, with a return line labeled repeat with updated parameters.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 13, 2026
- Originality: original programmatic composition generated from the verified Chapter 6 probe
- External assets: none
- Typeface: DejaVu Sans
- Format: SVG, 1200 × 760 view box
- Deterministic SVG SHA-256: `9c89f5c7fd9d5efe55e03a1c74a15cacd90b50c3df4fba45947be5650f962226`

## Required Tests

| Test | Result |
|---|---|
| loss and parameter values derive from the verified probe | pass |
| SVG parses and rasterizes | pass |
| 1200 × 760 color export is nonblank | pass |
| 1200 × 760 grayscale export is nonblank | pass |
| loss plot, parameter path, and repeated loop remain recognizable at 100 pixels wide | pass |
| labels, solid and dashed paths, and loop geometry do not rely on color alone | pass |
| full-size labels, plots, and arrows do not clip or overlap | pass |
| failed control remains visible without compressing the base trace against its scale | pass |
| exactly one Chapter 6 anchor remains in the production package | pass |

The first raster pass exposed overlapping base-rate and control-rate annotations. The control annotation was moved to a separate horizontal region before the visual was promoted.