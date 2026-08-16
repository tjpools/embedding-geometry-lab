import tempfile
import unittest
from pathlib import Path

from engine import chapter_balance, linkcheck, markdown_strip, readability, terminology_scan, wordcount


class AnalyticOperatorTests(unittest.TestCase):
    def test_markdown_cleaner_is_canonical_for_all_metrics(self):
        source = """---
title: Test
---
# Heading

Architecture [opens a path](target.md) through `visible code`.

```python
hidden implementation words
```
"""
        clean = markdown_strip.strip_markdown(source)
        self.assertIn("opens a path", clean)
        self.assertIn("visible code", clean)
        self.assertNotIn("hidden implementation", clean)
        self.assertEqual(wordcount.measure(clean)["words"], 8)

    def test_readability_metrics_include_book_one_cci(self):
        result = readability.measure("One short sentence. Another sentence.\n\nA third sentence.")
        self.assertEqual(result["sentences"], 3)
        self.assertEqual(result["paragraphs"], 2)
        self.assertEqual(result["cci"], 1.5)

    def test_terminology_density_uses_per_thousand_words(self):
        result = terminology_scan.scan("architecture " + "word " * 9, terms=("architecture",))
        self.assertEqual(result["term_counts"], {"architecture": 1})
        self.assertEqual(result["terminology_density"], 100.0)

    def test_linkcheck_separates_local_external_and_broken(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            (root / "exists.md").write_text("ok", encoding="utf-8")
            result = linkcheck.scan(
                "[ok](exists.md) [bad](missing.md) [web](https://example.com) [part](#part)",
                source,
            )
        self.assertEqual(result["links"], 4)
        self.assertEqual(result["local_links"], 2)
        self.assertEqual(result["external_links"], 1)
        self.assertEqual(result["anchor_links"], 1)
        self.assertEqual(result["broken_targets"], ["missing.md"])

    def test_balance_reports_distribution_without_grading_it(self):
        result = chapter_balance.calculate([
            {"order": 1, "title": "A", "words": 100},
            {"order": 2, "title": "B", "words": 200},
            {"order": 3, "title": "C", "words": 300},
        ])
        self.assertEqual(result["median_words"], 200.0)
        self.assertEqual(result["distribution"][0]["ratio_to_median"], 0.5)


if __name__ == "__main__":
    unittest.main()
