#!/usr/bin/env python3

from pathlib import Path
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evidence.chapter_16_constraint_envelope_probe import run_probe


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


def panel(root: ET.Element, x: float, y: float, title: str, lines: tuple[str, ...], fill: str, result_type: str) -> None:
    box(root, x, y, 350, 150, fill)
    text(root, title, x + 18, y + 26, 14, anchor="start", weight=700)
    text(root, result_type, x + 332, y + 26, 9, anchor="end")
    for index, line in enumerate(lines):
        text(root, line, x + 18, y + 56 + index * 23, 11, anchor="start", weight=700 if index == 0 else 400)


def build_svg(output: Path) -> None:
    probe = run_probe()
    experiments = {item["experiment_id"]: item for item in probe["experiments"]}
    context = experiments["limits.context_capacity"]["result"]
    representation = experiments["limits.representation_width"]["result"]
    compute = experiments["limits.attention_work"]["result"]
    vocabulary = experiments["limits.vocabulary_coverage"]["result"]
    decoding = experiments["limits.decoding_policy"]["result"]
    architecture = experiments["limits.architecture_contribution"]["result"]

    root = ET.Element(f"{{{SVG}}}svg", {"width": str(WIDTH), "height": str(HEIGHT), "viewBox": f"0 0 {WIDTH} {HEIGHT}", "role": "img", "aria-labelledby": "title description"})
    title_node = element(root, "title", id="title")
    title_node.text = "The Constraint Envelope"
    description = element(root, "desc", id="description")
    description.text = (
        "Six distinct panels surround one fixed width-four Transformer fixture. Context and representation show acceptance gates; "
        "compute shows structural counts rather than time; vocabulary shows two absent strings collapsing to unknown ID zero; decoding "
        "shows fixed logits selecting different IDs under two policies; architecture shows a nonzero output difference. A claim boundary "
        "classifies understands, is person, and cannot ever understand as outside operational evidence, not false."
    )
    metadata = element(root, "metadata")
    metadata.text = "Original visual by Terrence J McLaughlin; generated from the verified Chapter 16 probe; August 14, 2026."
    element(root, "rect", width=WIDTH, height=HEIGHT, fill=FIELD)

    text(root, "The Constraint Envelope", WIDTH / 2, 44, 34, weight=700)
    text(root, "six typed boundaries around one fixed fixture; panel scales and units are not shared", WIDTH / 2, 72, 16)

    panel(root, 30, 98, "CONTEXT", ("capacity 3: admit 1 | 2 | 3", f"reject {context['first_rejected_length']} before embedding", "CONTEXT_CAPACITY_EXCEEDED"), CONSTRAINT, "acceptance boundary")
    panel(root, 425, 98, "REPRESENTATION", ("width 4: accepted", "width 5: rejected at block gate", "block math unexecuted"), REPRESENTATION, "interface gate")
    counts = compute["records"]
    panel(root, 820, 98, "COMPUTE", (f"n=1  {counts[0]['multiplications']}/{counts[0]['additions']}/{counts[0]['exponentials']}", f"n=2  {counts[1]['multiplications']}/{counts[1]['additions']}/{counts[1]['exponentials']}", f"n=3  {counts[2]['multiplications']}/{counts[2]['additions']}/{counts[2]['exponentials']}  mult/add/exp", "structural counts; not timing"), COMPUTATION, "formula counts")

    box(root, 340, 275, 520, 120, FIELD, double=True)
    text(root, "FIXED CHAPTER 15 FIXTURE", 600, 307, 17, weight=700)
    text(root, 'request "small models run" | context 3 | width 4 | vocabulary 6', 600, 337, 13)
    text(root, "same declared functions, constants, and baseline trace", 600, 363, 12)
    text(root, "changed variables are isolated inside their typed panels", 600, 384, 11, weight=700)

    panel(root, 30, 425, "DATA / VOCABULARY", ("quartzbird -> <unk> ID 0", "velvetaxiom -> <unk> ID 0", f"same embedding {vocabulary['embeddings'][0]}"), REPRESENTATION, "representation collision")
    panel(root, 425, 425, "DECODING", (f"global argmax -> ID {decoding['global_argmax_id']}", f"allowed-ID argmax -> ID {decoding['constrained_allowed_id']}", "logit bytes equal before / after"), OPERATION, "policy comparison")
    panel(root, 820, 425, "ARCHITECTURE", ("attention contribution -> zero", f"max |output difference| {architecture['maximum_absolute_difference']:.9f}", "request + other parameters fixed"), OPERATION, "numerical difference")

    box(root, 30, 600, 1140, 86, FIELD, dash="9 7")
    text(root, "CLAIM-SCOPE BOUNDARY", 52, 628, 14, anchor="start", weight=700)
    text(root, "understands | is_person | cannot_ever_understand", 600, 628, 12, weight=700)
    text(root, "OUTSIDE_OPERATIONAL_EVIDENCE", 600, 654, 14, weight=700)
    text(root, "scope rejection means outside these records; it does not mean false", 600, 676, 11)

    text(root, "THE ENVELOPE BOUNDS OBSERVED OPERATION, NOT ONTOLOGY", WIDTH / 2, 720, 15, weight=700)
    text(root, "exact incoming edges: architecture + execution -> limits | no outgoing Book Two module edge", WIDTH / 2, 744, 11)

    ET.indent(root, space="  ")
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    destination = Path(__file__).with_suffix(".svg")
    build_svg(destination)
    print(destination)