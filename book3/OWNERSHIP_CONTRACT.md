# Book Three — Ownership Contract

**Status:** Canonical cross-cutting contract established August 12, 2026

Collaboration, provenance, and responsibility govern every Book Three crate. They are not modules in `meaning/` because they regulate how all modules produce and exchange claims. The machine-readable registry is [ownership_invariants.tsv](ownership_invariants.tsv). Decisions and recommendations are additionally governed by [CLOSURE_PROBE.md](CLOSURE_PROBE.md).

## Collaboration Invariants

### C1 — The collaboration is the operative system

Analysis may attribute different causal contributions to the human, transformer, tools, sources, and tests. It may not explain a collaborative result as the isolated product of either the human or transformer.

### C2 — Collaboration does not imply co-authorship

The transformer may generate language, transformations, alternatives, and relational paths. Authorship, publication, ownership, and accountability remain human.

### C3 — Voice must remain attributable

The manuscript's assertions belong to Terrence J McLaughlin. Transformer output used as evidence must be identifiable as output, excerpt, trace, or transformed artifact. A collective “we” must name its referent: author and reader, research community, or human-machine workflow.

### C4 — Interaction does not validate itself

A productive conversation is evidence about the collaboration, not automatic evidence that its historical, technical, or philosophical claims are true. Claims return through build, test, reverse engineering, sourcing, or counterexample.

## Provenance Invariants

### P1 — Historical claims require historical ground

Claims about Leibniz, Berkeley, Kant, and later thinkers must distinguish primary text, scholarly interpretation, Book Three's reconstruction, and contemporary application. Historical proximity does not imply endorsement.

Protagonist status grants Berkeley narrative priority, not exemption from this rule. A modern paraphrase, metaphor, or reconstructed question may not be styled as his voice or quotation without a verified textual basis.

### P2 — Learned relation is not cited provenance

Transformer output may expose patterns worth investigating. It may not be presented as evidence of a source, quotation, influence, or lineage without independent verification.

### P3 — Every imported claim declares its evidence class

Book Three arguments distinguish:

- inherited technical evidence from Book One or Book Two
- primary or secondary historical evidence
- inspectable comparative case
- philosophical inference
- analogy
- open speculation

The classes may interact, but they may not silently substitute for one another.

### P4 — Cases test; they do not universalize

A Rubik's Cube, programming language, engineered system, or transformer may reveal a structure or counterexample. No single case establishes a general ontology of intelligence or meaning.

## Responsibility Invariants

### R1 — Human responsibility is non-transferable

The author selects, verifies, interprets, publishes, and answers for the manuscript. Tool contribution does not dilute that responsibility.

### R2 — Technical evidence retains its original scope

Book Three may interpret a Book Two finding only after stating the inherited claim and its limits. It may not strengthen, weaken, or rewrite the technical result to support a philosophical conclusion.

### R3 — Interpretation exposes its assumptions

A philosophical conclusion must identify the assumptions connecting evidence to argument, plausible counterexamples, and the point where warranted inference ends.

### R4 — Persuasion is not verification

Clarity, fluency, elegance, historical resonance, and geometric imagery do not establish truth. The manuscript remains responsible for the evidence and distinctions beneath its language.

## Trust Boundaries

| Boundary | Allowed export | Forbidden inference |
|---|---|---|
| Book Two → Book Three | scoped technical finding, method, measurement, limitation | architecture directly proves ontology |
| Lineage → operators | documented question, distinction, argument, historical tension | historical thinker endorses this system |
| Closure ↔ Geometry | qualified structural analogy with explicit domain | algebraic and geometric descriptions are interchangeable |
| Operators → Comparative Systems | definition or prediction that a case can test | the case is selected only because it confirms the operator |
| Comparative Systems → Meaning | observation, disanalogy, counterexample, bounded pattern | one case establishes universal meaning |
| Transformer → manuscript | attributable output, transformation, alternative, trace | generated fluency establishes intent, agency, provenance, or truth |
| Meaning → reader | argument with assumptions, evidence class, and limits | interpretation transfers responsibility to the system |

## Crate Obligations

| Crate | Required invariants | Local responsibility |
|---|---|---|
| `lineage` | C3, P1, P2, P3, R3 | preserve historical voices and label contemporary reconstruction |
| `closure` | P3, P4, R2, R3 | preserve domain distinctions when closure changes meaning across systems |
| `geometry` | P3, P4, R2, R3, R4 | prevent mathematical models from becoming unsupported ontology |
| `meaning` | C1, C2, C3, C4, P2, P3, R1, R3, R4 | own synthesis without inventing provenance, agency, or transferred responsibility |
| `comparative_systems` | C4, P3, P4, R2, R3 | expose cases and disanalogies without owning conclusions |

## Enforcement

Every module brief must name:

1. its imported evidence classes
2. the invariants most likely to fail
3. its allowed exports to dependent modules
4. at least one forbidden inference
5. the human verification required before integration

A chapter may combine modules, but it may not weaken their crate obligations. Violations return the argument to briefing rather than being repaired through rhetorical qualification alone.
