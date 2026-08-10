# Kindle Update Runbook (2026-08-08)

Use this runbook to publish the corrected Kindle cover.

## Upload Packet

- `embedding-geometry-kdp.epub` (primary)
- `cover_kindle.png` (cover fallback if KDP asks)
- `embedding-geometry-kdp.docx` (manuscript fallback only if EPUB fails)
- `SHA256SUMS.txt` (artifact verification)

## KDP Update Path

1. Open KDP Bookshelf.
2. Select `Embedding Geometry`.
3. Click `Edit eBook Content`.
4. Under manuscript upload, upload `embedding-geometry-kdp.epub`.
5. Cover step:
   - First, keep embedded cover path.
   - If KDP asks for separate image, upload `cover_kindle.png`.
6. Launch preview.
7. Confirm:
   - Cover thumbnail appears in preview list.
   - Cover page renders as first visual page.
   - TOC and chapter navigation still function.
8. Save and continue to pricing.
9. Submit update for republication.

## Acceptance Gate

All must be true before submit:

- Correct title: `Embedding Geometry`
- Correct subtitle present on cover image
- Correct author present on cover image
- Stickman/Rock art visible with no extra `THE BOOK` text
- No preview errors

## Expected Timing

KDP states republish timing may vary; monitor listing until updated cover is visible in store and on-device.
