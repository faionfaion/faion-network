#!/usr/bin/env python3
"""validate-claude-api-integration.py — validate output JSON against the methodology contract.

Inputs:
  - path to a JSON file produced by the methodology

Outputs:
  - stdout: human-readable violation list (empty on pass)
  - exit 0 on pass, 1 on schema violations, 2 on usage error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["surfaces_wired", "default_model", "stop_reason_centralised", "retry_installed", "forbidden_seen"]
KNOWN_SURFACES = {
    "completion_sync", "completion_async", "streaming", "tool_use",
    "vision", "extended_thinking", "prompt_caching", "batch_api",
}
MODEL_ID_RE = re.compile(r"^claude-[a-z0-9-]+-\d{8}$")


def validate(doc: dict) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing required field: {k}")
    surfaces = doc.get("surfaces_wired")
    if not isinstance(surfaces, list) or not all(s in KNOWN_SURFACES for s in surfaces):
        errs.append("surfaces_wired must be a list with values from the allowed surface set")
    if not MODEL_ID_RE.match(doc.get("default_model", "")):
        errs.append("default_model must include full-date suffix — f1 forbidden")
    if not doc.get("stop_reason_centralised"):
        errs.append("stop_reason_centralised must be true — f2 forbidden")
    if not doc.get("retry_installed"):
        errs.append("retry_installed must be true — f3 forbidden")
    pc = doc.get("prompt_caching")
    if pc is not None and pc.get("cached_prefix_tokens", 0) < 1024:
        errs.append("prompt_caching.cached_prefix_tokens must be >= 1024 — f4 forbidden")
    et = doc.get("extended_thinking")
    if et is not None and "temperature" in et:
        errs.append("extended_thinking.temperature must not be present — f5 forbidden")
    fs = doc.get("forbidden_seen")
    if not isinstance(fs, list):
        errs.append("forbidden_seen must be an array")
    elif fs:
        errs.append(f"forbidden_seen non-empty: {fs}")
    return errs


SMOKE = {
    "surfaces_wired": ["completion_sync", "prompt_caching", "streaming", "tool_use"],
    "default_model": "claude-sonnet-4-20250514",
    "stop_reason_centralised": True,
    "retry_installed": True,
    "prompt_caching": {"cached_prefix_tokens": 3200, "hit_ratio_target": 0.75},
    "forbidden_seen": [],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate claude-api-integration output JSON.")
    parser.add_argument("path", nargs="?", help="Path to JSON output to validate.")
    parser.add_argument("--self-test", action="store_true", help="Run an in-process smoke test.")
    args = parser.parse_args()

    if args.self_test:
        errs = validate(SMOKE)
        if errs:
            sys.stderr.write(f"self-test failed: {errs}\n")
            return 1
        sys.stdout.write("self-test ok\n")
        return 0

    if not args.path:
        parser.print_help()
        return 2

    p = Path(args.path)
    if not p.exists():
        sys.stderr.write(f"file not found: {p}\n")
        return 2

    try:
        doc = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError) as e:
        sys.stderr.write(f"json parse error: {e}\n")
        return 1

    errs = validate(doc)
    if errs:
        for e in errs:
            sys.stdout.write(e + "\n")
        return 1
    sys.stdout.write("ok\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
