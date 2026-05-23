#!/usr/bin/env python3
"""validate-ci-quality-gate-design.py

Validate a ci-design artefact JSON against schema + budget rule.

Inputs:
    --file PATH      path to ci-design JSON
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

ID_RE = re.compile(r"^cgd-[a-z0-9-]{6,}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
TEAM_ALIASES = {"engineering", "dev", "ops", "team", "platform", "qa", "support"}
TIERS = {"BLOCK", "WARN", "NIGHTLY"}
VERDICTS = {"commit-design", "block-budget-exceeded", "block-missing-rationale", "block-config-drift"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "checks", "budget", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^cgd-[a-z0-9-]{6,}$")

    checks = obj.get("checks") or []
    if not isinstance(checks, list) or len(checks) < 1:
        errs.append("checks must be a non-empty list")
    else:
        for i, c in enumerate(checks):
            for sub in ("name", "tier", "runtime_p50_min", "owner_email", "last_reviewed"):
                if sub not in c:
                    errs.append(f"checks[{i}] missing {sub}")
            if c.get("tier") not in TIERS:
                errs.append(f"checks[{i}].tier must be one of {sorted(TIERS)}")
            em = str(c.get("owner_email", ""))
            if em and not EMAIL_RE.match(em):
                errs.append(f"checks[{i}].owner_email must be valid email")
            local = em.split("@", 1)[0].lower() if "@" in em else em.lower()
            if local in TEAM_ALIASES:
                errs.append(f"checks[{i}].owner_email is a team alias ({local})")
            if c.get("tier") == "BLOCK":
                if not isinstance(c.get("rationale"), str) or not c.get("rationale").strip():
                    errs.append(f"checks[{i}] BLOCK without rationale (r2 violation)")

    budget = obj.get("budget") or {}
    if not isinstance(budget, dict):
        errs.append("budget must be an object")
    else:
        for sub in ("target_min", "block_critical_path_min", "headroom_min"):
            if sub not in budget:
                errs.append(f"budget.{sub} missing")
        target = budget.get("target_min")
        critical = budget.get("block_critical_path_min")
        headroom = budget.get("headroom_min")
        if all(isinstance(v, (int, float)) for v in (target, critical, headroom)):
            if abs((target - critical) - headroom) > 0.01:
                errs.append("budget.headroom_min must equal target_min - block_critical_path_min")
            if critical > target and not budget.get("remediation"):
                errs.append("block_critical_path_min > target_min requires non-empty remediation (r3 violation)")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")
    if verdict == "commit-design":
        if isinstance(budget, dict):
            t = budget.get("target_min")
            cp = budget.get("block_critical_path_min")
            if isinstance(t, (int, float)) and isinstance(cp, (int, float)) and cp > t:
                errs.append("verdict=commit-design forbidden when critical_path > target")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "cgd-faion-net-be",
    "checks": [
        {"name": "lint", "tier": "BLOCK", "runtime_p50_min": 1.2, "rationale": "style + obvious bugs", "owner_email": "ruslan@faion.net", "last_reviewed": "2026-05-23"},
        {"name": "unit-tests", "tier": "BLOCK", "runtime_p50_min": 3.4, "rationale": "regression net", "owner_email": "ruslan@faion.net", "last_reviewed": "2026-05-23"},
    ],
    "budget": {"target_min": 10, "block_critical_path_min": 4.6, "headroom_min": 5.4},
    "verdict": "commit-design",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "ci",
    "checks": [{"name": "lint", "tier": "BLOCK", "runtime_p50_min": 1, "owner_email": "team@faion.net", "last_reviewed": "today"}],
    "budget": {"target_min": 10, "block_critical_path_min": 28, "headroom_min": -18},
    "verdict": "commit-design",
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
    ap.add_argument("--file", type=str, help="path to ci-design JSON")
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
