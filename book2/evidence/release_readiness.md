# Book Two — Publication Release Readiness

**Audit date:** August 14, 2026; updated August 31, 2026  
**Decision:** Not yet a publication release candidate

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

- canonical builds: [manifest.yml](../manifest.yml), [metadata.md](../metadata.md), and [build_book.sh](../build_book.sh) produce a working EPUB and KDP DOCX from one canonical source order, with all 16 chapter SVGs embedded and zero math-rendering warnings after the Chapter 1 arrow-notation fix

## Open Gates

| Gate | Current evidence | Required completion |
|---|---|---|
| front matter | copyright, dedication, epigraph, KDP title page, table of contents, promise to the reader, how-to-read, and preface exist and build cleanly into the EPUB in correct nav order ([copyright.md](../copyright.md), [dedication.md](../dedication.md), [epigraph.md](../epigraph.md), [kdp_title_page.md](../kdp_title_page.md), [TOC.md](../TOC.md), [promise_to_the_reader.md](../promise_to_the_reader.md), [HOW_TO_READ_THIS_BOOK.md](../HOW_TO_READ_THIS_BOOK.md), [preface.md](../preface.md)) | author review of drafted front matter |
| back matter | no canonical glossary, consolidated references, index/notes, or author/back matter package | decide required back matter and create canonical sources |
| acknowledgments | no Book Two acknowledgments artifact | author review and approval |
| citation resolution | 16 source ledgers exist | consolidate references, recheck external URLs, normalize citation style, and resolve permissions/attributions |
| metadata | [../publication/BOOK2_METADATA.md](../../publication/BOOK2_METADATA.md): publisher (`McLaughlin Tools Press`), release date (September 30, 2026), price (`$4.99 USD`), ISBN (KDP free ISBN), category intent, and keyword list resolved; edition, primary marketplace, publication rights, and KDP Select remain `[CONFIRM]`/`[DECIDE]` | confirm remaining fields in the live KDP selector; recompute the internal manuscript freeze date against the actual submission deadline |
| print cover | ebook-sized cover assets exist (1600×2560); no print cover with spine and bleed | confirm print trim size and produce a print-ready export |
| canonical builds | working EPUB and KDP DOCX build from [manifest.yml](../manifest.yml) with all chapter visuals embedded and no math-rendering warnings | PDF/print build remains deliberately deferred pending trim/spine/bleed decisions |
| production QA | chapter visuals pass local production checks | validate typography, navigation, contents, image scaling, accessibility, Kindle/device behavior, and print proofs in final builds |

## Publication Boundary

The manuscript may be described as technically complete and integrated. It should not be described as customer-delivery ready, uploaded, submitted, available for preorder, or publication-final until every open gate passes.

The KDP metadata and submission decisions require author or publisher input and should not be inferred from manuscript evidence.
