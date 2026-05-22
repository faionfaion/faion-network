#!/usr/bin/env python3
"""Validate output contract for llm-classifier-design config.

USAGE:
    validate-llm-classifier-design.py <input.json>  Validate a classifier-config.json.
    validate-llm-classifier-design.py --self-test   Run built-in fixture.
    validate-llm-classifier-design.py --help        Show this help.

EXIT CODES:
    0 on pass
    1 on schema violation
    2 on usage error

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("model", "tool_name", "tool_choice", "system_prompt", "batch_size", "max_turns"):
        if k not in c:
            v.append(f"missing required field: {k}")
    if not c.get("tool_name"):
        v.append("tool_name must be non-empty (rule r2)")
    tc = c.get("tool_choice") or {}
    if tc.get("type") != "tool":
        v.append('tool_choice.type must be "tool" (forced; rule r2)')
    if tc.get("name") and c.get("tool_name") and tc["name"] != c["tool_name"]:
        v.append("tool_choice.name must match tool_name")
    sp = c.get("system_prompt") or ""
    if len(sp) < 10:
        v.append("system_prompt must be >=10 chars; replaces SDK preset (rule r3)")
    if "setting_sources" in c and c["setting_sources"] != []:
        v.append("setting_sources must be empty list (rule r3)")
    at = c.get("allowed_tools")
    if isinstance(at, list) and len(at) != 1:
        v.append("allowed_tools must contain exactly one entry (rule r3)")
    bs = c.get("batch_size")
    if isinstance(bs, int) and (bs < 1 or bs > 15):
        v.append("batch_size must be 1..15 (rule r5)")
    mt = c.get("max_turns")
    if isinstance(mt, int) and mt < 2:
        v.append("max_turns must be >=2 (rule r4)")
    return v


def _self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text())
    smoke_clean = {k: v for k, v in smoke.items() if not k.startswith("_")}
    assert validate(smoke_clean) == [], f"smoke must pass: {validate(smoke_clean)}"
    bad = dict(smoke_clean)
    bad["batch_size"] = 30
    assert any("batch_size" in x for x in validate(bad)), "should reject batch_size 30"
    bad = dict(smoke_clean)
    bad["max_turns"] = 1
    assert any("max_turns" in x for x in validate(bad)), "should reject max_turns 1"
    bad = dict(smoke_clean)
    bad["tool_choice"] = {"type": "auto"}
    assert any("tool_choice" in x for x in validate(bad)), "should require forced tool"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-llm-classifier-design.py")
    p.add_argument("path", nargs="?", help="JSON config to validate")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    raw = json.loads(Path(args.path).read_text())
    clean = {k: v for k, v in raw.items() if not k.startswith("_")}
    out = validate(clean)
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
