#!/usr/bin/env python3
"""validate-output.py — validate an agent-replay-harness-cookbook manifest.

Inputs:  path to a JSON manifest file.
Outputs: exit 0 if valid; exit 1 with violation list on stderr.
Exit codes: 0=valid, 1=violations, 2=usage error, 3=load error.

stdlib + json only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_STUB_TYPES = {"llm", "tool", "clock", "random"}


def validate(payload: dict) -> list[str]:
    v: list[str] = []
    required = [
        "harness_id",
        "trace_path",
        "coverage_ratio",
        "stubs",
        "reproduces",
        "owner",
        "version",
        "produced_at",
    ]
    for k in required:
        if k not in payload:
            v.append(f"missing required field: {k}")
    if v:
        return v

    if not (0 <= payload["coverage_ratio"] <= 1):
        v.append("coverage_ratio must be in [0,1]")
    if payload["coverage_ratio"] < 0.9 and payload.get("reproduces"):
        v.append("coverage_ratio < 0.9 but reproduces=true — implausible, capture more state")

    if not isinstance(payload["stubs"], list) or not payload["stubs"]:
        v.append("stubs must be non-empty list")
    else:
        for s in payload["stubs"]:
            if "type" not in s or s["type"] not in ALLOWED_STUB_TYPES:
                v.append(f"stub.type must be in {sorted(ALLOWED_STUB_TYPES)}")
            if "class" not in s:
                v.append("stub.class missing")

    if not payload["owner"] or payload["owner"].lower() in {"team", "we", "us"}:
        v.append("owner must be a named individual or rotating named role")

    if not re.fullmatch(r"\d+\.\d+\.\d+", payload["version"]):
        v.append("version must be semver")

    return v


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        good = {
            "harness_id": "h-1",
            "trace_path": "traces/r1.jsonl",
            "coverage_ratio": 0.95,
            "stubs": [{"type": "llm", "class": "ReplayLLM"}],
            "reproduces": True,
            "owner": "ruslan@faion.net",
            "version": "1.0.0",
            "produced_at": "2026-05-22T11:00:00Z",
        }
        violations = validate(good)
        if violations:
            sys.stderr.write(f"self-test FAILED: {violations}\n")
            return 1
        sys.stdout.write("self-test passed\n")
        return 0

    if len(argv) < 2:
        sys.stderr.write("usage: validate-output.py <manifest.json> [--self-test] [--help]\n")
        return 2

    p = Path(argv[1])
    try:
        payload = json.loads(p.read_text())
    except Exception as exc:
        sys.stderr.write(f"cannot read {p}: {exc}\n")
        return 3

    violations = validate(payload)
    if violations:
        for vio in violations:
            sys.stderr.write(f"VIOLATION: {vio}\n")
        return 1
    sys.stdout.write(f"OK: {p}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
