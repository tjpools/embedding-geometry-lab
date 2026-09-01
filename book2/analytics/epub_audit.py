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
XHTML_NS = "http://www.w3.org/1999/xhtml"


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
    spine_paths = [manifest[identifier] for identifier in spine if identifier in manifest]
    spine_positions = {path: index for index, path in enumerate(spine_paths)}

    ids_by_document: dict[PurePosixPath, set[str]] = {}
    references: Counter[tuple[PurePosixPath, str]] = Counter()
    missing_targets: list[str] = []
    missing_fragments: list[str] = []
    nav_positions: list[int] = []
    nav_labels: list[str] = []

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

    print(f"Manifest items: {len(manifest)}")
    print(f"Spine items: {len(spine)}")
    print(f"Missing manifest files: {len(missing_manifest_files)}")
    print(f"Missing spine idrefs: {len(missing_spine_items)}")
    print(f"Missing href targets: {len(missing_targets)}")
    print(f"Missing fragments: {len(missing_fragments)}")
    print(f"Navigation inversions: {nav_inversions}")
    print(f"Unreferenced anchors (informational): {len(orphaned_anchors)}")
    print("Navigation sequence:")
    for label in nav_labels:
        print(f"  {label}")

    failures = (
        missing_manifest_files
        + missing_spine_items
        + missing_targets
        + missing_fragments
    )
    return 1 if failures or nav_inversions else 0


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