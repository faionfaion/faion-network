#!/usr/bin/env python3
"""validate-behavior-parity-verification.py

Validate a parity-report JSON against the behavior-parity-verification schema
and threshold rules (see content/02-output-contract.xml).

Inputs:
    --file PATH      path to parity-report JSON
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

ALLOWED_DISP = {"fixed", "accepted-with-justification", "open"}
ALLOWED_VERDICTS = {"promote", "freeze", "revert"}
ID_RE = re.compile(r"^bpv-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?$")
MIN_SAMPLES = 1000
DIFF_RATE_GATE = 0.5


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    required = [
        "artefact_id", "scope", "observable_fields", "ramp_stage",
        "window_start", "window_end", "total_compared", "diff_rate",
        "clusters", "version", "last_reviewed",
    ]
    for k in required:
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^bpv-[a-z0-9-]{6,}$")

    if "observable_fields" in obj:
        of = obj["observable_fields"]
        if not isinstance(of, list) or len(of) < 1:
            errs.append("observable_fields must be a non-empty list of strings")

    if "ramp_stage" in obj and obj["ramp_stage"] not in (1, 2, 3, 4):
        errs.append("ramp_stage must be one of 1, 2, 3, 4")

    for ts_key in ("window_start", "window_end"):
        if ts_key in obj and not DT_RE.match(str(obj[ts_key])):
            errs.append(f"{ts_key} must be ISO 8601 date-time (e.g. 2026-05-20T00:00:00Z)")

    if "total_compared" in obj:
        tc = obj["total_compared"]
        if not isinstance(tc, int) or tc < MIN_SAMPLES:
            errs.append(f"total_compared must be int >= {MIN_SAMPLES}")

    if "diff_rate" in obj:
        dr = obj["diff_rate"]
        if not isinstance(dr, (int, float)) or not (0 <= dr <= 100):
            errs.append("diff_rate must be number in [0,100]")

    clusters = obj.get("clusters", [])
    if not isinstance(clusters, list):
        errs.append("clusters must be a list")
    else:
        any_open = False
        for i, cl in enumerate(clusters):
            for k in ("cluster_id", "sample_count", "disposition"):
                if k not in cl:
                    errs.append(f"clusters[{i}] missing {k}")
            disp = cl.get("disposition")
            if disp and disp not in ALLOWED_DISP:
                errs.append(f"clusters[{i}].disposition must be one of {sorted(ALLOWED_DISP)}")
            if disp == "accepted-with-justification" and not cl.get("justification"):
                errs.append(f"clusters[{i}] accepted-with-justification requires non-empty justification")
            if disp == "open":
                any_open = True

        verdict = obj.get("verdict")
        if verdict and verdict not in ALLOWED_VERDICTS:
            errs.append(f"verdict must be one of {sorted(ALLOWED_VERDICTS)}")

        # Promotion gate: diff_rate < 0.5 AND no open clusters.
        if verdict == "promote":
            dr = obj.get("diff_rate", 999)
            if dr >= DIFF_RATE_GATE:
                errs.append(f"verdict=promote requires diff_rate < {DIFF_RATE_GATE}")
            if any_open:
                errs.append("verdict=promote requires zero open clusters")
            if not obj.get("signed_off_by") or not obj.get("signed_off_at"):
                errs.append("verdict=promote requires signed_off_by + signed_off_at")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "bpv-quote-stage4",
    "scope": "/api/v2/quote",
    "observable_fields": ["response.total_cents", "response.currency"],
    "ramp_stage": 4,
    "window_start": "2026-05-23T00:00:00Z",
    "window_end": "2026-05-24T00:00:00Z",
    "total_compared": 49216,
    "diff_rate": 0.04,
    "clusters": [{"cluster_id": "fx-rounding", "sample_count": 18, "disposition": "fixed"}],
    "verdict": "promote",
    "signed_off_by": "ruslan@faion.net",
    "signed_off_at": "2026-05-24",
    "version": "1.0.0",
    "last_reviewed": "2026-05-24",
}

INVALID_FIXTURE = {
    "artefact_id": "bad",
    "scope": "/api/v2/quote",
    "observable_fields": [],
    "ramp_stage": 5,
    "window_start": "2026-05-20",
    "window_end": "2026-05-21",
    "total_compared": 12,
    "diff_rate": 0.0,
    "clusters": [],
    "verdict": "promote",
    "version": "1.0",
    "last_reviewed": "yesterday",
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
    ap.add_argument("--file", type=str, help="path to parity-report JSON")
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
