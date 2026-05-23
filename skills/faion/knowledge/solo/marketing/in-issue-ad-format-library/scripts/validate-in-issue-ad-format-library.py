#!/usr/bin/env python3
"""validate-in-issue-ad-format-library.py

Validate an in-issue ad format library bundle against content/02-output-contract.xml.

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

ALLOWED_FORMATS = {"top_banner", "soft_ps", "mid_issue_case", "dedicated_send"}
ALLOWED_FMT_ROTATION = ALLOWED_FORMATS | {"none"}
ALLOWED_CTAS = {"product_paywall", "waitlist", "lead_magnet",
                "feature_announcement", "none"}


def _check_cadence(plan, errs):
    # sliding 6-issue window cadence enforcement
    n = len(plan)
    for start in range(max(1, n - 5)):
        window = plan[start:start + 6]
        counts = {}
        for row in window:
            f = row.get("format")
            counts[f] = counts.get(f, 0) + 1
        if counts.get("dedicated_send", 0) > 1:
            errs.append("rotation_plan window starting at issue "
                        + str(start + 1) + " exceeds dedicated_send cap (1/6)")
        if counts.get("top_banner", 0) > 6:
            errs.append("rotation_plan window has too many top_banner")
        # self-promo share — require >=1 'none' per 6-issue window
        non_none = sum(1 for r in window if r.get("format") != "none")
        if len(window) >= 6 and non_none > len(window) - 1:
            errs.append("rotation_plan window starting at issue "
                        + str(start + 1) + " has no 'none' issue (trust-reset gap missing)")
    # 4-issue soft_ps cap
    for start in range(max(1, n - 3)):
        window = plan[start:start + 4]
        c = sum(1 for r in window if r.get("format") == "soft_ps")
        if c > 3:
            errs.append("rotation_plan 4-issue window starting at "
                        + str(start + 1) + " exceeds soft_ps cap (3/4)")
    # 2-issue mid_issue_case cap
    for start in range(max(1, n - 1)):
        window = plan[start:start + 2]
        c = sum(1 for r in window if r.get("format") == "mid_issue_case")
        if c > 1:
            errs.append("rotation_plan 2-issue window starting at "
                        + str(start + 1) + " exceeds mid_issue_case cap (1/2)")


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("library", "baseline", "rotation_plan", "review"):
        if k not in obj:
            errs.append("missing required: " + k)
    lib = obj.get("library", {})
    if isinstance(lib, dict):
        keys = set(lib.keys())
        unauth = keys - ALLOWED_FORMATS
        if unauth:
            errs.append("library contains unauthorised format(s): " + ",".join(sorted(unauth)))
        for f in ALLOWED_FORMATS:
            if f not in lib:
                errs.append("library missing required format: " + f)
    baseline = obj.get("baseline", {})
    if isinstance(baseline, dict):
        for k in ("ctr_pct", "cvr_pct", "computed_at"):
            if k not in baseline:
                errs.append("baseline missing " + k)
        for k in ("ctr_pct", "cvr_pct"):
            v = baseline.get(k)
            if v is not None and (not isinstance(v, (int, float)) or v < 0 or v > 100):
                errs.append("baseline." + k + " must be in [0,100]")
    plan = obj.get("rotation_plan", [])
    if not isinstance(plan, list) or len(plan) < 1 or len(plan) > 8:
        errs.append("rotation_plan must have 1-8 entries")
    else:
        for i, row in enumerate(plan):
            for k in ("issue_n", "format", "cta_destination"):
                if k not in row:
                    errs.append("rotation_plan[" + str(i) + "] missing " + k)
            if row.get("format") not in ALLOWED_FMT_ROTATION:
                errs.append("rotation_plan[" + str(i) + "] format not in enum")
            if row.get("cta_destination") not in ALLOWED_CTAS:
                errs.append("rotation_plan[" + str(i) + "] cta_destination not in enum")
        _check_cadence(plan, errs)
    review = obj.get("review", {})
    if isinstance(review, dict) and "reviewed_at" not in review:
        errs.append("review missing reviewed_at")
    return errs


OK = {
    "library": {
        "top_banner": {"max_per_issue": 1},
        "soft_ps": {"max_per_4_issues": 3},
        "mid_issue_case": {"max_per_2_issues": 1},
        "dedicated_send": {"max_per_6_issues": 1},
    },
    "baseline": {"ctr_pct": 3.2, "cvr_pct": 0.6, "computed_at": "2026-05-01"},
    "rotation_plan": [
        {"issue_n": 1, "format": "top_banner", "cta_destination": "product_paywall"},
        {"issue_n": 2, "format": "soft_ps", "cta_destination": "lead_magnet"},
        {"issue_n": 3, "format": "mid_issue_case", "cta_destination": "product_paywall"},
        {"issue_n": 4, "format": "none", "cta_destination": "none"},
        {"issue_n": 5, "format": "soft_ps", "cta_destination": "waitlist"},
        {"issue_n": 6, "format": "dedicated_send", "cta_destination": "product_paywall"},
    ],
    "review": {"reviewed_at": "2026-05-23"},
}
BAD = {
    "library": {"top_banner": {}, "footer_micro": {}},
    "baseline": {"ctr_pct": 200, "cvr_pct": -1, "computed_at": "later"},
    "rotation_plan": [{"issue_n": 1, "format": "popup", "cta_destination": "mixed"}],
    "review": {},
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
