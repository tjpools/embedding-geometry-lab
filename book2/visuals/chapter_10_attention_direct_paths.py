#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_10_attention_paths_probe import run_probe


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


def box(
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
    final_weights = probe["full_attention"]["weights"][-1]
    final_contributions = probe["full_attention"]["contributions"][-1]
    final_output = probe["full_attention"]["outputs"][-1]
    control_difference = probe["value_only_control"]["observed_output_differences"][-1]

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
    title_node.text = "Attention Opens Direct Paths"
    description = element(root, "desc", id="description")
    description.text = (
        "A recurrent lane carries position one through five state updates. An attention "
        "lane connects five value vectors directly to output five through normalized "
        "weights. Changing value one leaves the weights fixed but changes the output. "
        "A causal-mask inset marks future positions as excluded by rule."
    )
    metadata = element(root, "metadata")
    metadata.text = (
        "Original visual by Terrence J McLaughlin; generated from the verified "
        "Chapter 10 probe; August 14, 2026."
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

    text(root, "ATTENTION OPENS DIRECT PATHS", WIDTH / 2, 52, 34, weight=700)
    text(root, "graph structure changes; runtime and causal attribution remain unmeasured", WIDTH / 2, 86, 19)

    text(root, "RECURRENT PATH", 45, 128, 16, anchor="start", weight=700)
    recurrent_x = [155, 355, 555, 755, 955]
    for index, x_position in enumerate(recurrent_x, start=1):
        box(root, x_position - 52, 145, 104, 58, COMPUTATION)
        text(root, f"h{index}", x_position, 180, 18, weight=700)
        if index > 1:
            line(root, (recurrent_x[index - 2] + 60, 174), (x_position - 62, 174), width=4, arrow=True)
    text(root, "x1", 55, 180, 16, weight=700)
    line(root, (72, 174), (95, 174), width=4, arrow=True)
    text(root, "x1 to h5: 5 abstract edges", 600, 226, 15, weight=700)

    text(root, "FULL ATTENTION FOR QUERY 5", 45, 258, 16, anchor="start", weight=700)
    value_x = [110, 300, 490, 680, 870]
    output_x = 1080
    for index, (x_position, weight, contribution) in enumerate(
        zip(value_x, final_weights, final_contributions, strict=True), start=1
    ):
        box(root, x_position - 58, 278, 116, 72, REPRESENTATION)
        text(root, f"v{index}", x_position, 304, 17, weight=700)
        text(root, f"weight {weight:.3f}", x_position, 330, 13)
        line(root, (x_position + 62, 314), (output_x - 76, 365), width=3, arrow=True)
        text(root, f"({contribution[0]:.3f}, {contribution[1]:.3f})", x_position, 378, 13, weight=700)
    box(root, output_x - 70, 330, 140, 80, OPERATION)
    text(root, "o5", output_x, 357, 18, weight=700)
    text(root, f"({final_output[0]:.3f},", output_x, 382, 14, weight=700)
    text(root, f" {final_output[1]:.3f})", output_x, 400, 14, weight=700)
    text(root, "1 abstract contribution edge from v1 to o5", 600, 424, 15, weight=700)

    box(root, 55, 462, 1090, 95, CONSTRAINT)
    text(root, "VALUE-ONLY CONTROL", 80, 492, 16, anchor="start", weight=700)
    text(root, "v1 += (0.4, -0.2)", 270, 526, 16, weight=700)
    text(root, "scores unchanged", 520, 526, 16, weight=700)
    text(root, "weights unchanged", 750, 526, 16, weight=700)
    text(root, f"delta o5 = ({control_difference[0]:.3f}, {control_difference[1]:.3f})", 1010, 526, 16, weight=700)

    box(root, 55, 594, 1090, 90, FIELD, dash="10 7")
    text(root, "CAUSAL MASK", 80, 622, 16, anchor="start", weight=700)
    text(root, "query 2 admits positions 1, 2", 285, 654, 16, weight=700)
    text(root, "future 3-5: EXCLUDED", 620, 654, 16, weight=700)
    text(root, "zero by mask rule", 950, 654, 16, weight=700)

    text(root, "normalized weights scale values; displaying a weight row is not a causal explanation", WIDTH / 2, 724, 16, weight=700)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)