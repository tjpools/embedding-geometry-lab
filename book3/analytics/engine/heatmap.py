import math
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Sequence, Tuple

from runtime.mode import CorpusMode


FIELD = "#f7f7f3"
INK = "#141719"
COLOR_STOPS = (
    (247, 247, 243),
    (185, 221, 234),
    (239, 239, 183),
    (239, 220, 174),
    (239, 213, 213),
)


def normalize(values: Sequence[float]) -> List[float]:
    low = min(values, default=0.0)
    high = max(values, default=0.0)
    if math.isclose(low, high):
        return [0.5 if high else 0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]


def heat_color(value: float) -> str:
    scaled = max(0.0, min(1.0, value)) * (len(COLOR_STOPS) - 1)
    index = min(int(scaled), len(COLOR_STOPS) - 2)
    fraction = scaled - index
    left = COLOR_STOPS[index]
    right = COLOR_STOPS[index + 1]
    color = tuple(round(a + (b - a) * fraction) for a, b in zip(left, right))
    return "#{:02x}{:02x}{:02x}".format(*color)


def framing_matrix(
    architecture: dict, book_name: str
) -> Tuple[str, List[str], List[str], List[List[float]], List[List[str]]]:
    rows = architecture["chapter_density"]
    labels = [f"Chapter {row['chapter']}" for row in rows]
    columns = ["modules", "incoming", "internal", "outgoing", "cross-crate"]
    values = [
        [
            row["module_count"],
            row["incoming_dependencies"],
            row["internal_dependencies"],
            row["outgoing_dependencies"],
            row["cross_crate_edges"],
        ]
        for row in rows
    ]
    displays = [[str(value) for value in row] for row in values]
    return f"{book_name.upper()} ARCHITECTURE DENSITY", labels, columns, values, displays


def chapter_matrix(
    metrics: Sequence[dict], book_name: str
) -> Tuple[str, List[str], List[str], List[List[float]], List[List[str]]]:
    labels = [f"Ch {metric['order']}: {metric['title']}" for metric in metrics]
    columns = ["words", "sentence length", "CCI", "lexical diversity", "term density", "links"]
    values = [
        [
            metric["words"],
            metric["average_sentence_words"],
            metric["cci"],
            metric["lexical_diversity"],
            metric["terminology_density"],
            metric["links"],
        ]
        for metric in metrics
    ]
    displays = [
        [
            f"{metric['words']:,}",
            f"{metric['average_sentence_words']:.1f}",
            f"{metric['cci']:.2f}",
            f"{metric['lexical_diversity']:.1f}%",
            f"{metric['terminology_density']:.1f}",
            str(metric["links"]),
        ]
        for metric in metrics
    ]
    return f"{book_name.upper()} CHAPTER ANALYTICS", labels, columns, values, displays


def add_text(parent: ET.Element, x: float, y: float, value: str, **attributes: str) -> ET.Element:
    element = ET.SubElement(parent, "text", {"x": str(x), "y": str(y), **attributes})
    element.text = value
    return element


def write(
    path: Path, mode: CorpusMode, metrics: Sequence[dict], architecture: dict, book_name: str
) -> None:
    title, labels, columns, values, displays = (
        framing_matrix(architecture, book_name)
        if mode == CorpusMode.FRAMING
        else chapter_matrix(metrics, book_name)
    )
    label_width = 300
    cell_width = 145
    row_height = 48
    header_height = 100
    width = label_width + cell_width * len(columns) + 30
    height = header_height + row_height * len(labels) + 80
    column_values = list(zip(*values)) if values else [[] for _ in columns]
    normalized_columns = [normalize(column) for column in column_values]

    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(width),
        "height": str(height),
        "viewBox": f"0 0 {width} {height}",
        "role": "img",
        "aria-labelledby": "title desc",
    })
    title_element = ET.SubElement(svg, "title", {"id": "title"})
    title_element.text = title.title()
    description = ET.SubElement(svg, "desc", {"id": "desc"})
    description.text = "Column-normalized analytics. Color indicates relative intensity, not quality."
    ET.SubElement(svg, "rect", {"width": "100%", "height": "100%", "fill": FIELD})
    group = ET.SubElement(svg, "g", {"font-family": "DejaVu Sans, sans-serif", "fill": INK})
    add_text(group, 20, 35, title, **{"font-size": "22", "font-weight": "700"})

    for column_index, column in enumerate(columns):
        x = label_width + column_index * cell_width + cell_width / 2
        add_text(group, x, 76, column, **{"text-anchor": "middle", "font-size": "13"})

    for row_index, label in enumerate(labels):
        y = header_height + row_index * row_height
        add_text(group, 20, y + 30, label, **{"font-size": "14"})
        for column_index, column in enumerate(columns):
            x = label_width + column_index * cell_width
            intensity = normalized_columns[column_index][row_index]
            cell = ET.SubElement(group, "rect", {
                "x": str(x),
                "y": str(y),
                "width": str(cell_width - 4),
                "height": str(row_height - 4),
                "fill": heat_color(intensity),
                "stroke": INK,
                "stroke-width": "1",
            })
            tooltip = ET.SubElement(cell, "title")
            tooltip.text = f"{label}; {column}: {displays[row_index][column_index]}"
            add_text(
                group,
                x + (cell_width - 4) / 2,
                y + 29,
                displays[row_index][column_index],
                **{"text-anchor": "middle", "font-size": "13"},
            )

    legend_y = header_height + row_height * len(labels) + 35
    add_text(group, 20, legend_y, "lower relative intensity", **{"font-size": "13"})
    definitions = ET.SubElement(svg, "defs")
    gradient = ET.SubElement(definitions, "linearGradient", {"id": "scale"})
    for offset, color in (("0", FIELD), ("0.33", "#b9ddea"), ("0.66", "#efefb7"), ("1", "#efd5d5")):
        ET.SubElement(gradient, "stop", {"offset": offset, "stop-color": color})
    ET.SubElement(group, "rect", {
        "x": "175", "y": str(legend_y - 16), "width": "180", "height": "20",
        "fill": "url(#scale)", "stroke": INK, "stroke-width": "1",
    })
    add_text(group, 365, legend_y, "higher relative intensity", **{"font-size": "13"})
    ET.ElementTree(svg).write(path, encoding="utf-8", xml_declaration=True)
