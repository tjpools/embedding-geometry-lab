#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_09_recurrent_runtime_probe import run_probe


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


def line(
    parent: ET.Element,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    width: int = 3,
    dash: str | None = None,
    arrow: bool = False,
) -> None:
    attributes: dict[str, object] = {
        "x1": start[0],
        "y1": start[1],
        "x2": end[0],
        "y2": end[1],
        "stroke": INK,
        "stroke_width": width,
    }
    if dash is not None:
        attributes["stroke_dasharray"] = dash
    if arrow:
        attributes["marker_end"] = "url(#arrow)"
    element(parent, "line", **attributes)


def rounded_box(
    parent: ET.Element,
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    *,
    dash: str | None = None,
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
    if dash is not None:
        attributes["stroke_dasharray"] = dash
    element(parent, "rect", **attributes)


def build_svg(output: Path) -> None:
    probe = run_probe()
    base = probe["base"]
    sensitivities = base["analytic_final_state_sensitivity_by_input"]
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
    title_node.text = "The Recurrent Bottleneck"
    description = element(root, "desc", id="description")
    description.text = (
        "Five ordered inputs update hidden states h one through h five. Each state "
        "requires its predecessor, and final-state sensitivity to the first input "
        "crosses all five updates. A zero-recurrence control breaks cross-position "
        "sensitivity. Counts describe dependencies, not measured runtime."
    )
    metadata = element(root, "metadata")
    metadata.text = (
        "Original visual by Terrence J McLaughlin; generated from the verified "
        "Chapter 9 probe; August 14, 2026."
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

    text(root, "THE RECURRENT BOTTLENECK", WIDTH / 2, 52, 35, weight=700)
    text(root, "ordered state availability | sensitivity across the path | structural counts", WIDTH / 2, 86, 19)

    positions = [85, 285, 485, 685, 885, 1085]
    state_y = 230
    text(root, "FORWARD STATE PATH", 36, 128, 17, anchor="start", weight=700)
    for index, (x_position, state) in enumerate(zip(positions, base["states"], strict=True)):
        fill = CONSTRAINT if index == 0 else COMPUTATION
        rounded_box(root, x_position - 58, state_y - 35, 116, 70, fill)
        text(root, f"h{index}", x_position, state_y - 5, 18, weight=700)
        text(root, f"{state:.3f}", x_position, state_y + 20, 14)
        if index > 0:
            previous_x = positions[index - 1]
            line(root, (previous_x + 62, state_y), (x_position - 68, state_y), width=4, arrow=True)
            input_value = probe["inputs"][index - 1]
            rounded_box(root, x_position - 45, 126, 90, 44, REPRESENTATION)
            text(root, f"x{index} = {input_value:.1f}", x_position, 154, 14, weight=700)
            line(root, (x_position, 174), (x_position, state_y - 42), width=3, arrow=True)

    text(root, "FINAL-STATE SENSITIVITY", 36, 330, 17, anchor="start", weight=700)
    line(root, (85, 374), (1085, 374), width=4, arrow=True)
    for index, sensitivity in enumerate(sensitivities, start=1):
        x_position = positions[index]
        element(root, "circle", cx=x_position, cy=374, r=10, fill=OPERATION, stroke=INK, stroke_width=3)
        text(root, f"dh5/dx{index}", x_position, 350, 13, weight=700)
        text(root, f"{sensitivity:.3f}", x_position, 409, 14, weight=700)
    text(root, "x1 influence reaches h5 only through every intervening recurrent derivative", 600, 438, 15, weight=700)

    rounded_box(root, 55, 472, 1090, 82, CONSTRAINT)
    text(root, "DECLARED STRUCTURAL COUNTS", 80, 500, 15, anchor="start", weight=700)
    count_labels = (
        "5 updates",
        "5 predecessor edges",
        "5 state reads",
        "5 state writes",
        "depth 5",
    )
    for index, label in enumerate(count_labels):
        text(root, label, 235 + index * 205, 530, 16, weight=700)

    rounded_box(root, 55, 592, 1090, 92, FIELD, dash="10 7")
    text(root, "ZERO-RECURRENCE CONTROL", 80, 620, 16, anchor="start", weight=700)
    text(root, "x1", 315, 652, 16, weight=700)
    line(root, (345, 647), (540, 647), width=3, dash="9 7")
    text(root, "BROKEN", 442, 638, 13, weight=700)
    text(root, "h5", 585, 652, 16, weight=700)
    text(root, "dh5/dx1..4 = 0", 760, 652, 16, weight=700)
    text(root, "dh5/dx5 = 0.961", 980, 652, 16, weight=700)

    text(root, "dependency and operation counts only; no timing, kernel, or memory-traffic measurement", WIDTH / 2, 724, 16, weight=700)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)