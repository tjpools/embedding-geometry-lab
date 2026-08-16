#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from pathlib import Path


WIDTH = 1200
HEIGHT = 800
FIELD = "#f7f7f3"
INK = "#141719"
REPRESENTATION = "#efd5d5"
OPERATION = "#efdcae"
CONSTRAINT = "#efefb7"
COMPUTATION = "#b9ddea"
FONT = "DejaVu Sans, sans-serif"

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)

ROOT = Path(__file__).resolve().parents[1]
RUST_SOURCE = ROOT / "evidence" / "chapter_01_door_model.rs"

STATES = (
    ("LC", "locked, closed"),
    ("UC", "unlocked, closed"),
    ("UO", "unlocked, open"),
)

PANELS = (
    {
        "title": "ALGEBRAIC",
        "subtitle": "partial transformations on D",
        "gate_one": "LC in dom(u)",
        "gate_two": "UC in dom(o)",
        "result": "unlock then open: LC -> UO",
        "failure": "o(LC) undefined",
        "fill": OPERATION,
    },
    {
        "title": "SYMBOLIC",
        "subtitle": "represented facts and actions",
        "gate_one": "pre: locked + closed",
        "gate_two": "pre: unlocked + closed",
        "result": "effects of UNLOCK enable OPEN",
        "failure": "OPEN preconditions fail",
        "fill": CONSTRAINT,
    },
    {
        "title": "PROGRAMMED",
        "subtitle": "typed state, match, and Result",
        "gate_one": "match LockedClosed",
        "gate_two": "match UnlockedClosed",
        "result": "Ok(UnlockedOpen)",
        "failure": "Err(Locked)",
        "fill": COMPUTATION,
    },
)


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


def arrow(parent: ET.Element, x1: float, y: float, x2: float) -> None:
    element(parent, "line", x1=x1, y1=y, x2=x2 - 11, y2=y, stroke=INK, stroke_width=3)
    element(parent, "polygon", points=f"{x2 - 11},{y - 7} {x2},{y} {x2 - 11},{y + 7}", fill=INK)


def state_box(parent: ET.Element, x: float, y: float, code: str, label: str) -> None:
    element(parent, "rect", x=x, y=y, width=88, height=74, rx=6, fill=REPRESENTATION, stroke=INK, stroke_width=3)
    text(parent, code, x + 44, y + 31, 23, weight=700)
    text(parent, label, x + 44, y + 55, 11, weight=700)


def gate(parent: ET.Element, x: float, y: float, label: str, action: str) -> None:
    element(parent, "rect", x=x, y=y, width=112, height=48, rx=6, fill=CONSTRAINT, stroke=INK, stroke_width=2)
    text(parent, action, x + 56, y + 19, 13, weight=700)
    text(parent, label, x + 56, y + 37, 10)


def verify_rust_alignment() -> None:
    source = RUST_SOURCE.read_text(encoding="utf-8")
    required = (
        "DoorState::LockedClosed => Ok(DoorState::UnlockedClosed)",
        "DoorState::UnlockedClosed => Ok(DoorState::UnlockedOpen)",
        "DoorState::LockedClosed => Err(DoorError::Locked)",
        "unlock_then_open(DoorState::LockedClosed)",
        "Ok(DoorState::UnlockedOpen)",
    )
    missing = [snippet for snippet in required if snippet not in source]
    if missing:
        raise ValueError(f"visual data no longer aligns with Rust source: {missing}")


def build_svg(output: Path) -> None:
    verify_rust_alignment()

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
    title_node.text = "Three Forms of Constraint"
    description = element(root, "desc", id="description")
    description.text = (
        "Three aligned panels compare the represented transition locked-closed to unlocked-closed "
        "to unlocked-open. The algebraic panel gates partial operations by their domains. The symbolic "
        "panel gates actions by represented preconditions. The programmed panel gates typed states by "
        "Rust match branches and returns Result values. A failed attempt to open locked-closed is undefined, "
        "inapplicable, or Err Locked respectively. This is a comparison of interfaces, not an equivalence."
    )
    metadata = element(root, "metadata")
    metadata.text = (
        "Original visual by Terrence J McLaughlin; generated from the execution-verified "
        "chapter_01_door_model.rs; August 12, 2026."
    )

    element(root, "rect", width=WIDTH, height=HEIGHT, fill=FIELD)
    text(root, "THREE FORMS OF CONSTRAINT", WIDTH / 2, 50, 36, weight=700)
    text(root, "same represented transition; different sources of permission and consequence", WIDTH / 2, 82, 18)

    panel_width = 360
    panel_y = 116
    panel_height = 530
    for index, panel in enumerate(PANELS):
        panel_x = 35 + index * 390
        element(
            root,
            "rect",
            x=panel_x,
            y=panel_y,
            width=panel_width,
            height=panel_height,
            rx=6,
            fill=FIELD,
            stroke=INK,
            stroke_width=3,
        )
        element(root, "rect", x=panel_x, y=panel_y, width=panel_width, height=72, rx=6, fill=panel["fill"])
        element(root, "line", x1=panel_x, y1=188, x2=panel_x + panel_width, y2=188, stroke=INK, stroke_width=3)
        text(root, panel["title"], panel_x + panel_width / 2, 148, 22, weight=700)
        text(root, panel["subtitle"], panel_x + panel_width / 2, 174, 13)

        state_y = 238
        state_x = (panel_x + 18, panel_x + 136, panel_x + 254)
        for x, (code, label) in zip(state_x, STATES):
            state_box(root, x, state_y, code, label)
        arrow(root, state_x[0] + 88, state_y + 37, state_x[1])
        arrow(root, state_x[1] + 88, state_y + 37, state_x[2])

        text(root, "PERMISSION", panel_x + 180, 332, 11, weight=700)
        gate(root, panel_x + 82, 342, panel["gate_one"], "UNLOCK")
        gate(root, panel_x + 202, 342, panel["gate_two"], "OPEN")

        element(root, "rect", x=panel_x + 24, y=414, width=312, height=64, rx=6, fill=panel["fill"], stroke=INK, stroke_width=2)
        text(root, "CONSEQUENCE", panel_x + 180, 436, 11, weight=700)
        text(root, panel["result"], panel_x + 180, 462, 15, weight=700)

        element(
            root,
            "rect",
            x=panel_x + 24,
            y=510,
            width=312,
            height=88,
            rx=6,
            fill=FIELD,
            stroke=INK,
            stroke_width=2,
            stroke_dasharray="7 5",
        )
        text(root, "BOUNDARY: OPEN(LC)", panel_x + 180, 536, 12, weight=700)
        text(root, panel["failure"], panel_x + 180, 567, 16, weight=700)
        text(root, "no transition to UO", panel_x + 180, 588, 11)

    element(root, "rect", x=35, y=680, width=1130, height=72, rx=6, fill=INK)
    text(root, "COMPARISON OF INTERFACES, NOT EQUIVALENCE", WIDTH / 2, 710, 20, weight=700, fill=FIELD)
    text(root, "internal success does not establish physical correspondence or operational adequacy", WIDTH / 2, 737, 15, fill=FIELD)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)