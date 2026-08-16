#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_04_map_and_local_change_probe import add, matvec, nonlinear_map, run_probe, scale


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


def screen(point: tuple[float, float], origin: tuple[float, float], scale_factor: float) -> tuple[float, float]:
    return (origin[0] + scale_factor * point[0], origin[1] - scale_factor * point[1])


def line_between(
    parent: ET.Element,
    first: tuple[float, float],
    second: tuple[float, float],
    *,
    stroke: str = INK,
    width: int = 2,
    dash: str | None = None,
    opacity: float = 1.0,
) -> None:
    attributes: dict[str, object] = {
        "x1": first[0],
        "y1": first[1],
        "x2": second[0],
        "y2": second[1],
        "stroke": stroke,
        "stroke_width": width,
        "opacity": opacity,
    }
    if dash is not None:
        attributes["stroke_dasharray"] = dash
    element(parent, "line", **attributes)


def build_svg(output: Path) -> None:
    probe = run_probe()
    matrix = probe["linear_map"]
    local = probe["local_change_case"]
    point = tuple(local["point"])
    direction = tuple(local["direction"])
    jacobian = local["jacobian"]

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
    title_node.text = "A Map and Its Local Change"
    description = element(root, "desc", id="description")
    description.text = (
        "The left side shows a square coordinate grid transformed globally by matrix A. "
        "The right side compares the nonlinear map near p with the local directional "
        "change predicted by the Jacobian at p; the two short arrows nearly coincide."
    )
    metadata = element(root, "metadata")
    metadata.text = "Original visual by Terrence J McLaughlin; generated from the verified Chapter 4 probe; August 13, 2026."
    element(root, "rect", width=WIDTH, height=HEIGHT, fill=FIELD)

    text(root, "A MAP AND ITS LOCAL CHANGE", WIDTH / 2, 58, 36, weight=700)
    text(root, "global linear transformation | local first-order approximation", WIDTH / 2, 94, 20)

    left_origin = (300.0, 385.0)
    left_scale = 92.0
    text(root, "MATRIX MAP", 300, 142, 22, weight=700)
    text(root, "A = [[1, 0.5], [-0.25, 1]]", 300, 174, 17)

    for coordinate in range(-2, 3):
        horizontal_start = matvec(matrix, (-2.0, float(coordinate)))
        horizontal_end = matvec(matrix, (2.0, float(coordinate)))
        vertical_start = matvec(matrix, (float(coordinate), -2.0))
        vertical_end = matvec(matrix, (float(coordinate), 2.0))
        line_between(
            root,
            screen(horizontal_start, left_origin, left_scale),
            screen(horizontal_end, left_origin, left_scale),
            stroke=REPRESENTATION if coordinate else INK,
            width=3 if coordinate == 0 else 2,
        )
        line_between(
            root,
            screen(vertical_start, left_origin, left_scale),
            screen(vertical_end, left_origin, left_scale),
            stroke=OPERATION if coordinate else INK,
            width=3 if coordinate == 0 else 2,
        )

    text(root, "one matrix acts across the field", 300, 650, 18, weight=700)

    line_between(root, (600, 130), (600, 650), width=2, dash="8 8", opacity=0.45)

    right_origin = (855.0, 410.0)
    right_scale = 310.0
    text(root, "JACOBIAN AT ONE POINT", 865, 142, 22, weight=700)
    text(root, "p = (0.6, -0.8),  d = (0.3, -0.2)", 865, 174, 17)

    mapped_point = nonlinear_map(point)
    step = 0.35
    actual_endpoint = nonlinear_map(add(point, scale(step, direction)))
    predicted_endpoint = add(mapped_point, scale(step, matvec(jacobian, direction)))
    center = screen((0.0, 0.0), right_origin, right_scale)
    actual_delta = add(actual_endpoint, scale(-1.0, mapped_point))
    predicted_delta = add(predicted_endpoint, scale(-1.0, mapped_point))
    actual_screen = screen(actual_delta, right_origin, right_scale)
    predicted_screen = screen(predicted_delta, right_origin, right_scale)

    element(root, "circle", cx=center[0], cy=center[1], r=86, fill=CONSTRAINT, opacity=0.42)
    line_between(root, (center[0] - 125, center[1]), (center[0] + 125, center[1]), opacity=0.35)
    line_between(root, (center[0], center[1] - 125), (center[0], center[1] + 125), opacity=0.35)
    element(root, "circle", cx=center[0], cy=center[1], r=10, fill=INK)
    text(root, "f(p)", center[0] - 16, center[1] + 28, 16, anchor="end", weight=700)

    line_between(root, center, actual_screen, stroke=COMPUTATION, width=9)
    line_between(root, center, predicted_screen, stroke=INK, width=4, dash="10 7")
    element(root, "circle", cx=actual_screen[0], cy=actual_screen[1], r=9, fill=COMPUTATION, stroke=INK, stroke_width=2)
    element(root, "circle", cx=predicted_screen[0], cy=predicted_screen[1], r=6, fill=FIELD, stroke=INK, stroke_width=2)
    text(root, "actual local change", 735, 555, 16, anchor="start")
    line_between(root, (705, 550), (725, 550), stroke=COMPUTATION, width=8)
    text(root, "Jacobian prediction", 735, 586, 16, anchor="start")
    line_between(root, (705, 581), (725, 581), width=4, dash="8 5")
    text(root, "local agreement is not global identity", 865, 650, 18, weight=700)

    element(root, "rect", x=260, y=687, width=680, height=42, rx=6, fill=CONSTRAINT, stroke=INK, stroke_width=2)
    text(root, "MATRIX: GLOBAL LINEAR MAP        JACOBIAN: LOCAL LINEAR APPROXIMATION", 600, 714, 17, weight=700)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)