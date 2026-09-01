#!/usr/bin/env python3
import argparse
import posixpath
import tempfile
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

CONTAINER_NS = "urn:oasis:names:tc:opendocument:xmlns:container"
OPF_NS = "http://www.idpf.org/2007/opf"
DC_NS = "http://purl.org/dc/elements/1.1/"
XHTML_NS = "http://www.w3.org/1999/xhtml"

EXPECTED_METADATA = {
    "identifier": "urn:uuid:ab0e3a95-77eb-4231-9fce-479936fd588d",
    "language": "en-US",
    "creator": "Terrence J McLaughlin",
    "publisher": "McLaughlin Tools Press",
}
EXPECTED_SUBJECTS = [
    "COM004000 — COMPUTERS / Artificial Intelligence / General",
    "MAT003000 — MATHEMATICS / Applied",
    "TEC000000 — TECHNOLOGY & ENGINEERING / General",
    "transformer model",
    "geometric computation",
    "machine learning architecture",
    "embeddings",
    "attention mechanism",
    "mathematics and programming",
    "deep learning systems",
]


def package_path(root: Path) -> PurePosixPath:
    container = ET.parse(root / "META-INF/container.xml")
    rootfile = container.find(f".//{{{CONTAINER_NS}}}rootfile")
    if rootfile is None:
        raise ValueError("container.xml has no rootfile")
    return PurePosixPath(rootfile.attrib["full-path"])


def document_ids(path: Path) -> set[str]:
    return {
        element.attrib["id"]
        for element in ET.parse(path).iter()
        if "id" in element.attrib
    }


def audit(root: Path) -> int:
    opf_relative = package_path(root)
    opf_directory = opf_relative.parent
    package = ET.parse(root / opf_relative)
    package_root = package.getroot()
    metadata = package_root.find(f"{{{OPF_NS}}}metadata")
    if metadata is None:
        raise ValueError("package document has no metadata element")
    manifest = {
        item.attrib["id"]: PurePosixPath(posixpath.normpath(str(opf_directory / item.attrib["href"])))
        for item in package.findall(f".//{{{OPF_NS}}}manifest/{{{OPF_NS}}}item")
    }
    spine = [
        item.attrib["idref"]
        for item in package.findall(f".//{{{OPF_NS}}}spine/{{{OPF_NS}}}itemref")
    ]
    missing_manifest_files = sorted(
        str(path) for path in manifest.values() if not (root / path).is_file()
    )
    missing_spine_items = [identifier for identifier in spine if identifier not in manifest]
    fallback_items = [
        item.attrib["id"]
        for item in package.findall(f".//{{{OPF_NS}}}manifest/{{{OPF_NS}}}item")
        if "fallback" in item.attrib
    ]
    spine_paths = [manifest[identifier] for identifier in spine if identifier in manifest]
    spine_positions = {path: index for index, path in enumerate(spine_paths)}

    ids_by_document: dict[PurePosixPath, set[str]] = {}
    references: Counter[tuple[PurePosixPath, str]] = Counter()
    missing_targets: list[str] = []
    missing_fragments: list[str] = []
    nav_positions: list[int] = []
    nav_labels: list[str] = []

    metadata_issues: list[str] = []
    for name, expected in EXPECTED_METADATA.items():
        values = [
            element.text or ""
            for element in metadata.findall(f"{{{DC_NS}}}{name}")
        ]
        if values != [expected]:
            metadata_issues.append(f"dc:{name} expected {expected!r}, found {values!r}")

    titles = {
        element.attrib.get("id"): element.text or ""
        for element in metadata.findall(f"{{{DC_NS}}}title")
    }
    refinements = {
        (element.attrib.get("refines"), element.attrib.get("property")): element.text or ""
        for element in metadata.findall(f"{{{OPF_NS}}}meta")
    }
    expected_titles = {
        "epub-title-1": ("Transformers: An Architecture for Geometric Computation", "main"),
        "epub-title-2": ("How AI, Mathematics, and Programming Converge into a Single Tool", "subtitle"),
        "epub-title-3": ("First Edition", "edition"),
    }
    if len(titles) != len(expected_titles):
        metadata_issues.append(f"expected {len(expected_titles)} dc:title elements, found {len(titles)}")
    for identifier, (text, title_type) in expected_titles.items():
        if titles.get(identifier) != text or refinements.get((f"#{identifier}", "title-type")) != title_type:
            metadata_issues.append(f"title metadata mismatch for {identifier}")

    property_elements: dict[str, list[ET.Element]] = {}
    for element in metadata.findall(f"{{{OPF_NS}}}meta"):
        property_elements.setdefault(element.attrib.get("property", ""), []).append(element)
    expected_properties = {
        "belongs-to-collection": "The Geometry of Meaning",
        "collection-type": "series",
        "group-position": "2",
        "dcterms:audience": "General adult",
    }
    for name, expected in expected_properties.items():
        elements = property_elements.get(name, [])
        if len(elements) != 1 or (elements[0].text or "") != expected:
            metadata_issues.append(f"meta property {name!r} is missing, duplicated, or not {expected!r}")
    for name in ("collection-type", "group-position"):
        elements = property_elements.get(name, [])
        if elements and elements[0].attrib.get("refines") != "#series-title":
            metadata_issues.append(f"meta property {name!r} does not refine #series-title")

    subjects = [element.text or "" for element in metadata.findall(f"{{{DC_NS}}}subject")]
    if subjects != EXPECTED_SUBJECTS:
        metadata_issues.append("dc:subject values or ordering do not match the canonical set")

    identifier_id = metadata.find(f"{{{DC_NS}}}identifier").attrib.get("id")
    if package_root.attrib.get("unique-identifier") != identifier_id:
        metadata_issues.append("package unique-identifier does not reference dc:identifier")
    modified = [
        element.text or ""
        for element in metadata.findall(f"{{{OPF_NS}}}meta")
        if element.attrib.get("property") == "dcterms:modified"
    ]
    if len(modified) != 1 or not modified[0].endswith("Z"):
        metadata_issues.append("dcterms:modified is missing, duplicated, or not UTC")
    dates = [element.text or "" for element in metadata.findall(f"{{{DC_NS}}}date")]
    if dates != ["2026-09-30"]:
        metadata_issues.append("dc:date does not match the canonical publication date")
    package_xml = ET.tostring(package_root, encoding="unicode").lower()
    calibre_markers = package_xml.count("calibre")

    xhtml_paths = [
        path for path in manifest.values() if path.suffix in {".xhtml", ".html"}
    ]
    for relative in xhtml_paths:
        ids_by_document[relative] = document_ids(root / relative)

    for source in xhtml_paths:
        tree = ET.parse(root / source)
        toc_links = {
            id(link)
            for element in tree.iter(f"{{{XHTML_NS}}}nav")
            if any(key.endswith("}type") and value == "toc" for key, value in element.attrib.items())
            for link in element.iter(f"{{{XHTML_NS}}}a")
        }
        for link in tree.iter(f"{{{XHTML_NS}}}a"):
            href = link.attrib.get("href", "")
            if not href or ":" in href.split("/", 1)[0]:
                continue
            target_name, _, fragment = href.partition("#")
            target = source if not target_name else PurePosixPath(
                posixpath.normpath(str(source.parent / target_name))
            )
            if not (root / target).is_file():
                missing_targets.append(f"{source}: {href}")
                continue
            if fragment:
                references[(target, fragment)] += 1
                if fragment not in ids_by_document.get(target, set()):
                    missing_fragments.append(f"{source}: {href}")
            if id(link) in toc_links and target in spine_positions:
                nav_positions.append(spine_positions[target])
                nav_labels.append("".join(link.itertext()).strip())

    orphaned_anchors = sorted(
        f"{document}#{identifier}"
        for document, identifiers in ids_by_document.items()
        for identifier in identifiers
        if references[(document, identifier)] == 0
    )
    nav_inversions = sum(
        current < previous
        for previous, current in zip(nav_positions, nav_positions[1:])
    )
    required_handoffs = ["From Book One", "Continue to Book Three"]
    handoff_positions = [
        nav_labels.index(label) if label in nav_labels else -1
        for label in required_handoffs
    ]
    handoff_issues = []
    if -1 in handoff_positions:
        handoff_issues.append("required trilogy handoff is missing from navigation")
    elif handoff_positions[0] >= nav_labels.index("Chapter 1 — Rules, Operations, and Programs"):
        handoff_issues.append("From Book One does not precede Chapter 1")
    elif handoff_positions[1] <= nav_labels.index("Book Two — Man Pages"):
        handoff_issues.append("Continue to Book Three does not follow the reference layer")

    print(f"Manifest items: {len(manifest)}")
    print(f"Spine items: {len(spine)}")
    print(f"Missing manifest files: {len(missing_manifest_files)}")
    print(f"Missing spine idrefs: {len(missing_spine_items)}")
    print(f"Manifest fallbacks: {len(fallback_items)}")
    print(f"Missing href targets: {len(missing_targets)}")
    print(f"Missing fragments: {len(missing_fragments)}")
    print(f"Navigation inversions: {nav_inversions}")
    print(f"Handoff issues: {len(handoff_issues)}")
    print(f"Metadata issues: {len(metadata_issues)}")
    for issue in metadata_issues:
        print(f"  {issue}")
    print(f"Calibre markers: {calibre_markers}")
    print(f"Unreferenced anchors (informational): {len(orphaned_anchors)}")
    print("Navigation sequence:")
    for label in nav_labels:
        print(f"  {label}")

    failures = (
        missing_manifest_files
        + missing_spine_items
        + fallback_items
        + missing_targets
        + missing_fragments
        + metadata_issues
        + handoff_issues
    )
    return 1 if failures or nav_inversions or calibre_markers else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit an EPUB package or extracted root")
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    if args.package.is_dir():
        return audit(args.package)
    with tempfile.TemporaryDirectory() as directory:
        with zipfile.ZipFile(args.package) as archive:
            archive.extractall(directory)
        return audit(Path(directory))


if __name__ == "__main__":
    raise SystemExit(main())