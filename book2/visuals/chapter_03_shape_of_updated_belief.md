# Chapter 3 Visual — The Shape of Updated Belief

**Status:** Verified August 12, 2026  
**Canonical source:** [chapter_03_shape_of_updated_belief.svg](chapter_03_shape_of_updated_belief.svg)  
**Generator:** [chapter_03_shape_of_updated_belief.py](chapter_03_shape_of_updated_belief.py)  
**Data source:** [../evidence/chapter_03_bayesian_update_probe.py](../evidence/chapter_03_bayesian_update_probe.py)

**Production exports:**

- [full-size color PNG](chapter_03_shape_of_updated_belief.png)
- [full-size grayscale PNG](chapter_03_shape_of_updated_belief_grayscale.png)
- [100-pixel thumbnail](chapter_03_shape_of_updated_belief_thumbnail.png)

## Structural Reveal

Evidence changes the relative weight of represented hypotheses without converting the favored hypothesis into certainty.

## Caption

Under the declared prior and likelihood model, observing `red` shifts probability from $(0.6,0.4)$ to $(0.8,0.2)$. The posterior remains a distribution conditioned on the model and evidence; sensitivity marks show how alternate prior or likelihood assumptions change that distribution.

## Alternative Text

A shared vertical probability axis from zero to one compares prior and posterior probabilities for two door-state hypotheses. `locked`, drawn with circles and solid lines, rises from 0.6 to 0.8. `unlocked`, drawn with squares and dashed lines, falls from 0.4 to 0.2. Between them, the observed value `red` weights `locked` by 0.8 to produce joint weight 0.48 and weights `unlocked` by 0.3 to produce joint weight 0.12. Both weights are normalized by evidence probability 0.60. Small posterior-axis marks show the changed-prior result $(0.64,0.36)$ and changed-likelihood result $(5/7,2/7)$. Neither posterior hypothesis has probability zero or one, and no decision or action is shown.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 12, 2026
- Originality: Original programmatic composition generated from the verified Chapter 3 probe
- External assets: None
- Typeface: DejaVu Sans
- Palette: Locked Book Two functional colors from [../VISUAL_LANGUAGE.md](../VISUAL_LANGUAGE.md)
- Format: SVG, 1200 × 760 view box
- Deterministic SVG SHA-256: `e483c0443aaf5c33b3bbd0de1de0ee2a25a77ead49ec24e7c72b41e8486a3770`

## Required Tests

| Test | Result |
|---|---|
| source values equal the verified probe output | pass |
| SVG parses without error | pass |
| 1200 × 760 raster export is nonblank | pass |
| primary structure remains present at 100 pixels wide | pass |
| grayscale retains luminance levels and structural contrast | pass |
| labels and marks do not rely on color alone | pass |
| exactly one Chapter 3 anchor remains in the production package | pass |

The first raster pass exposed a clipped axis label and an undersized normalization box. Both defects were corrected in the generator before this record was promoted.
