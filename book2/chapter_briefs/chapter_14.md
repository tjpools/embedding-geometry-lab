# Chapter 14 Brief — Architecture in Full

**Status:** Verified; Part IV integrated  
**Part:** IV — One Executable Architecture  
**Module:** `convergence.architecture`  
**Visual anchor:** **One Architecture, Four Scales**

## Reader Entry

Chapter 13 aligned AI architecture, mathematical rules, and programmed implementation contracts at named interfaces. The reader may still confuse inspection scale with object identity, treat one block as a complete model, or treat one attention map as an explanation of the whole system.

## Intended Exit

The reader can distinguish system, stack, block, and operation views while tracking one architecture identity; distinguish containment from execution order; and distinguish selected detail from a complete explanation.

## Central Question

How can one Transformer be inspected at four scales without substituting a component for the architecture that contains it?

## Chapter Claim

A multi-scale architectural elevation preserves one object identity and one declared containment path while changing the selected scope and visible interfaces. The system contains a repeated stack, the stack contains blocks, the block contains attention and feed-forward sublayers, and the attention operation contains score, normalization, and value-combination interfaces. The probe verifies cross-scale identity, parent-child containment, dimensions, repeated-block count, and interface ownership. A scope-substitution control rejects an attention-row record presented as the whole architecture. This chapter does not trace one request through execution or measure limits.

## Dependency Alignment

**Incoming edge:** `convergence.alignment -> convergence.architecture` supplies the three validated lineage interfaces.

**Outgoing edges:**

- `convergence.architecture -> convergence.execution` prepares Chapter 15's representation trace.
- `convergence.architecture -> convergence.limits` supplies the declared architecture whose constraints Chapter 16 will measure.

## Reader Movement

1. Declare one deterministic architecture identity and fixed dimensions.
2. Inspect the system boundary: input/output interfaces and one repeated stack.
3. Zoom to the stack: ordered repeated blocks with shared block contract but distinct instance IDs.
4. Zoom to one block: attention, residual/normalization, feed-forward, and second residual/normalization interfaces.
5. Zoom to one attention operation: projections, score, softmax, value combination, and output projection.
6. Verify exact parent-child containment and preserve the architecture ID at every scale.
7. Verify that changing scale changes visible detail but not object identity.
8. Present one attention-row record as a whole-system candidate and reject it for incomplete scope and interfaces.
9. Hand the architecture to Chapter 15 for execution and Chapter 16 for limits without performing either task here.

## Evidence Plan

Create a standard-library deterministic Python probe with structured records for:

- one architecture ID and model dimensions
- system, stack, block, and operation views
- exact parent/child IDs and containment path
- repeated block instance count and contract identity
- scale-specific visible interfaces
- invariants preserved at all four scales
- deterministic rerun equality
- a scope-substitution control where one attention row fails system requirements
- exact outgoing dependency edges

## Visual Anchor

**One Architecture, Four Scales** is a nested or aligned architectural elevation showing system, stack, block, and operation views of the same identified object. Labels must expose containment and selected interfaces without implying that zoom order is runtime order. A subordinate rejection panel shows why an attention row is not the whole model.

## Verification Questions

- Is one architecture ID preserved across all scales?
- Are containment edges exact and acyclic?
- Are repeated block instances distinct while sharing one contract?
- Does each scale expose only interfaces it owns?
- Is containment kept distinct from execution order?
- Does the attention-row substitution fail explicit system requirements?
- Are outgoing edges limited to execution and limits?
- Are Chapters 15 and 16 left unperformed?

## Explicit Exclusions

This chapter does not tokenize, execute a request, record intermediate activation values, decode output, benchmark runtime, measure context/compute/data constraints, infer semantics from attention, or settle philosophical questions.

## Narrative Transition

Chapter 14 establishes one object across four inspection scales. Chapter 15 will send one representation through that object in execution order; Chapter 16 will measure its constraint envelope.

## Drafting Gate

**Result:** Verified. One architecture ID is preserved across four exact scales; containment is exact and acyclic; three distinct block instances share `transformer.block.v1`; scale-owned interfaces remain distinct; and the attention-row control returns `INCOMPLETE_SCOPE_MISSING_INTERFACES`. Two probe runs produce identical JSON at SHA-256 `d096c45e27cf083e3af1d7344c8629476711cb038ca940257e1ef28ce2abd8cf`. The visual regenerates twice at SHA-256 `b96576733a310b72f21b687f6d6f502ec153eb1caf02818d5feb0f706e011f00`, and all color, grayscale, and thumbnail exports pass inspection. Analytics discovers 14 units, Chapter 14 contains 1,619 words and four local links, zero links are broken, all 10 canonical tests pass, and diagnostics are clean.

**Drafting gate:** Verified. The four-scale identity fixture, exact containment checks, scope-substitution control, bounded source ledger, deterministic visual production package, chapter prose, analytics, tests, and diagnostics all pass their focused gates. Chapters 15 and 16 remain unperformed.
