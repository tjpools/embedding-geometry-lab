import json
import tempfile
import unittest
from pathlib import Path

from runtime.mode import CorpusMode, load_architecture, select_corpus


class CorpusModeTests(unittest.TestCase):
    def write_registry(self, root: Path) -> Path:
        registry = {
            "schema_version": 1,
            "architecture": {},
            "framing_sources": [
                {"order": 1, "title": "Frame", "path": "FRAME.md"}
            ],
            "chapter_globs": ["chapters/chapter_*.md"],
        }
        path = root / "registry.json"
        path.write_text(json.dumps(registry), encoding="utf-8")
        return path

    def test_selects_framing_mode_without_chapters(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "FRAME.md").write_text("# Frame\n", encoding="utf-8")
            mode, sources, _ = select_corpus(root, self.write_registry(root))

        self.assertEqual(mode, CorpusMode.FRAMING)
        self.assertEqual([source.path for source in sources], ["FRAME.md"])

    def test_switches_to_chapter_mode_when_draft_appears(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "FRAME.md").write_text("# Frame\n", encoding="utf-8")
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "chapter_02_path.md").write_text("# The Path\n", encoding="utf-8")
            mode, sources, _ = select_corpus(root, self.write_registry(root))

        self.assertEqual(mode, CorpusMode.CHAPTER)
        self.assertEqual(sources[0].order, 2)
        self.assertEqual(sources[0].title, "The Path")

    def test_architecture_is_derived_from_machine_readable_registries(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "modules.txt").write_text("a.one\nb.two\n", encoding="utf-8")
            (root / "dependencies.tsv").write_text("a.one\tb.two\n", encoding="utf-8")
            (root / "chapters.tsv").write_text("1\ta.one\n2\tb.two\n", encoding="utf-8")
            registry = {
                "architecture": {
                    "modules": "modules.txt",
                    "dependencies": "dependencies.tsv",
                    "chapter_mapping": "chapters.tsv",
                }
            }
            architecture = load_architecture(root, registry)

        self.assertEqual(architecture["module_count"], 2)
        self.assertEqual(architecture["edge_count"], 1)
        self.assertEqual(architecture["layers"], [["a.one"], ["b.two"]])
        self.assertEqual(architecture["chapter_density"][0]["outgoing_dependencies"], 1)

    def test_architecture_rejects_backward_chapter_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "modules.txt").write_text("a.one\nb.two\n", encoding="utf-8")
            (root / "dependencies.tsv").write_text("a.one\tb.two\n", encoding="utf-8")
            (root / "chapters.tsv").write_text("2\ta.one\n1\tb.two\n", encoding="utf-8")
            registry = {
                "architecture": {
                    "modules": "modules.txt",
                    "dependencies": "dependencies.tsv",
                    "chapter_mapping": "chapters.tsv",
                }
            }

            with self.assertRaisesRegex(ValueError, "backward dependency"):
                load_architecture(root, registry)

    def test_book_three_canonical_architecture(self):
        book_dir = Path(__file__).resolve().parents[2]
        registry = json.loads(
            (book_dir / "analytics/runtime/registry.json").read_text(encoding="utf-8")
        )

        architecture = load_architecture(book_dir, registry)

        self.assertEqual(architecture["module_count"], 27)
        self.assertEqual(architecture["edge_count"], 54)
        self.assertEqual(architecture["chapter_count"], 16)
        self.assertEqual(len(architecture["layers"]), 13)

    def test_book_three_framing_includes_governing_contracts(self):
        book_dir = Path(__file__).resolve().parents[2]
        registry_path = book_dir / "analytics/runtime/registry.json"

        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        paths = {source["path"] for source in registry["framing_sources"]}

        self.assertIn("CLOSURE_PROBE.md", paths)
        self.assertIn("PROVENANCE.md", paths)


if __name__ == "__main__":
    unittest.main()
