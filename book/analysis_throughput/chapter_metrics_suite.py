import os
import re
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Directory containing chapters
CHAPTERS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Find all chapter files
chapter_files = [f for f in os.listdir(CHAPTERS_DIR) if re.match(r'^chapter_.*\\.md$', f)]
chapter_files = [f for f in chapter_files if not f.startswith('book_structure')]

# Coherence Tracker & Learning Manifold Toolkit (modularized)
import os
import re
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

UNITS_DIR = '../'  # Directory containing units (chapters, topics, etc.)
UNIT_PREFIX = 'chapter_'  # Default prefix (can be changed for other domains)
UNIT_SUFFIX = '.md'      # Default suffix (can be changed for other domains)

def count_words(text):
    return len(text.split())

def count_sentences(text):
    return len(re.findall(r'[.!?]+', text))

def count_paragraphs(text):
    return len([p for p in text.split('\n') if p.strip()])

def get_unit_files():
    # Only include chapters 01-12 in the correct directory
    chapter_nums = [f"{i:02d}" for i in range(1, 13)]
    files = []
    for num in chapter_nums:
        pattern = f"chapter_{num}"
        for f in os.listdir(CHAPTERS_DIR):
            if f.startswith(pattern) and f.endswith(UNIT_SUFFIX):
                files.append(f)
    return files

def get_last_modified(path):
    return datetime.fromtimestamp(os.path.getmtime(path))

def analyze_unit(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    word_count = count_words(text)
    sentence_count = count_sentences(text)
    para_count = count_paragraphs(text)
    last_modified = get_last_modified(path)
    cci = round(sentence_count / para_count, 2) if para_count > 0 else 0
    return {
        'words': word_count,
        'sentences': sentence_count,
        'paragraphs': para_count,
        'cci': cci,
        'last_modified': last_modified,
    }

def main():
    unit_files = get_unit_files()
    units = []
    for fname in sorted(unit_files):
        path = os.path.join(CHAPTERS_DIR, fname)
        metrics = analyze_unit(path)
        metrics['name'] = fname
        units.append(metrics)
    total_words = sum(u['words'] for u in units)
    percentages = [u['words'] / total_words * 100 if total_words > 0 else 0 for u in units]

    # Markdown summary table
    with open('chapters_wordcount/chapters_metrics.md', 'w', encoding='utf-8') as f:
        f.write('| Unit | Words | % of Total | Sentences | Paragraphs | CCI | Last Modified |\n')
        f.write('|------|-------|------------|-----------|------------|-----|---------------|\n')
        for u, pct in zip(units, percentages):
            f.write(f"| {u['name']} | {u['words']} | {pct:.1f}% | {u['sentences']} | {u['paragraphs']} | {u['cci']} | {u['last_modified'].strftime('%Y-%m-%d %H:%M')} |\n")
        f.write(f"\nTotal words: {total_words}\n")

    # Heatmap visualization
    word_counts = [u['words'] for u in units]
    fig, ax = plt.subplots(figsize=(10, 1))
    ax.imshow([word_counts], cmap='viridis', aspect='auto')
    ax.set_yticks([])
    ax.set_xticks(range(len(units)))
    ax.set_xticklabels([u['name'] for u in units], rotation=90, fontsize=8)
    for i, count in enumerate(word_counts):
        ax.text(i, 0, str(count), va='center', ha='center', color='white', fontsize=8)
    plt.tight_layout()
    plt.savefig('chapters_wordcount/heatmap.png')
    plt.close()

if __name__ == '__main__':
    main()
