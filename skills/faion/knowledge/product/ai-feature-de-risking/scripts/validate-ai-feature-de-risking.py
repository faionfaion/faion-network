#!/usr/bin/env python3
"""validate-ai-feature-de-risking.py — Validate an AI-feature de-risking eval report.

Inputs:
  - <report.json>  Path to the eval report JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - report validates.
  1 - report violates contract.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

OWNER_RE = re.compile(r"^[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+$")
JUDGE_STALE_DAYS = 90
MIN_N = 30

VALID_FIXTURE = {
    "feature": "jtbd-synthesis",
    "owner": "ai-pm:alice",
    "kill_criteria_committed_at": "2026-04-10",
    "set_version": "golden-v3-frozen-2026-05-15",
    "n": 247,
    "mean": 0.83,
    "ci_low": 0.79,
    "ci_high": 0.87,
    "judge_calibrated_at": dt.date.today().isoformat(),
    "cost_per_run_usd": 75,
    "cost_ceiling_usd": 80,
    "verdict": "PASS",
}
INVALID_FIXTURE = {"feature": "x", "mean": 0.85}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    for k in ("feature", "owner", "kill_criteria_committed_at", "set_version", "n", "mean", "ci_low", "ci_high", "judge_calibrated_at", "cost_per_run_usd", "cost_ceiling_usd", "verdict"):
        if k not in spec:
            out.append(f"{k} missing")
    if "owner" in spec and not OWNER_RE.match(str(spec["owner"])):
        out.append("owner must be role:person")
    if "n" in spec and (not isinstance(spec["n"], int) or spec["n"] < MIN_N):
        out.append(f"n must be >= {MIN_N}")
    if all(k in spec for k in ("ci_low", "ci_high", "mean")):
        if not (spec["ci_low"] <= spec["mean"] <= spec["ci_high"]):
            out.append("ci_low <= mean <= ci_high violated")
    if "judge_calibrated_at" in spec:
        try:
            d = dt.date.fromisoformat(str(spec["judge_calibrated_at"]))
            age = (dt.date.today() - d).days
            if age > JUDGE_STALE_DAYS:
                out.append(f"judge_calibrated_at stale ({age} days; max {JUDGE_STALE_DAYS})")
        except ValueError:
            out.append("judge_calibrated_at not ISO date")
    if "kill_criteria_committed_at" in spec and "set_version" in spec:
        try:
            kc = dt.date.fromisoformat(str(spec["kill_criteria_committed_at"]))
            # set_version is a string with date; allow if kill_criteria predates set freeze OR a sensible date
            if kc > dt.date.today():
                out.append("kill_criteria_committed_at is in the future")
        except ValueError:
            out.append("kill_criteria_committed_at not ISO date")
    if "cost_per_run_usd" in spec and "cost_ceiling_usd" in spec:
        if spec["cost_per_run_usd"] > spec["cost_ceiling_usd"]:
            out.append("cost_per_run_usd exceeds cost_ceiling_usd (rule r5-bounded-eval-cost)")
    if spec.get("verdict") not in {"PASS", "FAIL", "FREEZE"}:
        out.append("verdict must be PASS / FAIL / FREEZE")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid fixture rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(spec)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
