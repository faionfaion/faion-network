#!/usr/bin/env python3
"""F-065 phase 5 validator: playbook goal taxonomy.

Checks:
- Root tag is <taxonomy>.
- Exactly 11 <category> entries.
- Each category has id + trigger attrs and child <intent> + <scope> + <typical-outputs> tags with non-empty text.
- <decision-tree> exists with >= 11 <step> entries.

Usage:
    python3 scripts/validate-playbook-taxonomy.py [path]

Default path: skills/faion/playbooks/taxonomy.xml

Exit codes:
    0 - taxonomy valid
    1 - validation failed
"""

from __future__ import annotations

import sys
from pathlib import Path
from xml.etree import ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "skills" / "faion" / "playbooks" / "taxonomy.xml"
EXPECTED_CATEGORIES = 11
REQUIRED_CHILD_TAGS = ("intent", "scope", "typical-outputs")
REQUIRED_CATEGORY_ATTRS = ("id", "trigger")


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"taxonomy file missing: {path}"]
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"xml parse error: {exc}"]
    root = tree.getroot()
    if root.tag != "taxonomy":
        errors.append(f"root tag must be <taxonomy>, got <{root.tag}>")

    categories = root.findall("category")
    if len(categories) != EXPECTED_CATEGORIES:
        errors.append(
            f"expected {EXPECTED_CATEGORIES} <category> entries, got {len(categories)}"
        )
    seen_ids: set[str] = set()
    for cat in categories:
        cid = cat.get("id") or "<no-id>"
        for attr in REQUIRED_CATEGORY_ATTRS:
            if not cat.get(attr):
                errors.append(f"category {cid!r} missing attr: {attr}")
        if cid in seen_ids:
            errors.append(f"duplicate category id: {cid}")
        seen_ids.add(cid)
        for tag in REQUIRED_CHILD_TAGS:
            child = cat.find(tag)
            if child is None or not (child.text or "").strip():
                errors.append(f"category {cid!r} missing or empty <{tag}>")

    dt = root.find("decision-tree")
    if dt is None:
        errors.append("<decision-tree> element missing")
    else:
        steps = dt.findall("step")
        if len(steps) < EXPECTED_CATEGORIES:
            errors.append(
                f"<decision-tree> needs >= {EXPECTED_CATEGORIES} <step> entries, got {len(steps)}"
            )

    return errors


def main() -> int:
    args = sys.argv[1:]
    path = Path(args[0]) if args else DEFAULT_PATH
    errors = validate(path)
    if errors:
        sys.stdout.write(f"FAIL {path}\n")
        for e in errors:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write(f"PASS {path}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
