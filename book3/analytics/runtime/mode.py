import csv
import json
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Tuple


CHAPTER_NUMBER_RE = re.compile(r"chapter[_\s-]*(\d+)", re.IGNORECASE)
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


class CorpusMode(str, Enum):
    FRAMING = "framing"
    CHAPTER = "chapter"


@dataclass(frozen=True)
class SourceUnit:
    kind: str
    order: int
    title: str
    path: str


def load_registry(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        registry = json.load(handle)
    if registry.get("schema_version") != 1:
        raise ValueError("Unsupported analytics registry schema")
    return registry


def infer_chapter_number(path: Path) -> int:
    match = CHAPTER_NUMBER_RE.search(path.stem)
    if not match:
        raise ValueError(f"Chapter filename has no number: {path.name}")
    return int(match.group(1))


def infer_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = HEADING_RE.search(text)
    return match.group(1).strip() if match else path.stem.replace("_", " ").replace("-", " ").title()


def discover_chapters(book_dir: Path, registry: dict) -> List[SourceUnit]:
    discovered = {}
    for pattern in registry.get("chapter_globs", []):
        for path in book_dir.glob(pattern):
            resolved = path.resolve()
            discovered[resolved] = SourceUnit(
                kind=CorpusMode.CHAPTER.value,
                order=infer_chapter_number(path),
                title=infer_title(path),
                path=str(path.relative_to(book_dir)),
            )
    return sorted(discovered.values(), key=lambda unit: (unit.order, unit.path))


def framing_sources(registry: dict) -> List[SourceUnit]:
    return [
        SourceUnit(
            kind=CorpusMode.FRAMING.value,
            order=int(item["order"]),
            title=item["title"],
            path=item["path"],
        )
        for item in registry.get("framing_sources", [])
    ]


def select_corpus(book_dir: Path, registry_path: Path) -> Tuple[CorpusMode, List[SourceUnit], dict]:
    registry = load_registry(registry_path)
    chapters = discover_chapters(book_dir, registry)
    if chapters:
        return CorpusMode.CHAPTER, chapters, registry
    return CorpusMode.FRAMING, framing_sources(registry), registry


def read_nonblank_lines(path: Path) -> List[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def read_edges(path: Path) -> List[Tuple[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [(row[0].strip(), row[1].strip()) for row in csv.reader(handle, delimiter="\t") if len(row) >= 2]


def topological_layers(modules: List[str], edges: List[Tuple[str, str]]) -> List[List[str]]:
    outgoing = defaultdict(list)
    indegree = {module: 0 for module in modules}
    for source, target in edges:
        outgoing[source].append(target)
        indegree[target] += 1

    queue = deque(sorted(module for module, degree in indegree.items() if degree == 0))
    layers = []
    visited = 0
    while queue:
        current_layer = list(queue)
        queue.clear()
        layers.append(current_layer)
        for source in current_layer:
            visited += 1
            for target in outgoing[source]:
                indegree[target] -= 1
                if indegree[target] == 0:
                    queue.append(target)
        queue = deque(sorted(queue))
    if visited != len(modules):
        raise ValueError("Analytics architecture registry contains a dependency cycle")
    return layers


def load_architecture(book_dir: Path, registry: dict) -> dict:
    paths = registry["architecture"]
    modules = read_nonblank_lines(book_dir / paths["modules"])
    edges = read_edges(book_dir / paths["dependencies"])
    chapter_pairs = read_edges(book_dir / paths["chapter_mapping"])
    module_chapters = {module: int(chapter) for chapter, module in chapter_pairs}

    if len(chapter_pairs) != len(module_chapters):
        raise ValueError("Analytics chapter mapping assigns a module more than once")
    if set(modules) != set(module_chapters):
        raise ValueError("Analytics chapter mapping does not cover the canonical module registry")
    if any(source not in module_chapters or target not in module_chapters for source, target in edges):
        raise ValueError("Analytics dependencies reference an unknown module")
    if any(module_chapters[source] > module_chapters[target] for source, target in edges):
        raise ValueError("Analytics chapter mapping contains a backward dependency")

    chapter_density = []
    for chapter in sorted(set(module_chapters.values())):
        chapter_modules = sorted(module for module, number in module_chapters.items() if number == chapter)
        incoming = sum(module_chapters[source] < chapter == module_chapters[target] for source, target in edges)
        internal = sum(module_chapters[source] == chapter == module_chapters[target] for source, target in edges)
        outgoing = sum(module_chapters[source] == chapter < module_chapters[target] for source, target in edges)
        cross_crate = sum(
            module_chapters[source] == chapter and source.split(".", 1)[0] != target.split(".", 1)[0]
            for source, target in edges
        )
        chapter_density.append({
            "chapter": chapter,
            "modules": chapter_modules,
            "module_count": len(chapter_modules),
            "incoming_dependencies": incoming,
            "internal_dependencies": internal,
            "outgoing_dependencies": outgoing,
            "cross_crate_edges": cross_crate,
        })

    return {
        "module_count": len(modules),
        "edge_count": len(edges),
        "chapter_count": len(chapter_density),
        "layers": topological_layers(modules, edges),
        "chapter_density": chapter_density,
    }
