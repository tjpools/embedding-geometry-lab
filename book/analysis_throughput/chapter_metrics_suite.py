import csv
import re
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


ROOT_DIR = Path(__file__).resolve().parents[2]
BOOK_DIR = ROOT_DIR / "book"
CHAPTERS_CSV = BOOK_DIR / "chapters.csv"
METRICS_OUTPUT = ROOT_DIR / "chapters_wordcount" / "chapters_metrics.md"
HEATMAP_OUTPUT = ROOT_DIR / "chapters_wordcount" / "heatmap.png"

WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)
FRONTMATTER_RE = re.compile(r"(?s)\A---\n.*?\n---\n?")
FENCED_CODE_RE = re.compile(r"(?s)```.*?```")
INLINE_CODE_RE = re.compile(r"`([^`]*)`")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
FOOTNOTE_RE = re.compile(r"\[\^([^\]]+)\]")
HEADER_MARK_RE = re.compile(r"^\s{0,3}#{1,6}\s*", re.MULTILINE)
BLOCKQUOTE_RE = re.compile(r"^\s{0,3}>\s?", re.MULTILINE)
LIST_MARK_RE = re.compile(r"^\s*[-*+]\s+", re.MULTILINE)
ORDERED_LIST_RE = re.compile(r"^\s*\d+\.\s+", re.MULTILINE)
TABLE_PIPE_RE = re.compile(r"\|")
EMPHASIS_RE = re.compile(r"[*_~]")
REFERENCE_LINK_DEF_RE = re.compile(r"^\s*\[[^\]]+\]:\s+\S+.*$", re.MULTILINE)


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def strip_markdown(text: str) -> str:
    text = strip_frontmatter(text)
    text = FENCED_CODE_RE.sub(" ", text)
    text = REFERENCE_LINK_DEF_RE.sub(" ", text)
    text = IMAGE_RE.sub(r"\1", text)
    text = LINK_RE.sub(r"\1", text)
    text = INLINE_CODE_RE.sub(r"\1", text)
    text = HEADER_MARK_RE.sub("", text)
    text = BLOCKQUOTE_RE.sub("", text)
    text = LIST_MARK_RE.sub("", text)
    text = ORDERED_LIST_RE.sub("", text)
    text = FOOTNOTE_RE.sub(r"\1", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = TABLE_PIPE_RE.sub(" ", text)
    text = EMPHASIS_RE.sub("", text)
    return text


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def count_sentences(text: str) -> int:
    return len(re.findall(r"[.!?]+", text))


def count_paragraphs(text: str) -> int:
    return len([p for p in text.split("\n\n") if p.strip()])


def load_chapters():
    with CHAPTERS_CSV.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def analyze_unit(file_path: Path):
    raw_text = file_path.read_text(encoding="utf-8")
    clean_text = strip_markdown(raw_text)
    word_count = count_words(clean_text)
    sentence_count = count_sentences(clean_text)
    para_count = count_paragraphs(clean_text)
    last_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
    cci = round(sentence_count / para_count, 2) if para_count > 0 else 0
    return {
        "words": word_count,
        "sentences": sentence_count,
        "paragraphs": para_count,
        "cci": cci,
        "last_modified": last_modified,
    }


def main():
    units = []
    for row in load_chapters():
        rel_path = Path(row["path"].strip())
        file_path = ROOT_DIR / rel_path
        metrics = analyze_unit(file_path)
        metrics["name"] = file_path.name
        units.append(metrics)

    total_words = sum(unit["words"] for unit in units)
    percentages = [unit["words"] / total_words * 100 if total_words > 0 else 0 for unit in units]

    with METRICS_OUTPUT.open("w", encoding="utf-8") as handle:
        handle.write("| Unit | Words | % of Total | Sentences | Paragraphs | CCI | Last Modified |\n")
        handle.write("|------|-------|------------|-----------|------------|-----|---------------|\n")
        for unit, pct in zip(units, percentages):
            handle.write(
                f"| {unit['name']} | {unit['words']} | {pct:.1f}% | {unit['sentences']} | {unit['paragraphs']} | {unit['cci']} | {unit['last_modified'].strftime('%Y-%m-%d %H:%M')} |\n"
            )
        handle.write(f"\nTotal words: {total_words}\n")

    word_counts = [unit["words"] for unit in units]
    fig, ax = plt.subplots(figsize=(12, 2.5))
    ax.imshow([word_counts], cmap="viridis", aspect="auto")
    ax.set_yticks([])
    ax.set_xticks(range(len(units)))
    ax.set_xticklabels(
        [unit["name"].replace("chapter_", "ch_").replace(".md", "") for unit in units],
        rotation=60,
        ha="right",
        fontsize=8,
    )
    for index, count in enumerate(word_counts):
        ax.text(index, 0, str(count), va="center", ha="center", color="white", fontsize=8)
    plt.tight_layout()
    plt.savefig(HEATMAP_OUTPUT)
    plt.close()


if __name__ == "__main__":
    main()
