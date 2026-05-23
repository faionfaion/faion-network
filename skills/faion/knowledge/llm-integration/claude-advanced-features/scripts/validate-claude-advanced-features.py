#!/usr/bin/env python3
"""validate-claude-advanced-features.py — validate output JSON against the methodology output contract.

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

REQUIRED = ["features_enabled", "model_id", "cache_hit_ratio", "forbidden_seen"]
KNOWN_FEATURES = {"extended_thinking", "prompt_caching", "batch_api", "computer_use"}
MODEL_ID_RE = re.compile(r"^claude-[a-z0-9-]+-\d{8}$")


def validate(doc: dict) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing required field: {k}")
    feats = doc.get("features_enabled")
    if not isinstance(feats, list) or not all(f in KNOWN_FEATURES for f in feats):
        errs.append("features_enabled must be a subset of {extended_thinking, prompt_caching, batch_api, computer_use}")
    mid = doc.get("model_id", "")
    if not MODEL_ID_RE.match(mid):
        errs.append(f"model_id must include full-date suffix (got: {mid!r}) — f1 forbidden")
    if "extended_thinking" in doc:
        et = doc["extended_thinking"]
        if "temperature" in et:
            errs.append("extended_thinking.temperature must not be present — f2 forbidden")
        if et.get("max_tokens", 0) < et.get("budget_tokens", 0) + 4096:
            errs.append("extended_thinking.max_tokens must be >= budget_tokens + 4096")
    if "prompt_caching" in doc:
        pc = doc["prompt_caching"]
        if pc.get("cached_prefix_tokens", 0) < 1024:
            errs.append("prompt_caching.cached_prefix_tokens must be >= 1024 — f3 forbidden")
    if "batch_api" in doc:
        ba = doc["batch_api"]
        if ba.get("poll_interval_seconds", 0) < 60:
            errs.append("batch_api.poll_interval_seconds must be >= 60 — f4 forbidden")
    if "computer_use" in doc:
        cu = doc["computer_use"]
        if "sandbox_kind" not in cu:
            errs.append("computer_use must declare sandbox_kind — f5 forbidden")
    fs = doc.get("forbidden_seen", None)
    if not isinstance(fs, list):
        errs.append("forbidden_seen must be an array")
    elif fs:
        errs.append(f"forbidden_seen non-empty: {fs}")
    return errs


SMOKE = {
    "features_enabled": ["extended_thinking", "prompt_caching"],
    "model_id": "claude-opus-4-5-20251101",
    "extended_thinking": {"budget_tokens": 5000, "max_tokens": 9096},
    "prompt_caching": {"cached_prefix_tokens": 4200, "hit_ratio_target": 0.75},
    "cache_hit_ratio": 0.82,
    "forbidden_seen": [],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate claude-advanced-features output JSON.")
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
