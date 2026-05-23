#!/usr/bin/env python3
"""validate-aarrr-pirate-metrics.py — schema validator. --self-test runs built-in fixtures."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BANNED = re.compile(r"^(team|we|us)$", re.I)
REQUIRED = ['report_id', 'as_of', 'stages', 'bottleneck', 'tactics_queued', 'owner']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required: {k}")
    owner = obj.get("owner", "")
    if isinstance(owner, str) and owner:
        if len(owner) < 3 or BANNED.match(owner.strip()):
            errs.append(f"owner invalid: {owner!r}")
    STAGES = {"acquisition", "activation", "retention", "revenue", "referral"}
    stages = obj.get("stages") or {}
    for s in STAGES:
        if s not in stages:
            errs.append(f"stages.{s} missing (rule weekly-all-five-published)")
        else:
            for k in ("metric", "value", "baseline_30d"):
                if k not in stages[s]:
                    errs.append(f"stages.{s}.{k} missing (rule metric-per-stage-with-baseline)")
    if obj.get("bottleneck") not in STAGES:
        errs.append(f"bottleneck invalid: {obj.get('bottleneck')!r}")
    for i, t in enumerate(obj.get("tactics_queued") or []):
        if not t.get("stage") or t.get("stage") not in STAGES:
            errs.append(f"tactics_queued[{i}].stage missing/invalid (rule tactic-stage-tagged)")

    return errs


OK = {'report_id': 'aarrr-x', 'as_of': '2026-05-20', 'stages': {'acquisition': {'metric': 'signups', 'value': 420, 'baseline_30d': 410}, 'activation': {'metric': 'd7', 'value': 0.31, 'baseline_30d': 0.38}, 'retention': {'metric': 'd30', 'value': 0.42, 'baseline_30d': 0.45}, 'revenue': {'metric': 'mrr', 'value': 4.1, 'baseline_30d': 4.0}, 'referral': {'metric': 'k', 'value': 0.18, 'baseline_30d': 0.17}}, 'bottleneck': 'activation', 'tactics_queued': [{'tactic': 'Pre-seed empty state', 'stage': 'activation'}], 'owner': '@ruslan'}
BAD = {'report_id': 'x', 'stages': {}, 'bottleneck': 'unknown', 'tactics_queued': [{'tactic': 'growth happens'}], 'owner': 'team', 'as_of': '2026-05-20'}


def self_test():
    if OK and validate(OK):
        sys.stderr.write(f"ok rejected: {validate(OK)}\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str); ap.add_argument("--self-test", action="store_true")
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
