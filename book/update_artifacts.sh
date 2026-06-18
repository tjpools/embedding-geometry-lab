#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Refreshing chapter word counts..."
python3 book/wordcount_report.py

echo "Refreshing chapter metrics..."
python3 book/analysis_throughput/chapter_metrics_suite.py

echo "Refreshing chapter heatmap..."
python3 book/analysis_throughput/chapter_heatmap.py

echo "Building EPUB and PDF..."
bash book/build_book.sh

echo "All manuscript artifacts updated."