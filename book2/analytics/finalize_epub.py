#!/usr/bin/env python3
import argparse
import os
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

CONTAINER_NS = "urn:oasis:names:tc:opendocument:xmlns:container"
OPF_NS = "http://www.idpf.org/2007/opf"
DC_NS = "http://purl.org/dc/elements/1.1/"


def package_path(container: bytes) -> PurePosixPath:
    root = ET.fromstring(container)
    rootfile = root.find(f".//{{{CONTAINER_NS}}}rootfile")
    if rootfile is None:
        raise ValueError("container.xml has no rootfile")
    return PurePosixPath(rootfile.attrib["full-path"])


def finalize(package: bytes) -> bytes:
    ET.register_namespace("", OPF_NS)
    ET.register_namespace("dc", DC_NS)
    root = ET.fromstring(package)
    metadata = root.find(f"{{{OPF_NS}}}metadata")
    if metadata is None:
        raise ValueError("package document has no metadata element")

    managed_properties = {
        "belongs-to-collection",
        "collection-type",
        "group-position",
        "dcterms:audience",
    }
    for element in list(metadata):
        if element.tag == f"{{{OPF_NS}}}meta" and element.attrib.get("property") in managed_properties:
            metadata.remove(element)

    collection = ET.SubElement(
        metadata,
        f"{{{OPF_NS}}}meta",
        {"id": "series-title", "property": "belongs-to-collection"},
    )
    collection.text = "The Geometry of Meaning"
    collection_type = ET.SubElement(
        metadata,
        f"{{{OPF_NS}}}meta",
        {"refines": "#series-title", "property": "collection-type"},
    )
    collection_type.text = "series"
    position = ET.SubElement(
        metadata,
        f"{{{OPF_NS}}}meta",
        {"refines": "#series-title", "property": "group-position"},
    )
    position.text = "2"
    audience = ET.SubElement(
        metadata,
        f"{{{OPF_NS}}}meta",
        {"property": "dcterms:audience"},
    )
    audience.text = "General adult"
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def finalize_epub(path: Path) -> None:
    with zipfile.ZipFile(path) as source:
        entries = [(item, source.read(item.filename)) for item in source.infolist()]
    if not entries or entries[0][0].filename != "mimetype":
        raise ValueError("mimetype is not the first EPUB entry")

    opf_path = package_path(dict((item.filename, data) for item, data in entries)["META-INF/container.xml"])
    replacement = finalize(dict((item.filename, data) for item, data in entries)[str(opf_path)])

    descriptor, temporary_name = tempfile.mkstemp(dir=path.parent, suffix=".epub")
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(temporary, "w") as target:
            for item, data in entries:
                if item.filename == str(opf_path):
                    data = replacement
                target.writestr(item, data)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize Book Two EPUB metadata")
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    finalize_epub(args.package)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())