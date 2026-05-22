#!/usr/bin/env python3
"""validate-ai-option-cost-grid-template — verify grid JSON.

Inputs: argv[1] = path to grid JSON.
Flags: --help, --self-test.
Exit: 0 pass, 1 fail, 2 cli misuse.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TBD_RE = re.compile(r"\bTBD\b|lorem ipsum|<fill>", re.IGNORECASE)
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
HEX_RE = re.compile(r"^[a-f0-9]{16,64}$")


def validate(grid: dict) -> list[str]:
    errors: list[str] = []
    for key in ("template_version", "decision_owner", "eval_set_hash", "rows", "recommendation", "last_reviewed"):
        if key not in grid:
            errors.append(f"missing {key}")
    if "template_version" in grid and not SEMVER_RE.match(str(grid["template_version"])):
        errors.append("template_version not semver")
    if "eval_set_hash" in grid and not HEX_RE.match(str(grid["eval_set_hash"])):
        errors.append("eval_set_hash not hex 16..64")
    rows = grid.get("rows") or []
    if len(rows) < 2:
        errors.append("rows must have >=2 entries")
    rec = grid.get("recommendation") or ""
    if len(rec) < 20:
        errors.append("recommendation < 20 chars")
    body_text = json.dumps(grid, ensure_ascii=False)
    if TBD_RE.search(body_text):
        errors.append("TBD/placeholder text present")
    return errors


def _self_test() -> int:
    good = {"template_version": "1.0.0", "decision_owner": "founder:r",
            "eval_set_hash": "a" * 16, "rows": [{"x": 1}, {"x": 2}],
            "recommendation": "Ship the RAG option immediately",
            "last_reviewed": "2026-05-22"}
    if validate(good):
        return 1
    bad = {**good, "rows": [{"x": "TBD"}]}
    if not validate(bad):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) != 2:
        sys.stderr.write("usage: validate-ai-option-cost-grid-template.py <grid.json>\n")
        return 2
    grid = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    errors = validate(grid)
    if errors:
        for e in errors:
            sys.stderr.write(f"ERROR: {e}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
