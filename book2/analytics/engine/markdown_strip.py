import re
from typing import List


WORD_RE = re.compile(r"\b[\w]+(?:[\u2019'-][\w]+)*\b", re.UNICODE)
FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n?", re.DOTALL)
FENCED_CODE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`([^`]*)`")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s+\S+.*$", re.MULTILINE)
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", re.MULTILINE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
LIST_MARK_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+", re.MULTILINE)
BLOCKQUOTE_RE = re.compile(r"^\s{0,3}>\s?", re.MULTILINE)
EMPHASIS_RE = re.compile(r"[*_~]")


def strip_markdown(text: str) -> str:
    text = FRONTMATTER_RE.sub("", text, count=1)
    text = FENCED_CODE_RE.sub(" ", text)
    text = REFERENCE_LINK_RE.sub(" ", text)
    text = IMAGE_RE.sub(r"\1", text)
    text = LINK_RE.sub(r"\1", text)
    text = INLINE_CODE_RE.sub(r"\1", text)
    text = HEADING_RE.sub(r"\1", text)
    text = BLOCKQUOTE_RE.sub("", text)
    text = LIST_MARK_RE.sub("", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = EMPHASIS_RE.sub("", text)
    return text.replace("|", " ")


def extract_words(text: str) -> List[str]:
    return WORD_RE.findall(text)


def sentence_word_counts(text: str) -> List[int]:
    segments = re.findall(r"[^.!?]+(?:[.!?]+|$)", text)
    return [len(extract_words(segment)) for segment in segments if extract_words(segment)]


def count_paragraphs(text: str) -> int:
    return len([block for block in re.split(r"\n\s*\n", text) if extract_words(block)])
