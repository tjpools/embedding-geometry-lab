#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_05_intent_through_compiler_probe import run_probe


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


def arrow(parent: ET.Element, start: tuple[float, float], end: tuple[float, float], *, dashed: bool = False) -> None:
    attributes: dict[str, object] = {
        "x1": start[0],
        "y1": start[1],
        "x2": end[0],
        "y2": end[1],
        "stroke": INK,
        "stroke_width": 4,
        "marker_end": "url(#arrow)",
    }
    if dashed:
        attributes["stroke_dasharray"] = "10 8"
    element(parent, "line", **attributes)


def box(
    parent: ET.Element,
    center_x: float,
    top: float,
    width: float,
    height: float,
    fill: str,
    heading: str,
    lines: tuple[str, ...],
) -> None:
    element(
        parent,
        "rect",
        x=center_x - width / 2,
        y=top,
        width=width,
        height=height,
        rx=6,
        fill=fill,
        stroke=INK,
        stroke_width=3,
    )
    text(parent, heading, center_x, top + 31, 18, weight=700)
    for index, line in enumerate(lines):
        text(parent, line, center_x, top + 61 + index * 24, 15)


def build_svg(output: Path) -> None:
    probe = run_probe()
    layout = probe["declared_layout"]

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
    title_node.text = "Intent Through the Compiler"
    description = element(root, "desc", id="description")
    description.text = (
        "An accepted Rust TokenRecord crosses source declaration, type checking, declared "
        "layout, MIR translation, and executable output. A temporary active integer value "
        "branches downward at type checking and is rejected before later artifacts exist."
    )
    metadata = element(root, "metadata")
    metadata.text = "Original visual by Terrence J McLaughlin; generated from the verified Chapter 5 probe; August 13, 2026."

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

    text(root, "INTENT THROUGH THE COMPILER", WIDTH / 2, 58, 36, weight=700)
    text(root, "distinct interfaces constrain, lay out, translate, and execute", WIDTH / 2, 94, 20)

    centers = (125, 365, 605, 845, 1085)
    top = 205
    node_width = 190
    node_height = 180

    box(root, centers[0], top, node_width, node_height, REPRESENTATION, "SOURCE", ("TokenRecord", "u32 | f32 | bool", "active: true"))
    box(root, centers[1], top, node_width, node_height, CONSTRAINT, "TYPE CHECK", ("field types agree", "accepted source", "3 tests pass"))
    box(
        root,
        centers[2],
        top,
        node_width,
        node_height,
        OPERATION,
        "LAYOUT",
        (
            f"size {layout['size']} | align {layout['alignment']}",
            "offsets 0 | 4 | 8",
            "trailing padding",
        ),
    )
    box(root, centers[3], top, node_width, node_height, COMPUTATION, "MIR", ("typed function", "typed record", "intermediate form"))
    box(root, centers[4], top, node_width, node_height, REPRESENTATION, "OUTPUT", ("size=12", "offsets=0,4,8", "result=1.5"))

    for left, right in zip(centers, centers[1:]):
        arrow(root, (left + node_width / 2 + 8, top + 90), (right - node_width / 2 - 12, top + 90))

    arrow(root, (centers[1], top + node_height + 8), (centers[1], 514), dashed=True)
    box(root, centers[1], 525, 240, 112, FIELD, "REJECTED", ("active: 1", "mismatched types"))
    text(root, "no layout, MIR, or executable", 365, 675, 17, weight=700)

    element(root, "rect", x=190, y=700, width=820, height=42, rx=6, fill=CONSTRAINT, stroke=INK, stroke_width=2)
    text(root, "TYPE ACCEPTANCE IS NOT PROOF OF PURPOSE OR TASK CORRECTNESS", 600, 727, 17, weight=700)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)