#!/usr/bin/env python3
"""validate-ai-failure-mode-taxonomy.py — validate taxonomy.json.

Usage:
    validate-ai-failure-mode-taxonomy.py --taxonomy <path>
    validate-ai-failure-mode-taxonomy.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^fm\.[a-z0-9-]+(\.[a-z0-9-]+)+$")
SEM_RE = re.compile(r"^\d+\.\d+\.\d+$")
SEVERITIES = {"low", "medium", "high", "critical"}


def validate(tx: dict) -> list[dict]:
    v: list[dict] = []
    for k in ["version", "owner", "modes"]:
        if k not in tx:
            v.append({"rule": "schema", "field": k, "msg": "missing"})
    if v:
        return v
    if not SEM_RE.fullmatch(tx["version"]):
        v.append({"rule": "r3", "field": "version", "msg": "must be semver"})
    if tx["owner"].strip().lower() in {"team", "us", "tbd", "n/a"}:
        v.append({"rule": "r5", "field": "owner", "msg": "owner must be named"})
    modes = tx.get("modes") or []
    if len(modes) != 12:
        v.append({"rule": "r1", "field": "modes", "msg": f"must be exactly 12, got {len(modes)}"})
    ids = set()
    for i, m in enumerate(modes):
        for k in ["id", "name", "definition", "detector", "severity", "linked_methodology"]:
            if not m.get(k):
                v.append({"rule": "r2", "field": f"modes[{i}].{k}", "msg": "missing"})
        if not ID_RE.fullmatch(m.get("id", "")):
            v.append({"rule": "r4", "field": f"modes[{i}].id", "msg": "id must match fm.x.y pattern"})
        if m.get("id") in ids:
            v.append({"rule": "r4", "field": f"modes[{i}].id", "msg": f"duplicate id {m['id']}"})
        ids.add(m.get("id"))
        if m.get("severity") not in SEVERITIES:
            v.append({"rule": "r2", "field": f"modes[{i}].severity", "msg": "severity out of enum"})
    return v


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate(smoke) == [], f"smoke must pass: {validate(smoke)}"
    bad = dict(smoke); bad["modes"] = smoke["modes"][:5]
    assert any(x["rule"] == "r1" for x in validate(bad))
    bad2 = dict(smoke); bad2["version"] = "v1"
    assert any(x["rule"] == "r3" for x in validate(bad2))
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--taxonomy", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.taxonomy:
        ap.error("--taxonomy required")
        return 2
    data = json.loads(args.taxonomy.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
