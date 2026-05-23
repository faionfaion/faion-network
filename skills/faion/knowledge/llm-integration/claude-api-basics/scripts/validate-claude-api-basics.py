#!/usr/bin/env python3
"""validate-claude-api-basics.py — validate output JSON against the methodology contract.

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

REQUIRED = ["auth_source", "model_id", "retry_policy", "cost_tracker_installed", "request_id_logged", "forbidden_seen"]
MODEL_ID_RE = re.compile(r"^claude-[a-z0-9-]+-\d{8}$")
EXPECTED_RETRY_CODES = {"429", "500", "502", "503", "529"}


def validate(doc: dict) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing required field: {k}")
    if doc.get("auth_source") != "env":
        errs.append("auth_source must be 'env' — f1 forbidden")
    if not MODEL_ID_RE.match(doc.get("model_id", "")):
        errs.append("model_id must include full-date suffix — f2 forbidden")
    rp = doc.get("retry_policy", {})
    retry_on = set(rp.get("retry_on", []))
    if "529" not in retry_on:
        errs.append("retry_policy.retry_on must include 529 — f3 forbidden")
    if not doc.get("cost_tracker_installed"):
        errs.append("cost_tracker_installed must be true — f4 forbidden")
    if not doc.get("request_id_logged"):
        errs.append("request_id_logged must be true — f5 forbidden")
    fs = doc.get("forbidden_seen", None)
    if not isinstance(fs, list):
        errs.append("forbidden_seen must be an array")
    elif fs:
        errs.append(f"forbidden_seen non-empty: {fs}")
    return errs


SMOKE = {
    "auth_source": "env",
    "model_id": "claude-sonnet-4-20250514",
    "retry_policy": {"retry_on": ["429", "500", "502", "503", "529"], "max_attempts": 5},
    "cost_tracker_installed": True,
    "request_id_logged": True,
    "forbidden_seen": [],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate claude-api-basics output JSON.")
    parser.add_argument("path", nargs="?", help="Path to JSON output to validate.")
    parser.add_argument("--self-test", action="store_true", help="Run an in-process smoke test against a built-in fixture.")
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
