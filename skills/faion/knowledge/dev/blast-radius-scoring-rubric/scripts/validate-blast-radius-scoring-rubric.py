#!/usr/bin/env python3
"""validate-blast-radius-scoring-rubric.py

Validate a per-PR blast-radius rubric JSON against the schema and consistency rules.

Inputs:
    --file PATH      path to rubric JSON
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

ALLOWED_OVERRIDES = {None, "auth", "payments", "rbac", "secrets", "migrations", "deletions", "money", "pii", "cron"}
ALLOWED_VERDICTS = {"light-skim", "standard", "deep-read", "block-missing-rollback"}
AXES_ALLOWED = {1, 3, 5}
ID_RE = re.compile(r"^brsr-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "pr_ref", "axes", "total", "verdict", "override_fired", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^brsr-[a-z0-9-]{6,}$")

    axes = obj.get("axes") or {}
    if not isinstance(axes, dict):
        errs.append("axes must be an object")
    else:
        for k in ("services", "users", "reversibility"):
            if k not in axes:
                errs.append(f"axes missing {k}")
            elif axes[k] not in AXES_ALLOWED:
                errs.append(f"axes.{k} must be one of 1, 3, 5")

    if "total" in obj and isinstance(obj["total"], int):
        if not (3 <= obj["total"] <= 15):
            errs.append("total must be in [3,15]")
        axes_sum = sum(axes.get(k, 0) for k in ("services", "users", "reversibility"))
        if axes_sum and obj["total"] != axes_sum:
            errs.append(f"total ({obj['total']}) must equal axes sum ({axes_sum})")

    of = obj.get("override_fired")
    oc = obj.get("override_category")
    if oc not in ALLOWED_OVERRIDES:
        errs.append(f"override_category must be null or one of {sorted(x for x in ALLOWED_OVERRIDES if x)}")
    if of is True and oc in (None, ""):
        errs.append("override_fired=true requires non-null override_category")
    if of is False and oc not in (None, ""):
        errs.append("override_fired=false but override_category is set — state inconsistent")

    verdict = obj.get("verdict")
    if verdict not in ALLOWED_VERDICTS:
        errs.append(f"verdict must be one of {sorted(ALLOWED_VERDICTS)}")

    rev = axes.get("reversibility")
    plan = obj.get("rollback_plan")
    if rev == 5 and (plan is None or (isinstance(plan, str) and not plan.strip())):
        if verdict != "block-missing-rollback":
            errs.append("reversibility=5 with empty rollback_plan requires verdict=block-missing-rollback")

    if of is True and verdict not in ("deep-read", "block-missing-rollback"):
        errs.append("override_fired=true requires verdict in {deep-read, block-missing-rollback}")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "brsr-pr-483",
    "pr_ref": "https://github.com/org/repo/pull/483",
    "axes": {"services": 1, "users": 5, "reversibility": 3},
    "total": 9,
    "override_fired": True,
    "override_category": "auth",
    "verdict": "deep-read",
    "rollback_plan": None,
    "scored_by": "ruslan@faion.net",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "pr-999",
    "pr_ref": "config",
    "axes": {"services": 1, "users": 1, "reversibility": 5},
    "total": 7,
    "override_fired": False,
    "verdict": "light-skim",
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
    ap.add_argument("--file", type=str, help="path to rubric JSON")
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
