#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_06_learning_loop_probe import run_probe


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
    width: int = 2,
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


def build_svg(output: Path) -> None:
    probe = run_probe()
    trace = probe["base_case"]["trace"]
    control = probe["control_case"]

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
    title_node.text = "The Learning Loop"
    description = element(root, "desc", id="description")
    description.text = (
        "A loss plot shows learning rate 0.2 decreasing loss over twelve updates while "
        "learning rate 1.2 leaves the plotted region toward final loss 197.53. A parameter "
        "plot shows weight and bias moving from zero toward two and one. Predict, loss, "
        "gradient, and update boxes form a repeated loop."
    )
    metadata = element(root, "metadata")
    metadata.text = "Original visual by Terrence J McLaughlin; generated from the verified Chapter 6 probe; August 13, 2026."

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

    text(root, "THE LEARNING LOOP", WIDTH / 2, 56, 36, weight=700)
    text(root, "objective, gradient, update size, repeated measurement", WIDTH / 2, 92, 20)

    plot_left, plot_right = 92.0, 655.0
    plot_top, plot_bottom = 166.0, 474.0
    text(root, "TRAINING LOSS", (plot_left + plot_right) / 2, 137, 21, weight=700)
    line(root, (plot_left, plot_top), (plot_left, plot_bottom), width=3)
    line(root, (plot_left, plot_bottom), (plot_right, plot_bottom), width=3)

    for loss_tick in (0.0, 1.5, 3.0, 4.5):
        y = plot_bottom - (loss_tick / 4.5) * (plot_bottom - plot_top)
        line(root, (plot_left - 7, y), (plot_right, y), width=1)
        text(root, f"{loss_tick:g}", plot_left - 14, y + 5, 14, anchor="end")
    for step in (0, 3, 6, 9, 12):
        x = plot_left + (step / 12) * (plot_right - plot_left)
        line(root, (x, plot_bottom), (x, plot_bottom + 7), width=2)
        text(root, str(step), x, plot_bottom + 25, 14)
    text(root, "UPDATE STEP", (plot_left + plot_right) / 2, 520, 15, weight=700)

    base_points = []
    for entry in trace:
        x = plot_left + (entry["step"] / 12) * (plot_right - plot_left)
        y = plot_bottom - (entry["loss"] / 4.5) * (plot_bottom - plot_top)
        base_points.append(f"{x},{y}")
        element(root, "circle", cx=x, cy=y, r=5, fill=COMPUTATION, stroke=INK, stroke_width=2)
    element(root, "polyline", points=" ".join(base_points), fill="none", stroke=INK, stroke_width=4)
    text(root, "η = 0.2: 4.5 → decreasing", 112, 188, 16, anchor="start", weight=700)

    control_start = (plot_left, plot_bottom - (control["initial_loss"] / 4.5) * (plot_bottom - plot_top))
    control_end = (plot_left + 48, plot_top - 18)
    line(root, control_start, control_end, width=4, dash="10 7", marker=True)
    text(root, "η = 1.2 leaves plot", 390, 188, 16, anchor="start", weight=700)
    text(root, "final loss 197.53", 390, 212, 15, anchor="start")

    plane_left, plane_right = 760.0, 1110.0
    plane_top, plane_bottom = 166.0, 474.0
    text(root, "PARAMETER PATH", (plane_left + plane_right) / 2, 137, 21, weight=700)
    line(root, (plane_left, plane_top), (plane_left, plane_bottom), width=3)
    line(root, (plane_left, plane_bottom), (plane_right, plane_bottom), width=3)
    text(root, "bias", plane_left - 18, plane_top + 5, 14, anchor="end")
    text(root, "weight", plane_right, plane_bottom + 25, 14, anchor="end")

    parameter_points = []
    for entry in trace:
        x = plane_left + (entry["weight"] / 2.2) * (plane_right - plane_left)
        y = plane_bottom - (entry["bias"] / 1.2) * (plane_bottom - plane_top)
        parameter_points.append(f"{x},{y}")
        element(root, "circle", cx=x, cy=y, r=5, fill=OPERATION, stroke=INK, stroke_width=2)
    element(root, "polyline", points=" ".join(parameter_points), fill="none", stroke=INK, stroke_width=4)
    target_x = plane_left + (2.0 / 2.2) * (plane_right - plane_left)
    target_y = plane_bottom - (1.0 / 1.2) * (plane_bottom - plane_top)
    element(root, "circle", cx=target_x, cy=target_y, r=11, fill=FIELD, stroke=INK, stroke_width=3)
    text(root, "declared relation (2, 1)", target_x - 8, target_y - 18, 15, anchor="end", weight=700)

    loop_y = 615.0
    loop_centers = (255.0, 485.0, 715.0, 945.0)
    loop_labels = ("PREDICT", "LOSS", "GRADIENT", "UPDATE")
    loop_fills = (REPRESENTATION, CONSTRAINT, COMPUTATION, OPERATION)
    for center, label, fill in zip(loop_centers, loop_labels, loop_fills, strict=True):
        element(root, "rect", x=center - 78, y=loop_y - 35, width=156, height=70, rx=6, fill=fill, stroke=INK, stroke_width=3)
        text(root, label, center, loop_y + 7, 17, weight=700)
    for left_center, right_center in zip(loop_centers, loop_centers[1:]):
        line(root, (left_center + 86, loop_y), (right_center - 90, loop_y), width=4, marker=True)
    line(root, (loop_centers[-1], loop_y + 44), (loop_centers[-1], 704), width=3)
    line(root, (loop_centers[-1], 704), (loop_centers[0], 704), width=3)
    line(root, (loop_centers[0], 704), (loop_centers[0], loop_y + 45), width=3, marker=True)
    text(root, "repeat with updated parameters", 600, 730, 16, weight=700)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)