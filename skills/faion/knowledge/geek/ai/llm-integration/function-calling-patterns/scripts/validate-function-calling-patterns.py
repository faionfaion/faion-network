#!/usr/bin/env python3
"""validate-function-calling-patterns.py — validate tool-registry entries.

Usage:
    validate-function-calling-patterns.py --registry <path-to-json-or-jsonl>
    validate-function-calling-patterns.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")
SEM_RE = re.compile(r"^\d+\.\d+\.\d+$")


def validate_one(t: dict, i: int) -> list[dict]:
    v: list[dict] = []
    for k in ["name", "version", "description", "schema_id", "input_schema", "category"]:
        if not t.get(k):
            v.append({"rule": "r7", "field": f"tools[{i}].{k}", "msg": "missing"})
    if v:
        return v
    if not NAME_RE.fullmatch(t["name"]):
        v.append({"rule": "r1", "field": f"tools[{i}].name", "msg": "invalid identifier"})
    if not SEM_RE.fullmatch(t["version"]):
        v.append({"rule": "r7", "field": f"tools[{i}].version", "msg": "not semver"})
    if len(t["description"]) < 30:
        v.append({"rule": "r1", "field": f"tools[{i}].description", "msg": "<30 chars"})
    return v


def validate(tools: list[dict]) -> list[dict]:
    out: list[dict] = []
    for i, t in enumerate(tools):
        out.extend(validate_one(t, i))
    if len(tools) > 20:
        out.append({"rule": "r1", "field": "registry", "msg": f">20 tools without routing ({len(tools)})"})
    return out


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate([smoke]) == [], f"smoke must pass: {validate([smoke])}"
    bad = dict(smoke); bad["version"] = "v1"
    assert any(x["rule"] == "r7" for x in validate([bad]))
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registry", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.registry:
        ap.error("--registry required")
        return 2
    raw = args.registry.read_text(encoding="utf-8").strip()
    if raw.startswith("["):
        tools = json.loads(raw)
    else:
        tools = [json.loads(raw)] if "\n" not in raw else [json.loads(line) for line in raw.splitlines() if line.strip()]
    v = validate(tools)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
