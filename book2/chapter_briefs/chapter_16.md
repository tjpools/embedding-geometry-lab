# Chapter 16 Brief — Measured Limits

**Status:** Verified; Part IV integrated  
**Part:** IV — One Executable Architecture  
**Module:** `convergence.limits`  
**Visual anchor:** **The Constraint Envelope**

## Central Question

Which boundaries of the fixed Transformer fixture can be demonstrated, and what conclusions remain unsupported by those measurements?

## Chapter Claim

The fixture operates inside a typed constraint envelope. Context length and representation width create explicit acceptance boundaries; declared attention work grows with sequence length; finite vocabulary coverage collapses distinct unknown strings to one ID; decoding policy can change the selected token while logits remain fixed; and changing an architectural component changes the numerical output. These are local operational findings under declared rules. They do not define intelligence, understanding, meaning, personhood, or the ultimate possibilities of other systems.

## Dependency Alignment

**Incoming edges:**

- `convergence.architecture -> convergence.limits` supplies the declared object and structural constraints.
- `convergence.execution -> convergence.limits` supplies the observed baseline trace and work records.

There is no outgoing Book Two module edge. The handoff to Book Three is epistemic: mechanisms and measured boundaries transfer; philosophical predicates do not.

## Evidence Plan

Create a standard-library deterministic probe with six separately typed experiments:

1. **Context:** requests of lengths 1–3 are admitted by a declared capacity of 3; length 4 is rejected before embedding.
2. **Representation:** width 4 is accepted; width 5 is rejected at block input.
3. **Compute structure:** evaluate the exact declared attention multiplication/addition/exponential formulas for lengths 1, 2, and 3; report growth as structural counts, not timing.
4. **Data/vocabulary coverage:** two distinct absent strings map to the same `<unk>` ID and embedding, demonstrating information loss under the fixed vocabulary without making claims about training corpora in general.
5. **Decoding:** hold one logit vector fixed and compare deterministic argmax with a declared alternative constrained-selection rule that selects a different allowed ID; policy changes, logits do not.
6. **Architecture:** hold request and parameters fixed while removing one declared attention contribution; record a nonzero output difference without inferring semantic or universal causal importance.

Every experiment must record changed variables, held-fixed variables, result type, and permitted inference. Rerun must be identical.

Add an inference-boundary validator that rejects unsupported conclusion records such as `understands`, `is_person`, or `cannot_ever_understand` with `OUTSIDE_OPERATIONAL_EVIDENCE`. This is a claim-scope control, not an experiment about those predicates.

## Visual Anchor

**The Constraint Envelope** must show six distinct boundary panels around one fixed fixture: context, representation, compute, data/vocabulary, decoding, and architecture. Accepted regions, rejection points, growth records, and output sensitivity should remain visually distinct. A strong footer must state that the envelope bounds observed operation, not ontology.

## Verification Questions

- Does each result identify changed and held-fixed variables?
- Are rejection boundaries detected before invalid downstream work?
- Are structural counts kept distinct from measured performance?
- Is unknown-token collision described as fixture information loss rather than a universal language claim?
- Does decoding policy vary while logits stay identical?
- Is architectural change reported numerically without semantic attribution?
- Are unsupported philosophical conclusions explicitly rejected as outside evidence rather than disproved?
- Are both incoming dependency edges exact?

## Explicit Exclusions

No production benchmark, trained-model evaluation, corpus-quality judgment, safety evaluation, universal scaling law, consciousness test, personhood criterion, semantic ontology, proof of understanding, or proof of impossibility.

## Ending Handoff

Book Two ends with mechanisms and measured boundaries. Book Three may ask what systems mean for humanity, but it must inherit these observations without treating computation and meaning as equivalent or treating absent evidence as disproof.

## Drafting Gate

**Result:** Verified. Six separately typed experiments record changed variables, held-fixed variables, result types, and permitted inferences. Context capacity 3 admits lengths 1–3 and rejects 4 before embedding; width 4 passes Chapter 15's block gate while width 5 fails there; attention counts for lengths 1–3 are `72/51/1`, `160/116/4`, and `264/195/9` multiplications/additions/exponentials; two distinct absent strings share `<unk>` ID 0 and one embedding; global and constrained selection choose IDs 2 and 0 from byte-identical logits; and removing the declared attention contribution produces maximum absolute output difference `0.138179224`. The scope control returns `OUTSIDE_OPERATIONAL_EVIDENCE` for all three named unsupported predicates without classifying them false.

**Drafting gate:** Verified. Two probe runs are byte-identical at SHA-256 `f0eff86f8826caee1af09ba508ed170a568374b4bf898963e69f230281c460fa`. The visual regenerates twice at SHA-256 `426e91d0871b98acd812c8056e68761a5482f97367c699d3696982a3a084a1a4`; its color, grayscale, and 100-pixel exports pass inspection. Analytics discovers 16 units, Chapter 16 contains 1,611 words and four local links, zero links are broken, all 10 canonical tests pass, and diagnostics are clean. The exact incoming edges are architecture and execution; no outgoing Book Two module edge is declared. Part IV integration and workflow remain unchanged.
