
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT_DIR = Path(__file__).resolve().parents[2]
WORDCOUNTS_CSV = ROOT_DIR / "book" / "wordcounts.csv"
OUTPUT_MD = ROOT_DIR / "book" / "analysis_throughput" / "chapters_heatmap.md"
OUTPUT_IMG = ROOT_DIR / "book" / "analysis_throughput" / "chapter_heatmap.png"


def load_wordcounts():
    with WORDCOUNTS_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if row.get("status") == "ok"]


def make_bar(value: float, max_value: float, width: int = 6) -> str:
    if max_value <= 0:
        return ""
    filled = max(1, round((value / max_value) * width))
    return "█" * filled


def main():
    rows = load_wordcounts()
    labels = [f"Ch {row['chapter']}" for row in rows]
    counts = np.array([int(row["word_count"]) for row in rows])
    titles = [row["title"] for row in rows]
    total = counts.sum()
    percentages = counts / total * 100 if total > 0 else np.zeros_like(counts)

    fig, ax = plt.subplots(figsize=(max(10, len(labels) * 0.7), 4))
    heat = ax.imshow([percentages], cmap="YlOrRd", aspect="auto")
    ax.set_yticks([])
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")

    for index, pct in enumerate(percentages):
        ax.text(index, 0, f"{counts[index]}\n{pct:.1f}%", va="center", ha="center", color="black", fontsize=9)

    plt.title("Chapter Word Count Heatmap")
    plt.colorbar(heat, orientation="vertical", label="Relative Density (%)")
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG)
    plt.close()

    max_pct = float(percentages.max()) if len(percentages) > 0 else 1.0
    md_lines = [
        "| Chapter | Title | Word Count | % of Total | Heatmap |",
        "|---------|-------|-----------:|-----------:|---------|",
    ]
    for label, title, count, pct in zip(labels, titles, counts, percentages):
        md_lines.append(f"| {label} | {title} | {count} | {pct:.1f}% | {make_bar(float(pct), max_pct):<6} |")
    md_lines.append("")
    md_lines.append(f"Total words: {int(total):,}")

    OUTPUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
