#!/usr/bin/env python3
"""validate-web-scraping-agentic-workflow.py

Validate a scrape-run report JSON against the schema and rule consistency.

Inputs:
    --file PATH      path to report JSON
    --self-test      run built-in valid + invalid fixtures
    --help           this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^wsr-[a-z0-9-]{6,}$")
RUN_ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}\d{2}Z-[a-z0-9]+$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?$")

RENDER_TOOL = {
    "ssr": {"httpx-selectolax"},
    "js":  {"playwright"},
    "managed": {"firecrawl", "jina-reader"},
}
VERDICTS = {"promote", "block-validation-low", "block-drift-high", "block-tool-mismatch", "block-robots-disallow"}
VALIDATION_GATE = 0.9
DRIFT_GATE = 5.0


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "source", "run_id", "render_mode", "tool", "rows_seen", "rows_valid", "drift_score", "robots_check", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^wsr-[a-z0-9-]{6,}$")
    if "run_id" in obj and not RUN_ID_RE.match(str(obj["run_id"])):
        errs.append("run_id must match ^YYYY-MM-DDTHHMMZ-[a-z0-9]+$")

    rm = obj.get("render_mode")
    tl = obj.get("tool")
    if rm not in RENDER_TOOL:
        errs.append(f"render_mode must be one of {sorted(RENDER_TOOL)}")
    elif tl not in RENDER_TOOL[rm]:
        errs.append(f"tool '{tl}' does not match render_mode '{rm}' (allowed: {sorted(RENDER_TOOL[rm])})")

    rs = obj.get("rows_seen", 0)
    rv = obj.get("rows_valid", 0)
    for k, v in (("rows_seen", rs), ("rows_valid", rv)):
        if not isinstance(v, int) or v < 0:
            errs.append(f"{k} must be non-negative integer")
    if isinstance(rs, int) and isinstance(rv, int) and rv > rs:
        errs.append("rows_valid must be <= rows_seen")

    ds = obj.get("drift_score")
    if not isinstance(ds, (int, float)) or not (0 <= ds <= 100):
        errs.append("drift_score must be number in [0,100]")

    rc = obj.get("robots_check") or {}
    if not isinstance(rc, dict):
        errs.append("robots_check must be an object")
    else:
        if "fetched_at" not in rc or not DT_RE.match(str(rc.get("fetched_at", ""))):
            errs.append("robots_check.fetched_at must be ISO 8601 date-time")
        if "allowed" not in rc or not isinstance(rc["allowed"], bool):
            errs.append("robots_check.allowed must be boolean")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")

    # Verdict consistency.
    if verdict == "promote":
        if isinstance(rc, dict) and rc.get("allowed") is False:
            errs.append("verdict=promote forbidden when robots_check.allowed=false")
        if isinstance(rs, int) and rs > 0 and rv / rs < VALIDATION_GATE:
            errs.append(f"verdict=promote requires rows_valid/rows_seen >= {VALIDATION_GATE}")
        if isinstance(ds, (int, float)) and ds > DRIFT_GATE:
            errs.append(f"verdict=promote requires drift_score <= {DRIFT_GATE}")
        if rm in RENDER_TOOL and tl not in RENDER_TOOL[rm]:
            errs.append("verdict=promote requires tool to match render_mode")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "wsr-news-2026-05-23",
    "source": "example.com/news",
    "run_id": "2026-05-23T0900Z-a1b2c3",
    "render_mode": "ssr",
    "tool": "httpx-selectolax",
    "rows_seen": 124,
    "rows_valid": 122,
    "drift_score": 0.0,
    "robots_check": {"fetched_at": "2026-05-23T08:59:50Z", "allowed": True},
    "raw_path": "raw/2026-05-23/example-news.jsonl",
    "user_agent": "faion-network/1.0 (+mailto:ruslan@faion.net)",
    "verdict": "promote",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "news",
    "source": "example.com/news",
    "run_id": "now",
    "render_mode": "ssr",
    "tool": "playwright",
    "rows_seen": 10,
    "rows_valid": 4,
    "drift_score": 12,
    "robots_check": {"allowed": False},
    "verdict": "promote",
    "version": "1.0",
    "last_reviewed": "soon",
}


def self_test() -> int:
    errs = validate(VALID_FIXTURE)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid fixture rejected: {errs}\n")
        return 1
    errs = validate(INVALID_FIXTURE)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to report JSON")
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
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
