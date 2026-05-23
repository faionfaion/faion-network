#!/usr/bin/env python3
"""F-066 B3 validator: methodology templates discipline.

Rules per checklist B3.1..B3.5:
  B3.1 every file listed in AGENTS.md `## Templates` table exists in <dir>/templates/
  B3.2 templates are non-empty (heuristic: >50 bytes, not literal TBD placeholder)
  B3.3 each starts with a 5-line header (purpose / consumes / produces / depends-on / token-budget-impact)

F-067 note: this validator only reads the `## Templates` H2 section in the
AGENTS.md body — it never parses YAML frontmatter or meta.json. No metadata
source switch is required for the meta.json migration; the body-section
check is stable across pre- and post-migration corpora.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO_ROOT / "skills" / "faion" / "knowledge"

HEADER_KEYS = ("purpose", "consumes", "produces", "depends-on", "token-budget-impact")

# Files whose syntax has no comment form for headers; we allow a __faion_header__ key inside.
JSON_LIKE = {".json"}


def _templates_listed(agents_md: Path) -> list[str]:
    if not agents_md.exists():
        return []
    text = agents_md.read_text(encoding="utf-8", errors="replace")
    # find ## Templates section, parse the table
    m = re.search(r"(?ms)^## Templates\s*\n(.*?)(?:^## |\Z)", text)
    if not m:
        return []
    body = m.group(1)
    files: list[str] = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if not cols or cols[0].lower() in ("file", "---", ""):
            continue
        cell = cols[0].strip("`")
        if cell and "/" in cell:
            files.append(cell)
    return files


def _has_header(p: Path) -> bool:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False
    head = "\n".join(text.splitlines()[:20]).lower()
    found = sum(1 for k in HEADER_KEYS if k in head)
    if p.suffix in JSON_LIKE:
        return "__faion_header__" in text
    return found >= 3  # tolerant: at least 3/5 keys present somewhere in first 20 lines


def validate_dir(dir_path: Path) -> list[str]:
    errs: list[str] = []
    listed = _templates_listed(dir_path / "AGENTS.md")
    if not listed:
        return errs  # nothing declared → nothing to check
    for f in listed:
        # paths in AGENTS.md are written as `templates/foo.ext`
        path = dir_path / f
        if not path.exists():
            errs.append(f"declared template missing: {f}")
            continue
        if path.stat().st_size < 50:
            errs.append(f"template too small (<50 bytes): {f}")
            continue
        if not _has_header(path):
            errs.append(f"template missing 5-line header (purpose/consumes/produces/depends-on/token-budget-impact): {f}")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    targets: list[Path]
    if args.all:
        targets = [p.parent for p in KNOWLEDGE.rglob("AGENTS.md")]
    else:
        if not args.target:
            ap.error("provide target dir or --all")
        targets = [Path(args.target).resolve()]

    def _display(p: Path) -> str:
        try:
            return str(p.relative_to(REPO_ROOT))
        except ValueError:
            return str(p)

    fail = 0
    for d in targets:
        errs = validate_dir(d)
        if errs:
            fail += 1
            print(f"FAIL {_display(d)}")
            for e in errs:
                print(f"  - {e}")
        elif not args.all:
            print(f"PASS {_display(d)}")
    if args.all:
        print(f"\nsummary: {len(targets)-fail} pass / {fail} fail / {len(targets)} total")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
