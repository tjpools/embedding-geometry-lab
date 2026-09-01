#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

OUTDIR=".."
EPUB_OUT="$OUTDIR/transformers.epub"
KDP_EPUB_OUT="$OUTDIR/transformers-kdp.epub"
KDP_DOCX_OUT="$OUTDIR/transformers-kdp.docx"
COVER_IMAGE="cover_kindle.jpg"

if [[ ! -f "$COVER_IMAGE" ]]; then
  COVER_IMAGE="cover_front.png"
fi

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc is not installed." >&2
  exit 1
fi

mapfile -t manifest_files < <(awk '/^  - book2\/.*\.md$/ { sub(/^  - /, ""); print }' manifest.yml)

if [[ ${#manifest_files[@]} -eq 0 ]]; then
  echo "Error: manifest.yml did not yield any manuscript files." >&2
  exit 1
fi

book_files=()
for file in "${manifest_files[@]}"; do
  book_files+=("${file#book2/}")
done

echo "Building EPUB..."
pandoc "${book_files[@]}" \
  --file-scope \
  --lua-filter=epub_links.lua \
  --resource-path=.:chapters:visuals:man \
  --metadata-file=metadata.md \
  --toc \
  --epub-cover-image="$COVER_IMAGE" \
  -o "$EPUB_OUT"
python3 analytics/finalize_epub.py "$EPUB_OUT"

echo "EPUB build complete: $EPUB_OUT"

echo "Preparing KDP EPUB from validated canonical artifact..."
cp "$EPUB_OUT" "$KDP_EPUB_OUT"
echo "KDP EPUB complete: $KDP_EPUB_OUT"

echo "Building KDP DOCX..."
pandoc "${book_files[@]}" \
  --file-scope \
  --lua-filter=epub_links.lua \
  --resource-path=.:chapters:visuals:man \
  --metadata-file=metadata.md \
  --toc \
  -o "$KDP_DOCX_OUT"

echo "KDP DOCX build complete: $KDP_DOCX_OUT"

echo "PDF and print builds are deliberately deferred: no trim size, spine, or bleed decisions have been made (see evidence/release_readiness.md)."
