#!/usr/bin/env python3
"""validate-gemini-api-integration.py — validate a gemini-config.json.

Usage:
    validate-gemini-api-integration.py --config <path>
    validate-gemini-api-integration.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_CATEGORIES = {"HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"}
THRESHOLDS = {"BLOCK_NONE", "BLOCK_LOW_AND_ABOVE", "BLOCK_MEDIUM_AND_ABOVE", "BLOCK_ONLY_HIGH"}


def validate(c: dict) -> list[dict]:
    v: list[dict] = []
    if not c.get("model", "").startswith("gemini-"):
        v.append({"rule": "r1", "field": "model", "msg": "model must start with gemini-"})
    gc = c.get("generation_config") or {}
    if "temperature" not in gc or "max_output_tokens" not in gc:
        v.append({"rule": "r3", "field": "generation_config", "msg": "temperature + max_output_tokens required"})
    ss = c.get("safety_settings") or []
    cats = {s.get("category") for s in ss}
    missing = REQUIRED_CATEGORIES - cats
    if missing:
        v.append({"rule": "r4", "field": "safety_settings", "msg": f"missing categories {sorted(missing)}"})
    for i, s in enumerate(ss):
        if s.get("threshold") not in THRESHOLDS:
            v.append({"rule": "r4", "field": f"safety_settings[{i}].threshold", "msg": "invalid threshold"})
    return v


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate(smoke) == [], f"smoke must pass: {validate(smoke)}"
    bad = dict(smoke); bad["safety_settings"] = smoke["safety_settings"][:2]
    assert any(x["rule"] == "r4" for x in validate(bad))
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
