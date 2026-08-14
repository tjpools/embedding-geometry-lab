# Comparative Systems

This crate supplies cases that expose constraints and interfaces without pretending that unlike systems are identical.

Modules:

1. `rubiks_cube` — visible move closure, non-commutativity, and reachable states
2. `programming_languages` — syntax, semantics, types, execution, and enforced meaning
3. `engineered_systems` — physical, procedural, organizational, and human constraints
4. `transformers` — learned architecture as a constrained system for derived outputs

Cases test philosophical claims; they do not own them. Similarity must be stated at the level where it holds, and disanalogy must remain visible.

**Ownership invariants:** C4, P3, P4, R2, R3. Each case exports observations, disanalogies, and counterexamples rather than universal conclusions under [the ownership contract](../OWNERSHIP_CONTRACT.md).

**Crate question:** What do real systems reveal when compared without collapsing their differences?
