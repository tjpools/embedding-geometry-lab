#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_11_transformer_block_probe import run_probe


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


def line(
    parent: ET.Element,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    width: int = 3,
    arrow: bool = False,
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
    if arrow:
        attributes["marker_end"] = "url(#arrow)"
    if dash is not None:
        attributes["stroke_dasharray"] = dash
    element(parent, "line", **attributes)


def render_pipeline_stage(
    root: ET.Element,
    *,
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    subtitle: str,
    fill: str,
) -> None:
    box(root, x, y, width, height, fill)
    text(root, title, x + width / 2, y + 32, 15, weight=700)
    text(root, subtitle, x + width / 2, y + 56, 12)


def build_svg(output: Path) -> None:
    probe = run_probe()
    summary = probe["summary"]
    l2 = probe["control_no_attention"]["difference_l2_per_position"]

    head1 = summary["head_1_query_4_weights"]
    head2 = summary["head_2_query_4_weights"]
    z4 = summary["projected_attention_query_4"]
    y4 = summary["final_norm_query_4"]
    delta4 = summary["control_difference_query_4"]

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
    title_node.text = "Transformer Architectural Elevation"
    description = element(root, "desc", id="description")
    description.text = (
        "A deterministic transformer block fixture starts from token and positional rows, "
        "projects Q K V, splits into two attention heads with distinct normalized rows, "
        "concatenates and projects, applies residual plus normalization, applies a "
        "positionwise feed-forward stage, then applies a second residual plus normalization. "
        "A control removes projected attention and changes final outputs."
    )
    metadata = element(root, "metadata")
    metadata.text = (
        "Original visual by Terrence J McLaughlin; generated from the verified "
        "Chapter 11 probe; August 14, 2026."
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

    text(root, "TRANSFORMER ARCHITECTURAL ELEVATION", WIDTH / 2, 52, 34, weight=700)
    text(root, "attention is one interface inside a larger constrained block", WIDTH / 2, 86, 19)

    pipeline_y = 122
    stage_h = 78
    stages = [
        (45, 145, "INPUTS", "token rows X", REPRESENTATION),
        (210, 145, "POSITION", "fixed rows P", REPRESENTATION),
        (375, 145, "H0 = X + P", "model dim = 4", COMPUTATION),
        (540, 145, "Q K V PROJ", "fixed Wq Wk Wv", OPERATION),
        (705, 145, "MHA", "2 heads, dh = 2", OPERATION),
        (870, 145, "CONCAT + Wo", "project to dmodel", OPERATION),
        (1035, 145, "+ RES + LN", "first interface", CONSTRAINT),
    ]
    for x, width, title, subtitle, fill in stages:
        render_pipeline_stage(
            root,
            x=x,
            y=pipeline_y,
            width=width,
            height=stage_h,
            title=title,
            subtitle=subtitle,
            fill=fill,
        )

    for index in range(len(stages) - 1):
        current = stages[index]
        nxt = stages[index + 1]
        line(
            root,
            (current[0] + current[1] + 4, pipeline_y + stage_h / 2),
            (nxt[0] - 4, pipeline_y + stage_h / 2),
            width=3,
            arrow=True,
        )

    box(root, 70, 250, 515, 205, FIELD)
    text(root, "HEAD DISTINCTION (QUERY ROW 4)", 328, 278, 17, weight=700)
    box(root, 90, 296, 230, 132, COMPUTATION)
    box(root, 335, 296, 230, 132, COMPUTATION)
    text(root, "HEAD 1 WEIGHTS", 205, 324, 15, weight=700)
    text(root, f"({head1[0]:.3f}, {head1[1]:.3f},", 205, 352, 14, weight=700)
    text(root, f" {head1[2]:.3f}, {head1[3]:.3f})", 205, 374, 14, weight=700)
    text(root, "row sum = 1.000", 205, 404, 13)

    text(root, "HEAD 2 WEIGHTS", 450, 324, 15, weight=700)
    text(root, f"({head2[0]:.3f}, {head2[1]:.3f},", 450, 352, 14, weight=700)
    text(root, f" {head2[2]:.3f}, {head2[3]:.3f})", 450, 374, 14, weight=700)
    text(root, "row sum = 1.000", 450, 404, 13)

    text(root, "distinct heads, shared input rows", 328, 438, 13, weight=700)

    line(root, (775, 224), (602, 224), width=3)
    line(root, (602, 224), (602, 286), width=3)
    line(root, (602, 286), (575, 286), width=3, arrow=True)

    box(root, 620, 250, 535, 205, FIELD)
    text(root, "ATTENTION OUTPUT AND FIRST RESIDUAL INTERFACE", 888, 278, 17, weight=700)
    text(root, f"projected attention z4 approx ({z4[0]:.3f}, {z4[1]:.3f}, {z4[2]:.3f}, {z4[3]:.3f})", 888, 325, 14, weight=700)
    text(root, "r1 = h0 + z, then layer norm", 888, 357, 14, weight=700)
    text(root, "row means approx 0, row variances approx 1", 888, 389, 14)
    text(root, "deterministic rerun: identical final rows", 888, 421, 14)

    render_pipeline_stage(
        root,
        x=380,
        y=478,
        width=180,
        height=78,
        title="POSITIONWISE FFN",
        subtitle="ReLU(W1,b1) then W2,b2",
        fill=OPERATION,
    )
    render_pipeline_stage(
        root,
        x=620,
        y=478,
        width=180,
        height=78,
        title="+ RES + LN",
        subtitle="second interface",
        fill=CONSTRAINT,
    )
    render_pipeline_stage(
        root,
        x=860,
        y=478,
        width=260,
        height=78,
        title="FINAL ROW 4",
        subtitle=f"({y4[0]:.3f}, {y4[1]:.3f}, {y4[2]:.3f}, {y4[3]:.3f})",
        fill=COMPUTATION,
    )

    line(root, (1120, 184), (602, 184), width=3)
    line(root, (602, 184), (602, 474), width=3, arrow=True)
    line(root, (560, 517), (616, 517), width=3, arrow=True)
    line(root, (800, 517), (856, 517), width=3, arrow=True)

    box(root, 45, 582, 1110, 122, CONSTRAINT)
    text(root, "NO-ATTENTION CONTROL", 100, 611, 16, anchor="start", weight=700)
    text(root, "set projected multi-head output z = 0 before first residual", 600, 633, 15, weight=700)
    text(root, f"delta final row4 approx ({delta4[0]:.3f}, {delta4[1]:.3f}, {delta4[2]:.3f}, {delta4[3]:.3f})", 600, 655, 15, weight=700)
    text(root, f"per-position ||delta||2: {l2[0]:.3f}, {l2[1]:.3f}, {l2[2]:.3f}, {l2[3]:.3f}", 600, 677, 15, weight=700)
    text(root, "fixed deterministic fixture; not trained and not production-equivalent", 600, 699, 15, weight=700)

    text(root, "attention alone is not the transformer: the block depends on interfaces between components", WIDTH / 2, 728, 16, weight=700)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)