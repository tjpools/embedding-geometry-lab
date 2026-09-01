# Book Two — EPUB Metadata Provenance

**Established:** September 1, 2026
**Scope:** canonical and KDP-named EPUB artifacts

## Identity Source

The canonical source is [../metadata.md](../metadata.md), aligned with [../../publication/BOOK2_METADATA.md](../../publication/BOOK2_METADATA.md). The EPUB package identifier is the stable UUID `urn:uuid:ab0e3a95-77eb-4231-9fce-479936fd588d`. It is not an ISBN or ASIN. Kindle ebooks do not require an ISBN; Amazon assigns catalog identifiers during KDP ingestion.

Pandoc writes the Dublin Core title, subtitle, edition, creator, language, identifier, publisher, description, rights, type, subjects, date, and modified timestamp. [../analytics/finalize_epub.py](../analytics/finalize_epub.py) then adds the EPUB 3 collection and audience properties that Pandoc 2.9.2.1 does not emit from YAML:

- `belongs-to-collection`: `The Geometry of Meaning`
- `collection-type`: `series`
- `group-position`: `2`
- `dcterms:audience`: `General adult`

The finalizer parses and serializes the OPF as XML, preserves the EPUB entry order and compression metadata, and replaces any previously managed properties before adding one canonical set.

## Classification

The embedded subject set contains three BISAC codes and labels:

- `COM004000 — COMPUTERS / Artificial Intelligence / General`
- `MAT003000 — MATHEMATICS / Applied`
- `TEC000000 — TECHNOLOGY & ENGINEERING / General`

It also contains the seven final keyword phrases recorded in the publication metadata package. Amazon categories and keywords remain live KDP catalog fields and must be entered and confirmed there.

## Verification

On September 1, 2026:

- `transformers.epub` and `transformers-kdp.epub` were byte-identical
- EPUBCheck 5.3.0 reported zero errors and zero warnings
- `analytics/epub_audit.py` reported zero metadata issues and zero Calibre markers
- the package identifier was unique and referenced by the OPF `unique-identifier` attribute
- `dc:date` carried the canonical September 30, 2026 publication date and `dcterms:modified` carried the build-generated UTC timestamp

Book One's metadata source declares series position 1, and Book Three's publication metadata declares position 3. Their artifact-level OPF metadata is outside this Book Two gate and must be verified when those EPUBs are rebuilt.