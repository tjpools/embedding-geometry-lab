# KDP Upload Checklist

Use this as the final execution checklist for Amazon KDP upload.

It is ordered by the actual upload flow: files first, listing fields second, preview third, publish decision last.

## Release Strategy

Treat the two book types as separate publication tracks.

1. Ebook publishes first.
2. Paperback follows after the cover package is rebuilt and proofed.
3. Do not hold the ebook for print readiness.
4. A one-week gap between ebook publication and paperback publication is acceptable and operationally clean.

Working stance:

- Ebook: ready to complete first
- Paperback: a second release step after cover production and print preview

## Current Source of Truth

- Listing metadata: `KDP_LISTING_PACKAGE.md`
- General artifact checks: `PUBLICATION_ARTIFACT_CHECKLIST.md`
- Paperback cover package: `PRINT_PACKAGE_CHECKLIST.md`
- Paperback cover build notes: `SCRIBUS_KDP_COVER_WORKFLOW.md`

## Current Artifacts

- Kindle source EPUB: `../embedding-geometry.epub`
- Kindle KDP upload EPUB: `../embedding-geometry-kdp.epub`
- Kindle KDP upload DOCX: `../embedding-geometry-kdp.docx`
- Kindle cover image upload file: `cover_kindle.png`
- Reading PDF: `../embedding-geometry.pdf`
- KDP interior PDF: `../embedding-geometry-6x9.pdf`

## Track A: Ebook First

This is the immediate publication track.

## Phase 1: Pre-Upload Lock

Confirm these before opening KDP:

1. Title is `Embedding Geometry` everywhere.
2. Subtitle is `A Walkable Introduction to AI Through Building, Testing, and Collaboration` everywhere.
3. Author is `Terrence J McLaughlin` everywhere.
4. `embedding-geometry-kdp.epub` is the current ebook upload file.
5. KDP interior PDF is the current 158-page `6 x 9 in` artifact.
6. Any last-minute copy edits are committed before upload.

## Phase 2: Kindle Ebook Upload

Use these first-pass values unless KDP forces a concrete change.

### Ebook Details

- Title: `Embedding Geometry`
- Subtitle: `A Walkable Introduction to AI Through Building, Testing, and Collaboration`
- Author: `Terrence J McLaughlin`
- Description: use the `Optimized KDP Description` from `KDP_LISTING_PACKAGE.md`
- Keywords:
  - `artificial intelligence for beginners`
  - `programmer introduction to ai`
  - `understanding transformers and embeddings`
  - `human machine collaboration`
  - `ai concepts without hype`
  - `reasoning tools and machine intelligence`
  - `mathematics and structure of ai`
- Category direction:
  - `Computers / Artificial Intelligence`
  - `Computers / Programming / General`
  - `Science / Philosophy & Social Aspects`

### Ebook Files

1. Upload `embedding-geometry-kdp.epub`.
2. If KDP asks for a separate cover image, upload `cover_kindle.png`.
3. Use `embedding-geometry-kdp.docx` only as fallback if EPUB upload fails.
4. Confirm the cover appears correctly in KDP preview.

### Ebook Pricing

- Recommended launch price: `$8.99`
- Adjust only if there is a deliberate launch reason to do so.

## Phase 3: Ebook Preview Pass

Check these in Kindle Previewer or the KDP online previewer:

1. The table of contents begins with one title page entry, not duplicate book-title entries.
2. Front matter order is correct:
   - Copyright
   - Dedication
   - Epigraph
   - How to Read This Book
   - Promise to the Reader
   - Preface
3. Chapter labels are correct from Chapter 1 through Chapter 18.
4. Navigation into the back matter works.
5. No malformed section breaks, missing glyphs, or broken math renderings appear in sampled locations.
6. Sample pages communicate the intended public-facing stance: serious, walkable, anti-hype.

## Ebook Publish Gate

Publish the ebook as soon as all of these are true:

1. EPUB upload is accepted.
2. Ebook preview is clean.
3. Listing copy is entered and reads correctly.
4. Categories and keywords are set.
5. Price is intentional.

Once those are true, publish the ebook.

## Track B: Paperback Later

This is a separate follow-on release track.

The paperback can lag behind the ebook without harming the public representation of the project, as long as the paperback package is cleaner when it arrives.

## Phase 4: Paperback Interior Upload

Use this only when you are ready to proceed with print.

### Paperback Interior

1. Upload `embedding-geometry-6x9.pdf` as the interior file.
2. Confirm KDP reads it as a `6 x 9 in` interior.
3. Confirm the previewed page count matches the uploaded interior behavior.

### Paperback Metadata

- Use the same title, subtitle, author, description, and keyword strategy as the ebook unless KDP requires separate adjustments.
- Recommended starting paperback price: `$16.99`

## Phase 5: Paperback Cover Gate

Do not finalize paperback until all of these are true:

1. The KDP cover template has been regenerated for the current 158-page interior.
2. The final cover is built against that current template, not the older 161-page reference template.
3. The front-cover art is print-ready, not the current low-resolution concept PNG.
4. The barcode exclusion area is clear.
5. Spine text contains only title and author.
6. The final cover PDF has been checked in the KDP previewer.

## Paperback Delay Gate

Delay paperback publication if any of these remain true:

1. The KDP template is still the old 161-page reference asset.
2. The final wraparound cover has not been rebuilt from the current 158-page interior.
3. The front-cover art is still the low-resolution concept image.
4. Spine alignment has not been previewed in KDP.
5. The barcode-safe area has not been checked against the final cover export.

If any one of those is still unresolved, keep the ebook on schedule and push the paperback out by the needed week.

## Phase 6: Manual Decision Sheet

These still require owner judgment during upload:

1. Final browse-category mapping inside KDP’s live interface.
2. Final keyword phrasing if KDP field behavior rewards shorter wording.
3. Territory and royalty settings.
4. Whether ebook pricing is introductory or steady-state.
5. Whether paperback upload happens one week after ebook launch or on a later print-ready date.

## Phase 7: Final Go / No-Go

Go forward with ebook publication when these are all true:

1. EPUB preview is clean.
2. Listing copy looks serious and accurate.
3. Categories and keywords are entered.
4. Price is intentional.
5. Sample pages represent the book well.

Go forward with paperback publication only when these are all true:

1. Interior preview is clean.
2. Final cover is rebuilt from the current page-count template.
3. Cover art is print-grade.
4. Spine alignment is confirmed.
5. Barcode-safe area is clear.

## Recommended Immediate Sequence

1. Upload `embedding-geometry-kdp.epub` first.
2. Run the Kindle/KDP preview pass.
3. Publish the ebook once the preview is clean.
4. Announce or circulate the ebook as the first public artifact.
5. Spend the next week completing the paperback cover package.
6. Upload paperback only after the cover is truly production-ready.