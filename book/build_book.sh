#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

OUTDIR=".."
EPUB_OUT="$OUTDIR/embedding-geometry.epub"
PDF_OUT="$OUTDIR/embedding-geometry.pdf"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc is not installed." >&2
  exit 1
fi

toc_files=$(grep -o '[a-zA-Z0-9_/-]*\.md' TOC.md | xargs)

echo "Building EPUB..."
pandoc $toc_files \
  --metadata-file=metadata.md \
  --toc \
  --epub-cover-image=cover.png \
  -o "$EPUB_OUT"

echo "EPUB build complete: $EPUB_OUT"

echo "Building PDF..."
if command -v xelatex >/dev/null 2>&1; then
  PDF_ENGINE="xelatex"
elif command -v pdflatex >/dev/null 2>&1; then
  PDF_ENGINE="pdflatex"
else
  echo "Warning: no LaTeX PDF engine found (xelatex or pdflatex)." >&2
  echo "Skipping PDF build." >&2
  exit 0
fi

pandoc $toc_files \
  --metadata-file=metadata.md \
  --toc \
  --pdf-engine="$PDF_ENGINE" \
  -o "$PDF_OUT"

echo "PDF build complete: $PDF_OUT"
