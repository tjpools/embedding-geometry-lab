import os
import matplotlib.pyplot as plt
import numpy as np

# Chapter word counts
chapters = [
    ("chapter_01_me", 83),
    ("chapter_02_machine", 95),
    ("chapter_cockpit", 892),
    ("chapter_michael_karina", 827),
    ("chapter_transformer", 936),
    ("chapter_03_us", 900),
]

labels = [c[0] for c in chapters]
counts = np.array([c[1] for c in chapters])
total = counts.sum()
percentages = counts / total * 100

fig, ax = plt.subplots(figsize=(8, 4))
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
