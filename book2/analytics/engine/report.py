import csv
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence

from engine import chapter_balance, heatmap, linkcheck, manpages, markdown_strip, readability, terminology_scan, wordcount
from runtime.mode import CorpusMode, SourceUnit, load_architecture, select_corpus


def analyze_unit(unit: SourceUnit, book_dir: Path) -> dict:
    source_path = book_dir / unit.path
    if not source_path.exists():
        raise FileNotFoundError(f"Source does not exist: {unit.path}")
    raw = source_path.read_text(encoding="utf-8")
    clean = markdown_strip.strip_markdown(raw)
    volume = wordcount.measure(clean)
    shape = readability.measure(clean)
    vocabulary = terminology_scan.scan(clean)
    links = linkcheck.scan(raw, source_path)
    words = volume["words"]
    return {
        "kind": unit.kind,
        "order": unit.order,
        "title": unit.title,
        "path": unit.path,
        **volume,
        **shape,
        "headings": len(markdown_strip.HEADING_RE.findall(raw)),
        "code_blocks": len(markdown_strip.FENCED_CODE_RE.findall(raw)),
        "figures": len(markdown_strip.IMAGE_RE.findall(raw)),
        "lexical_diversity": round(volume["unique_words"] / words * 100, 1) if words else 0.0,
        **vocabulary,
        **links,
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, metrics: Sequence[dict]) -> None:
    fields = [
        "kind", "order", "title", "path", "words", "unique_words", "characters",
        "characters_no_spaces", "sentences", "paragraphs", "headings", "code_blocks",
        "figures", "lexical_diversity", "average_sentence_words", "long_sentence_percent",
        "cci", "reading_ease_estimate", "terminology_density", "links", "local_links",
        "external_links", "anchor_links", "broken_links",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for metric in metrics:
            writer.writerow({field: metric[field] for field in fields})


def output_payloads(mode: CorpusMode, metrics: Sequence[dict], architecture: dict) -> Dict[str, dict]:
    balance = chapter_balance.calculate(metrics)
    term_totals = terminology_scan.aggregate(metrics)
    broken_total = sum(metric["broken_links"] for metric in metrics)
    common = {"schema_version": 1, "mode": mode.value}
    wordcounts = {
        **common,
        "total_words": sum(metric["words"] for metric in metrics),
        "units": [
            {key: metric[key] for key in (
                "order", "title", "path", "words", "unique_words", "characters", "characters_no_spaces"
            )}
            for metric in metrics
        ],
    }
    terminology = {
        **common,
        "terms": list(terminology_scan.DEFAULT_TERMS),
        "totals": term_totals,
        "units": [
            {
                "order": metric["order"], "title": metric["title"],
                "density_per_1000_words": metric["terminology_density"],
                "counts": metric["term_counts"],
            }
            for metric in metrics
        ],
    }
    readability_payload = {
        **common,
        "note": "Reading ease is a heuristic estimate for comparative inspection, not a quality score.",
        "units": [
            {key: metric[key] for key in (
                "order", "title", "sentences", "paragraphs", "average_sentence_words",
                "long_sentence_percent", "cci", "reading_ease_estimate"
            )}
            for metric in metrics
        ],
    }
    links = {
        **common,
        "broken_local_links": broken_total,
        "external_link_policy": "inventoried_not_network_checked",
        "units": [
            {key: metric[key] for key in (
                "order", "title", "path", "links", "local_links", "external_links",
                "anchor_links", "broken_links", "broken_targets"
            )}
            for metric in metrics
        ],
    }
    balance_payload = {**common, "corpus": balance, "architecture": architecture}
    unified = {
        **common,
        "totals": {
            "sources": len(metrics),
            "words": wordcounts["total_words"],
            "broken_links": broken_total,
        },
        "architecture": architecture,
        "sources": list(metrics),
    }
    return {
        "wordcounts.json": wordcounts,
        "balance.json": balance_payload,
        "terminology.json": terminology,
        "readability.json": readability_payload,
        "links.json": links,
        "report.json": unified,
    }


def write_manpages_section(lines: List[str], man_report: dict) -> None:
    lines.extend([
        "",
        "## Component Lookup Layer (man/)",
        "",
    ])
    if not man_report["present"]:
        lines.append("No `man/` directory found.")
        return
    lines.extend([
        f"- Pages: {man_report['page_count']} (indexed: {man_report['indexed_count']}, clean: {man_report['clean_pages']})",
        f"- Orphan pages (file exists, not indexed): {man_report['orphan_pages'] or 'none'}",
        f"- Missing pages (indexed, no file): {man_report['missing_pages'] or 'none'}",
    ])
    broken = [
        p for p in man_report["pages"]
        if p["missing_sections"] or p["broken_see_also"] or p["broken_source"]
    ]
    if broken:
        lines.append("- Pages with issues:")
        for page in broken:
            issues = []
            if page["missing_sections"]:
                issues.append(f"missing sections: {', '.join(page['missing_sections'])}")
            if page["broken_see_also"]:
                issues.append(f"broken SEE ALSO: {', '.join(page['broken_see_also'])}")
            if page["broken_source"]:
                issues.append(f"broken SOURCE chapter: {page['broken_source']}")
            lines.append(f"  - {page['name']}: {'; '.join(issues)}")
    else:
        lines.append("- All pages pass structural, cross-reference, and source checks.")


def write_markdown(path: Path, mode: CorpusMode, metrics: Sequence[dict], architecture: dict, man_report: dict) -> None:
    total_words = sum(metric["words"] for metric in metrics)
    term_totals = Counter()
    for metric in metrics:
        term_totals.update(metric["term_counts"])
    lines = [
        "# Book Two Analytics",
        "",
        "> Generated by `python3 analytics/analyze.py`. Do not edit manually.",
        "",
        "## Runtime",
        "",
        f"- Mode: **{mode.value}**",
        f"- Measured units: {len(metrics)}",
        f"- Words: {total_words:,}",
        f"- Canonical modules: {architecture['module_count']}",
        f"- Dependency edges: {architecture['edge_count']}",
        f"- Dependency layers: {len(architecture['layers'])}",
        f"- Broken local links: {sum(metric['broken_links'] for metric in metrics)}",
        "",
        "## Unit Metrics",
        "",
        "| Unit | Words | Share | Avg words/sentence | Long sentences | CCI | Lexical diversity | Reading ease* | Term density | Links |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for metric in metrics:
        share = metric["words"] / total_words * 100 if total_words else 0.0
        lines.append(
            f"| {metric['title']} | {metric['words']:,} | {share:.1f}% | "
            f"{metric['average_sentence_words']:.1f} | {metric['long_sentence_percent']:.1f}% | "
            f"{metric['cci']:.2f} | {metric['lexical_diversity']:.1f}% | "
            f"{metric['reading_ease_estimate']:.1f} | {metric['terminology_density']:.1f} | "
            f"{metric['links']} ({metric['broken_links']} broken) |"
        )
    lines.extend([
        "",
        "*Reading ease is heuristic and comparative; technical vocabulary can lower it without indicating weak prose.*",
        "",
        "## Structural Vocabulary",
        "",
        "| Term | Exact count |",
        "|---|---:|",
    ])
    for term in terminology_scan.DEFAULT_TERMS:
        lines.append(f"| {term} | {term_totals[term]} |")
    heatmap_name = "Architecture density" if mode == CorpusMode.FRAMING else "Chapter analytics"
    lines.extend([
        "",
        f"## {heatmap_name}",
        "",
        "![Book Two analytic heatmap](heatmap.svg)",
        "",
        "Each column is normalized independently. Color shows relative intensity, not quality.",
    ])
    write_manpages_section(lines, man_report)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(book_dir: Path, registry_path: Path, output_dir: Path) -> dict:
    mode, units, registry = select_corpus(book_dir, registry_path)
    architecture = load_architecture(book_dir, registry)
    metrics = [analyze_unit(unit, book_dir) for unit in units]
    man_report = manpages.scan(book_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, payload in output_payloads(mode, metrics, architecture).items():
        write_json(output_dir / filename, payload)
    write_json(output_dir / "manpages.json", {"schema_version": 1, **man_report})
    write_csv(output_dir / "metrics.csv", metrics)
    write_markdown(output_dir / "report.md", mode, metrics, architecture, man_report)
    heatmap.write(output_dir / "heatmap.svg", mode, metrics, architecture)
    man_issues = 0
    if man_report["present"]:
        man_issues = (
            len(man_report["orphan_pages"]) + len(man_report["missing_pages"])
            + (man_report["page_count"] - man_report["clean_pages"])
        )
    return {
        "mode": mode.value,
        "sources": len(metrics),
        "words": sum(metric["words"] for metric in metrics),
        "broken_links": sum(metric["broken_links"] for metric in metrics),
        "man_pages": man_report["page_count"] if man_report["present"] else 0,
        "man_issues": man_issues,
        "output": str(output_dir),
    }
