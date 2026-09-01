# Book Two — KDP Upload Checklist

Use this as the execution checklist for Amazon KDP upload. Ordered by upload flow: files first, listing fields second, preview third, publish decision last. Repository evidence was last checked September 1, 2026.

## Dry-Run Result Against the Submission Gate (September 1, 2026)

Checked line-by-line against [../publication/KDP_RULES.md](../publication/KDP_RULES.md)'s Submission Gate. This is a repository-evidence check, not a live KDP session - some items cannot be resolved without an actual KDP account.

| Submission gate requirement | Status | Evidence |
|---|---|---|
| uploaded manuscript is the complete customer-delivery version | PASS (front matter); OPEN (back matter) | dedication and epigraph added August 31, 2026 ([dedication.md](dedication.md), [epigraph.md](epigraph.md)), author-chosen (collaborative framing). Back matter (glossary, consolidated references, index) remains undecided - does not block EPUB upload, but is tracked separately in `evidence/release_readiness.md`. |
| cover is final and rights-cleared | PASS (ebook only) | 1600×2560 assets exist, rights documented in [evidence/cover_provenance.md](evidence/cover_provenance.md). Print cover remains out of scope for this launch. |
| title, subtitle, author match exactly | PASS | verified across manifest, cover, README, KDP metadata |
| series data matches | PASS (August 31, 2026) | `publication/BOOK2_METADATA.md` names series `The Geometry of Meaning`, confirmed against [book3/TRILOGY_ARC.md](../book3/TRILOGY_ARC.md). Book One's own files (`book/metadata.md`, `book/KDP_LISTING_PACKAGE.md`) now carry matching series title and number 1. |
| edition data matches | PASS | `First Edition`, set August 31, 2026 |
| trilogy reader handoffs agree with metadata | PASS (Book Two artifact) | `From Book One` precedes Chapter 1 and `Continue to Book Three` follows the reference layer; `analytics/epub_audit.py` enforces both positions and series metadata remains `The Geometry of Meaning`, position 2 |
| description has no URLs, reviews, availability claims, pricing, or time-sensitive promotion | PASS | verified against the current KDP Description text |
| categories accurate in the live selector | OPEN | three BISAC subjects finalized in the EPUB; exact Amazon browse paths not yet confirmed in a KDP account |
| keywords relevant, non-redundant | PASS (pending live check) | 7 keywords set, within KDP's cap; not yet tested against Amazon's live search-suggestion behavior |
| territorial rights and pricing confirmed | **PARTIAL** | price resolved ($4.99 USD); territorial rights still `[CONFIRM IN KDP]` |
| required KDP content-origin disclosures reviewed | **OPEN, not addressed anywhere yet** | this project was substantially produced through human-AI collaboration (see `publication/README.md`'s "Shared Author Positioning"). KDP requires disclosure of AI-generated/AI-assisted content at submission. No disclosure language has been drafted. This should not be answered by inference - it needs a direct, honest answer from the author about the actual production process before submission. |
| release achievable without KDP's one-time delay exclusion | PASS | September 30, 2026 release is 30 days out from today with no scheduling conflict, assuming the BLOCK items above are resolved first |

**Dry-run verdict: the canonical ebook release candidate is ready for Kindle Previewer and KDP upload testing, but not for Submit for pre-order.** Author decisions on final back matter/acknowledgments and content-origin disclosure remain open alongside Previewer and live-account confirmations.

## Release Strategy

Ebook first. Print is deliberately deferred: no trim size, spine width, or bleed decision has been made (see [evidence/release_readiness.md](evidence/release_readiness.md)).

## Current Source of Truth

- Canonical source order: [manifest.yml](manifest.yml)
- Pandoc metadata: [metadata.md](metadata.md)
- Build script: [build_book.sh](build_book.sh)
- Listing metadata, description, categories, keywords: [../publication/BOOK2_METADATA.md](../publication/BOOK2_METADATA.md)
- Preorder rules and submission gate: [../publication/KDP_RULES.md](../publication/KDP_RULES.md)
- Release-readiness gate tracker: [evidence/release_readiness.md](evidence/release_readiness.md)

## Current Artifacts

- Source EPUB: `../transformers.epub`
- KDP upload EPUB: `../transformers-kdp.epub`
- KDP upload DOCX (fallback only): `../transformers-kdp.docx`
- Kindle cover image: `cover_kindle.jpg`
- Print interior PDF: does not exist (deferred)

## Phase 1: Pre-Upload Verification (checked, not assumed)

| Check | Result |
|---|---|
| Title consistent as `Transformers: An Architecture for Geometric Computation` across manifest, cover, README, KDP metadata | PASS |
| Author consistent as `Terrence J McLaughlin` | PASS |
| `transformers-kdp.epub` is copied directly from the canonical EPUB with no Calibre conversion | PASS — byte-identical artifacts with matching SHA-256 values on September 1, 2026 |
| Both EPUB artifacts pass EPUBCheck 5.3.0 and `analytics/epub_audit.py` | PASS — 0 errors, 0 warnings, 0 missing resources, 0 missing spine entries, 0 missing hrefs/fragments, 0 navigation inversions |
| All 16 chapter SVGs embed in the EPUB (verified: `unzip -l` shows 16 `.svg` entries) | PASS |
| Zero math-rendering warnings (Chapter 1 `\xrightarrow` notation fixed) | PASS |
| Front matter appears in nav in canonical order and ends with `From Book One` before Chapter 1 (verified against `nav.xhtml`) | PASS |
| Chapter headings 1 through 16 appear correctly and in order in nav (verified) | PASS |
| Man-page suite is present in reading order after Chapter 16 (verified: "Book Two — Man Pages" appears in nav) | PASS |
| `Continue to Book Three` appears after the man-page reference layer and names Book Three without an unverified availability claim | PASS |
| Analytics: 0 broken local links, 20/20 man pages clean; unit suite 13/13 | PASS |
| **Man-page internal structure survives EPUB conversion** (verified by inspecting rendered HTML) | PASS — each page renders as `<pre><code>` monospace block after fencing fix (August 31, 2026) |
| Dedication / epigraph | PASS — present in source and EPUB navigation |
| EPUB identity, publisher, release date, pricing resolved (`publication/BOOK2_METADATA.md`) | PASS - stable UUID (no ebook ISBN required), `McLaughlin Tools Press`, September 30, 2026, $4.99 USD |
| Embedded title, subtitle, edition, author, `en-US`, audience, subjects, and series position 2 | PASS — enforced by `analytics/epub_audit.py` in both byte-identical EPUB artifacts |
| BISAC, primary marketplace, KDP Select | `[CONFIRM]`/`[DECIDE]` remain - not resolved |

### Resolved: man-page structure (August 31, 2026)

Each of the 19 component man pages (excluding `man/README.md`, which stays as a normal Markdown index) is wrapped in a single fenced ```` ```text ```` code block. Verified by rebuilding the EPUB and inspecting the rendered HTML: each page emits `<pre class="text"><code>...</code></pre>`, preserving indentation, monospace, and section separation. Content is unchanged; current verification reports 20/20 pages clean, 0 broken links, and 13/13 unit tests passing.

## Phase 2: Kindle Ebook Upload

### Ebook Details

- Title: `Transformers: An Architecture for Geometric Computation`
- Subtitle: `How AI, Mathematics, and Programming Converge into a Single Tool`
- Author: `Terrence J McLaughlin`
- Description: use the KDP Description from `../publication/BOOK2_METADATA.md`
- Keywords: use the 7 candidates in `../publication/BOOK2_METADATA.md` after testing Amazon search suggestions
- Categories: use the finalized BISAC subjects in `../publication/BOOK2_METADATA.md` to choose and confirm the closest live KDP paths

### Ebook Files

1. Upload `transformers-kdp.epub`.
2. If KDP requests a separate cover image, upload `cover_kindle.jpg`.
3. Use `transformers-kdp.docx` only as fallback if EPUB upload fails.
4. Confirm the cover renders correctly in KDP preview.

### Ebook Pricing

`$4.99 USD`, 70% royalty bracket (resolved; see `../publication/BOOK2_METADATA.md`). Territories and KDP Select enrollment remain `[DECIDE]`.

## Phase 3: Ebook Preview Pass

Check these in Kindle Previewer or the KDP online previewer:

1. Front matter order matches Phase 1's verified nav order.
2. `From Book One` is readable as an independent entry point rather than a prerequisite summary.
3. Chapter labels are correct from Chapter 1 through Chapter 16.
4. Navigation reaches the man-page section and then `Continue to Book Three`.
5. No malformed section breaks, missing glyphs, or broken math renderings appear in sampled locations (spot-check Chapter 1's fixed equations specifically).
6. Sample pages communicate the intended stance: technical, evidence-grounded, boundary-aware.

## Ebook Publish Gate

Publish only when all of these are true:

1. EPUB upload is accepted by KDP.
2. Ebook preview is clean.
3. Listing copy, categories, and keywords are entered and confirmed in the live selector.
4. Price is intentional, not a placeholder.
5. `publication/KDP_RULES.md`'s submission gate checklist is fully satisfied.

Do not submit or publish while final back matter/acknowledgments, content-origin disclosure, `primary marketplace`, `publication rights`, or `KDP Select` remain open. The stable ebook UUID, publisher, release date, and price are resolved.
