#!/usr/bin/env python3
"""validate-claude-tool-use.py — validate one or more Claude tool definitions.

Usage:
    validate-claude-tool-use.py --tools <path-to-json-or-jsonl>
    validate-claude-tool-use.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")


def depth(obj, d=1) -> int:
    if not isinstance(obj, dict):
        return d
    props = obj.get("properties") or {}
    deepest = d
    for v in props.values():
        if isinstance(v, dict) and v.get("type") == "object":
            deepest = max(deepest, depth(v, d + 1))
    return deepest


def validate_one(t: dict, idx: int) -> list[dict]:
    v: list[dict] = []
    for k in ["name", "description", "input_schema"]:
        if k not in t:
            v.append({"rule": "schema", "field": f"tools[{idx}].{k}", "msg": "missing"})
    if v:
        return v
    if not NAME_RE.fullmatch(t["name"]):
        v.append({"rule": "r1", "field": f"tools[{idx}].name", "msg": "name must match identifier regex"})
    if len(t["description"]) < 30:
        v.append({"rule": "r1", "field": f"tools[{idx}].description", "msg": "description must be >=30 chars"})
    s = t.get("input_schema") or {}
    if s.get("type") != "object":
        v.append({"rule": "schema", "field": f"tools[{idx}].input_schema.type", "msg": "must be object"})
    if depth(s) > 2:
        v.append({"rule": "r1", "field": f"tools[{idx}].input_schema", "msg": "nesting depth >2"})
    if s.get("additionalProperties") is False:
        v.append({"rule": "ap-05", "field": f"tools[{idx}].input_schema.additionalProperties", "msg": "avoid additionalProperties=false unless strict mode needed"})
    return v


def validate(tools: list[dict]) -> list[dict]:
    out: list[dict] = []
    for i, t in enumerate(tools):
        out.extend(validate_one(t, i))
    return out


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate([smoke]) == [], f"smoke must pass: {validate([smoke])}"
    bad = dict(smoke); bad["description"] = "short"
    assert any(x["rule"] == "r1" for x in validate([bad]))
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tools", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.tools:
        ap.error("--tools required")
        return 2
    raw = args.tools.read_text(encoding="utf-8").strip()
    if raw.startswith("["):
        tools = json.loads(raw)
    else:
        tools = [json.loads(raw)] if raw.startswith("{") and "\n" not in raw else [json.loads(line) for line in raw.splitlines() if line.strip()]
    v = validate(tools)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
