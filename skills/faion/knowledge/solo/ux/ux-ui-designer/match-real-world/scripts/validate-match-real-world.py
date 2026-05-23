#!/usr/bin/env python3
"""validate-match-real-world.py - stdlib-only validator for the match-real-world output artefact.

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

REQUIRED = ["artefact_id", "owner", "version", "last_reviewed", "product_surface", "findings"]
SURFACE = {"web", "mobile", "email", "docs", "multi"}
CATEGORY = {"jargon", "inconsistency", "locale-blind", "over-simplified-domain-term", "icon-only", "system-centric"}
CONSISTENCY = {"passes", "needs-cross-surface-update"}
FINDING_REQUIRED = ["string_id", "current", "category", "rewrite", "evidence", "consistency_check"]
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
    surf = obj.get("product_surface", "")
    if surf and surf not in SURFACE:
        errs.append(f"product_surface not in enum {sorted(SURFACE)}: {surf!r}")
    findings = obj.get("findings", [])
    if isinstance(findings, list):
        if not findings:
            errs.append("findings must be non-empty")
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
            cc = f.get("consistency_check")
            if cc and cc not in CONSISTENCY:
                errs.append(f"findings[{i}].consistency_check not in enum: {cc!r}")
            if cat == "inconsistency" and cc == "passes":
                errs.append(f"findings[{i}] inconsistency contradicts consistency_check=passes")
    return errs


OK_JSON = json.dumps({
    "artefact_id": "language-audit-app-2026-05-23",
    "owner": "Maria Yuskiv <maria@faion.net>",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "product_surface": "multi",
    "findings": [{
        "string_id": "settings.email.smtp_label",
        "current": "Configure SMTP parameters for outbound mail relay",
        "category": "jargon",
        "rewrite": "Set up email sending",
        "evidence": "TKT-9182: I just want to send email, no idea what SMTP is",
        "consistency_check": "needs-cross-surface-update",
    }],
})
BAD_JSON = json.dumps({
    "owner": "the team",
    "product_surface": "stuff",
    "findings": [{"current": "fix this", "rewrite": "better"}],
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
