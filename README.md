# Embedding Geometry Lab

Embedding Geometry Lab is the public repository for Embedding Geometry, a book-length project about computation, tools, mathematical structure, and human collaboration with transformer models.

The repository is not only a container for the book. It is part of the book's public structure: the place where builds, metrics, artifacts, and supporting documents remain inspectable.

## Core Thesis

Computation is the substrate.
Tools are configurations.
Understanding the configurations is understanding the domain.

The project treats modern AI neither as magic nor as personhood theater. Its guiding claim is that transformers become more intelligible when placed inside the longer history of tools, operators, notation, mathematics, and human craft.

## Start Here

If you want the reader-facing entry point, begin in [book/HOW_TO_READ_THIS_BOOK.md](book/HOW_TO_READ_THIS_BOOK.md).

If you want the full manuscript spine, go to [book/TOC.md](book/TOC.md).

If you want the package-facing structure for cover, title page, and framing, see [book/book_structure.md](book/book_structure.md), [book/metadata.md](book/metadata.md), and [book/SCRIBUS_KDP_COVER_WORKFLOW.md](book/SCRIBUS_KDP_COVER_WORKFLOW.md).

If you want the repository-side architecture, read [book/architecture_of_the_repository.md](book/architecture_of_the_repository.md).

## Repository Structure

- `book/` — the authoritative manuscript, front matter, eighteen chapters, back matter, build scripts, and package-facing docs
- `chapters_wordcount/` — generated chapter metrics and supporting artifacts
- `book/analysis_throughput/` — heatmaps, metric reports, and structural analysis outputs
- `experiments/` — runnable experiments and supporting code
- `notes/`, `pipeline/`, `tools/`, `environment/` — broader lab infrastructure and supporting materials around the book

The manuscript in `book/` is the current source of truth. EPUB, PDF, metrics, and related outputs are downstream artifacts.

## Architecture Map

The repository is organized by function rather than by file type alone.

- `README.md` — public entry point and governing stance
- `book/` — source of truth for manuscript, spine, front matter, back matter, and package decisions
- `book/analysis_throughput/` and `chapters_wordcount/` — analytics and self-description layers
- `book/BOOK_COVER.md`, `book/SCRIBUS_KDP_COVER_WORKFLOW.md`, `book/PRINT_PACKAGE_CHECKLIST.md`, `book/PRINT_COVER_TYPOGRAPHY_SPEC.md` — cover and packaging layer
- `book/build_book.sh`, `book/update_artifacts.sh`, `book/manifest.yml`, `book/metadata.md` — production layer
- `embedding-geometry.epub`, `embedding-geometry.pdf`, `embedding-geometry-6x9.pdf` — output artifacts
- `notes/`, `experiments/`, `pipeline/`, `environment/`, `marketing/` — support materials, exploratory work, and launch-facing surfaces around the book

This layout keeps the operating philosophy visible: source first, production second, analytics nearby, outputs downstream, and support materials clearly separated from the canonical manuscript.

## Build The Book

From the repository root:

```bash
bash book/build_book.sh
```

To rebuild the full downstream artifact set:

```bash
bash book/update_artifacts.sh
```

This refreshes the manuscript outputs plus structural metrics such as word counts and heatmaps.

`book/build_book.sh` and `book/update_artifacts.sh` are the canonical build entry points.

## Public Framing

The public-facing package currently centers on:

- Title: Embedding Geometry
- Subtitle: A Walkable Introduction to AI Through Building, Testing, and Collaboration
- Author: Terrence J McLaughlin

The book's structural core is organized around three coupled terms:

- Me
- Machine
- Us

The later chapters make explicit that the transformer matters not only as a machine, but as a bridge object in which the long human lineage and the long tool lineage become operationally joined.

## Rights

This repository is public so readers can inspect the structure, tooling, and development of the project. The text of the book itself is not open-licensed.

All chapters and written materials in `book/` remain All Rights Reserved unless stated otherwise.

## Working Principle

The project is meant to be entered, not merely consumed.

## Economics of Collaboration

The true cost of this project was never primarily financial. It was the cost every practitioner recognizes:

- time spent in the loop
- effort applied with discipline
- minimal tools used with precision
- curiosity sustained across complexity
- support exchanged in conversation

Those are the real inputs. Small in material terms, large in human terms.

The value created is disproportionate: priceless.

The price of the book will be determined later. The valuation of the work will be determined by the people who walk it. But the value is already clear: a system built through contact, constraint, inspection, and return.