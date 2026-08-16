#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_12_callable_tool_probe import run_probe


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


def box(parent: ET.Element, x: float, y: float, width: float, height: float, fill: str, *, dash: str | None = None) -> None:
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


def path(parent: ET.Element, points: str, *, arrow: bool = True, dash: str | None = None) -> None:
    attributes: dict[str, object] = {
        "d": points,
        "fill": "none",
        "stroke": INK,
        "stroke_width": 3,
    }
    if arrow:
        attributes["marker_end"] = "url(#arrow)"
    if dash:
        attributes["stroke_dasharray"] = dash
    element(parent, "path", **attributes)


def stage(parent: ET.Element, x: float, title: str, lines: tuple[str, ...], fill: str) -> None:
    box(parent, x, 160, 170, 142, fill)
    text(parent, title, x + 85, 193, 15, weight=700)
    for index, line_value in enumerate(lines):
        text(parent, line_value, x + 85, 226 + index * 23, 13)


def build_svg(output: Path) -> None:
    probe = run_probe()
    package = probe["serialized_model_package"]
    response = probe["callable_exchange"]["response"]["values"]
    corrupt = probe["corrupted_package_control"]

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
    title_node.text = "From Specification to Callable Tool"
    description = element(root, "desc", id="description")
    description.text = (
        "A deterministic contract chain connects an architecture specification, framework operation registry, "
        "serialized model package, validating loader, selected runtime capabilities, and callable request and response. "
        "A corrupted declared dimension follows a dashed path to rejection before construction or invocation."
    )
    metadata = element(root, "metadata")
    metadata.text = "Original visual by Terrence J McLaughlin; generated from the verified Chapter 12 probe; August 14, 2026."

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

    text(root, "From Specification to Callable Tool", WIDTH / 2, 54, 34, weight=700)
    text(root, "callability appears only when each boundary preserves its declared contract", WIDTH / 2, 88, 18)

    stage_x = (35, 225, 415, 605, 795, 985)
    for left, right in zip(stage_x, stage_x[1:]):
        path(root, f"M {left + 174} 231 L {right - 7} 231")

    stage(root, stage_x[0], "SPECIFICATION", ("book2.affine-row", "version 1.0", "dimensions 3 -> 2"), REPRESENTATION)
    stage(root, stage_x[1], "FRAMEWORK", ("operation registry", "affine_row", "resolve by name"), OPERATION)
    stage(root, stage_x[2], "MODEL PACKAGE", ("structured JSON", f"{package['byte_length']} bytes", f"sha256 {package['sha256'][:8]}..."), REPRESENTATION)
    stage(root, stage_x[3], "LOADER", ("parse then validate", "shape + operation", "construct on pass"), CONSTRAINT)
    stage(root, stage_x[4], "RUNTIME", ("selected capabilities", "float64 arithmetic", "structured JSON"), COMPUTATION)
    stage(root, stage_x[5], "CALLABLE", ("request vector.v1", "internal affine row", "response vector.v1"), OPERATION)

    box(root, 76, 355, 490, 165, FIELD)
    text(root, "VALID PACKAGE PATH", 100, 388, 16, anchor="start", weight=700)
    text(root, "validation result", 205, 428, 14)
    box(root, 305, 402, 220, 48, CONSTRAINT)
    text(root, "PACKAGE_VALID", 415, 433, 15, weight=700)
    text(root, "construction count = 2", 205, 480, 14)
    text(root, "reload + reinvoke identical", 415, 480, 14, weight=700)

    box(root, 634, 355, 490, 165, COMPUTATION)
    text(root, "CALLABLE EXCHANGE", 658, 388, 16, anchor="start", weight=700)
    box(root, 658, 410, 180, 66, REPRESENTATION)
    text(root, "REQUEST", 748, 435, 14, weight=700)
    text(root, "[2, -1, 0.5]", 748, 460, 14)
    path(root, "M 845 443 L 907 443")
    box(root, 916, 410, 180, 66, REPRESENTATION)
    text(root, "RESPONSE", 1006, 435, 14, weight=700)
    text(root, f"[{response[0]}, {response[1]}]", 1006, 460, 14, weight=700)
    text(root, "interface validation remains separate from package loading", 879, 502, 13)

    path(root, "M 500 306 L 500 330 L 50 330 L 50 610 L 67 610", dash="9 7")
    box(root, 75, 552, 275, 116, REPRESENTATION, dash="9 7")
    text(root, "CORRUPT PACKAGE", 212, 583, 15, weight=700)
    text(root, "input dimension: 3 -> 4", 212, 612, 14)
    text(root, "parameter payload unchanged", 212, 640, 13)

    path(root, "M 357 610 L 467 610", dash="9 7")
    box(root, 476, 552, 648, 116, CONSTRAINT)
    text(root, "REJECTED BEFORE INVOCATION", 800, 583, 16, weight=700)
    text(root, corrupt["validation"]["code"], 800, 616, 17, weight=700)
    text(root, "constructed: false   |   invoked: false", 800, 646, 14)

    text(root, "deterministic, dependency-free fixture; not production compatibility, performance, quality, or full inference", WIDTH / 2, 718, 15, weight=700)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)