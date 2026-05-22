#!/usr/bin/env python3
"""validate-files-reference.py — validate a routing candidates report.

Usage:
    validate-files-reference.py --report report.json [--root /path/to/workspace]
    validate-files-reference.py --self-test

Inputs:
    --report PATH  JSON file matching the output contract
    --root PATH    workspace root for resolving candidate_path (default: cwd)
Outputs: stdout JSON {ok, violations}
Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def validate(report: dict, root: Path) -> list[dict]:
    v: list[dict] = []
    if "task" not in report:
        v.append({"rule": "schema", "message": "missing task"})
    section = report.get("section", "")
    if not section or section == "all":
        v.append({"rule": "r1", "message": "section must be a single named section, not 'all'"})
    candidates = report.get("candidates", [])
    if len(candidates) > 2:
        v.append({"rule": "r2", "message": f"candidates count {len(candidates)} > 2"})
    for c in candidates:
        slug = c.get("slug", "")
        if not SLUG_RE.match(slug):
            v.append({"rule": "r2", "message": f"bad slug: {slug!r}"})
        path = c.get("candidate_path", "")
        if not path:
            v.append({"rule": "schema", "message": f"missing candidate_path for {slug}"})
            continue
        resolved = c.get("resolved", False)
        actually = (root / path).exists()
        if resolved and not actually:
            v.append({"rule": "r3", "message": f"resolved=true but {path} does not exist"})
        if not resolved and actually:
            v.append({"rule": "r3", "message": f"{path} exists but resolved=false (should re-resolve)"})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "skills/faion/knowledge/free/dev/software-developer/python").mkdir(parents=True)
        (root / "skills/faion/knowledge/free/dev/software-developer/python/AGENTS.md").touch()
        good = {
            "task": "pytest fixture",
            "section": "python",
            "candidates": [{
                "slug": "python",
                "candidate_path": "skills/faion/knowledge/free/dev/software-developer/python/AGENTS.md",
                "confidence": "high",
                "resolved": True,
            }],
        }
        assert not validate(good, root), "good case must pass"
        bad = {"task": "x", "section": "all", "candidates": [
            {"slug": "1bad", "candidate_path": "missing", "confidence": "high", "resolved": True}
        ] * 3}
        violations = validate(bad, root)
        rules = {x["rule"] for x in violations}
        assert "r1" in rules and "r2" in rules and "r3" in rules
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", type=Path)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.report:
        ap.error("--report required")
        return 2
    report = json.loads(args.report.read_text(encoding="utf-8"))
    violations = validate(report, args.root)
    sys.stdout.write(json.dumps({"ok": not violations, "violations": violations}, indent=2) + "\n")
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
