from pathlib import Path
from typing import Dict, List

from engine.markdown_strip import LINK_RE


EXTERNAL_SCHEMES = ("http://", "https://", "mailto:")


def scan(raw_text: str, source_path: Path) -> Dict[str, object]:
    targets = [match.group(2).strip() for match in LINK_RE.finditer(raw_text)]
    local_targets: List[str] = []
    external_targets: List[str] = []
    broken_targets: List[str] = []
    anchors = 0

    for target in targets:
        if target.startswith("#"):
            anchors += 1
            continue
        if target.startswith(EXTERNAL_SCHEMES):
            external_targets.append(target)
            continue
        local_targets.append(target)
        file_target = target.split("#", 1)[0]
        if file_target and not (source_path.parent / file_target).resolve().exists():
            broken_targets.append(target)

    return {
        "links": len(targets),
        "local_links": len(local_targets),
        "external_links": len(external_targets),
        "anchor_links": anchors,
        "broken_links": len(broken_targets),
        "broken_targets": broken_targets,
    }
