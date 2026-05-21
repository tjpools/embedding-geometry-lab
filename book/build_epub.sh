#!/usr/bin/env bash
# Build EPUB from canonical TOC and metadata
set -e
cd "$(dirname "$0")"

# Extract .md files in order from TOC.md
toc_files=$(grep -o '[a-zA-Z0-9_/-]*\.md' TOC.md | xargs)

# Build EPUB with Pandoc
pandoc $toc_files \
  --metadata-file=metadata.md \
  --toc \
  --epub-cover-image=cover.png \
  -o ../embedding-geometry.epub

echo "EPUB build complete: ../embedding-geometry.epub"