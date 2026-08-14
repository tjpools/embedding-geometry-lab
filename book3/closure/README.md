# Closure

This crate asks how a system's permitted operations and boundaries shape what remains reachable within it, and how humans act when operational evidence reaches those boundaries.

Modules:

1. `operations` — what operations preserve, generate, or leave a system
2. `constraints` — what a formal, programmed, learned, or institutional system excludes
3. `interfaces` — how systems exchange representations without dissolving their boundaries
4. `limits` — when technical closure supports a philosophical claim and when it does not

Algebraic closure, software boundaries, learned constraints, social institutions, and philosophical closure are not interchangeable. The crate earns comparisons by preserving those distinctions.

**Ownership invariants:** P3, P4, R2, R3. Every use of closure names its domain, imported evidence class, and the inference that cannot cross into another domain under [the ownership contract](../OWNERSHIP_CONTRACT.md).

**Crate question:** What can closure legitimately tell us about intelligence and meaning?

Technical closure does not warrant action by itself. Every case that moves from a system boundary to a recommendation or decision must satisfy [the closure probe](../CLOSURE_PROBE.md).
