# Meaning

This crate develops meaning as a derived outcome of structured relations, transformations, constraints, interpretation, and verification. Derived meaning is necessary to closure but does not warrant its own use.

Modules:

1. `derivation` — how meaning emerges through operations rather than appearing as an intact retrieved object
2. `interpretation` — how human purposes and contexts select among possible relations
3. `limits` — how absence, impossibility, ambiguity, and system boundaries condition meaning
4. `anti_narrative` — a critique of explanations that substitute a persuasive story for inspectable structure

`anti_narrative` does not claim that narrative is inherently false or structurally illegitimate. It targets narrative used as an untested explanation of AI behavior.

**Ownership invariants:** C1, C2, C3, C4, P2, P3, R1, R3, R4. This crate owns synthesis, but it cannot invent provenance, attribute human-equivalent agency, create a synthetic authorial voice, or transfer responsibility under [the ownership contract](../OWNERSHIP_CONTRACT.md).

**Crate question:** How is meaning derived, what makes a derivation trustworthy, and what additional judgment is required before it can support action?

Any module that converts interpretation into recommendation, reliance, or action must satisfy [the closure probe](../CLOSURE_PROBE.md).

## `interpretation` — Chapter 12 Research Contract

**Question:** What care is required when transformer output enters different human contexts?

The unit of analysis is a bounded interaction among a person or defined user group, a transformer-mediated task, an output, a use context, and an observable consequence. “The user” may not stand for humanity in general. Each case must state relevant experience, access needs, stakes, task, and institutional setting without converting those differences into a hierarchy of intelligence or worth.

### Imported evidence classes

- inherited Book Two evidence about the transformer's scoped capabilities and limits
- empirical human-computer interaction or human-factors research
- attributable interaction case or collaboration trace
- provenance audit
- philosophical interpretation with declared assumptions
- counterexample

Transformer output, authorial intuition, and a productive conversation may generate a research question. They may not serve as empirical human-factors evidence by themselves.

### Interaction record

Every case must identify:

1. **participants:** the person or bounded user group and the characteristics relevant to the task
2. **task:** what the participant is trying to accomplish and why a transformer is involved
3. **system:** model or product identity when known, interface, settings, date, and material limitations on reproducibility
4. **context:** stakes, time pressure, access conditions, prior knowledge, and available verification
5. **output and use:** what the system produced, what the person did with it, and where human judgment entered
6. **consequence:** an observed outcome or explicitly labeled risk, including who bears it

### Failure classes

The chapter may examine:

- misplaced reliance on fluent but unsupported output
- provenance loss, fabricated attribution, or source substitution
- automation bias or failure to inspect alternatives
- unequal accessibility or burdens of verification
- task mismatch, ambiguity, or interface-induced error
- privacy, disclosure, or downstream-use failures
- responsibility obscured by anthropomorphic language

These categories are prompts for evidence collection, not findings in advance. A case must distinguish observed harm, measured effect, participant report, design risk, and authorial inference.

### Allowed exports

The module may export to `meaning.limits` and `meaning.anti_narrative`:

- a scoped interaction finding
- the conditions under which it was observed
- a documented uncertainty or counterexample
- a practical care obligation tied to the evidence

It may not export a universal claim about human cognition, transformer intent, or the inherent safety of a class of users.

### Likely invariant failures

- **C4:** treating a compelling interaction as self-validating
- **P2:** using learned relation as provenance
- **P3:** allowing anecdote, empirical result, risk, and interpretation to blur
- **R1:** transferring responsibility to the transformer or workflow
- **R3:** hiding assumptions about users, expertise, vulnerability, or benefit
- **R4:** mistaking fluent guidance for verified guidance

### Forbidden inference

Differences in response do not establish dense or sparse personal Jacobians, fixed cognitive types, genius, deficiency, human value, or that one group needs paternalistic control. A transformer response that helps one participant does not establish that the model understood the participant, intended the result, or will produce the same consequence elsewhere.

### Human verification gate

Before Chapter 12 drafting, the author must:

1. define at least two bounded interaction cases with materially different contexts
2. ground every general human-factors claim in appropriate empirical or scholarly evidence
3. preserve participant privacy and distinguish direct observation from reconstruction
4. trace imported transformer claims to Book Two and retain their original scope
5. record at least one disconfirming case or plausible counterexample
6. state which recommendations follow from evidence and which remain authorial judgment

Until this gate is complete, Chapter 12 may retain its manifest framing but is not drafting-eligible.
