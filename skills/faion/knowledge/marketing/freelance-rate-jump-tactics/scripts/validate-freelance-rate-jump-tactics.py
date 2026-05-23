#!/usr/bin/env python3
"""validate-freelance-rate-jump-tactics.py — schema validator. --self-test runs built-in fixtures."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BANNED = re.compile(r"^(team|we|us)$", re.I)
REQUIRED = ['jump_id', 'niche', 'current_rate', 'target_rate', 'market_band', 'case_studies', 'existing_client_notice', 'rollout_plan', 'owner']


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
    cs = obj.get("case_studies") or []
    if len(cs) < 3:
        errs.append("case_studies < 3 (rule three-case-studies-required)")
    mb = obj.get("market_band") or {}
    if len(mb.get("sources") or []) < 3:
        errs.append("market_band.sources < 3 (rule market-band-citation)")
    ecn = obj.get("existing_client_notice") or {}
    if not isinstance(ecn.get("notice_days"), int) or ecn.get("notice_days") < 60:
        errs.append("notice_days < 60 (rule 60-day-notice-existing-clients)")
    if ecn.get("wip_billing") != "old-rate-until-complete":
        errs.append("wip_billing must be 'old-rate-until-complete' (rule no-retroactive-billing)")

    return errs


OK = {'jump_id': 'rj-x', 'niche': 'x', 'current_rate': 100, 'target_rate': 150, 'market_band': {'median': 140, 'p75': 175, 'sources': ['a', 'b', 'c']}, 'case_studies': [{'customer': 'a', 'outcome': 'x', 'url': 'https://x'}, {'customer': 'b', 'outcome': 'y', 'url': 'https://y'}, {'customer': 'c', 'outcome': 'z', 'url': 'https://z'}], 'existing_client_notice': {'notice_days': 60, 'wip_billing': 'old-rate-until-complete'}, 'rollout_plan': {'new_leads_at': '2026-06-01', 'existing_clients_at': '2026-08-01'}, 'owner': '@ruslan'}
BAD = {'jump_id': 'x', 'case_studies': [], 'owner': 'team', 'existing_client_notice': {'notice_days': 7}, 'niche': 'x', 'current_rate': 1, 'target_rate': 2, 'market_band': {'median': 1, 'p75': 2, 'sources': []}, 'rollout_plan': {}}


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
