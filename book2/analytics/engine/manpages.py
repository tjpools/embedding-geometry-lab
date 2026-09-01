"""Cross-reference check for the book2/man/ lookup layer.

Verifies that the man-page suite is internally consistent: every page has the
required Unix-style sections, every SEE ALSO reference resolves to another
page that actually exists, every SOURCE citation resolves to an existing
chapter, and the README index matches the files on disk exactly. This is a
structural check, not a content grade.
"""

import re
from pathlib import Path
from typing import Dict, List

REQUIRED_SECTIONS = ("NAME", "SYNOPSIS", "DESCRIPTION", "NOTES", "SEE ALSO", "SOURCE")
SEE_ALSO_REF_RE = re.compile(r"\b([a-z][a-z0-9-]*)\((\d+)\)")
INDEX_ROW_RE = re.compile(r"^\|\s*\[([a-z0-9-]+)\]\(([a-z0-9-]+\.md)\)\s*\|")
CHAPTER_REF_RE = re.compile(r"Chapter (\d+)")


def _section_positions(text: str) -> Dict[str, int]:
    positions = {}
    for match in re.finditer(r"(?m)^([A-Z][A-Z ]+)$", text):
        label = match.group(1).strip()
        if label in REQUIRED_SECTIONS and label not in positions:
            positions[label] = match.start()
    return positions


def _section_body(text: str, positions: Dict[str, int], label: str) -> str:
    if label not in positions:
        return ""
    start = positions[label]
    later = sorted(pos for pos in positions.values() if pos > start)
    end = later[0] if later else len(text)
    return text[start:end]


def scan(book_dir: Path) -> Dict[str, object]:
    man_dir = book_dir / "man"
    if not man_dir.exists():
        return {"present": False}

    page_paths = sorted(p for p in man_dir.glob("*.md") if p.name != "README.md")
    page_names = {p.stem for p in page_paths}
    chapters_dir = book_dir / "chapters"

    pages: List[dict] = []
    for path in page_paths:
        text = path.read_text(encoding="utf-8")
        positions = _section_positions(text)
        missing_sections = [label for label in REQUIRED_SECTIONS if label not in positions]

        see_also_body = _section_body(text, positions, "SEE ALSO")
        referenced = sorted(set(m.group(1) for m in SEE_ALSO_REF_RE.finditer(see_also_body)))
        broken_see_also = [name for name in referenced if name != path.stem and name not in page_names]

        source_body = _section_body(text, positions, "SOURCE")
        chapter_numbers = [int(m.group(1)) for m in CHAPTER_REF_RE.finditer(source_body)]
        broken_source = [
            n for n in chapter_numbers
            if not (chapters_dir / f"chapter_{n:02d}.md").exists()
        ]

        pages.append({
            "name": path.stem,
            "missing_sections": missing_sections,
            "see_also_refs": referenced,
            "broken_see_also": broken_see_also,
            "source_chapters": chapter_numbers,
            "broken_source": broken_source,
        })

    readme_path = man_dir / "README.md"
    indexed_names = []
    if readme_path.exists():
        for line in readme_path.read_text(encoding="utf-8").splitlines():
            match = INDEX_ROW_RE.match(line)
            if match:
                indexed_names.append(match.group(1))

    orphan_pages = sorted(page_names - set(indexed_names))
    missing_pages = sorted(set(indexed_names) - page_names)

    clean_pages = sum(
        1 for p in pages
        if not p["missing_sections"] and not p["broken_see_also"] and not p["broken_source"]
    )

    return {
        "present": True,
        "page_count": len(pages),
        "indexed_count": len(indexed_names),
        "clean_pages": clean_pages,
        "orphan_pages": orphan_pages,
        "missing_pages": missing_pages,
        "pages": pages,
    }
