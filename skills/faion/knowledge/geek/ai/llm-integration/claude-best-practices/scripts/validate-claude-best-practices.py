#!/usr/bin/env python3
"""validate-claude-best-practices.py — validate output JSON against the methodology contract.

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

REQUIRED = ["model_tier_table", "fallback_logging", "shared_rate_bucket", "cache_layout", "retry_after_parsing", "forbidden_seen"]
MODEL_ID_RE = re.compile(r"^claude-[a-z0-9-]+-\d{8}$")
TIERS = ("routing", "generation", "reasoning")


def validate(doc: dict) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing required field: {k}")
    tier_table = doc.get("model_tier_table", {})
    for tier in TIERS:
        mid = tier_table.get(tier, "")
        if not MODEL_ID_RE.match(mid):
            errs.append(f"model_tier_table.{tier} must be pinned with full-date suffix — f1 forbidden")
    if not doc.get("fallback_logging"):
        errs.append("fallback_logging must be true — f2 forbidden")
    if not doc.get("shared_rate_bucket"):
        errs.append("shared_rate_bucket must be true — f3 forbidden")
    cl = doc.get("cache_layout", {})
    if cl.get("cached_prefix_tokens", 0) < 1024:
        errs.append("cache_layout.cached_prefix_tokens must be >= 1024 — f4 forbidden")
    if not doc.get("retry_after_parsing"):
        errs.append("retry_after_parsing must be true — f5 forbidden")
    fs = doc.get("forbidden_seen")
    if not isinstance(fs, list):
        errs.append("forbidden_seen must be an array")
    elif fs:
        errs.append(f"forbidden_seen non-empty: {fs}")
    return errs


SMOKE = {
    "model_tier_table": {
        "routing": "claude-3-5-haiku-20241022",
        "generation": "claude-sonnet-4-20250514",
        "reasoning": "claude-opus-4-5-20251101",
    },
    "fallback_logging": True,
    "shared_rate_bucket": True,
    "cache_layout": {"stable_prefix_first": True, "cached_prefix_tokens": 4200},
    "retry_after_parsing": True,
    "batch_api_enabled": True,
    "forbidden_seen": [],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate claude-best-practices output JSON.")
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
