# Session Analysis and Benchmark

**Date:** July 29, 2026

## Commands Run
- `bash ./update_artifacts.sh`
- Full analytics refresh completed for word counts, chapter metrics, heatmap outputs, and book artifacts.

## Generated Artifacts
- `book/wordcounts.csv`
- `book/analysis_throughput/chapters_heatmap.md`
- `book/analysis_throughput/chapter_heatmap.png`
- `chapters_wordcount/chapters_metrics.md`
- `embedding-geometry.epub`
- `embedding-geometry.pdf`
- `embedding-geometry-6x9.pdf`

## Word Count Findings
- Total manuscript length: **42,208 words** across 18 chapters.
- Average chapter length: **2,344.89 words**.
- Median chapter length: **2,237 words**.
- Longest chapter: **Chapter 7, Leibniz/dx** at **5,579 words** (**13.2%** of total).
- Next largest chapters: **Chapter 3** at **3,735 words**, **Chapter 15** at **3,331 words**, and **Chapter 11** at **3,051 words**.
- Shortest chapters remain the intentional threshold chapters: **Chapter 1** at **670 words** and **Chapter 2** at **847 words**.

## Heatmap Findings
- The manuscript shows one dominant density peak at **Chapter 7**, which remains the main curvature ridge of the book.
- Secondary concentration bands appear at **Chapter 3**, **Chapter 11**, and **Chapter 15**.
- The closing arc from **Chapter 14** through **Chapter 18** forms a sustained but controlled ridge rather than a spike, which supports the late-book compression strategy.
- The Chapters **8-10** story band reads as a coherent mid-book shelf rather than a distortion peak:
  - Chapter 8: **1,405** words
  - Chapter 9: **2,092** words
  - Chapter 10: **1,624** words
  - Combined 8-10 total: **5,121** words

## Metrics Findings
- The late analytic and closure arc, **Chapters 14-18**, totals **12,867 words**, indicating substantial but not runaway final density.
- Highest CCI values:
  - **Chapter 2**: **4.92**
  - **Chapter 1**: **4.67**
  - **Chapter 16**: **4.18**
  - **Chapter 17**: **4.04**
- Lowest CCI values:
  - **Chapter 9**: **1.68**
  - **Chapter 7**: **2.23**
  - **Chapter 10**: **2.52**
- Interpretation:
  - Higher CCI chapters are carrying more compressed sentence density per paragraph.
  - Lower CCI chapters are using broader paragraph distribution, which helps navigability in structurally heavy material.
  - **Chapter 9** is notably spacious in paragraphing, which fits its role as architectural orientation.
  - **Chapter 10** remains operationally readable rather than overcompressed, which suits its cockpit function.

## Structural Findings
- The front matter of the argument remains intentionally light: Chapters 1-2 act as threshold chapters rather than mass-bearing chapters.
- The book's central conceptual load still sits where expected: the human-machine coupling, differential inheritance, and executable proof-object regions.
- The revised late arc now behaves coherently:
  - Chapter 17 widens the landscape.
  - Chapter 18 resolves the manifold into triadic closure.
  - The postscript performs the final compression into the glyph thesis.
- No new structural imbalance was introduced by the recent reframing work.

## Validation
- EPUB build: passed.
- PDF build: passed.
- KDP interior PDF build: passed.
- Workspace diagnostics: no errors found.

## Line Separation, Syntax, and Structure Pass
- Parser-backed markdown syntax check run with `pandoc` across all 18 chapter files.
- Result: **all chapters parsed successfully**; no markdown syntax failures detected.
- Code fence balance: no unbalanced fenced code blocks detected.
- Line-separation findings:
  - Most initial spacing flags were false positives caused by the standard chapter preamble (`\newpage` and `\vspace*`) before the chapter H1.
  - After refinement, the only remaining spacing flags were in **Chapter 7** and **Chapter 9**.
  - These are heading-stack patterns rather than parser errors: an H1 immediately followed by an H2 in Chapter 7, and repeated H2/H3 adjacency in Chapter 9.
  - Interpretation: these are **style-level structure issues**, not syntax failures.
- Paragraph structure findings:
  - **Chapter 8** contains one long paragraph at **142 words**.
  - **Chapter 12** contains one long paragraph at **168 words**.
  - No other chapters crossed the long-paragraph threshold used in the test pass.
- Average prose paragraph length remained controlled across the manuscript, with especially readable structural chapters in the middle band:
  - **Chapter 9** average prose paragraph length: **21.8 words**
  - **Chapter 10** average prose paragraph length: **25.3 words**

## Grammar Pass Status
- No dedicated grammar linter is currently installed in the environment.
- Checked tools: `vale`, `write-good`, `markdownlint`, `aspell`, and `hunspell` were unavailable.
- `pandoc` was available and used for syntax validation only.
- Result: **no true automated grammar check was run** in this pass.
- Practical proxy used instead: paragraph-length analytics plus parser-backed markdown validation.

## Vale Grammar Pass
- Installed **Vale 3.16.0** locally at `/home/tjpools/.local/bin/vale`.
- Added a repo-local Vale configuration at `book/.vale.ini` with manuscript-specific rules.
- Current ruleset checks:
  - repeated-word detection
  - average sentence-length pressure
  - average paragraph-length pressure
- Command run:
  - `PATH="/home/tjpools/.local/bin:$PATH" vale --config=.vale.ini chapter_*.md`
- Result: **0 errors, 0 warnings, and 0 suggestions across 18 files**.
- Interpretation: under the current manuscript-focused Vale ruleset, the prose passed cleanly.

## Non-Blocking Warnings
- Matplotlib `Axes3D` import warning.
- `QStandardPaths` runtime directory permissions warning.
- `tight_layout` warning from `chapter_metrics_suite.py`.

These warnings did not block analytics generation or manuscript builds.

## Benchmark Summary
- The manuscript is currently balanced around one major central peak and a deliberate late-book ridge.
- The story triad is proportionate and operationally stable.
- The final arc has enough mass to feel conclusive without overwhelming Chapter 18 or the postscript.
- Markdown syntax is clean across all tracked chapters.
- Remaining line-separation flags are limited and stylistic rather than blocking.
- Current state is suitable for continued editorial refinement, packaging, or release preparation.