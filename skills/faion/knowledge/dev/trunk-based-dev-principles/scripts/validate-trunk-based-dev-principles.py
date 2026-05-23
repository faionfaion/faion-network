#!/usr/bin/env python3
"""validate-trunk-based-dev-principles.py

Validate a TBD-readiness checklist JSON against the schema and consistency rules.

Inputs:
    --file PATH      path to checklist JSON
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

PRINCIPLES = ("single_trunk", "small_commits", "releasable_trunk", "fast_ci")
VERDICTS = {"adopt", "partial-adopt", "not-ready"}
ID_RE = re.compile(r"^tbd-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "repo_ref", "principles", "total", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^tbd-[a-z0-9-]{6,}$")

    pr = obj.get("principles") or {}
    if not isinstance(pr, dict):
        errs.append("principles must be an object")
    else:
        summed = 0
        for name in PRINCIPLES:
            block = pr.get(name)
            if not isinstance(block, dict):
                errs.append(f"principles.{name} missing or not object")
                continue
            for sub in ("score", "evidence"):
                if sub not in block:
                    errs.append(f"principles.{name}.{sub} missing")
            score = block.get("score")
            if not isinstance(score, int) or not (0 <= score <= 25):
                errs.append(f"principles.{name}.score must be int in [0,25]")
            else:
                summed += score
            ev = block.get("evidence")
            if not isinstance(ev, str) or not ev.strip():
                errs.append(f"principles.{name}.evidence must be non-empty string")

        if "total" in obj and isinstance(obj["total"], int):
            if obj["total"] != summed:
                errs.append(f"total ({obj['total']}) must equal sum of principle scores ({summed})")
            if not (0 <= obj["total"] <= 100):
                errs.append("total must be in [0,100]")

        verdict = obj.get("verdict")
        if verdict not in VERDICTS:
            errs.append(f"verdict must be one of {sorted(VERDICTS)}")

        # Aggregate consistency.
        weak = [n for n in PRINCIPLES if isinstance(pr.get(n, {}).get("score"), int) and pr[n]["score"] < 15]
        if verdict == "adopt" and weak:
            errs.append(f"verdict=adopt requires every principle score >= 15; weak: {weak}")
        if verdict == "adopt" and isinstance(obj.get("total"), int) and obj["total"] < 70:
            errs.append("verdict=adopt requires total >= 70")
        if verdict == "not-ready" and not weak and isinstance(obj.get("total"), int) and obj["total"] >= 70:
            errs.append("verdict=not-ready inconsistent with total >= 70 and no weak principles")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "tbd-myrepo-2026-05",
    "repo_ref": "github.com/org/myrepo",
    "principles": {
        "single_trunk":     {"score": 24, "evidence": "0 branches > 2 days, BRANCHING.md present"},
        "small_commits":    {"score": 22, "evidence": "median PR 142 LoC, median branch age 11h"},
        "releasable_trunk": {"score": 20, "evidence": "auto-revert on, 14 flags, gates composed"},
        "fast_ci":          {"score": 18, "evidence": "p50 6m12s, p95 9m48s"},
    },
    "total": 84,
    "verdict": "adopt",
    "fixes": [],
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "myrepo",
    "repo_ref": "myrepo",
    "principles": {"single_trunk": {"score": 30, "evidence": "ok"}},
    "total": 30,
    "verdict": "adopt",
    "version": "1.0",
    "last_reviewed": "today",
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
    ap.add_argument("--file", type=str, help="path to checklist JSON")
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
