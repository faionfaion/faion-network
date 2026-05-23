#!/usr/bin/env python3
"""validate-ai-leverage-estimation-model.py

Validate a leverage-adjusted estimate against the schema declared in
content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to estimate JSON
    --self-test       run built-in fixtures (no external file required)
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_CLASSES = {"glue", "scaffold", "tests", "business-logic", "regulated", "novel"}
BAND_VERSION_RE = re.compile(r"^[0-9]{4}-Q[1-4]$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]

    for k in ("engagement_id", "band_version", "tasks", "totals"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    if not isinstance(obj["engagement_id"], str) or not obj["engagement_id"]:
        errs.append("engagement_id must be non-empty string")
    if not BAND_VERSION_RE.match(str(obj["band_version"])):
        errs.append(f"band_version must match YYYY-Qn, got {obj['band_version']!r}")
    if not isinstance(obj["tasks"], list):
        errs.append("tasks must be array")
        return errs

    fallback = obj.get("fallback_reason")
    if fallback and obj["tasks"]:
        errs.append("fallback_reason set AND tasks non-empty (skip path is exclusive)")
    if not fallback and not obj["tasks"]:
        errs.append("tasks must be non-empty unless fallback_reason set")

    for i, t in enumerate(obj["tasks"]):
        prefix = f"tasks[{i}]"
        if not isinstance(t, dict):
            errs.append(f"{prefix} must be object"); continue
        for k in ("leaf_id", "task_class", "raw_hours", "multiplier_band",
                  "evidence_rows", "adjusted_hours"):
            if k not in t:
                errs.append(f"{prefix}.{k} missing")
        if t.get("task_class") not in ALLOWED_CLASSES:
            errs.append(f"{prefix}.task_class invalid: {t.get('task_class')!r}")
        band = t.get("multiplier_band") or {}
        for c in ("low", "mid", "high"):
            v = band.get(c)
            if not isinstance(v, (int, float)) or v < 1.0 or v > 8.0:
                errs.append(f"{prefix}.multiplier_band.{c} must be number 1.0..8.0")
        if isinstance(band.get("mid"), (int, float)) and band["mid"] > 5.0:
            errs.append(f"{prefix}.multiplier_band.mid > 5.0 (vanity reject)")
        if t.get("task_class") == "novel" and isinstance(band.get("mid"), (int, float)) and band["mid"] > 1.2:
            errs.append(f"{prefix} novel class with mid > 1.2 (no AI track record)")
        ev = t.get("evidence_rows") or []
        if not isinstance(ev, list) or not ev:
            errs.append(f"{prefix}.evidence_rows must be non-empty list")
    return errs


GOOD = {
    "engagement_id": "acme-2026-Q2",
    "band_version": "2026-Q2",
    "tasks": [{
        "leaf_id": "wbs-1",
        "task_class": "glue",
        "raw_hours": 6.0,
        "multiplier_band": {"low": 2.0, "mid": 3.0, "high": 4.0},
        "evidence_rows": [{"log_task_id": "t1", "date": "2026-03-01",
                           "planned_hours": 8, "actual_hours": 2.5}],
        "adjusted_hours": {"low": 3.0, "mid": 2.0, "high": 1.5},
    }],
    "totals": {"mid_hours": 2.0, "low_hours": 1.5, "high_hours": 3.0},
}
BAD = {"engagement_id": "x", "band_version": "Q2-2026", "tasks": [
    {"leaf_id": "wbs-1", "task_class": "fast", "raw_hours": 8,
     "multiplier_band": {"mid": 5.0}}
], "totals": {}}


def self_test() -> int:
    if validate(GOOD):
        sys.stderr.write("good case rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad case accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="estimate JSON path")
    ap.add_argument("--self-test", action="store_true",
                    help="run built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n"); return 2

    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
