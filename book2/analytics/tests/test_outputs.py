import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from engine.report import run


class OutputContractTests(unittest.TestCase):
    def build_book(self, root: Path) -> Path:
        (root / "FRAME.md").write_text("# Frame\n\nArchitecture constrains execution.\n", encoding="utf-8")
        (root / "modules.txt").write_text("a.one\nb.two\n", encoding="utf-8")
        (root / "dependencies.tsv").write_text("a.one\tb.two\n", encoding="utf-8")
        (root / "chapters.tsv").write_text("1\ta.one\n2\tb.two\n", encoding="utf-8")
        registry = {
            "schema_version": 1,
            "architecture": {
                "modules": "modules.txt",
                "dependencies": "dependencies.tsv",
                "chapter_mapping": "chapters.tsv",
            },
            "framing_sources": [{"order": 1, "title": "Frame", "path": "FRAME.md"}],
            "chapter_globs": ["chapters/chapter_*.md"],
        }
        registry_path = root / "registry.json"
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        return registry_path

    def test_framing_mode_emits_complete_output_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            result = run(root, self.build_book(root), output)
            expected = {
                "wordcounts.json", "balance.json", "terminology.json", "readability.json",
                "links.json", "heatmap.svg", "report.md", "metrics.csv", "report.json",
            }
            files = {path.name for path in output.iterdir()}
            heatmap_title = ET.parse(output / "heatmap.svg").getroot().find("{http://www.w3.org/2000/svg}title")

        self.assertEqual(result["mode"], "framing")
        self.assertEqual(files, expected)
        self.assertIsNotNone(heatmap_title)
        self.assertEqual(heatmap_title.text, "Book Two Architecture Density")

    def test_chapter_draft_switches_report_and_heatmap_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = self.build_book(root)
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "chapter_01_start.md").write_text("# Start\n\nA chapter begins.\n", encoding="utf-8")
            output = root / "output"
            result = run(root, registry, output)
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            heatmap_title = ET.parse(output / "heatmap.svg").getroot().find("{http://www.w3.org/2000/svg}title")

        self.assertEqual(result["mode"], "chapter")
        self.assertEqual(report["mode"], "chapter")
        self.assertEqual(heatmap_title.text, "Book Two Chapter Analytics")


if __name__ == "__main__":
    unittest.main()
