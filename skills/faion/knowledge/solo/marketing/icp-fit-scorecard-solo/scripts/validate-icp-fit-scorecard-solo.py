#!/usr/bin/env python3
"""validate-icp-fit-scorecard-solo.py

Validate an ICP fit scorecard bundle against content/02-output-contract.xml.

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
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
BANDS = {"keep", "nurture", "remove"}
ACTIONS = {"sunset_email", "refund_offer", "polite_no", "exception"}
SIG_MAX = {"pain_match": 25, "budget_fit": 20, "urgency": 15,
           "product_fit": 25, "accessibility": 15}


def _check_row(i, row, errs):
    req = ["customer_id", "pain_match", "budget_fit", "urgency", "product_fit",
           "accessibility", "total", "band", "evidence"]
    for k in req:
        if k not in row:
            errs.append("rows[" + str(i) + "] missing " + k)
    for sig, mx in SIG_MAX.items():
        v = row.get(sig)
        if not isinstance(v, int) or v < 0 or v > mx:
            errs.append("rows[" + str(i) + "] " + sig + " must be int [0," + str(mx) + "]")
    if all(isinstance(row.get(k), int) for k in SIG_MAX):
        s = sum(row[k] for k in SIG_MAX)
        if row.get("total") != s:
            errs.append("rows[" + str(i) + "] total != sum of signals")
    band = row.get("band")
    total = row.get("total") if isinstance(row.get("total"), int) else None
    if band not in BANDS:
        errs.append("rows[" + str(i) + "] band not in enum")
    elif total is not None:
        if band == "keep" and total < 70:
            errs.append("rows[" + str(i) + "] band='keep' but total<70")
        if band == "remove" and total >= 40:
            errs.append("rows[" + str(i) + "] band='remove' but total>=40")
        if band == "nurture" and (total < 40 or total >= 70):
            errs.append("rows[" + str(i) + "] band='nurture' but total outside [40,69]")
    ev = row.get("evidence")
    if not isinstance(ev, dict):
        errs.append("rows[" + str(i) + "] evidence must be object")
    else:
        for sig in SIG_MAX:
            note = ev.get(sig)
            if not isinstance(note, str) or len(note) < 5:
                errs.append("rows[" + str(i) + "] evidence." + sig + " missing or too short")


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("version", "scored_at", "rows", "histogram", "remove_list"):
        if k not in obj:
            errs.append("missing required: " + k)
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    rows = obj.get("rows", [])
    if not isinstance(rows, list) or not rows:
        errs.append("rows must be non-empty list")
    else:
        for i, row in enumerate(rows):
            _check_row(i, row, errs)
    hist = obj.get("histogram", {})
    if isinstance(hist, dict):
        for k in ("keep", "nurture", "remove", "median"):
            if k not in hist:
                errs.append("histogram missing " + k)
        if isinstance(hist.get("median"), int) and (hist["median"] < 0 or hist["median"] > 100):
            errs.append("histogram.median out of [0,100]")
    rl = obj.get("remove_list", [])
    if isinstance(rl, list):
        for i, r in enumerate(rl):
            for k in ("customer_id", "action", "due_date"):
                if k not in r:
                    errs.append("remove_list[" + str(i) + "] missing " + k)
            if r.get("action") not in ACTIONS and "action" in r:
                errs.append("remove_list[" + str(i) + "] action not in enum")
    # remove band requires entry in remove_list
    if isinstance(rows, list) and isinstance(rl, list):
        rl_ids = {r.get("customer_id") for r in rl}
        for i, row in enumerate(rows):
            if row.get("band") == "remove" and row.get("customer_id") not in rl_ids:
                errs.append("rows[" + str(i) + "] band='remove' but no remove_list entry")
    return errs


OK = {
    "version": "1.1.0",
    "scored_at": "2026-05-23",
    "rows": [{
        "customer_id": "cus_smoke_1",
        "pain_match": 22, "budget_fit": 18, "urgency": 12,
        "product_fit": 23, "accessibility": 13,
        "total": 88, "band": "keep",
        "evidence": {
            "pain_match": "ticket #1 cites the exact problem",
            "budget_fit": "Pro plan since week 1",
            "urgency": "deadline in onboarding survey",
            "product_fit": "uses 7 of 8 core features",
            "accessibility": "responds within 24h"
        }
    }],
    "histogram": {"keep": 1, "nurture": 0, "remove": 0, "median": 88},
    "remove_list": []
}
BAD = {
    "version": "1",
    "scored_at": "later",
    "rows": [{
        "customer_id": "x",
        "pain_match": 50, "budget_fit": 30, "urgency": 0, "product_fit": 0, "accessibility": 0,
        "total": 150, "band": "keep", "evidence": {}
    }],
    "histogram": {"keep": 0, "nurture": 0, "remove": 0, "median": 200},
    "remove_list": []
}


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
