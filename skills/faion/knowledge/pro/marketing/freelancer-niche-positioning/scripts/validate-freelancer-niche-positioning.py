#!/usr/bin/env python3
"""validate-freelancer-niche-positioning.py — schema validator. --self-test runs built-in fixtures."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BANNED = re.compile(r"^(team|we|us)$", re.I)
REQUIRED = ['positioning_id', 'x', 'y', 'z', 'validations', 'valid_after', 'owner']


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
    z = obj.get("z")
    if not isinstance(z, dict) or not all(k in z for k in ("unit", "direction", "magnitude")):
        errs.append("z must be object with unit/direction/magnitude (rule numeric-outcome)")
    for f in ("x", "y"):
        v = obj.get(f, "")
        if not isinstance(v, str) or len(v) < 3:
            errs.append(f"{f} too short (rule format-x-y-z)")
    vs = obj.get("validations") or {}
    for k in ("search_find", "peer_recall", "buyer_paraphrase"):
        if k not in vs or not isinstance(vs[k], dict) or "passed" not in vs[k]:
            errs.append(f"validations.{k} missing")

    return errs


OK = {'positioning_id': 'fnp-1', 'x': 'rebuild onboarding', 'y': 'B2B SaaS founders', 'z': {'unit': '%', 'direction': 'up', 'magnitude': '+20%'}, 'validations': {'search_find': {'passed': True, 'evidence': 'top 3'}, 'peer_recall': {'passed': True, 'evidence': '4 of 5'}, 'buyer_paraphrase': {'passed': True, 'evidence': 'buyer @x'}}, 'valid_after': '2026-05-23', 'owner': '@ruslan'}
BAD = {'positioning_id': 'x', 'x': 'x', 'y': 'x', 'z': 'more better', 'validations': {}, 'owner': 'team', 'valid_after': '2026-05-23'}


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
