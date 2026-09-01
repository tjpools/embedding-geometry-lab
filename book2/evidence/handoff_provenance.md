# Book Two — Trilogy Handoff Provenance

**Established:** September 1, 2026
**Series:** *The Geometry of Meaning*

## Reader Sequence

The reader-facing sequence is:

1. Book One, *Embedding Geometry*, encounters AI through conversation, building, testing, and reverse engineering.
2. Book Two, *Transformers: An Architecture for Geometric Computation*, makes the technical excursion into the architecture.
3. Book Three, *The Architecture of Geometric Semantics*, returns the bounded architecture to questions of interpretation, judgment, provenance, and responsibility.

This sequence agrees with Book Two's embedded series position 2 and the canonical [Book Three trilogy arc](../../book3/TRILOGY_ARC.md).

## Implemented Surfaces

- [../../book/Postscript.md](../../book/Postscript.md) now names Book Two as the next volume without claiming availability or preorder status.
- [../from_book_one.md](../from_book_one.md) appears after Book Two's preface and before Chapter 1. It summarizes inherited method without making Book One required reading.
- [../chapters/chapter_16.md](../chapters/chapter_16.md) closes the operational evidence boundary and exports only measured mechanisms and limits.
- [../continue_to_book_three.md](../continue_to_book_three.md) appears after the man-page reference layer and names Book Three without claiming availability or a release date.
- [../../book3/INTERFACE_PREFACE.md](../../book3/INTERFACE_PREFACE.md) receives the handoff by distinguishing architectural evidence from philosophical warrant.

Man pages remain operation-scoped and do not carry promotional cross-book links. Their source and boundary contracts would be weakened by mixing component lookup with series navigation.

## Verification Boundary

`analytics/epub_audit.py` requires both Book Two handoff labels and enforces their positions relative to Chapter 1 and the man-page layer. EPUBCheck validates the resulting package structure.

The Book Two EPUB contains both handoffs now. Book One's source contains its outgoing handoff, but the existing Book One EPUB predates this change and requires a separate validated rebuild before that pointer is present in the distributed artifact. Book Three's interface source is established, while its full publication artifact remains future work.