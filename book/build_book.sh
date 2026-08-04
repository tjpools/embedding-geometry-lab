#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

OUTDIR=".."
EPUB_OUT="$OUTDIR/embedding-geometry.epub"
PDF_OUT="$OUTDIR/embedding-geometry.pdf"
KDP_PDF_OUT="$OUTDIR/embedding-geometry-6x9.pdf"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc is not installed." >&2
  exit 1
fi

mapfile -t manifest_files < <(awk '/^  - book\/.*\.md$/ { sub(/^  - /, ""); print }' manifest.yml)

if [[ ${#manifest_files[@]} -eq 0 ]]; then
  echo "Error: manifest.yml did not yield any manuscript files." >&2
  exit 1
fi

book_files=()
for file in "${manifest_files[@]}"; do
  book_files+=("${file#book/}")
done

kdp_pdf_files=("kdp_title_page.md")
for local_file in "${book_files[@]}"; do

  if [[ "$local_file" == "BOOK_COVER.md" ]]; then
    continue
  fi

  if [[ "$local_file" == "chapter_01_me.md" ]]; then
    kdp_pdf_files+=("kdp_mainmatter_break.md")
  fi

  kdp_pdf_files+=("$local_file")
done

echo "Building EPUB..."
pandoc "${book_files[@]}" \
  --file-scope \
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

pandoc "${book_files[@]}" \
  --file-scope \
  --metadata-file=metadata.md \
  --toc \
  -H pdf_preamble.tex \
  --pdf-engine="$PDF_ENGINE" \
  -o "$PDF_OUT"

echo "PDF build complete: $PDF_OUT"

echo "Building KDP interior PDF..."
pandoc "${kdp_pdf_files[@]}" \
  --file-scope \
  --metadata-file=metadata.md \
  --toc \
  --pdf-engine="$PDF_ENGINE" \
  -H pdf_preamble.tex \
  -H kdp_preamble.tex \
  -V classoption=twoside \
  -V geometry:paperwidth=6in \
  -V geometry:paperheight=9in \
  -V geometry:top=0.75in \
  -V geometry:bottom=0.75in \
  -V geometry:inner=0.75in \
  -V geometry:outer=0.5in \
  -o "$KDP_PDF_OUT"

echo "KDP interior PDF build complete: $KDP_PDF_OUT"
