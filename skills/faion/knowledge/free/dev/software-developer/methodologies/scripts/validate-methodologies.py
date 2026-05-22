#!/usr/bin/env python3
"""validate-methodologies.py — validate dispatcher output (single slug, resolved).

Usage:
    validate-methodologies.py --report rep.json [--root /workspace]
    validate-methodologies.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def validate(rep: dict, root: Path) -> list[dict]:
    v: list[dict] = []
    if "task" not in rep:
        v.append({"rule": "schema", "message": "missing task"})
    cand = rep.get("candidate")
    if cand is None:
        if not rep.get("escalation"):
            v.append({"rule": "schema", "message": "candidate is null and escalation is missing"})
    else:
        if not SLUG.match(cand.get("slug", "")):
            v.append({"rule": "rule:r4", "message": f"bad slug: {cand.get('slug')!r}"})
        path = cand.get("path", "")
        resolved = cand.get("resolved", False)
        actually = (root / path).exists() if path else False
        if resolved and not actually:
            v.append({"rule": "rule:r2", "message": f"resolved=true but {path} does not exist"})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "skills/x").mkdir(parents=True)
        (root / "skills/x/AGENTS.md").touch()
        good = {"task": "t", "candidate": {"slug": "x", "path": "skills/x/AGENTS.md", "resolved": True}}
        assert not validate(good, root)
        bad = {"task": "t", "candidate": {"slug": "missing", "path": "skills/missing/AGENTS.md", "resolved": True}}
        v = validate(bad, root)
        assert any("rule:r2" in x["rule"] for x in v), f"should flag: {v}"
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
    rep = json.loads(args.report.read_text(encoding="utf-8"))
    v = validate(rep, args.root)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
