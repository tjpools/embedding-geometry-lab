import csv
import re
from pathlib import Path

INPUT_CSV = "book/chapters.csv"
OUTPUT_CSV = "book/wordcounts.csv"
BASE_DIR = Path(".")

WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)
FRONTMATTER_RE = re.compile(r"(?s)\A---\n.*?\n---\n?")
FENCED_CODE_RE = re.compile(r"(?s)```.*?```")
INLINE_CODE_RE = re.compile(r"`([^`]*)`")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
FOOTNOTE_RE = re.compile(r"\[\^([^\]]+)\]")
HEADER_MARK_RE = re.compile(r"^\s{0,3}#{1,6}\s*", re.MULTILINE)
BLOCKQUOTE_RE = re.compile(r"^\s{0,3}>\s?", re.MULTILINE)
LIST_MARK_RE = re.compile(r"^\s*[-*+]\s+", re.MULTILINE)
ORDERED_LIST_RE = re.compile(r"^\s*\d+\.\s+", re.MULTILINE)
TABLE_PIPE_RE = re.compile(r"\|")
EMPHASIS_RE = re.compile(r"[*_~]")
REFERENCE_LINK_DEF_RE = re.compile(r"^\s*\[[^\]]+\]:\s+\S+.*$", re.MULTILINE)


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def infer_title_from_markdown(text: str, fallback: str = "") -> str:
    text = strip_frontmatter(text)
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def strip_markdown(text: str) -> str:
    text = strip_frontmatter(text)
    text = FENCED_CODE_RE.sub(" ", text)
    text = REFERENCE_LINK_DEF_RE.sub(" ", text)
    text = IMAGE_RE.sub(r"\1", text)
    text = LINK_RE.sub(r"\1", text)
    text = INLINE_CODE_RE.sub(r"\1", text)
    text = HEADER_MARK_RE.sub("", text)
    text = BLOCKQUOTE_RE.sub("", text)
    text = LIST_MARK_RE.sub("", text)
    text = ORDERED_LIST_RE.sub("", text)
    text = FOOTNOTE_RE.sub(r"\1", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = TABLE_PIPE_RE.sub(" ", text)
    text = EMPHASIS_RE.sub("", text)
    return text


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def load_chapter_rows(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    required = {"chapter", "path"}
    missing = required - set(reader.fieldnames or [])
    if missing:
        raise ValueError(f"Missing required CSV columns: {sorted(missing)}")
    return rows


def process_chapters(rows):
    results = []
    for row in rows:
        chapter = row["chapter"].strip()
        rel_path = row["path"].strip()
        given_title = row.get("title", "").strip()

        file_path = BASE_DIR / rel_path
        if not file_path.exists():
            results.append({
                "chapter": chapter,
                "title": given_title,
                "path": rel_path,
                "word_count": "",
                "status": "missing_file",
            })
            continue

        raw_text = file_path.read_text(encoding="utf-8")
        title = given_title or infer_title_from_markdown(raw_text, fallback=rel_path)
        clean_text = strip_markdown(raw_text)
        word_count = count_words(clean_text)

        results.append({
            "chapter": chapter,
            "title": title,
            "path": rel_path,
            "word_count": word_count,
            "status": "ok",
        })
    return results


def write_output_csv(path: str, rows):
    fieldnames = ["chapter", "title", "path", "word_count", "status"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def make_bar(value: int, max_value: int, width: int = 32) -> str:
    if max_value <= 0:
        return ""
    filled = max(1, round((value / max_value) * width))
    return "█" * filled


def print_summary(rows):
    ok_rows = [r for r in rows if r["status"] == "ok"]
    total = sum(int(r["word_count"]) for r in ok_rows)

    print("\nWord Count Summary\n")
    print(f"{'Ch':>2}  {'Words':>7}  Title")
    print("-" * 72)
    for r in rows:
        wc = r["word_count"] if r["word_count"] != "" else "ERROR"
        print(f"{str(r['chapter']):>2}  {str(wc):>7}  {r['title']}")
    print("-" * 72)
    print(f"Total words: {total:,}")
    print(f"Exported: {OUTPUT_CSV}")


def print_sorted_report(rows):
    ok_rows = [r for r in rows if r["status"] == "ok"]
    sorted_rows = sorted(ok_rows, key=lambda r: int(r["word_count"]), reverse=True)

    print("\nLongest to Shortest\n")
    print(f"{'Rank':>4}  {'Ch':>2}  {'Words':>7}  Title")
    print("-" * 72)
    for i, r in enumerate(sorted_rows, start=1):
        print(f"{i:>4}  {str(r['chapter']):>2}  {int(r['word_count']):>7,}  {r['title']}")


def print_ascii_chart(rows):
    ok_rows = [r for r in rows if r["status"] == "ok"]
    if not ok_rows:
        return

    max_words = max(int(r["word_count"]) for r in ok_rows)
    title_width = max(len(r["title"]) for r in ok_rows)

    print("\nASCII Bar Chart\n")
    for r in ok_rows:
        words = int(r["word_count"])
        bar = make_bar(words, max_words, width=32)
        print(f"Ch {str(r['chapter']).rjust(2)}  {r['title']:<{title_width}}  {bar:<32}  {words:>5,}")


def main():
    rows = load_chapter_rows(INPUT_CSV)
    results = process_chapters(rows)
    write_output_csv(OUTPUT_CSV, results)
    print_summary(results)
    print_sorted_report(results)
    print_ascii_chart(results)


if __name__ == "__main__":
    main()
