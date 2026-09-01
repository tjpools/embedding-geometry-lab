# Book Two — Publication Release Readiness

**Audit date:** September 1, 2026
**Decision:** Canonical ebook release candidate; not yet cleared for KDP submission

The committed EPUB is the canonical candidate for Kindle Previewer and KDP upload testing. This decision closes repository engineering Gates 1–4. It does not authorize **Submit for pre-order** or publication while the editorial decisions, production preview, content-origin disclosure, and live KDP fields below remain open.

The artifact hashes, closed-gate evidence, verification commands, and submission boundary are recorded in the [canonical release-candidate provenance](release_candidate_provenance.md).

## Passing Gates

- all 16 chapters are verified and integrated
- all 16 original anchors are complete, accessible, reproducible, and have matching production checksums
- all local manuscript links pass
- all chapter probes and analytics tests pass
- workspace diagnostics are clean
- author attribution is consistently `Terrence J McLaughlin`
- title, subtitle, and author agree across the global manifest, README, cover specification, and metadata draft
- cover front assets and a Kindle JPG proof exist (1600×2560 PNG/JPG, plus a 100×160 thumbnail)
- cover rights and provenance are resolved (see [evidence/cover_provenance.md](cover_provenance.md)): the artwork is original, and its component layout references a published architecture, not a reproduced image
- every chapter has a bounded source ledger
- the final Book Two/Book Three boundary review passes after the Chapter 11 scope repair
- the component lookup layer (`man/`) is established, cross-reference-checked, and integrated into analytics

- canonical builds: [manifest.yml](../manifest.yml), [metadata.md](../metadata.md), and [build_book.sh](../build_book.sh) produce EPUB and KDP DOCX artifacts from one canonical source order, with all 16 chapter SVGs embedded and zero math-rendering warnings after the Chapter 1 arrow-notation fix
- EPUB structural integrity: the canonical EPUB and direct-copy KDP EPUB are byte-identical, contain no Calibre conversion layer, and independently pass EPUBCheck 5.3.0 and `analytics/epub_audit.py` with zero errors, warnings, missing resources, missing spine entries, missing hrefs/fragments, or navigation inversions
- EPUB metadata identity: both EPUB names carry the canonical title, subtitle, author, stable UUID, `en-US`, imprint, edition, BISAC subjects, keyword subjects, general-adult audience, and `The Geometry of Meaning` series position 2; the metadata audit reports zero issues and zero Calibre markers (see [metadata provenance](metadata_provenance.md))
- trilogy handoffs: `From Book One` precedes Chapter 1 and `Continue to Book Three` follows the component reference layer in both byte-identical EPUBs; Book One's canonical postscript points to Book Two, and Book Three's interface preface receives Book Two's measured boundary (see [handoff provenance](handoff_provenance.md))

## Submission Gates Still Open

| Gate | Current evidence | Required completion |
|---|---|---|
| front matter | copyright, dedication, epigraph, KDP title page, table of contents, promise to the reader, how-to-read, preface, and `From Book One` exist and build cleanly into the EPUB in correct nav order ([copyright.md](../copyright.md), [dedication.md](../dedication.md), [epigraph.md](../epigraph.md), [kdp_title_page.md](../kdp_title_page.md), [TOC.md](../TOC.md), [promise_to_the_reader.md](../promise_to_the_reader.md), [HOW_TO_READ_THIS_BOOK.md](../HOW_TO_READ_THIS_BOOK.md), [preface.md](../preface.md), [from_book_one.md](../from_book_one.md)) | author review of drafted front matter and trilogy handoff |
| back matter | the candidate intentionally contains the trilogy continuation after the reference layer; no glossary, consolidated references, or index/notes package is included | author decides whether the candidate is complete without additional back matter before submission |
| acknowledgments | no Book Two acknowledgments artifact is included | author decides whether omission is final before submission |
| citation resolution | 16 source ledgers exist | consolidate references, recheck external URLs, normalize citation style, and resolve permissions/attributions |
| metadata | embedded EPUB identity, edition, audience, BISAC subjects, keywords, series title/position, publisher, release date, and price are resolved; ebooks use a stable UUID rather than a KDP free ISBN; primary marketplace, publication rights, live categories, and KDP Select remain `[CONFIRM]`/`[DECIDE]` | confirm remaining catalog fields in the live KDP selector; recompute the internal manuscript freeze date against the actual submission deadline |
| print cover | ebook-sized cover assets exist (1600×2560); no print cover with spine and bleed | confirm print trim size and produce a print-ready export |
| canonical builds | validated canonical and KDP EPUBs plus KDP DOCX build from [manifest.yml](../manifest.yml), with all chapter visuals embedded and no math-rendering warnings | ebook gate passes; PDF/print remains deliberately deferred pending trim/spine/bleed decisions |
| production QA | chapter visuals pass local production checks | validate typography, navigation, contents, image scaling, accessibility, Kindle/device behavior, and print proofs in final builds |

## Publication Boundary

The manuscript and ebook package may be described as a canonical release candidate ready for Previewer and upload testing. They should not be described as submitted, available for preorder, or publication-final until every submission gate passes.

The KDP metadata and submission decisions require author or publisher input and should not be inferred from manuscript evidence.
