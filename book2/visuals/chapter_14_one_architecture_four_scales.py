#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_14_four_scales_probe import run_probe


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


def line(parent: ET.Element, x1: float, y1: float, x2: float, y2: float, *, dash: str | None = None) -> None:
    attributes: dict[str, object] = {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "stroke": INK,
        "stroke_width": 3,
    }
    if dash:
        attributes["stroke_dasharray"] = dash
    element(parent, "line", **attributes)


def panel_header(root: ET.Element, x: float, scale: str, object_id: str, architecture_id: str) -> None:
    text(root, scale.upper(), x + 132, 145, 17, weight=700)
    text(root, architecture_id, x + 132, 168, 11)
    text(root, object_id, x + 132, 190, 10)


def labeled_cell(root: ET.Element, x: float, y: float, width: float, label: str, fill: str) -> None:
    box(root, x, y, width, 43, fill)
    text(root, label, x + width / 2, y + 27, 11, weight=700)


def build_svg(output: Path) -> None:
    probe = run_probe()
    views = {view["scale"]: view for view in probe["views"]}
    blocks = probe["block_instances"]
    control = probe["attention_row_scope_substitution_control"]
    dimensions = probe["dimensions"]

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
    title_node.text = "One Architecture, Four Scales"
    description = element(root, "desc", id="description")
    description.text = (
        "Four aligned views preserve one architecture identifier while selecting system, repeated stack, block, "
        "and attention-operation detail. Dashed connectors mean containment and zoom, not runtime order. A lower "
        "control rejects one attention row as a whole system because its scope and required interfaces are incomplete."
    )
    metadata = element(root, "metadata")
    metadata.text = (
        "Original visual by Terrence J McLaughlin; generated from the verified Chapter 14 probe; August 14, 2026."
    )
    element(root, "rect", width=WIDTH, height=HEIGHT, fill=FIELD)

    text(root, "One Architecture, Four Scales", WIDTH / 2, 48, 34, weight=700)
    text(root, "one object identity; changing scope reveals interfaces owned at that scale", WIDTH / 2, 78, 17)

    panel_x = (25, 315, 605, 895)
    for x in panel_x:
        box(root, x, 112, 264, 426, FIELD, double=True)

    panel_header(root, panel_x[0], "system", views["system"]["selected_object_id"], probe["architecture_id"])
    labeled_cell(root, 47, 220, 220, "TOKEN IDS IN", REPRESENTATION)
    box(root, 65, 286, 184, 132, CONSTRAINT, double=True)
    text(root, "REPEATED STACK", 157, 316, 13, weight=700)
    text(root, f"{dimensions['blocks']} block instances", 157, 346, 12)
    text(root, f"d_model = {dimensions['model']}", 157, 372, 12)
    text(root, f"context = {dimensions['context']}", 157, 396, 12)
    labeled_cell(root, 47, 465, 220, "LOGITS OUT", REPRESENTATION)

    panel_header(root, panel_x[1], "stack", views["stack"]["selected_object_id"], probe["architecture_id"])
    text(root, "shared contract", 447, 220, 12, weight=700)
    text(root, blocks[0]["contract_id"], 447, 241, 11)
    for index, block in enumerate(blocks):
        y = 268 + index * 67
        box(root, 342, y, 210, 48, COMPUTATION if index != 1 else OPERATION)
        text(root, f"BLOCK {block['position']:02d}", 360, y + 22, 12, anchor="start", weight=700)
        text(root, block["instance_id"].split(".")[-1], 535, y + 22, 11, anchor="end")
    text(root, "distinct instance IDs", 447, 487, 12, weight=700)
    text(root, "same block contract", 447, 509, 12)

    panel_header(root, panel_x[2], "block", views["block"]["selected_object_id"], probe["architecture_id"])
    block_cells = (
        (220, "ATTENTION", OPERATION),
        (276, "RESIDUAL + NORM 01", CONSTRAINT),
        (332, "FEED-FORWARD", COMPUTATION),
        (388, "RESIDUAL + NORM 02", CONSTRAINT),
    )
    for y, label, fill in block_cells:
        labeled_cell(root, 632, y, 210, label, fill)
    text(root, "owned boundary interfaces", 737, 472, 12, weight=700)
    text(root, "hidden rows in / hidden rows out", 737, 497, 11)

    panel_header(root, panel_x[3], "operation", views["operation"]["selected_object_id"], probe["architecture_id"])
    operation_cells = (
        (218, "Q / K / V PROJECTIONS", REPRESENTATION),
        (270, "SCALED SCORES", OPERATION),
        (322, "SOFTMAX ROWS", CONSTRAINT),
        (374, "VALUE COMBINATION", OPERATION),
        (426, "OUTPUT PROJECTION", COMPUTATION),
    )
    for y, label, fill in operation_cells:
        labeled_cell(root, 922, y, 210, label, fill)
    text(root, f"{dimensions['heads']} heads x {dimensions['head']} = {dimensions['model']}", 1027, 502, 11, weight=700)

    for left, right in zip(panel_x, panel_x[1:]):
        line(root, left + 267, 104, right - 3, 104, dash="7 6")
        text(root, "contains / selected zoom", (left + right + 264) / 2, 99, 10)

    box(root, 25, 568, 1150, 130, FIELD, dash="9 7")
    text(root, "SCOPE-SUBSTITUTION CONTROL", 50, 598, 15, anchor="start", weight=700)
    box(root, 50, 615, 310, 54, OPERATION)
    text(root, "ONE ATTENTION ROW", 205, 638, 13, weight=700)
    text(root, control["candidate"]["record_id"], 205, 658, 10)
    line(root, 375, 642, 420, 642)
    text(root, "claims system", 397, 630, 9)
    box(root, 435, 615, 710, 54, CONSTRAINT, double=True)
    text(root, "REJECTED: INCOMPLETE SCOPE + MISSING INTERFACES", 790, 639, 13, weight=700)
    missing = " | ".join(control["result"]["missing_interfaces"])
    text(root, missing, 790, 659, 11)

    text(
        root,
        "dashed connectors describe containment and inspection zoom only; left-to-right placement is not runtime order",
        WIDTH / 2,
        735,
        13,
        weight=700,
    )

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)