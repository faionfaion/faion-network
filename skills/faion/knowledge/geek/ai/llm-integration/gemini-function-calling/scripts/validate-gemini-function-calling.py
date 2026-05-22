#!/usr/bin/env python3
"""validate-gemini-function-calling.py — validate a gemini-fc-config.json.

Usage:
    validate-gemini-function-calling.py --config <path>
    validate-gemini-function-calling.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(c: dict) -> list[dict]:
    v: list[dict] = []
    if c.get("mode") not in {"automatic", "manual"}:
        v.append({"rule": "r3", "field": "mode", "msg": "must be automatic or manual"})
    tools = c.get("tools") or []
    if len(tools) > 20:
        v.append({"rule": "r5", "field": "tools", "msg": f">20 tools ({len(tools)})"})
    for i, t in enumerate(tools):
        if not t.get("name"):
            v.append({"rule": "r1", "field": f"tools[{i}].name", "msg": "missing"})
        if len(t.get("description", "")) < 30:
            v.append({"rule": "r1", "field": f"tools[{i}].description", "msg": "<30 chars"})
    return v


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate(smoke) == [], f"smoke must pass: {validate(smoke)}"
    bad = dict(smoke); bad["mode"] = "auto"
    assert any(x["rule"] == "r3" for x in validate(bad))
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.config:
        ap.error("--config required")
        return 2
    data = json.loads(args.config.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
