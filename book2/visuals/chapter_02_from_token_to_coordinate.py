#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_02_representation_probe import run_probe


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
    fill: str = INK,
) -> ET.Element:
    node = element(
        parent,
        "text",
        x=x,
        y=y,
        fill=fill,
        font_family=FONT,
        font_size=size,
        font_weight=weight,
        text_anchor=anchor,
        letter_spacing=0,
    )
    node.text = value
    return node


def box(
    parent: ET.Element,
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    label: str,
    value: str,
    value_size: int = 20,
) -> None:
    element(parent, "rect", x=x, y=y, width=width, height=height, rx=6, fill=fill, stroke=INK, stroke_width=3)
    text(parent, label, x + width / 2, y + 25, 14, weight=700)
    text(parent, value, x + width / 2, y + 58, value_size, weight=700)


def arrow(parent: ET.Element, x1: float, y1: float, x2: float, y2: float) -> None:
    element(parent, "line", x1=x1, y1=y1, x2=x2 - 10, y2=y2, stroke=INK, stroke_width=3)
    element(parent, "polygon", points=f"{x2 - 10},{y2 - 7} {x2},{y2} {x2 - 10},{y2 + 7}", fill=INK)


def vector(values: object) -> str:
    return "(" + ", ".join(f"{value:g}" for value in values) + ")"


def coordinate(values: object) -> str:
    return "[" + ", ".join(str(value) for value in values) + "]"


def build_svg(output: Path) -> None:
    probe = run_probe()
    permutation = probe["permutation"]
    loss = probe["information_loss"]
    token = probe["tokens"][0]

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
    title_node.text = "From Token to Coordinate"
    description = element(root, "desc", id="description")
    description.text = (
        "Source text OPEN is normalized to open and split into the token open. In the base vocabulary, "
        "open has identifier 3, one-hot coordinate 0 0 0 1, and selects vector 0.2 0.9 0.5. "
        "After a consistent vocabulary and table permutation, open has identifier 1 and coordinate "
        "0 1 0 0 but selects the same vector. Under the declared unknown policy, ajar and obstructed "
        "both map to identifier 0 and zero vector."
    )
    metadata = element(root, "metadata")
    metadata.text = (
        "Original visual by Terrence J McLaughlin; generated from "
        "chapter_02_representation_probe.py; August 12, 2026."
    )

    element(root, "rect", width=WIDTH, height=HEIGHT, fill=FIELD)
    text(root, "FROM TOKEN TO COORDINATE", WIDTH / 2, 52, 36, weight=700)
    text(root, "each boundary applies a declared representation rule", WIDTH / 2, 88, 20)

    top_y = 120
    visible_source = f"SPACE | {probe['input'].strip()} | SPACE"
    box(root, 55, top_y, 190, 82, REPRESENTATION, "SOURCE TEXT", visible_source, value_size=14)
    box(root, 315, top_y, 230, 82, CONSTRAINT, "NORMALIZE", "NFC + casefold + trim")
    box(root, 615, top_y, 170, 82, REPRESENTATION, "NORMALIZED", repr(probe["normalized"]))
    box(root, 855, top_y, 290, 82, CONSTRAINT, "SPLIT ON WHITESPACE", f"token: {token}")
    arrow(root, 245, 161, 305, 161)
    arrow(root, 545, 161, 605, 161)
    arrow(root, 785, 161, 845, 161)

    text(root, "TOKEN", 245, 278, 15, weight=700)
    text(root, "VOCABULARY ENTRY", 445, 278, 15, weight=700)
    text(root, "IDENTIFIER", 625, 278, 15, weight=700)
    text(root, "ONE-HOT COORDINATE", 825, 278, 15, weight=700)
    text(root, "SELECTED VECTOR", 1060, 278, 15, weight=700)

    lane_specs = (
        (
            "BASE ASSIGNMENT",
            320,
            permutation["base_id"],
            permutation["base_one_hot"],
            permutation["base_vector"],
        ),
        (
            "CONSISTENT PERMUTATION",
            455,
            permutation["permuted_id"],
            permutation["permuted_one_hot"],
            permutation["permuted_vector"],
        ),
    )
    for lane_label, y, identifier, one_hot, selected_vector in lane_specs:
        if lane_label == "CONSISTENT PERMUTATION":
            text(root, "CONSISTENT", 35, y + 38, 14, anchor="start", weight=700)
            text(root, "PERMUTATION", 35, y + 58, 14, anchor="start", weight=700)
        else:
            text(root, lane_label, 35, y + 49, 14, anchor="start", weight=700)
        box(root, 185, y, 120, 82, REPRESENTATION, "TOKEN", token)
        box(root, 350, y, 190, 82, REPRESENTATION, "ASSIGNMENT", f"{token} → {identifier}")
        box(root, 585, y, 90, 82, COMPUTATION, "ID", str(identifier))
        box(root, 720, y, 220, 82, COMPUTATION, "DIMENSION 4", coordinate(one_hot))
        box(root, 985, y, 175, 82, OPERATION, "LOOKUP ROW", vector(selected_vector))
        arrow(root, 305, y + 41, 340, y + 41)
        arrow(root, 540, y + 41, 575, y + 41)
        arrow(root, 675, y + 41, 710, y + 41)
        arrow(root, 940, y + 41, 975, y + 41)

    text(root, "changes", 630, 430, 14, weight=700)
    element(root, "line", x1=630, y1=408, x2=630, y2=447, stroke=INK, stroke_width=2, stroke_dasharray="6 5")
    text(root, "changes position", 830, 430, 14, weight=700)
    element(root, "line", x1=830, y1=408, x2=830, y2=447, stroke=INK, stroke_width=2, stroke_dasharray="6 5")
    text(root, "same row value", 1072, 430, 14, weight=700)
    element(root, "line", x1=1072, y1=408, x2=1072, y2=447, stroke=INK, stroke_width=2, stroke_dasharray="6 5")

    element(root, "rect", x=85, y=575, width=1030, height=64, rx=6, fill=COMPUTATION, stroke=INK, stroke_width=3)
    text(root, "RENUMBERING CHANGES THE INDEX AND COORDINATE; ALIGNED LOOKUP PRESERVES THE SELECTED VECTOR", 600, 614, 17, weight=700)

    unknown_inputs = " + ".join(loss["distinct_inputs"])
    unknown_vector = vector(loss["shared_vector"])
    element(root, "rect", x=85, y=665, width=1030, height=54, rx=6, fill=CONSTRAINT, stroke=INK, stroke_width=3, stroke_dasharray="8 6")
    text(
        root,
        f"DECLARED UNKNOWN POLICY: {unknown_inputs} → ID {loss['shared_identifier']} → {unknown_vector}  |  distinction discarded",
        600,
        699,
        17,
        weight=700,
    )

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)