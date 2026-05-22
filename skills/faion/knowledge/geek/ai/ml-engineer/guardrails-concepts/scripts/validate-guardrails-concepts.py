#!/usr/bin/env python3
"""validate-guardrails-concepts.py — validate a guardrail-plan.json against the methodology schema.

Inputs:
    --file PATH    JSON file to validate
    --self-test    run built-in valid + invalid fixtures
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["artefact_id", "version", "last_reviewed", "pipeline_shape", "rails", "tiers", "frameworks"]
SHAPES = {"basic", "rag", "multi-agent"}
STAGES = {"input", "output", "dialog", "retrieval", "execution"}
ACTIONS = {"block", "filter", "transform", "warn", "log"}
FRAMEWORKS = {"nemo", "guardrails-ai", "llama-guard", "custom", "embedded"}
TIER_KINDS = {"regex", "classifier", "llm-judge"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("pipeline_shape") not in SHAPES:
        errs.append(f"pipeline_shape must be one of {sorted(SHAPES)}")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be YYYY-MM-DD")
    rails = obj.get("rails", [])
    if not isinstance(rails, list) or len(rails) < 2:
        errs.append("rails must be a list of >=2 entries")
    else:
        for i, r in enumerate(rails):
            if not isinstance(r, dict):
                errs.append(f"rails[{i}] must be object")
                continue
            if r.get("stage") not in STAGES:
                errs.append(f"rails[{i}].stage invalid")
            if r.get("action") not in ACTIONS:
                errs.append(f"rails[{i}].action invalid")
            if r.get("framework") not in FRAMEWORKS:
                errs.append(f"rails[{i}].framework invalid")
    tiers = obj.get("tiers", [])
    if not isinstance(tiers, list) or not tiers:
        errs.append("tiers must be a non-empty list")
    else:
        for i, t in enumerate(tiers):
            if not isinstance(t, dict):
                errs.append(f"tiers[{i}] must be object")
                continue
            if t.get("kind") not in TIER_KINDS:
                errs.append(f"tiers[{i}].kind invalid")
            if not isinstance(t.get("max_latency_ms"), int) or t["max_latency_ms"] < 1:
                errs.append(f"tiers[{i}].max_latency_ms must be positive int")
    return errs


VALID_FIX = {
    "artefact_id": "x",
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
    "pipeline_shape": "basic",
    "rails": [
        {"stage": "input", "rail_type": "len", "action": "block", "framework": "custom"},
        {"stage": "output", "rail_type": "schema", "action": "block", "framework": "guardrails-ai"},
    ],
    "tiers": [{"order": 1, "kind": "regex", "max_latency_ms": 5}],
    "frameworks": ["custom"],
}
INVALID_FIX: dict = {}


def self_test() -> int:
    if validate(VALID_FIX):
        sys.stderr.write("valid fixture rejected\n")
        return 1
    if not validate(INVALID_FIX):
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
