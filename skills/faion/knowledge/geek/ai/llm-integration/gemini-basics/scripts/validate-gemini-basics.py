#!/usr/bin/env python3
"""validate-gemini-basics.py — validate a starter gemini-config-basic.json.

Usage:
    validate-gemini-basics.py --config <path>
    validate-gemini-basics.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(c: dict) -> list[dict]:
    v: list[dict] = []
    if not c.get("model", "").startswith("gemini-"):
        v.append({"rule": "r1", "field": "model", "msg": "model must start with gemini-"})
    if c.get("model") == "gemini-pro" or c.get("model") == "gemini-flash":
        v.append({"rule": "r1", "field": "model", "msg": "model alias not allowed; pin a version"})
    t = c.get("temperature")
    if t is None or not (0 <= t <= 2):
        v.append({"rule": "r1", "field": "temperature", "msg": "temperature must be in [0, 2]"})
    m = c.get("max_output_tokens", 0)
    if not (1 <= m <= 65536):
        v.append({"rule": "r5", "field": "max_output_tokens", "msg": "must be in [1, 65536]"})
    if c.get("response_mime_type") and c["response_mime_type"] not in {"text/plain", "application/json"}:
        v.append({"rule": "r4", "field": "response_mime_type", "msg": "must be text/plain or application/json"})
    return v


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate(smoke) == [], f"smoke must pass: {validate(smoke)}"
    bad = dict(smoke); bad["model"] = "gemini-pro"
    assert any(x["rule"] == "r1" for x in validate(bad))
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
