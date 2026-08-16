#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_08_learned_space_probe import run_probe


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
    element(parent, "line", **attributes)


def draw_panel(
    root: ET.Element,
    *,
    left: float,
    title: str,
    subtitle: str,
    points: dict[str, tuple[float, float]],
    bounds: tuple[float, float, float, float],
    solid_neighbor: str,
    dashed_neighbor: str | None = None,
) -> None:
    panel_top = 172.0
    panel_width = 330.0
    panel_height = 350.0
    element(
        root,
        "rect",
        x=left,
        y=panel_top,
        width=panel_width,
        height=panel_height,
        rx=6,
        fill=FIELD,
        stroke=INK,
        stroke_width=3,
    )
    text(root, title, left + panel_width / 2, 142, 20, weight=700)
    text(root, subtitle, left + panel_width / 2, 165, 13)

    minimum_x, maximum_x, minimum_y, maximum_y = bounds

    def project(point: tuple[float, float]) -> tuple[float, float]:
        x = left + 30 + ((point[0] - minimum_x) / (maximum_x - minimum_x)) * (panel_width - 60)
        y = panel_top + panel_height - 30 - ((point[1] - minimum_y) / (maximum_y - minimum_y)) * (panel_height - 60)
        return (x, y)

    if minimum_x <= 0.0 <= maximum_x:
        axis_x = project((0.0, minimum_y))[0]
        line(root, (axis_x, panel_top + 15), (axis_x, panel_top + panel_height - 15), width=1)
    if minimum_y <= 0.0 <= maximum_y:
        axis_y = project((minimum_x, 0.0))[1]
        line(root, (left + 15, axis_y), (left + panel_width - 15, axis_y), width=1)

    anchor_point = project(points["anchor"])
    line(root, anchor_point, project(points[solid_neighbor]), width=5)
    if dashed_neighbor is not None:
        line(root, anchor_point, project(points[dashed_neighbor]), width=4, dash="9 7")

    fills = {
        "anchor": REPRESENTATION,
        "east": OPERATION,
        "north": COMPUTATION,
        "west": CONSTRAINT,
    }
    offsets = {
        "anchor": (0, 26),
        "east": (0, -15),
        "north": (0, -15),
        "west": (0, -15),
    }
    for name, point in points.items():
        x, y = project(point)
        element(root, "circle", cx=x, cy=y, r=9, fill=fills[name], stroke=INK, stroke_width=3)
        offset_x, offset_y = offsets[name]
        text(root, name, x + offset_x, y + offset_y, 14, weight=700)


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
    title_node.text = "Neighborhoods in a Learned Space"
    description = element(root, "desc", id="description")
    description.text = (
        "Three plots show illustrative coordinates. Euclidean distance selects north "
        "while cosine selects east in the base plot. Rotation preserves the Euclidean "
        "neighbor. Invertible anisotropic scaling changes that neighbor to east."
    )
    metadata = element(root, "metadata")
    metadata.text = "Original visual by Terrence J McLaughlin; generated from the verified Chapter 8 probe; August 13, 2026."
    element(root, "rect", width=WIDTH, height=HEIGHT, fill=FIELD)

    text(root, "NEIGHBORHOODS IN A LEARNED SPACE", WIDTH / 2, 54, 34, weight=700)
    text(root, "comparison rule and transformation determine what remains near", WIDTH / 2, 88, 19)

    draw_panel(
        root,
        left=45,
        title="BASE COORDINATES",
        subtitle="solid: Euclidean   dashed: cosine",
        points=probe["points"],
        bounds=(-1.5, 2.5, -0.5, 1.6),
        solid_neighbor=probe["base"]["nearest_by_euclidean"],
        dashed_neighbor=probe["base"]["nearest_by_cosine"],
    )
    draw_panel(
        root,
        left=435,
        title="ROTATED 37 DEGREES",
        subtitle="Euclidean distances preserved",
        points=probe["rotation"]["points"],
        bounds=(-1.8, 2.0, -0.5, 1.9),
        solid_neighbor=probe["rotation"]["nearest_by_euclidean"],
    )
    draw_panel(
        root,
        left=825,
        title="SCALED (0.2, 3.0)",
        subtitle="invertible; Euclidean neighbor changes",
        points=probe["anisotropic_scaling"]["points"],
        bounds=(-0.5, 0.7, -0.4, 3.5),
        solid_neighbor=probe["anisotropic_scaling"]["nearest_by_euclidean"],
    )

    element(root, "rect", x=100, y=570, width=1000, height=105, rx=6, fill=CONSTRAINT, stroke=INK, stroke_width=3)
    text(root, "EUCLIDEAN", 215, 605, 15, weight=700)
    text(root, "north", 215, 635, 18, weight=700)
    text(root, "COSINE", 450, 605, 15, weight=700)
    text(root, "east", 450, 635, 18, weight=700)
    text(root, "ROTATION ERROR", 700, 605, 15, weight=700)
    text(root, f"{probe['rotation']['maximum_pairwise_distance_error']:.2e}", 700, 635, 18, weight=700)
    text(root, "AFTER SCALING", 965, 605, 15, weight=700)
    text(root, "east", 965, 635, 18, weight=700)

    text(root, "illustrative coordinates; not learned by this probe; no semantic conclusion", WIDTH / 2, 720, 16, weight=700)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)