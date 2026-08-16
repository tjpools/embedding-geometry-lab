#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_15_token_execution_probe import run_probe


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
    return ET.SubElement(parent, f"{{{SVG}}}{tag}", {key.replace("_", "-"): str(value) for key, value in attributes.items()})


def text(parent: ET.Element, value: str, x: float, y: float, size: int, *, anchor: str = "middle", weight: int = 400) -> None:
    node = element(parent, "text", x=x, y=y, fill=INK, font_family=FONT, font_size=size, font_weight=weight, text_anchor=anchor, letter_spacing=0)
    node.text = value


def box(parent: ET.Element, x: float, y: float, width: float, height: float, fill: str, *, dash: str | None = None, double: bool = False) -> None:
    attributes: dict[str, object] = {"x": x, "y": y, "width": width, "height": height, "rx": 5, "fill": fill, "stroke": INK, "stroke_width": 3}
    if dash:
        attributes["stroke_dasharray"] = dash
    element(parent, "rect", **attributes)
    if double:
        element(parent, "rect", x=x + 6, y=y + 6, width=width - 12, height=height - 12, rx=2, fill="none", stroke=INK, stroke_width=2)


def arrow(parent: ET.Element, x1: float, y1: float, x2: float, y2: float, *, dash: str | None = None) -> None:
    attributes: dict[str, object] = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": INK, "stroke_width": 3, "marker_end": "url(#arrow)"}
    if dash:
        attributes["stroke_dasharray"] = dash
    element(parent, "line", **attributes)


def stage_box(root: ET.Element, x: float, y: float, width: float, title: str, detail: str, shape_label: str, work: str, fill: str) -> None:
    box(root, x, y, width, 94, fill)
    text(root, title, x + width / 2, y + 24, 13, weight=700)
    text(root, detail, x + width / 2, y + 47, 11)
    text(root, shape_label, x + width / 2, y + 67, 10)
    text(root, work, x + width / 2, y + 84, 9)


def short_digest(record: dict) -> str:
    return record["output_sha256"][:10]


def build_svg(output: Path) -> None:
    probe = run_probe()
    trace = probe["trace"]
    records = {record["stage"]: record for record in trace["stages"]}
    control = probe["width_corruption_control"]
    final_row = records["final_position_hidden"]["output_values"]
    logits = records["vocabulary_projection"]["output_values"]

    root = ET.Element(f"{{{SVG}}}svg", {"width": str(WIDTH), "height": str(HEIGHT), "viewBox": f"0 0 {WIDTH} {HEIGHT}", "role": "img", "aria-labelledby": "title description"})
    title_node = element(root, "title", id="title")
    title_node.text = "A Token Through the Machine"
    description = element(root, "desc", id="description")
    description.text = (
        "A deterministic execution trace carries the text small models run through token IDs, embedding plus position rows, "
        "one attention-residual-normalization-feed-forward-residual-normalization block, a final hidden row, vocabulary logits, "
        "lowest-ID-tie argmax, and decoding to models. A subordinate width-corruption lane stops at block input validation; later stages are unexecuted."
    )
    metadata = element(root, "metadata")
    metadata.text = "Original visual by Terrence J McLaughlin; generated from the verified Chapter 15 probe; August 14, 2026."
    definitions = element(root, "defs")
    marker = element(definitions, "marker", id="arrow", markerWidth=10, markerHeight=10, refX=8, refY=3, orient="auto", markerUnits="strokeWidth")
    element(marker, "path", d="M0,0 L0,6 L9,3 z", fill=INK)
    element(root, "rect", width=WIDTH, height=HEIGHT, fill=FIELD)

    text(root, "A Token Through the Machine", WIDTH / 2, 46, 34, weight=700)
    text(root, "validated values move in runtime order; each handoff records shape, digest, allocation, and work", WIDTH / 2, 76, 16)

    top = (
        (30, 210, "TEXT", '"small models run"', "scalar -> [3]", "15 character scans", REPRESENTATION),
        (270, 170, "TOKEN IDS", "[1, 2, 3]", "[3] -> [3]", "3 vocabulary lookups", REPRESENTATION),
        (470, 270, "EMBED + POSITION", "[[.2,0,.4,.4], ...]", "[3] -> [3,4]", f"12 add | sha {short_digest(records['embedding_plus_position'])}", REPRESENTATION),
        (770, 190, "BLOCK GATE", "accepted", "[3,4] -> [3,4]", "2 dimension comparisons", CONSTRAINT),
        (990, 180, "BLOCK INPUT", "width = 4", "[3,4]", f"sha {short_digest(records['block_input_validation'])}", REPRESENTATION),
    )
    for x, width, title, detail, shape_label, work, fill in top:
        stage_box(root, x, 108, width, title, detail, shape_label, work, fill)
    for left, right in zip(top, top[1:]):
        arrow(root, left[0] + left[1] + 4, 155, right[0] - 4, 155)

    block_y = 250
    block_stages = (
        (55, 235, "ATTENTION", f"out sha {short_digest(records['attention'])}", "[3,4] -> [3,4]", "264 mult | 195 add | 9 exp", OPERATION),
        (330, 230, "RESIDUAL + NORM 1", f"out sha {short_digest(records['residual_norm_1'])}", "[2,3,4] -> [3,4]", "12 residual add | 12 norm", CONSTRAINT),
        (600, 230, "FEED-FORWARD", f"out sha {short_digest(records['feed_forward'])}", "[3,4] -> [3,4]", "120 mult | 27 bias | 15 ReLU", COMPUTATION),
        (870, 275, "RESIDUAL + NORM 2", f"out sha {short_digest(records['residual_norm_2'])}", "[2,3,4] -> [3,4]", "12 residual add | 12 norm", CONSTRAINT),
    )
    box(root, 30, 228, 1140, 138, FIELD, double=True)
    text(root, "ONE FIXED TRANSFORMER BLOCK", 55, 248, 12, anchor="start", weight=700)
    for x, width, title, detail, shape_label, work, fill in block_stages:
        stage_box(root, x, block_y, width, title, detail, shape_label, work, fill)
    for left, right in zip(block_stages, block_stages[1:]):
        arrow(root, left[0] + left[1] + 4, block_y + 47, right[0] - 4, block_y + 47)

    output_y = 405
    output_stages = (
        (30, 260, "FINAL-POSITION HIDDEN", f"[{final_row[0]:.3f}, {final_row[1]:.3f}, {final_row[2]:.3f}, {final_row[3]:.3f}]", "[3,4] -> [4]", "1 row selection", REPRESENTATION),
        (330, 320, "VOCABULARY LOGITS", f"[{', '.join(f'{value:.3f}' for value in logits)}]", "[4] -> [6]", "24 mult | 18 add", COMPUTATION),
        (690, 210, "ARGMAX", "ID 2 (lowest-ID tie rule)", "[6] -> scalar", "5 comparisons", OPERATION),
        (940, 230, "DECODE", 'ID 2 -> "models"', "scalar -> scalar", "1 vocabulary lookup", REPRESENTATION),
    )
    for x, width, title, detail, shape_label, work, fill in output_stages:
        stage_box(root, x, output_y, width, title, detail, shape_label, work, fill)
    for left, right in zip(output_stages, output_stages[1:]):
        arrow(root, left[0] + left[1] + 4, output_y + 47, right[0] - 4, output_y + 47)

    box(root, 30, 548, 1140, 128, FIELD, dash="9 7")
    text(root, "WIDTH-CORRUPTION CONTROL", 55, 574, 14, anchor="start", weight=700)
    stage_box(root, 55, 586, 270, "CORRUPTED ROWS", "append one zero coordinate", "[3,5]", f"sha {control['corrupted_rows_sha256'][:10]}", REPRESENTATION)
    arrow(root, 330, 633, 395, 633)
    stage_box(root, 400, 586, 330, "BLOCK INPUT VALIDATION", "BLOCK_INPUT_WIDTH_MISMATCH", "expected [3,4]; actual [3,5]", "first failed stage", CONSTRAINT)
    arrow(root, 735, 633, 800, 633, dash="7 6")
    box(root, 805, 586, 335, 94, FIELD, dash="7 6")
    text(root, "UNEXECUTED", 972, 611, 13, weight=700)
    text(root, "block math | projection | argmax | decode", 972, 638, 11)
    text(root, "execution stops at the failed gate", 972, 660, 10, weight=700)

    text(root, "allocated-element and work counts are deterministic fixture records, not latency, throughput, or a runtime benchmark", WIDTH / 2, 720, 13, weight=700)
    text(root, f"deterministic rerun identical | {probe['validation_count']} validations", WIDTH / 2, 744, 12)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)