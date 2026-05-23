#!/usr/bin/env python3
"""validate-faion-cli-as-agent-skill.py — validate a faion-agent bundle JSON.

Usage:
    validate-faion-cli-as-agent-skill.py --bundle file.json
    validate-faion-cli-as-agent-skill.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(d: dict) -> list[dict]:
    v: list[dict] = []
    for k in ("provider", "tools", "system_prompt", "dispatcher", "budget"):
        if k not in d:
            v.append({"rule": "schema", "message": f"missing: {k}"})
    if v:
        return v
    if d["provider"] not in ("anthropic", "openai", "langgraph"):
        v.append({"rule": "schema", "message": f"bad provider: {d['provider']}"})
    b = d["budget"]
    if not (1 <= b.get("max_calls_per_turn", 0) <= 10):
        v.append({"rule": "rule:r1", "message": f"max_calls_per_turn out of range: {b.get('max_calls_per_turn')}"})
    if not (200 <= b.get("max_content_tokens", 0) <= 8000):
        v.append({"rule": "rule:r1", "message": f"max_content_tokens out of range: {b.get('max_content_tokens')}"})
    names = {t.get("name") for t in d["tools"]}
    if not {"faion_search", "faion_get_content"}.issubset(names):
        v.append({"rule": "rule:r2", "message": f"both tools required, got {names}"})
    sp = d["system_prompt"]
    if len(sp) < 100:
        v.append({"rule": "schema", "message": "system_prompt too short"})
    if "403" not in sp and "tier" not in sp.lower():
        v.append({"rule": "rule:r3", "message": "system_prompt does not address 403 tier path"})
    disp = d["dispatcher"]
    for k in ("cache", "pii_strip", "logging"):
        if disp.get(k) is not True:
            v.append({"rule": f"rule:{'r4' if k=='cache' else 'r5' if k=='pii_strip' else 'r6'}",
                      "message": f"dispatcher.{k} must be true"})
    return v


def self_test() -> int:
    good = {
        "provider": "anthropic",
        "budget": {"max_calls_per_turn": 3, "max_content_tokens": 2000},
        "tools": [
            {"name": "faion_search", "description": "x" * 30, "input_schema": {}},
            {"name": "faion_get_content", "description": "x" * 30, "input_schema": {}},
        ],
        "system_prompt": "x" * 110 + " 403 tier path",
        "dispatcher": {"cache": True, "pii_strip": True, "logging": True},
    }
    assert validate(good) == [], validate(good)
    bad = {
        "provider": "anthropic",
        "budget": {"max_calls_per_turn": 50, "max_content_tokens": 200000},
        "tools": [{"name": "faion_search", "description": "x", "input_schema": {}}],
        "system_prompt": "short",
        "dispatcher": {"cache": False, "pii_strip": False, "logging": False},
    }
    out = validate(bad)
    assert any(x["rule"] == "rule:r1" for x in out), out
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bundle", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.bundle:
        ap.error("--bundle required")
        return 2
    out = validate(json.loads(args.bundle.read_text(encoding="utf-8")))
    sys.stdout.write(json.dumps({"ok": not out, "violations": out}, indent=2) + "\n")
    return 0 if not out else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
