#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_07_tensor_parallel_probe import run_probe


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
    marker: bool = False,
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
    if marker:
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


def matrix_rows(matrix: list[list[float]]) -> list[str]:
    return ["[" + "  ".join(f"{value:g}" for value in row) + "]" for row in matrix]


def draw_input_tensor(
    root: ET.Element,
    label: str,
    tensor: list,
    tensor_shape: list[int],
    y: float,
) -> None:
    box(root, 45, y, 300, 150, REPRESENTATION)
    text(root, f"{label}  shape {tuple(tensor_shape)}", 65, y + 28, 16, anchor="start", weight=700)
    for batch, matrix in enumerate(tensor):
        batch_x = 65 + batch * 138
        text(root, f"batch {batch}", batch_x, y + 55, 13, anchor="start", weight=700)
        for row_index, row_text in enumerate(matrix_rows(matrix)):
            text(root, row_text, batch_x, y + 82 + row_index * 24, 14, anchor="start")


def draw_result_tensor(root: ET.Element, result: list, output_shape: list[int]) -> None:
    box(root, 855, 150, 300, 345, CONSTRAINT)
    text(root, f"C  shape {tuple(output_shape)}", 875, 182, 17, anchor="start", weight=700)
    for batch, matrix in enumerate(result):
        y = 225 + batch * 125
        text(root, f"batch {batch}", 895, y, 15, anchor="start", weight=700)
        for row_index, row_text in enumerate(matrix_rows(matrix)):
            text(root, row_text, 895, y + 35 + row_index * 32, 19, anchor="start")
    text(root, "equals serial reference", 1005, 465, 15, weight=700)


def build_svg(output: Path) -> None:
    probe = run_probe()
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
    title_node.text = "Tensor Work on Parallel Lanes"
    description = element(root, "desc", id="description")
    description.text = (
        "Two batched input tensors feed eight output coordinates assigned across four "
        "abstract lanes. The assembled output equals the serial reference. A dashed "
        "control omits coordinate one-one-one and leaves one output cell empty."
    )
    metadata = element(root, "metadata")
    metadata.text = "Original visual by Terrence J McLaughlin; generated from the verified Chapter 7 probe; August 13, 2026."

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

    text(root, "TENSOR WORK ON PARALLEL LANES", WIDTH / 2, 54, 34, weight=700)
    text(root, "shape, partition, complete assignment, one assembled result", WIDTH / 2, 88, 19)

    text(root, "BATCHED INPUTS", 195, 126, 20, weight=700)
    text(root, "DISJOINT OUTPUT WORK", 600, 126, 20, weight=700)
    text(root, "ASSEMBLED RESULT", 1005, 126, 20, weight=700)

    draw_input_tensor(root, "A", probe["left"], probe["left_shape"], 150)
    draw_input_tensor(root, "B", probe["right"], probe["right_shape"], 345)

    lane_y_values = (150, 238, 326, 414)
    for lane_index, (assignments, lane_y) in enumerate(
        zip(probe["lane_assignments"], lane_y_values, strict=True)
    ):
        box(root, 405, lane_y, 390, 62, COMPUTATION if lane_index % 2 == 0 else OPERATION)
        text(root, f"LANE {lane_index}", 425, lane_y + 25, 15, anchor="start", weight=700)
        assignment_labels = []
        for batch, row, column in assignments:
            value = probe["partitioned_result"][batch][row][column]
            assignment_labels.append(f"({batch},{row},{column}) -> {value:g}")
        text(root, "    ".join(assignment_labels), 500, lane_y + 39, 14, anchor="start")

    line(root, (355, 323), (393, 323), marker=True)
    line(root, (807, 323), (843, 323), marker=True)
    text(root, "3 product terms per output cell", 600, 505, 15, weight=700)
    draw_result_tensor(root, probe["partitioned_result"], probe["output_shape"])

    box(root, 120, 565, 960, 125, FIELD, dash="10 7")
    text(root, "OMITTED-WORK CONTROL", 145, 596, 17, anchor="start", weight=700)
    omitted = tuple(probe["control"]["omitted_coordinate"])
    text(root, f"remove {omitted} from LANE 3", 145, 630, 16, anchor="start")
    line(root, (430, 625), (535, 625), dash="8 6", marker=True)
    text(root, "batch 1  [[3  4]  [-2  EMPTY]]", 565, 632, 18, anchor="start", weight=700)
    text(root, "not equal to reference", 805, 664, 15, anchor="start")

    text(root, "abstract work lanes; no GPU execution or timing measured", 600, 732, 16, weight=700)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)