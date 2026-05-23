#!/usr/bin/env python3
"""validate-gumroad-ops-playbook.py

Validate a Gumroad listing config bundle against content/02-output-contract.xml.

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

PRICE_MODES = {"fixed", "pwyw", "tiers"}
PRODUCT_TYPES = {"file", "license", "link"}
REFUND_POLICIES = {"no_refunds", "7_day", "14_day", "30_day"}


def _check_listing(li, errs):
    req = ["product_id", "cover_url", "subtitle", "price", "product_type",
           "refund_policy", "tags"]
    for k in req:
        if k not in li:
            errs.append("listing missing " + k)
    if "product_id" in li and (not isinstance(li["product_id"], str) or len(li["product_id"]) < 3):
        errs.append("listing.product_id too short")
    if "subtitle" in li:
        s = li["subtitle"]
        if not isinstance(s, str) or len(s) < 10 or len(s) > 280:
            errs.append("listing.subtitle length must be [10,280]")
    if "tags" in li:
        t = li["tags"]
        if not isinstance(t, list) or len(t) < 1 or len(t) > 5:
            errs.append("listing.tags must have 1-5 entries")
    if "product_type" in li and li["product_type"] not in PRODUCT_TYPES:
        errs.append("listing.product_type not in enum")
    if "refund_policy" in li and li["refund_policy"] not in REFUND_POLICIES:
        errs.append("listing.refund_policy not in enum")
    if "price" in li:
        pr = li["price"]
        if not isinstance(pr, dict) or "mode" not in pr or "amount_usd" not in pr:
            errs.append("listing.price missing mode or amount_usd")
        else:
            if pr["mode"] not in PRICE_MODES:
                errs.append("listing.price.mode not in enum")
            if not isinstance(pr["amount_usd"], (int, float)) or pr["amount_usd"] < 0:
                errs.append("listing.price.amount_usd must be number >= 0")
    if li.get("cover_width_px") is not None and li["cover_width_px"] < 1280:
        errs.append("listing.cover_width_px must be >= 1280")
    if li.get("cover_height_px") is not None and li["cover_height_px"] < 720:
        errs.append("listing.cover_height_px must be >= 720")
    if li.get("product_type") == "license" and li.get("license_api_enabled") is False:
        errs.append("license product must enable License API")


def _check_affiliate(aff, errs):
    if "enabled" not in aff or "commission_pct" not in aff:
        errs.append("affiliate missing enabled or commission_pct")
    if "commission_pct" in aff:
        cp = aff["commission_pct"]
        if not isinstance(cp, (int, float)) or cp < 0 or cp > 90:
            errs.append("affiliate.commission_pct must be in [0,90]")


def _check_review(r, errs):
    for k in ("reviewed_at", "conversion_rate", "refund_rate"):
        if k not in r:
            errs.append("review missing " + k)


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("listing", "affiliate", "review"):
        if k not in obj:
            errs.append("missing required top-level: " + k)
    if isinstance(obj.get("listing"), dict):
        _check_listing(obj["listing"], errs)
    if isinstance(obj.get("affiliate"), dict):
        _check_affiliate(obj["affiliate"], errs)
    if isinstance(obj.get("review"), dict):
        _check_review(obj["review"], errs)
    return errs


OK = {
    "listing": {
        "product_id": "smoke-pack",
        "cover_url": "https://gumroad.com/u/cover.png",
        "cover_width_px": 1600,
        "cover_height_px": 900,
        "subtitle": "Smoke-test product — minimum viable listing for validator.",
        "price": {"mode": "fixed", "amount_usd": 19},
        "product_type": "file",
        "refund_policy": "14_day",
        "tags": ["smoke"],
        "uses_mor": True,
        "license_api_enabled": False,
    },
    "affiliate": {"enabled": True, "commission_pct": 40, "payout_cadence": "monthly"},
    "review": {"reviewed_at": "2026-05-23", "conversion_rate": 0.04, "refund_rate": 0.01,
               "rank_30d_revenue": 1},
}
BAD = {"listing": {"product_id": "x", "tags": [], "subtitle": "x"},
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
