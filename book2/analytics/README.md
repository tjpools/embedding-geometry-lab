# Book Two Analytics

This directory is Book Two's self-inspection layer. A standard-library Python engine measures the current corpus and emits human-readable, machine-readable, and visual artifacts.

## Architecture

- `engine/` contains focused analytic operators and reporters.
- `runtime/` contains corpus discovery and the canonical analytics registry.
- `tests/` contains parser, calculation, mode-switching, architecture, and output-contract tests.
- `output/` contains generated artifacts.
- `analyze.py` remains the stable public command.

## Run

From `book2/`:

```bash
python3 analytics/analyze.py
```

Run the full test suite with:

```bash
PYTHONPATH=analytics python3 -m unittest discover -s analytics/tests -p 'test_*.py'
```

## Runtime Modes

The engine selects its corpus automatically from [runtime/registry.json](runtime/registry.json).

- **Framing mode:** when no chapter drafts exist, it measures the canonical framing documents and visualizes module and dependency density across the 16-chapter architecture.
- **Chapter mode:** when a matching chapter draft appears under `chapters/` or `manuscript/`, it measures chapter prose and switches the heatmap to manuscript metrics.

Planning notes, generated reports, and publication outputs are never discovered as manuscript sources.

## Outputs

The `output/` directory contains:

- `wordcounts.json`
- `balance.json`
- `terminology.json`
- `readability.json`
- `links.json`
- `metrics.csv`
- `report.json`
- `report.md`
- `heatmap.svg`

## Engines

- **Volume:** words, corpus share, and median source length
- **Shape:** sentences, paragraphs, headings, average sentence length, long-sentence rate, and Chapter Curvature Index (sentences per paragraph)
- **Vocabulary:** unique-word ratio and selected structural-term density per 1,000 words
- **Readability:** a heuristic Flesch-style estimate, used comparatively rather than as a quality score
- **Integrity:** local Markdown targets plus an inventory of external and anchor links
- **Architecture:** module layers and chapter dependency density derived from the canonical DAG
- **Visual density:** a mode-aware, column-normalized heatmap using the Book Two palette

External URLs are inventoried but not requested over the network; network availability is not reproducible enough to be a default manuscript gate.

The metrics describe the manuscript; they do not grade it. A high or low value becomes meaningful only when inspected against the chapter's structural purpose.
