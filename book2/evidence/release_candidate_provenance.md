# Book Two — Canonical Ebook Release Candidate

**Established:** September 1, 2026
**Decision:** repository engineering Gates 1–4 closed; candidate ready for Kindle Previewer and KDP upload testing

## Canonical Artifacts

| Artifact | Role | SHA-256 |
|---|---|---|
| `transformers.epub` | canonical EPUB | `7889fff0635d42d87ce3096cb8548973077799c79945a3b50c18fc36ccb2f00c` |
| `transformers-kdp.epub` | KDP upload candidate | `7889fff0635d42d87ce3096cb8548973077799c79945a3b50c18fc36ccb2f00c` |
| `transformers-kdp.docx` | fallback upload candidate | generated from the same manifest and metadata source |

The two EPUB names are byte-identical. The KDP-named file is copied directly from the finalized canonical EPUB; no Calibre conversion occurs.

## Closed Engineering Gates

1. **Structural integrity:** manifest, spine, navigation, hrefs, fragments, assets, and heading order validate with no defects.
2. **Calibre removal:** both EPUB names share one Pandoc/XML build path and contain no Calibre markers.
3. **Metadata and numbering:** title, subtitle, edition, creator, stable UUID, `en-US`, publisher, publication date, audience, subjects, keywords, and *The Geometry of Meaning* position 2 are embedded and audited.
4. **Reader handoffs:** `From Book One` precedes Chapter 1; `Continue to Book Three` follows the man-page layer; Book One source points forward and Book Three source receives the measured boundary.

## Verification Record

The final candidate passed:

- EPUBCheck 5.3.0 on both EPUB names: 0 errors, 0 warnings
- `analytics/epub_audit.py` on both EPUB names: 0 missing files, spine entries, hrefs, fragments, fallbacks, navigation inversions, handoff issues, metadata issues, or Calibre markers
- `PYTHONPATH=analytics python3 -m unittest discover -s analytics/tests -p 'test_*.py'`: 13/13 tests
- `python3 analytics/analyze.py`: 16 chapters, 25,172 words, 0 broken local links, 20/20 man pages clean
- byte comparison of the canonical and KDP-named EPUBs
- workspace diagnostics and Git whitespace checks

## Submission Boundary

This record makes the repository artifact canonical. It does not record Kindle Previewer results, KDP upload acceptance, final live categories, territorial-rights confirmation, KDP Select choice, content-origin disclosure, or the author's final decisions about optional back matter and acknowledgments. Those remain visible in [release_readiness.md](release_readiness.md) and [../KDP_UPLOAD_CHECKLIST.md](../KDP_UPLOAD_CHECKLIST.md).