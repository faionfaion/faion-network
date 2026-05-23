#!/usr/bin/env python3
"""validate-mobile-ux.py - stdlib-only validator for the mobile-ux output artefact.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in OK / BAD fixtures
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

REQUIRED = ["artefact_id", "owner", "version", "last_reviewed", "platforms", "vitals", "findings"]
PLATFORMS = {"ios", "android", "mobile-web"}
CATEGORY = {"touch-target", "thumb-zone", "nav-pattern", "input-type", "vitals", "platform-gesture", "accessibility", "primary-action"}
FINDING_REQUIRED = ["screen", "element", "category", "observed", "threshold", "platform", "fix_direction"]
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
PLURAL_OWNERS = {"team", "we", "us", "ourselves", "everyone", "the team"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    owner = obj.get("owner", "")
    if isinstance(owner, str) and owner.strip().lower() in PLURAL_OWNERS:
        errs.append("owner is plural pronoun / generic group; must be a named individual")
    v = obj.get("version", "")
    if isinstance(v, str) and v and not SEMVER.match(v):
        errs.append(f"version not semver: {v!r}")
    d = obj.get("last_reviewed", "")
    if isinstance(d, str) and d and not DATE.match(d):
        errs.append(f"last_reviewed not YYYY-MM-DD: {d!r}")
    platforms = obj.get("platforms", [])
    if isinstance(platforms, list):
        if not platforms:
            errs.append("platforms must be non-empty")
        for p in platforms:
            if p not in PLATFORMS:
                errs.append(f"platforms entry not in enum: {p!r}")
    vitals = obj.get("vitals", {})
    if isinstance(vitals, dict):
        for k in ("lcp_s", "cls", "tti_s"):
            if k not in vitals:
                errs.append(f"vitals missing {k}")
    findings = obj.get("findings", [])
    if isinstance(findings, list):
        for i, f in enumerate(findings):
            if not isinstance(f, dict):
                errs.append(f"findings[{i}] not object")
                continue
            for k in FINDING_REQUIRED:
                if k not in f or f[k] in (None, ""):
                    errs.append(f"findings[{i}] missing or empty {k}")
            cat = f.get("category")
            if cat and cat not in CATEGORY:
                errs.append(f"findings[{i}].category not in enum: {cat!r}")
            plat = f.get("platform")
            if plat and platforms and plat not in platforms:
                errs.append(f"findings[{i}].platform {plat!r} not in top-level platforms")
    return errs


OK_JSON = json.dumps({
    "artefact_id": "mobile-audit-checkout-2026-05-23",
    "owner": "Maria Yuskiv <maria@faion.net>",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "platforms": ["mobile-web"],
    "vitals": {"lcp_s": 2.1, "cls": 0.08, "tti_s": 4.4},
    "findings": [{
        "screen": "/checkout",
        "element": "button.pay-now",
        "category": "touch-target",
        "observed": "36x36pt",
        "threshold": "44x44pt",
        "platform": "mobile-web",
        "fix_direction": "Increase target to 44x44pt; add 8px spacing from coupon link",
    }],
})
BAD_JSON = json.dumps({
    "owner": "we",
    "platforms": [],
    "vitals": {"lcp_s": 5.0},
    "findings": [{"screen": "/x", "category": "magic"}],
})


def self_test() -> int:
    ok = json.loads(OK_JSON)
    if validate(ok):
        sys.stderr.write("self-test FAIL: OK rejected: " + repr(validate(ok)) + "\n")
        return 1
    bad = json.loads(BAD_JSON)
    if not validate(bad):
        sys.stderr.write("self-test FAIL: BAD accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in OK / BAD fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"not valid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
