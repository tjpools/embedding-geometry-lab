# Book Two

**Title:** *Transformers: An Architecture for Geometric Computation*  
**Subtitle:** *How AI, Mathematics, and Programming Converge into a Single Tool*

Book Two is an independent manuscript package within the Embedding Geometry Lab. It follows the parallel AI, mathematical, and programming journeys that converge in the transformer.

The public promise is defined in [GLOBAL_MANIFEST.md](GLOBAL_MANIFEST.md). The canonical internal architecture is [book_structure.md](book_structure.md).
Module prerequisites and cross-crate interfaces are recorded in [dependency_map.md](dependency_map.md). The derived narrative order is [CHAPTER_MANIFEST.md](CHAPTER_MANIFEST.md). The book-wide visual grammar and chapter anchors are defined in [VISUAL_LANGUAGE.md](VISUAL_LANGUAGE.md) and [VISUAL_MANIFEST.md](VISUAL_MANIFEST.md). Development gates are defined in [manuscript_workflow.md](manuscript_workflow.md), and chapter execution begins with [chapter_briefs/chapter_01.md](chapter_briefs/chapter_01.md) and [chapter_briefs/chapter_02.md](chapter_briefs/chapter_02.md).

## Crates

- [ai_journey/](ai_journey/) — the conceptual lineage of AI
- [math_journey/](math_journey/) — the mathematical dependencies
- [programming_journey/](programming_journey/) — the executable systems lineage
- [convergence/](convergence/) — their integration in the transformer

## Boundary

Book Two explains architecture: what the transformer inherited, how its components work together, how mathematical ideas become executable systems, and where constraints enter the design.

Questions about closure, geometry as philosophy, and the ultimate limits of transformer intelligence belong to Book Three. Book Two may establish the technical evidence for those questions without attempting to close them philosophically.

## Analytics

The self-inspection engine is documented in [analytics/README.md](analytics/README.md). Run it from this directory with:

```bash
python3 analytics/analyze.py
```

The current generated report and heatmap are [analytics/output/report.md](analytics/output/report.md) and [analytics/output/heatmap.svg](analytics/output/heatmap.svg).

## Publication

The coordinated Book Two and Book Three rollout is [../publication/README.md](../publication/README.md). Book Two's KDP metadata draft is [../publication/BOOK2_METADATA.md](../publication/BOOK2_METADATA.md), subject to the manuscript-ready submission gate in [../publication/KDP_RULES.md](../publication/KDP_RULES.md).

## Status

The 16-chapter technical manuscript is verified and integrated across all four parts at 24,802 analytics words with zero broken local links. Every chapter has a brief, bounded source ledger, reproducible evidence record, and one original visual anchor with color, grayscale, and thumbnail exports. All chapter probes, documented visual checksums, analytics tests, and workspace diagnostics pass. The complete result is recorded in the [full-book integration audit](evidence/full_book_integration.md).

Publication release-candidate status remains open under the [release-readiness audit](evidence/release_readiness.md). Book Two still needs canonical front matter, back matter, acknowledgments, final bibliography and permissions resolution, confirmed publication metadata, and ebook/print build tooling with device and typography checks. Cover publication assets are available as working proofs.