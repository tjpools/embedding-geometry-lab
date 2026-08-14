# Book Three — Chapter Derivation Pipeline

**Status:** Canonical closure spine derived August 14, 2026

Book Three chapters will be derived from the philosophical DAG under the ownership contract. Topological order is necessary but insufficient: a chapter must create a reader movement, test a distinction, or join dependencies at a meaningful interface.

## Inputs

- module ownership from [book_structure.md](book_structure.md)
- canonical modules from [modules.txt](modules.txt)
- explanatory edges and build layers from [dependency_map.md](dependency_map.md)
- collaboration, provenance, and responsibility invariants from [OWNERSHIP_CONTRACT.md](OWNERSHIP_CONTRACT.md)
- evidence-to-action requirements from [CLOSURE_PROBE.md](CLOSURE_PROBE.md)
- Book Two evidence handoffs from [concurrent_workflow.md](concurrent_workflow.md)

## Derivation Sequence

1. **Start from the DAG:** preserve every prerequisite edge; do not use crate order as reading order.
2. **Find reader movements:** group neighboring modules only when they carry one philosophical problem from question through distinction or case.
3. **Locate pivots:** identify where interlocutors become operators, operators meet cases, cases support derivation, and derivation encounters interpretation and limits.
4. **Attach evidence classes:** state which technical, historical, comparative, or philosophical inputs each candidate inherits.
5. **Attach ownership risks:** name the collaboration, provenance, and responsibility invariants most likely to fail.
6. **Attach closure fields:** identify bounded evidence, unresolved judgment, declared values, accountable actor, authorized action, and revision path when the chapter supports action.
7. **Define forbidden inference:** record the attractive conclusion that the chapter's evidence does not warrant.
8. **Test the handoff:** name what the next dependent chapter may rely on after this chapter is complete.

## Candidate Chapter Contract

Every candidate chapter must record:

| Field | Requirement |
|---|---|
| reader entry | what the reader can already distinguish |
| central question | one philosophical problem, not a topic label |
| owned modules | complete and non-duplicated qualified names |
| inherited dependencies | concepts and evidence established earlier |
| evidence classes | technical, historical, comparative, philosophical, analogical, or speculative |
| ownership invariants | named IDs from `ownership_invariants.tsv` |
| inspectable object | text, dialogue, derivation, case, artifact, trace, or counterexample |
| closure record | all six closure fields, or an explicit statement that the chapter does not authorize action |
| forbidden inference | what the chapter explicitly does not establish |
| reader exit | the distinction or capability gained |
| outgoing handoff | what later chapters may safely import |

## Derivation Tests

A candidate becomes part of the spine only if it satisfies at least one structural test and every safety test.

Structural tests:

- establishes a prerequisite used by multiple later modules
- carries a distinct philosophical pivot
- joins previously separate dependencies at an explicit interface
- supports a case, counterexample, or provenance audit
- distinguishes two limits or meanings that would otherwise collapse

Safety tests:

- preserves all incoming DAG edges
- assigns every module exactly once
- declares evidence classes and ownership invariants
- satisfies the closure probe or explicitly withholds action
- states a forbidden inference
- preserves the Book Two/Book Three interface
- does not use a historical interlocutor as endorsement

## Research Readiness

Structural derivation may proceed before every source brief is complete. Drafting and verification may not. Before a chapter enters prose:

- Book Two handoffs must point to concrete evidence rather than planned modules alone
- historical claims must have primary-source and scholarly research briefs
- transformer claims must distinguish learned relation, retrieval, provenance, and verification
- comparative cases must record both the relevant similarity and disanalogy

## Output

The August 14 re-derivation operation produced:

- [CHAPTER_MANIFEST.md](CHAPTER_MANIFEST.md), the canonical 16-chapter closure spine
- [chapter_modules.tsv](chapter_modules.tsv), the machine-readable chapter-to-module mapping
- chapter-level invariant, evidence, forbidden-inference, and handoff assignments
- a validated order in which all 54 dependency edges remain internal or forward

The result contains 27 modules across 16 chapters and 13 topological build layers. Chapters 1–11 preserve the historical, operational, geometric, comparative, and semantic dependencies that survived the new thesis. Chapters 12–16 declare values, locate the evidence boundary, audit explanatory excess, assign judgment and authority, and complete action under revision.

The prior 21-module, 14-chapter result remains visible in version history as the structural baseline. It was not silently edited into the replacement.
