#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evidence.chapter_03_bayesian_update_probe import run_probe


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
    fill: str = INK,
) -> ET.Element:
    node = element(
        parent,
        "text",
        x=x,
        y=y,
        fill=fill,
        font_family=FONT,
        font_size=size,
        font_weight=weight,
        text_anchor=anchor,
        letter_spacing=0,
    )
    node.text = value
    return node


def probability_y(value: float) -> float:
    return 620 - (440 * value)


def format_probability(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def build_svg(output: Path) -> None:
    probe = run_probe()
    base = probe["base"]
    prior_case = probe["sensitivity"]["prior"]["posterior"]
    likelihood_case = probe["sensitivity"]["likelihood"]["posterior"]

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
    title_node.text = "The Shape of Updated Belief"
    description = element(root, "desc", id="description")
    description.text = (
        "A shared probability axis shows locked increasing from prior 0.6 to posterior 0.8 "
        "and unlocked decreasing from prior 0.4 to posterior 0.2 after likelihood weighting "
        "by 0.8 and 0.3 and normalization by evidence probability 0.60. Sensitivity marks "
        "show alternate posterior values without selecting a certain state."
    )
    metadata = element(root, "metadata")
    metadata.text = (
        "Original visual by Terrence J McLaughlin; generated from "
        "chapter_03_bayesian_update_probe.py; August 12, 2026."
    )

    element(root, "rect", width=WIDTH, height=HEIGHT, fill=FIELD)
    text(root, "THE SHAPE OF UPDATED BELIEF", WIDTH / 2, 62, 38, weight=700)
    text(root, "same hypotheses, same evidence, declared assumptions", WIDTH / 2, 102, 22)

    axis_x = 112
    plot_top = probability_y(1.0)
    plot_bottom = probability_y(0.0)
    element(root, "line", x1=axis_x, y1=plot_top, x2=axis_x, y2=plot_bottom, stroke=INK, stroke_width=3)
    text(root, "PROBABILITY", axis_x, 164, 16, anchor="middle", weight=700)

    for tick in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        y = probability_y(tick)
        element(root, "line", x1=axis_x - 8, y1=y, x2=axis_x + 8, y2=y, stroke=INK, stroke_width=2)
        element(root, "line", x1=axis_x + 8, y1=y, x2=1080, y2=y, stroke=INK, stroke_width=1, opacity=0.14)
        text(root, format_probability(tick), axis_x - 18, y + 6, 17, anchor="end")

    prior_x = 300
    operation_x = 595
    posterior_x = 890
    for x, label in ((prior_x, "PRIOR"), (operation_x, "EVIDENCE: red"), (posterior_x, "POSTERIOR")):
        text(root, label, x, 145, 22, weight=700)

    for x in (prior_x, posterior_x):
        element(root, "line", x1=x, y1=plot_top, x2=x, y2=plot_bottom, stroke=INK, stroke_width=3)

    series = (
        ("locked", "LOCKED", False),
        ("unlocked", "UNLOCKED", True),
    )
    for key, label, dashed in series:
        prior = base["prior"][key]
        likelihood = base["likelihood"][key]
        joint = base["joint_weight"][key]
        posterior = base["posterior"][key]
        prior_y = probability_y(prior)
        posterior_y = probability_y(posterior)
        operation_y = (prior_y + posterior_y) / 2
        dash = "10 8" if dashed else "none"

        element(
            root,
            "line",
            x1=prior_x,
            y1=prior_y,
            x2=operation_x - 100,
            y2=operation_y,
            stroke=INK,
            stroke_width=4,
            stroke_dasharray=dash,
        )
        element(
            root,
            "line",
            x1=operation_x + 100,
            y1=operation_y,
            x2=posterior_x,
            y2=posterior_y,
            stroke=INK,
            stroke_width=4,
            stroke_dasharray=dash,
        )

        if dashed:
            element(root, "rect", x=prior_x - 14, y=prior_y - 14, width=28, height=28, fill=REPRESENTATION, stroke=INK, stroke_width=3)
            element(root, "rect", x=posterior_x - 14, y=posterior_y - 14, width=28, height=28, fill=REPRESENTATION, stroke=INK, stroke_width=3)
        else:
            element(root, "circle", cx=prior_x, cy=prior_y, r=15, fill=REPRESENTATION, stroke=INK, stroke_width=3)
            element(root, "circle", cx=posterior_x, cy=posterior_y, r=15, fill=REPRESENTATION, stroke=INK, stroke_width=3)

        element(root, "rect", x=operation_x - 100, y=operation_y - 32, width=200, height=64, rx=6, fill=OPERATION, stroke=INK, stroke_width=3)
        text(root, f"× {format_probability(likelihood)}  →  {format_probability(joint)}", operation_x, operation_y + 8, 20, weight=700)
        text(root, f"{label}  {format_probability(prior)}", prior_x - 26, prior_y - 24, 18, anchor="end", weight=700)
        text(root, f"{format_probability(posterior)}  {label}", posterior_x + 26, posterior_y - 24, 18, anchor="start", weight=700)

    element(root, "rect", x=425, y=650, width=340, height=54, rx=6, fill=CONSTRAINT, stroke=INK, stroke_width=3)
    text(root, "NORMALIZE BY P(red) = 0.60", 595, 683, 18, weight=700)

    text(root, "SENSITIVITY", 1050, 164, 17, weight=700)
    text(root, "prior", 1000, 188, 15)
    text(root, "likelihood", 1090, 188, 15)
    for key in probe["hypotheses"]:
        for x, values, color in (
            (1000, prior_case, COMPUTATION),
            (1090, likelihood_case, CONSTRAINT),
        ):
            y = probability_y(values[key])
            element(root, "line", x1=x - 15, y1=y, x2=x + 15, y2=y, stroke=INK, stroke_width=5)
            element(root, "circle", cx=x, cy=y, r=7, fill=color, stroke=INK, stroke_width=2)
            text(root, format_probability(values[key]), x, y - 13, 14)

    text(root, "circle + solid = locked", 185, 728, 15, anchor="start")
    text(root, "square + dashed = unlocked", 425, 728, 15, anchor="start")
    text(root, "posterior remains a distribution, not a decision", 1015, 728, 15, anchor="end", weight=700)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)
