# Chapter 5 Visual — Intent Through the Compiler

**Status:** Verified August 13, 2026  
**Canonical source:** [chapter_05_intent_through_compiler.svg](chapter_05_intent_through_compiler.svg)  
**Generator:** [chapter_05_intent_through_compiler.py](chapter_05_intent_through_compiler.py)  
**Data source:** [../evidence/chapter_05_intent_through_compiler_probe.py](../evidence/chapter_05_intent_through_compiler_probe.py)

**Production exports:**

- [full-size color PNG](chapter_05_intent_through_compiler.png)
- [full-size grayscale PNG](chapter_05_intent_through_compiler_grayscale.png)
- [100-pixel thumbnail](chapter_05_intent_through_compiler_thumbnail.png)

## Structural Reveal

Source intent becomes executable only by crossing distinct enforcement and translation interfaces; rejection at type checking prevents later layout, MIR, and executable artifacts from existing.

## Caption

The accepted `TokenRecord` crosses source declaration, type checking, declared layout, typed MIR, and observable output. A temporary integer supplied to the Boolean field is rejected at type checking and produces no downstream artifact. Acceptance establishes conformity to these interfaces, not proof of program purpose or task correctness.

## Alternative Text

A left-to-right trace contains five labeled boxes: Source, Type Check, Layout, MIR, and Output. The source declares a `TokenRecord` with unsigned integer, floating-point, and Boolean fields. The accepted path records three passing tests; a 12-byte layout aligned to four bytes with field offsets zero, four, and eight; a typed MIR function and record; and output showing size 12, offsets zero, four, and eight, and result 1.5. A dashed branch descends from Type Check to a Rejected box containing `active: 1` and `mismatched types`. Text below states that the rejected source has no layout, MIR, or executable. The final band states that type acceptance is not proof of purpose or task correctness.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 13, 2026
- Originality: original programmatic composition generated from the verified Chapter 5 probe
- External assets: none
- Typeface: DejaVu Sans
- Format: SVG, 1200 × 760 view box
- Deterministic SVG SHA-256: `a8224075a72678181ff5eedc37a756f1dd40f472375727cc395d65d79f9251d5`

## Required Tests

| Test | Result |
|---|---|
| source values equal the verified probe output | pass |
| SVG parses and rasterizes | pass |
| 1200 × 760 color export is nonblank | pass |
| 1200 × 760 grayscale export is nonblank | pass |
| accepted path and rejected branch remain recognizable at 100 pixels wide | pass |
| labels, arrows, and dashed branch do not rely on color alone | pass |
| full-size labels do not clip or overlap | pass |
| exactly one Chapter 5 anchor remains in the production package | pass |

The first raster pass exposed a dashed line crossing the rejected source label. The line was removed before the visual was promoted.
