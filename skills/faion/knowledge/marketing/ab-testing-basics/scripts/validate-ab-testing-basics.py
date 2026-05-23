#!/usr/bin/env python3
"""validate-ab-testing-basics.py — schema validator. --self-test runs built-in fixtures."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BANNED = re.compile(r"^(team|we|us)$", re.I)
REQUIRED = ['test_id', 'hypothesis', 'primary_metric', 'secondary_metrics', 'mde', 'sample_size', 'split', 'starts_at', 'closes_at', 'owner']


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
    h = obj.get("hypothesis", "")
    if not isinstance(h, str) or len(h) < 20:
        errs.append("hypothesis <20 chars (rule pre-registration-required)")
    secs = obj.get("secondary_metrics") or []
    if isinstance(secs, list) and len(secs) > 2:
        errs.append("secondary_metrics > 2 (rule secondary-metrics-pre-registered)")
    sp = obj.get("split") or {}
    c = sp.get("control"); t = sp.get("treatment")
    if isinstance(c, (int, float)) and isinstance(t, (int, float)):
        if abs(c - 0.5) > 0.001 or abs(t - 0.5) > 0.001:
            if "split_justification" not in obj:
                errs.append("non-50/50 split requires split_justification (rule fifty-fifty-split-or-justify)")
    ss = obj.get("sample_size")
    if not isinstance(ss, int) or ss < 100:
        errs.append("sample_size <100 (rule pre-registration-required)")

    return errs


OK = {'test_id': 'EXP-X', 'hypothesis': 'Shortening the hero copy increases CTR for cold traffic.', 'primary_metric': {'name': 'cta_ctr', 'baseline': 0.062}, 'secondary_metrics': [{'name': 'signup_cr'}], 'mde': 0.05, 'sample_size': 12400, 'split': {'control': 0.5, 'treatment': 0.5}, 'starts_at': '2026-05-06', 'closes_at': '2026-05-20', 'owner': '@ruslan'}
BAD = {'test_id': 'x', 'hypothesis': 'x', 'secondary_metrics': [{'name': 'a'}, {'name': 'b'}, {'name': 'c'}], 'split': {'control': 0.8, 'treatment': 0.2}, 'owner': 'team', 'primary_metric': {}, 'mde': 0, 'sample_size': 0, 'starts_at': '2026-05-06', 'closes_at': '2026-05-20'}


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
