#!/usr/bin/env python3
"""validate-lemon-squeezy-ops-playbook.py

Validate a Lemon Squeezy store config bundle against content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CURRENCIES = {"usd", "eur"}
REFUND_POLICIES = {"no_refunds", "14_day", "30_day"}
INTERVALS = {"one_time", "monthly", "yearly"}


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("store", "variants", "dunning", "affiliate", "review"):
        if k not in obj:
            errs.append("missing required top-level: " + k)
    store = obj.get("store", {})
    if isinstance(store, dict):
        for k in ("store_id", "store_name", "currency", "refund_policy", "uses_mor"):
            if k not in store:
                errs.append("store missing " + k)
        if "currency" in store and store["currency"] not in CURRENCIES:
            errs.append("store.currency not in enum")
        if "refund_policy" in store and store["refund_policy"] not in REFUND_POLICIES:
            errs.append("store.refund_policy not in enum")
    variants = obj.get("variants", [])
    if not isinstance(variants, list) or not (1 <= len(variants) <= 8):
        errs.append("variants must be list of length 1-8")
    else:
        for i, v in enumerate(variants):
            for k in ("variant_id", "name", "amount", "interval", "license_api_enabled"):
                if k not in v:
                    errs.append("variants[" + str(i) + "] missing " + k)
            if "interval" in v and v["interval"] not in INTERVALS:
                errs.append("variants[" + str(i) + "] interval not in enum")
            if v.get("interval") in {"monthly", "yearly"} and v.get("license_api_enabled") is False:
                errs.append("variants[" + str(i) + "] subscription requires License API")
    dunning = obj.get("dunning", {})
    if isinstance(dunning, dict):
        seq = dunning.get("sequence_days", [])
        if not isinstance(seq, list) or len(seq) < 3:
            errs.append("dunning.sequence_days must have >=3 entries")
    affiliate = obj.get("affiliate", {})
    if isinstance(affiliate, dict):
        if "enabled" not in affiliate or "commission_pct" not in affiliate:
            errs.append("affiliate missing enabled or commission_pct")
        if "commission_pct" in affiliate:
            cp = affiliate["commission_pct"]
            if not isinstance(cp, (int, float)) or cp < 0 or cp > 90:
                errs.append("affiliate.commission_pct must be in [0,90]")
    review = obj.get("review", {})
    if isinstance(review, dict) and "reviewed_at" not in review:
        errs.append("review missing reviewed_at")
    return errs


OK = {
    "store": {"store_id": "ls-smoke-1", "store_name": "Smoke", "currency": "usd",
              "refund_policy": "14_day", "uses_mor": True},
    "variants": [{"variant_id": "v-smoke", "name": "Solo", "amount": 19,
                  "interval": "monthly", "license_api_enabled": True}],
    "dunning": {"sequence_days": [1, 4, 8]},
    "affiliate": {"enabled": True, "commission_pct": 40},
    "review": {"reviewed_at": "2026-05-23"},
}
BAD = {"store": {"store_id": "x", "currency": "gbp"}, "variants": [],
       "dunning": {"sequence_days": [1]},
       "affiliate": {"enabled": True, "commission_pct": 95},
       "review": {}}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
