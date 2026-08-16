#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_13_lineage_alignment_probe import run_probe


WIDTH = 1200
HEIGHT = 760
FIELD = "#f7f7f3"
INK = "#141719"
REPRESENTATION = "#efd5d5"
OPERATION = "#efdcae"
CONSTRAINT = "#efefb7"
COMPUTATION = "#b9ddea"
FONT = "DejaVu Sans, sans-serif"
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def element(parent: ET.Element, tag: str, **attributes: object) -> ET.Element:
    return ET.SubElement(
        parent,
        f"{{{SVG}}}{tag}",
        {key.replace("_", "-"): str(value) for key, value in attributes.items()},
    )


def text(
    parent: ET.Element,
    value: str,
    x: float,
    y: float,
    size: int,
    *,
    anchor: str = "middle",
    weight: int = 400,
) -> None:
    node = element(
        parent,
        "text",
        x=x,
        y=y,
        fill=INK,
        font_family=FONT,
        font_size=size,
        font_weight=weight,
        text_anchor=anchor,
        letter_spacing=0,
    )
    node.text = value


def box(
    parent: ET.Element,
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    *,
    dash: str | None = None,
    double: bool = False,
) -> None:
    attributes: dict[str, object] = {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "rx": 6,
        "fill": fill,
        "stroke": INK,
        "stroke_width": 3,
    }
    if dash:
        attributes["stroke_dasharray"] = dash
    element(parent, "rect", **attributes)
    if double:
        element(
            parent,
            "rect",
            x=x + 6,
            y=y + 6,
            width=width - 12,
            height=height - 12,
            rx=3,
            fill="none",
            stroke=INK,
            stroke_width=2,
        )


def path(parent: ET.Element, points: str, *, dash: str | None = None) -> None:
    attributes: dict[str, object] = {
        "d": points,
        "fill": "none",
        "stroke": INK,
        "stroke_width": 3,
        "marker_end": "url(#arrow)",
    }
    if dash:
        attributes["stroke_dasharray"] = dash
    element(parent, "path", **attributes)


def module(parent: ET.Element, x: float, y: float, title: str, subtitle: str, fill: str) -> None:
    box(parent, x, y, 220, 72, fill)
    text(parent, title, x + 110, y + 30, 15, weight=700)
    text(parent, subtitle, x + 110, y + 54, 12)


def export(parent: ET.Element, x: float, y: float, title: str, interface: str, fill: str) -> None:
    box(parent, x, y, 278, 72, fill)
    text(parent, title, x + 139, y + 29, 13, weight=700)
    text(parent, interface, x + 139, y + 53, 12)


def build_svg(output: Path) -> None:
    probe = run_probe()
    matches = probe["valid_alignment"]["accepted_matches"]
    missing = probe["missing_programming_edge_control"]["unsatisfied_requirements"][0]
    false_control = probe["vocabulary_only_false_equivalence_control"]

    root = ET.Element(
        f"{{{SVG}}}svg",
        {
            "width": str(WIDTH),
            "height": str(HEIGHT),
            "viewBox": f"0 0 {WIDTH} {HEIGHT}",
            "role": "img",
            "aria-labelledby": "title description",
        },
    )
    title_node = element(root, "title", id="title")
    title_node.text = "The Three-Lineage Interface"
    description = element(root, "desc", id="description")
    description.text = (
        "Three separate lanes carry AI architecture, mathematical geometry rules, and programming contracts through "
        "typed gates into one alignment record that preserves all three source identities. An outgoing arrow leads only "
        "to Chapter 14. Two lower controls reject a missing programming edge and vocabulary-only transform equivalence."
    )
    metadata = element(root, "metadata")
    metadata.text = (
        "Original visual by Terrence J McLaughlin; generated from the verified Chapter 13 probe; August 14, 2026."
    )

    definitions = element(root, "defs")
    marker = element(
        definitions,
        "marker",
        id="arrow",
        markerWidth=10,
        markerHeight=10,
        refX=8,
        refY=3,
        orient="auto",
        markerUnits="strokeWidth",
    )
    element(marker, "path", d="M0,0 L0,6 L9,3 z", fill=INK)
    element(root, "rect", width=WIDTH, height=HEIGHT, fill=FIELD)

    text(root, "The Three-Lineage Interface", WIDTH / 2, 50, 34, weight=700)
    text(root, "typed handoffs align distinct capabilities without collapsing their identities", WIDTH / 2, 82, 18)

    lanes = (
        (120, "AI.TRANSFORMER", "AI lineage", "ORDERED ARCHITECTURE", "alignment.architecture.v1", OPERATION),
        (230, "MATH.GEOMETRY", "mathematics lineage", "TRANSFORM + COMPARE", "alignment.geometry.v1", REPRESENTATION),
        (340, "PROGRAMMING.TOOLS", "programming lineage", "CALLABLE CONTRACTS", "alignment.implementation.v1", COMPUTATION),
    )
    for index, (y, source, lineage, capability, interface, fill) in enumerate(lanes):
        module(root, 35, y, source, lineage, fill)
        path(root, f"M 258 {y + 36} L 287 {y + 36}")
        export(root, 295, y, capability, interface, fill)
        path(root, f"M 576 {y + 36} L 607 {y + 36}")
        box(root, 615, y + 5, 145, 62, CONSTRAINT, double=True)
        text(root, f"TYPED GATE {index + 1}", 687, y + 32, 12, weight=700)
        text(root, "exact triple", 687, y + 52, 11)
        path(root, f"M 763 {y + 36} L 792 {y + 36}")

    box(root, 800, 112, 255, 310, CONSTRAINT, double=True)
    text(root, "CONVERGENCE.ALIGNMENT", 927, 145, 15, weight=700)
    text(root, "accepted: 3 / required: 3", 927, 170, 13)
    for index, match in enumerate(matches):
        y = 190 + index * 70
        box(root, 820, y, 215, 54, FIELD)
        text(root, match["lineage_id"].upper(), 837, y + 23, 12, anchor="start", weight=700)
        text(root, match["source_module"], 837, y + 42, 11, anchor="start")
    text(root, "identities preserved", 927, 399, 13, weight=700)

    path(root, "M 1058 267 L 1082 267")
    box(root, 1090, 205, 90, 124, OPERATION)
    text(root, "CHAPTER 14", 1135, 235, 12, weight=700)
    text(root, "CONVERGENCE.", 1135, 267, 10, weight=700)
    text(root, "ARCHITECTURE", 1135, 285, 10, weight=700)
    text(root, "inspect next", 1135, 311, 11)

    box(root, 35, 490, 535, 166, FIELD, dash="9 7")
    text(root, "CONTROL A — MISSING PROGRAMMING EDGE", 60, 522, 15, anchor="start", weight=700)
    text(root, "AI gate: accepted    |    mathematics gate: accepted", 60, 553, 13, anchor="start")
    text(root, "programming.tools edge removed", 60, 582, 13, anchor="start")
    box(root, 60, 600, 485, 38, CONSTRAINT)
    text(root, f"UNSATISFIED: {missing}", 302, 625, 13, weight=700)

    box(root, 605, 490, 560, 166, FIELD, dash="9 7")
    text(root, "CONTROL B — VOCABULARY IS NOT A TYPE", 630, 522, 15, anchor="start", weight=700)
    text(root, "shared term: transform", 630, 553, 13, anchor="start")
    text(root, "math.geometry attempts architecture requirement", 630, 582, 13, anchor="start")
    box(root, 630, 600, 510, 38, CONSTRAINT)
    failed = ", ".join(field.replace("_exact", "") for field in false_control["validation"]["failed_fields"])
    text(root, f"REJECTED: {failed} mismatch", 885, 625, 12, weight=700)

    text(
        root,
        "three exact interfaces meet here; scale, inference, limits, and philosophy remain outside this chapter",
        WIDTH / 2,
        714,
        14,
        weight=700,
    )

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)