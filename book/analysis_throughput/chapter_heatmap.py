
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

def count_words(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    # Count words by splitting on whitespace
    return len(text.split())

if __name__ == "__main__":
    # Accept chapter files as command-line arguments
    chapter_files = sys.argv[1:]
    chapters = []
    for f in chapter_files:
        label = os.path.splitext(os.path.basename(f))[0]
        wc = count_words(f)
        chapters.append((label, wc))

    labels = [c[0] for c in chapters]
    counts = np.array([c[1] for c in chapters])
    total = counts.sum()
    percentages = counts / total * 100 if total > 0 else np.zeros_like(counts)

    # Generate heatmap
    fig, ax = plt.subplots(figsize=(max(8, len(labels)), 4))
    heat = ax.imshow([percentages], cmap="YlOrRd", aspect="auto")

    ax.set_yticks([])
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")

    for i, pct in enumerate(percentages):
        ax.text(i, 0, f"{int(counts[i])}\n{pct:.1f}%", va="center", ha="center", color="black", fontsize=10)

    plt.title("Chapter Synthesis & Coherence Heatmap")
    plt.colorbar(heat, orientation="vertical", label="Relative Density (%)")
    plt.tight_layout()
    plt.savefig("chapter_heatmap.png")
    plt.show()

    # Write markdown table
    md_lines = [
        "| Chapter | Word Count | % of Total | Heatmap |",
        "|------------------------|------------|------------|---------|"
    ]
    # Compute heatmap bar
    max_pct = percentages.max() if len(percentages) > 0 else 1
    for label, count, pct in zip(labels, counts, percentages):
        bar = "█" * int(round(6 * pct / max_pct)) if max_pct > 0 else ""
        md_lines.append(f"| {label:<22} | {count:10} | {pct:10.1f}% | {bar:<7} |")
    md_lines.append("")
    md_lines.append(f"Total words: {total}")

    with open("book/analysis_throughput/chapters_heatmap.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
