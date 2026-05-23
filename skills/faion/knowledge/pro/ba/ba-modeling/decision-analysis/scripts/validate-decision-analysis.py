#!/usr/bin/env python3
"""validate-decision-analysis.py

Validate a decision-record artefact against 02-output-contract.xml.

Inputs:
    --file PATH       path to record JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid; 1 = invalid; 2 = usage / unreadable.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ("decision_id", "options", "criteria", "weights_locked_at", "scores", "sensitivity", "approver")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    options = obj.get("options", [])
    if len(options) < 2:
        errs.append("options must have >= 2 entries")
    if not any(o.get("is_baseline") for o in options if isinstance(o, dict)):
        errs.append("options must include at least one is_baseline=true (rule r3)")
    criteria = obj.get("criteria", [])
    if len(criteria) < 3:
        errs.append("criteria must have >= 3 entries")
    weights_sum = sum(c.get("weight", 0) for c in criteria if isinstance(c, dict))
    if criteria and abs(weights_sum - 1.0) > 0.01:
        errs.append(f"criteria weights sum {weights_sum:.3f} != 1.0")
    scores = obj.get("scores", [])
    for i, s in enumerate(scores):
        if not (s.get("evidence") or "").strip() or len(s.get("evidence", "")) < 4:
            errs.append(f"scores[{i}].evidence too short / empty (rule r2)")
        sc = s.get("score", 0)
        if not isinstance(sc, int) or sc < 1 or sc > 5:
            errs.append(f"scores[{i}].score must be int 1..5")
    sens = obj.get("sensitivity", {})
    if sens.get("monte_carlo_runs", 0) < 100:
        errs.append("sensitivity.monte_carlo_runs must be >= 100 (rule r4)")
    j = sens.get("weight_jitter_pct", 0)
    if not (5 <= j <= 50):
        errs.append("sensitivity.weight_jitter_pct must be in [5, 50] (rule r4)")
    rf = sens.get("rank_flip_rate", 0)
    unstable = sens.get("unstable_pairs", [])
    if rf > 0.15 and not unstable:
        errs.append("rank_flip_rate > 0.15 but unstable_pairs empty (rule r4)")
    appr = obj.get("approver", {})
    for k in ("name", "role", "signoff_ts"):
        if not appr.get(k):
            errs.append(f"approver.{k} missing (rule r5)")
    return errs


OK_FIXTURE = {
    "decision_id": "x",
    "options": [{"id": "n", "name": "do nothing", "is_baseline": True}, {"id": "a", "name": "A"}],
    "criteria": [{"id": "tco", "name": "TCO", "weight": 0.4},
                 {"id": "fit", "name": "Fit", "weight": 0.3},
                 {"id": "risk", "name": "Risk", "weight": 0.3}],
    "weights_locked_at": "2026-05-23T08:00:00Z",
    "scores": [{"option_id": o, "criterion_id": c, "score": 3, "evidence": f"e-{o}-{c}.md#L1"}
               for o in ("n", "a") for c in ("tco", "fit", "risk")],
    "sensitivity": {"monte_carlo_runs": 1000, "weight_jitter_pct": 20, "rank_flip_rate": 0.05, "unstable_pairs": []},
    "approver": {"name": "Pedro Silva", "role": "CFO", "signoff_ts": "2026-05-23T11:00:00Z"},
}
BAD_FIXTURE = {"decision_id": "x", "options": [{"id": "a", "name": "A"}], "criteria": [],
               "weights_locked_at": "x", "scores": [], "sensitivity": {}, "approver": {}}


def self_test() -> int:
    if validate(OK_FIXTURE):
        sys.stderr.write("OK rejected\n"); return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("BAD accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
