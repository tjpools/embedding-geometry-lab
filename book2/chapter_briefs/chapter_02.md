# Chapter 2 Brief — Representation Becomes Numerical

**Status:** Verified; Part I integrated  
**Part:** I — Structures  
**Modules:** `math.vectors`, `programming.representation`  
**Visual anchor:** **From Token to Coordinate**

## Reader Entry

Chapter 1 established that operations, symbolic rules, and programs act on represented objects under different internal constraints. The reader can distinguish internal validity from empirical correspondence and operational adequacy.

The reader may still treat a word, token, token identifier, stored encoding, and vector as interchangeable forms of the same object. The reader may also assume that a numerical identifier contains the meaning of the token it names.

## Intended Exit

The reader can distinguish:

- a referent from a sign used to represent it
- source text from the normalized text presented to a tokenizer
- a token from its identifier in a finite vocabulary
- an identifier from its stored numerical encoding
- a one-hot coordinate from a dense vector selected through an embedding table
- an illustrative vector lookup from a vector learned during training

The reader understands that representation choices preserve some distinctions, discard others, and establish the numerical objects later operations can transform.

## Central Question

How does a selected symbol become something a machine can distinguish and transform numerically?

## Chapter Claim

Numerical representation is not a neutral relabeling of language. Token boundaries, vocabulary membership, identifier assignment, numerical format, and vector lookup form a chain of design decisions. These decisions determine which distinctions remain available to later computation without making the resulting numbers intrinsically meaningful.

The verified representation probe establishes this claim within its declared toy system. External terminology and implementation semantics are bounded by the [Chapter 2 source ledger](../evidence/chapter_02_sources.md). The visual anchor and production tests are recorded in [../visuals/chapter_02_from_token_to_coordinate.md](../visuals/chapter_02_from_token_to_coordinate.md).

## Chapter Result

Within the declared representation system, consistent renumbering changes the token identifier and one-hot coordinate while preserving the selected lookup vector. The declared unknown-token policy also collapses distinct inputs to one identifier and vector. Representation therefore enables numerical transformation while determining which distinctions remain available.

## Inherited Terms and Claims

From Chapter 1:

- **modeled domain:** the represented objects admitted by a system
- **operation:** a specified transformation or combination over stated objects
- **constraint:** a condition limiting permitted states, expressions, transformations, or executions
- internal validity does not establish empirical correspondence or task adequacy

Chapter 2 sharpens **representation** as a constructed interface between selected distinctions and permitted numerical operations.

## Dependency Alignment

The chapter joins two modules at the reader level, but the canonical DAG does not place an edge between them.

**Incoming edge:**

| Source | Target | Inherited requirement |
|---|---|---|
| `math.algebra` | `math.vectors` | Objects, domains, operations, and composition are available before numerical coordinates are introduced. |

`programming.representation` has no incoming module edge. It enters as a parallel foundation rather than as a consequence of `programming.languages` or Chapter 1's door implementation.

**Outgoing edges:**

| Source | Target | Destination chapter | Handoff |
|---|---|---:|---|
| `math.vectors` | `math.matrices` | 4 | Coordinates become inputs to linear transformations. |
| `math.vectors` | `math.calculus` | 4 | Numerical coordinates provide variables with respect to which change can be measured. |
| `math.vectors` | `ai.neural` | 6 | Neural systems receive and transform numerical representations. |
| `programming.representation` | `programming.memory` | 5 | Encoded values require concrete storage. |
| `programming.representation` | `programming.compilers` | 5 | Representation choices cross checking and translation boundaries. |
| `programming.representation` | `ai.sequence` | 9 | Individual encoded items become ordered computational inputs. |

These six module edges are expressed through four chapter-level handoffs. Chapter 3 follows narratively but has no direct dependency edge from either Chapter 2 module.

## Reader Movement

1. Return to one named state from the door model and separate the physical condition, the word used for it, and the represented state.
2. Show that text must be selected and normalized before token boundaries can be assigned.
3. Define a deliberately small vocabulary and distinguish tokens from token identifiers.
4. Encode one identifier as a one-hot coordinate in a vector space.
5. Use a lookup table to select a dense vector, without claiming that the illustrative table has been learned.
6. Renumber the vocabulary and permute the lookup table consistently.
7. Verify that the identifier and one-hot coordinate change while the selected dense vector remains the same.
8. Map the distinctions preserved and discarded at each boundary.
9. Hand the resulting vectors to later chapters for transformation, learning, storage, and sequence processing.

## Worked Representation Chain

The candidate chain begins with the text token `open`:

```text
selected text
    -> normalized text
    -> token
    -> vocabulary identifier
    -> one-hot coordinate
    -> dense vector lookup
```

Use a declared toy vocabulary so every mapping remains inspectable. The example must keep these objects distinct:

- the character sequence `open`
- the token selected by the toy tokenizer
- the integer assigned by the vocabulary
- the corresponding basis vector
- the row selected from an illustrative embedding table

The example must not describe the illustrative dense vector as learned, semantic, or geometrically meaningful.

## Evidence Plan

The dependency-free probe is specified in [../evidence/chapter_02_representation_probe.md](../evidence/chapter_02_representation_probe.md) and implemented in [../evidence/chapter_02_representation_probe.py](../evidence/chapter_02_representation_probe.py). It records:

- the exact input text and normalization rule
- the complete toy vocabulary and unknown-token policy
- the token sequence and identifier sequence
- the one-hot encoding and its dimension
- the illustrative lookup table and selected dense vector
- a second vocabulary formed by permuting token identifiers
- the correspondingly permuted lookup table
- an assertion that consistent permutation preserves the selected dense vector
- an assertion that two out-of-vocabulary inputs collapse to the same unknown identifier

The first assertion verifies that token identifiers are assigned indices rather than intrinsic meanings. The second exposes one concrete distinction discarded by the declared representation policy. Both assertions pass; the result is recorded above but has not yet been integrated into prose or visual artwork.

## Visual Anchor

**From Token to Coordinate** is one left-to-right structural diagram with aligned stages:

1. named token
2. vocabulary entry
3. integer identifier
4. stored numerical encoding
5. one-hot coordinate
6. selected dense vector

The primary path shows the representation chain. A smaller aligned comparison shows the same token under a consistently permuted vocabulary and lookup table: the identifier and one-hot position change, while the selected dense vector remains fixed.

**Structural reveal:** A token becomes computable through several distinct mappings; no single intermediate number is the token's intrinsic meaning.

**Caption claim:** Vocabulary assignment determines an identifier and coordinate, while a lookup table selects the vector used by later computation; consistent renumbering changes the index without changing the selected vector.

**Alternative-text requirement:** Name every stage, identify which values change under permutation, and state which selected vector remains equal without relying on color.

## Verification Questions

- Are source text, normalized text, token, identifier, encoding, and vector consistently distinguished?
- Is the vocabulary finite and completely declared?
- Is the unknown-token policy explicit?
- Is vector dimension stated wherever a vector appears?
- Is a one-hot coordinate distinguished from a dense embedding vector?
- Is the lookup table labeled illustrative rather than learned?
- Does the renumbering probe permute vocabulary identifiers and table rows consistently?
- Does the unknown-token case expose information loss without claiming all production tokenizers behave identically?
- Does the visual remain legible in grayscale and at thumbnail size?

## Explicit Exclusions

This chapter does not:

- explain how sensors establish correspondence between physical and represented state
- claim that tokenization discovers natural or unique word boundaries
- treat token identifiers as semantic quantities
- explain probability or statistical inference; Chapter 3 owns uncertainty
- develop matrix transformations, derivatives, or gradients; Chapter 4 owns transformation and change
- explain memory layout, compiler translation, or numerical execution costs; Chapter 5 owns those implementation constraints
- explain how embedding vectors are learned; Chapter 6 owns neural learning and optimization
- interpret neighborhoods or directions in learned spaces; Chapter 8 owns learned geometry
- explain recurrence, context processing, or attention; Chapters 9 and 10 own those mechanisms
- claim that a vector is meaning or that numerical representation resolves interpretation; that philosophical work belongs to Book Three

## Outgoing Handoffs

### To Chapter 4 — Transformations and Change

Vectors provide the numerical objects on which matrices act and with respect to which local change can be measured.

### To Chapter 5 — Memory, Types, and Translation

Token identifiers and vector values require concrete formats, storage, checking, and translation before they can execute on a machine.

### To Chapter 6 — Learning by Adjustment

The illustrative lookup table establishes the operation without claiming learned content. Chapter 6 explains how optimization can adjust numerical parameters.

### To Chapter 9 — Sequence, Memory, and Runtime

Individual token representations become ordered computational objects whose processing introduces sequence and runtime constraints.

## Narrative Transition to Chapter 3

Chapter 2 establishes how distinctions become numerical. Chapter 3 asks how a system represents uncertainty about claims and outcomes. This is a narrative transition, not a direct module dependency.

## Drafting Gate

Prose begins only after:

- the toy vocabulary and normalization policy are fixed
- the representation probe passes both permutation and information-loss assertions
- every stage in the visual can be labeled without conflating identifiers, coordinates, and vectors
- the distinction between illustrative lookup and learned embedding is explicit
- primary or authoritative sources for the selected tokenization and representation concepts are recorded

The source requirement is satisfied by [../evidence/chapter_02_sources.md](../evidence/chapter_02_sources.md), and the visual-production requirement is satisfied by [../visuals/chapter_02_from_token_to_coordinate.md](../visuals/chapter_02_from_token_to_coordinate.md).

## Gate Revalidation

Completed August 12, 2026:

- probe execution and Python compilation pass
- source ledger and local references pass diagnostics
- SVG generation is deterministic from the verified probe
- full-size color, grayscale, and 100-pixel exports pass production checks
- the canonical DAG remains one incoming, zero internal, and six outgoing module edges
- exactly one Chapter 2 SVG anchor exists in the production package
- framing analytics complete with zero broken local links

The drafting gate is open. The verified manuscript chapter is [../chapters/chapter_02.md](../chapters/chapter_02.md); Part I integration remains open.

## Manuscript Verification

Completed August 13, 2026:

- every tokenizer, normalization, and lookup claim remains within the Chapter 2 source ledger
- equations, vocabulary assignments, and information-loss claims agree with the probe output
- probe and visual generators compile, and every probe assertion passes
- deterministic regeneration preserves the Chapter 2 SVG hash
- terminology and exclusions agree with Chapters 1 and 3 and preserve the canonical DAG boundary
- chapter-mode analytics measure two balanced chapters totaling 2,994 words with zero broken local links
- manuscript and brief pass workspace diagnostics

The chapter is verified. Integration with Chapters 1, 3, 4, and 5 remains a Part I operation.
