import tempfile
import unittest
from pathlib import Path

from engine import chapter_balance, linkcheck, manpages, markdown_strip, readability, terminology_scan, wordcount


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

    def test_manpages_reports_absent_when_no_man_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = manpages.scan(Path(directory))
        self.assertEqual(result, {"present": False})

    def _write_page(self, man_dir: Path, name: str, see_also: str, source: str) -> None:
        (man_dir / f"{name}.md").write_text(
            "NAME\n"
            f"    {name} - test page\n\n"
            "SYNOPSIS\n    x\n\n"
            "DESCRIPTION\n    y\n\n"
            "NOTES\n    z\n\n"
            "SEE ALSO\n"
            f"    {see_also}\n\n"
            "SOURCE\n"
            f"    {source}\n",
            encoding="utf-8",
        )

    def test_manpages_detects_broken_see_also_and_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            man_dir = root / "man"
            man_dir.mkdir()
            (root / "chapters").mkdir()
            (root / "chapters" / "chapter_01.md").write_text("# Chapter 1\n", encoding="utf-8")

            self._write_page(man_dir, "good", "good(3)", "Chapter 1, probe.")
            self._write_page(man_dir, "bad", "nonexistent(3)", "Chapter 99, probe.")
            (man_dir / "README.md").write_text(
                "| [good](good.md) | 3 | ok | Ch1 |\n", encoding="utf-8"
            )

            result = manpages.scan(root)

        self.assertTrue(result["present"])
        self.assertEqual(result["page_count"], 2)
        self.assertEqual(result["orphan_pages"], ["bad"])
        self.assertEqual(result["missing_pages"], [])
        pages_by_name = {p["name"]: p for p in result["pages"]}
        self.assertEqual(pages_by_name["bad"]["broken_see_also"], ["nonexistent"])
        self.assertEqual(pages_by_name["bad"]["broken_source"], [99])
        self.assertEqual(pages_by_name["good"]["broken_see_also"], [])
        self.assertEqual(pages_by_name["good"]["broken_source"], [])


if __name__ == "__main__":
    unittest.main()
