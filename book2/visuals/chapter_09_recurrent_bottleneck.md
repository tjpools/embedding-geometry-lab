# Chapter 9 Visual — The Recurrent Bottleneck

**Status:** Verified August 14, 2026  
**Canonical source:** [chapter_09_recurrent_bottleneck.svg](chapter_09_recurrent_bottleneck.svg)  
**Generator:** [chapter_09_recurrent_bottleneck.py](chapter_09_recurrent_bottleneck.py)  
**Data source:** [../evidence/chapter_09_recurrent_runtime_probe.py](../evidence/chapter_09_recurrent_runtime_probe.py)

**Production exports:**

- [full-size color PNG](chapter_09_recurrent_bottleneck.png)
- [full-size grayscale PNG](chapter_09_recurrent_bottleneck_grayscale.png)
- [100-pixel thumbnail](chapter_09_recurrent_bottleneck_thumbnail.png)

## Structural Reveal

Each recurrent state must be available before its successor can be evaluated, and influence from an early input reaches the final state through every intervening recurrence.

## Caption

Five ordered inputs update five hidden states through one shared scalar recurrence. Final-state sensitivity to $x_1$ crosses all five updates and is approximately 0.047, while sensitivity to the final input is approximately 0.989. Setting recurrent weight to zero removes cross-position sensitivity. Counts name declared dependencies and state accesses, not measured runtime or memory traffic.

## Alternative Text

An execution trace runs left to right from initial state h zero through states h one to h five. Each of five input boxes points into its corresponding state, and every state is connected to its predecessor. A sensitivity lane below reports final-state sensitivities of approximately 0.047, 0.101, 0.202, 0.476, and 0.989 for inputs one through five. A structural-count band reports five updates, five predecessor edges, five state reads, five state writes, and dependency depth five. A dashed zero-recurrence control breaks the path from early inputs to h five, reports zero sensitivity for inputs one through four, and retains final-input sensitivity of approximately 0.961. A footer states that no timing, kernel, or memory-traffic measurement was performed.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 14, 2026
- Originality: original programmatic composition generated from the verified Chapter 9 probe
- External assets: none
- Typeface: DejaVu Sans
- Format: SVG, 1200 × 760 view box
- Deterministic SVG SHA-256: `762343581679e144187a00f775112abcb17a5d84b280485db7cf87710a419ec9`

## Required Tests

| Test | Result |
|---|---|
| state values, sensitivities, and counts derive from the verified probe | pass |
| SVG parses and rasterizes | pass |
| 1200 × 760 color export is nonblank | pass |
| 1200 × 760 grayscale export is nonblank | pass |
| ordered path and broken control remain recognizable at 100 pixels wide | pass |
| labels and path distinctions do not rely on color alone | pass |
| full-size labels, arrows, states, and count band do not clip or overlap | pass |
| visual does not imply measured runtime or one-step/one-kernel correspondence | pass |
| exactly one Chapter 9 anchor remains in the production package | pass |