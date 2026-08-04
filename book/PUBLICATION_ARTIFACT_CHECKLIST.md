# Publication Artifact Checklist

Use this checklist when preparing a release-quality artifact set for EPUB, standard PDF, KDP interior PDF, and Scribus cover packaging.

## Canonical Sources

- Manuscript spine: `manifest.yml`
- Reader-facing mirror: `TOC.md`
- Metadata source: `metadata.md`
- Title-page source: `kdp_title_page.md`
- Cover package source: `PRINT_PACKAGE_CHECKLIST.md`
- Cover typography rules: `PRINT_COVER_TYPOGRAPHY_SPEC.md`

## Identity Lock

- Title matches everywhere: `Embedding Geometry`
- Subtitle matches everywhere: `A Walkable Introduction to Reasoning, Structure, and the Tools That Shape Us`
- Short subtitle is used only for cover-fit fallback, not interior metadata by default
- Author matches everywhere: `Terrence J McLaughlin`
- Rights line is current in `metadata.md`

## Interior Order

Front matter should appear in this order:

1. `copyright.md`
2. `dedication.md`
3. `epigraph.md`
4. `HOW_TO_READ_THIS_BOOK.md`
5. `preface.md`

Main matter should run from Chapter 1 through Chapter 18 with no drift from `manifest.yml`.

Back matter should appear in this order:

1. `epilogue_one_question_one_table.md`
2. `appendix_heatmap_manifold.md`
3. `appendix_ghost_chapters.md`
4. `appendix_deep_machinery.md`
5. `afterword_how_the_manifold_became_visible.md`
6. `Postscript.md`

## Interior Package Checks

- `manifest.yml` and `TOC.md` agree on front matter, main matter, and back matter
- Chapter 13 naming is consistent between spine docs and manuscript framing
- Chapter 18 closing lines match the current approved ending
- `kdp_title_page.md` matches `metadata.md` for title, subtitle, and author
- KDP interior build inserts `kdp_mainmatter_break.md` before Chapter 1 only

## Cover Package Checks

- Cover title, subtitle, and author match `metadata.md`
- Back-cover copy matches `PRINT_PACKAGE_CHECKLIST.md`
- Spine contains title and author only
- Barcode safe area is clear
- Scribus geometry still matches the current KDP template dimensions

## Artifact Targets

- EPUB: `../embedding-geometry.epub`
- PDF: `../embedding-geometry.pdf`
- KDP interior PDF: `../embedding-geometry-6x9.pdf`

## Build Checks

- `bash book/build_book.sh` succeeds
- `bash book/update_artifacts.sh` succeeds when a full refresh is needed
- No missing manuscript files referenced by `manifest.yml`
- No stale file order encoded only in `TOC.md`

## Final Review Pass

- EPUB opens and table of contents is correct
- Standard PDF opens and front matter order is correct
- KDP interior PDF opens and title page / chapter break behavior is correct
- Back matter appears in the intended sequence
- Cover and interior use the same public-facing identity

## Release Check

- Commit the final manuscript and artifact state
- Keep the generated artifacts paired with the source changes that produced them
- Record any last-minute subtitle or cover-fit fallback decisions before upload