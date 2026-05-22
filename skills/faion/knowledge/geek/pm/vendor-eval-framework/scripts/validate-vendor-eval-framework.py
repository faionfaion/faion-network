#!/usr/bin/env python3
"""validate-vendor-eval-framework.py — Validate a vendor-eval rubric + trial + rollback bundle.

Inputs:
  - <bundle.json>  Path to a JSON bundle with `rubric`, `trial`, `rollback` keys.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - bundle validates.
  1 - bundle violates rubric / trial / rollback rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

MIN_AXES = 4
MAX_AXES = 6
MIN_TRIAL_DAYS = 30

VALID_FIXTURE = {
    "rubric": {
        "category": "apm",
        "candidates": ["Datadog", "Grafana"],
        "axes": [
            {"id": "fit", "weight": 0.25, "scored_by": "eng-lead:alice"},
            {"id": "integrations", "weight": 0.15, "scored_by": "ops-lead:bob"},
            {"id": "pricing", "weight": 0.20, "scored_by": "finance:carol"},
            {"id": "support", "weight": 0.10, "scored_by": "ops-lead:bob"},
            {"id": "security", "weight": 0.15, "scored_by": "security:dan"},
            {"id": "exit_cost", "weight": 0.15, "scored_by": "eng-lead:alice"},
        ],
    },
    "trial": {
        "start": dt.date.today().isoformat(),
        "end": (dt.date.today() + dt.timedelta(days=31)).isoformat(),
        "real_workload_migrated": True,
    },
    "rollback": {
        "criteria": [{"axis": "fit", "threshold": 3}],
        "responsible_owner": "tech-lead:alice",
        "day_60_check_date": (dt.date.today() + dt.timedelta(days=60)).isoformat(),
    },
}
INVALID_FIXTURE = {"rubric": {"axes": [{"id": "fit", "weight": 1.0, "scored_by": "alice"}]}, "trial": {}, "rollback": {}}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    rubric = spec.get("rubric")
    if not isinstance(rubric, dict):
        out.append("rubric missing")
    else:
        cands = rubric.get("candidates", [])
        if not isinstance(cands, list) or len(cands) < 2:
            out.append("rubric.candidates must be >= 2")
        axes = rubric.get("axes", [])
        if not isinstance(axes, list) or not (MIN_AXES <= len(axes) <= MAX_AXES):
            out.append(f"rubric.axes must have between {MIN_AXES} and {MAX_AXES} entries")
        else:
            scorers = set()
            for i, ax in enumerate(axes):
                if not isinstance(ax, dict):
                    out.append(f"rubric.axes[{i}] not object")
                    continue
                if "id" not in ax or "weight" not in ax or "scored_by" not in ax:
                    out.append(f"rubric.axes[{i}] missing id/weight/scored_by")
                sb = str(ax.get("scored_by", ""))
                if ":" not in sb:
                    out.append(f"rubric.axes[{i}].scored_by must be role:person")
                scorers.add(sb.split(":")[0] if ":" in sb else sb)
            if len(scorers) < 2:
                out.append("rubric.axes must be scored by >= 2 distinct roles (multi-stakeholder rule)")
    trial = spec.get("trial", {})
    if not isinstance(trial, dict):
        out.append("trial missing")
    else:
        try:
            s = dt.date.fromisoformat(str(trial.get("start", "")))
            e = dt.date.fromisoformat(str(trial.get("end", "")))
            if (e - s).days < MIN_TRIAL_DAYS:
                out.append(f"trial must run >= {MIN_TRIAL_DAYS} days")
        except ValueError:
            out.append("trial.start / trial.end not ISO dates")
        if not trial.get("real_workload_migrated"):
            out.append("trial.real_workload_migrated must be true (demos disallowed)")
    rollback = spec.get("rollback", {})
    if not isinstance(rollback, dict) or not rollback.get("criteria") or not rollback.get("responsible_owner"):
        out.append("rollback must include criteria[] and responsible_owner (role:person)")
    elif ":" not in str(rollback["responsible_owner"]):
        out.append("rollback.responsible_owner must be role:person")
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
