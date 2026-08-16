# Chapter 1 Visual — Three Forms of Constraint

**Status:** Verified August 12, 2026  
**Canonical source:** [chapter_01_three_forms_of_constraint.svg](chapter_01_three_forms_of_constraint.svg)  
**Generator:** [chapter_01_three_forms_of_constraint.py](chapter_01_three_forms_of_constraint.py)  
**Data source:** [../evidence/chapter_01_door_model.rs](../evidence/chapter_01_door_model.rs)

**Production exports:**

- [full-size color PNG](chapter_01_three_forms_of_constraint.png)
- [full-size grayscale PNG](chapter_01_three_forms_of_constraint_grayscale.png)
- [100-pixel thumbnail](chapter_01_three_forms_of_constraint_thumbnail.png)

## Structural Reveal

The same represented transition can pass through three different constraint mechanisms without making those mechanisms equivalent.

## Caption

Unlocking and then opening moves the declared model from `LC` through `UC` to `UO` in all three views. The algebraic view requires inputs to lie in partial-operation domains, the symbolic view requires represented preconditions, and the programmed view selects typed `match` branches and returns `Result` values. Similar traces do not supply a shared source of permission or consequence.

## Alternative Text

Three aligned panels show the represented sequence locked-and-closed (`LC`) to unlocked-and-closed (`UC`) to unlocked-and-open (`UO`). In the algebraic panel, `UNLOCK` and `OPEN` are permitted when `LC` and `UC` lie in the respective domains of partial transformations. In the symbolic panel, represented facts satisfy the preconditions of `UNLOCK`, whose effects then satisfy the preconditions of `OPEN`. In the programmed panel, typed `DoorState` values reach Rust `match` branches and return `Ok(UnlockedOpen)`. A subordinate boundary in every panel compares an attempt to open `LC`: the algebraic operation is undefined, the symbolic preconditions fail, and the program returns `Err(Locked)`. A closing band states that the figure compares interfaces rather than asserting equivalence and that internal success does not establish physical correspondence or operational adequacy.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 12, 2026
- Originality: Original programmatic composition generated from the execution-verified Chapter 1 Rust artifact
- External assets: None
- Typeface: DejaVu Sans
- Palette: Locked Book Two functional colors from [../VISUAL_LANGUAGE.md](../VISUAL_LANGUAGE.md)
- Format: SVG, 1200 × 800 view box
- Deterministic SVG SHA-256: `0cbc702a9bd981028ab1add508f6dc2a3aec4396cbc6fc04988e348fd1257c4e`

## Required Tests

| Test | Result |
|---|---|
| labels and outcomes align with the verified Rust source | pass |
| deterministic regeneration preserves the SVG hash | pass |
| SVG parses without error | pass |
| 1200 × 800 raster export is nonblank | pass |
| primary three-panel structure remains present at 100 pixels wide | pass |
| grayscale retains structural contrast | pass |
| labels, borders, and line styles do not rely on color alone | pass |
| comparison and non-equivalence boundary are explicit | pass |
| exactly one Chapter 1 SVG anchor remains in the production package | pass |

The first raster pass exposed a collision between each permission label and its first gate. The labels were moved above the gate row and all exports were regenerated before this record was promoted.