#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

OUTDIR=".."
EPUB_OUT="$OUTDIR/embedding-geometry.epub"
PDF_OUT="$OUTDIR/embedding-geometry.pdf"
KDP_PDF_OUT="$OUTDIR/embedding-geometry-6x9.pdf"

strip_epub_title_stub() {
  python3 - "$1" <<'PY'
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


epub_path = Path(sys.argv[1])
if not epub_path.exists():
  raise SystemExit(0)

XHTML_NS = "http://www.w3.org/1999/xhtml"
NCX_NS = "http://www.daisy.org/z3986/2005/ncx/"
OPF_NS = "http://www.idpf.org/2007/opf"

ET.register_namespace("", XHTML_NS)
ET.register_namespace("epub", "http://www.idpf.org/2007/ops")
ET.register_namespace("", NCX_NS)
ET.register_namespace("", OPF_NS)

with tempfile.TemporaryDirectory() as tmp_dir:
  tmp_path = Path(tmp_dir)
  with zipfile.ZipFile(epub_path) as archive:
    archive.extractall(tmp_path)

  content_opf = tmp_path / "EPUB" / "content.opf"
  title_stub = tmp_path / "EPUB" / "text" / "ch001.xhtml"
  nav_path = tmp_path / "EPUB" / "nav.xhtml"
  ncx_path = tmp_path / "EPUB" / "toc.ncx"

  if not all(path.exists() for path in (content_opf, title_stub, nav_path, ncx_path)):
    raise SystemExit(0)

  opf_root = ET.parse(content_opf).getroot()
  opf_ns = {"opf": OPF_NS, "dc": "http://purl.org/dc/elements/1.1/"}
  title_node = opf_root.find("./opf:metadata/dc:title", opf_ns)
  if title_node is None or not (title_node.text or "").strip():
    raise SystemExit(0)
  book_title = (title_node.text or "").strip()

  stub_root = ET.parse(title_stub).getroot()
  body = stub_root.find(f".//{{{XHTML_NS}}}body")
  if body is None:
    raise SystemExit(0)

  text_content = " ".join(" ".join(body.itertext()).split())
  sections = body.findall(f"{{{XHTML_NS}}}section")
  if text_content != book_title or len(sections) != 1:
    raise SystemExit(0)

  manifest = opf_root.find(f"{{{OPF_NS}}}manifest")
  spine = opf_root.find(f"{{{OPF_NS}}}spine")
  if manifest is None or spine is None:
    raise SystemExit(0)

  for item in list(manifest):
    if item.get("id") == "ch001_xhtml":
      manifest.remove(item)

  for itemref in list(spine):
    if itemref.get("idref") == "ch001_xhtml":
      spine.remove(itemref)

  ET.ElementTree(opf_root).write(content_opf, encoding="utf-8", xml_declaration=True)

  nav_root = ET.parse(nav_path).getroot()
  toc_ol = nav_root.find(f".//{{{XHTML_NS}}}nav[@id='toc']/{{{XHTML_NS}}}ol")
  if toc_ol is not None:
    for li in list(toc_ol):
      anchor = li.find(f"{{{XHTML_NS}}}a")
      if anchor is not None and (anchor.get("href") or "").startswith("text/ch001.xhtml"):
        toc_ol.remove(li)
  ET.ElementTree(nav_root).write(nav_path, encoding="utf-8", xml_declaration=True)

  ncx_root = ET.parse(ncx_path).getroot()
  nav_map = ncx_root.find(f"{{{NCX_NS}}}navMap")
  if nav_map is not None:
    for nav_point in list(nav_map):
      content = nav_point.find(f"{{{NCX_NS}}}content")
      if content is not None and (content.get("src") or "").startswith("text/ch001.xhtml"):
        nav_map.remove(nav_point)
  ET.ElementTree(ncx_root).write(ncx_path, encoding="utf-8", xml_declaration=True)

  title_stub.unlink()

  with zipfile.ZipFile(epub_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    mimetype = tmp_path / "mimetype"
    if mimetype.exists():
      archive.write(mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)
    for path in sorted(tmp_path.rglob("*")):
      if path.is_dir() or path == mimetype:
        continue
      archive.write(path, path.relative_to(tmp_path).as_posix())
PY
}

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

strip_epub_title_stub "$EPUB_OUT"

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
