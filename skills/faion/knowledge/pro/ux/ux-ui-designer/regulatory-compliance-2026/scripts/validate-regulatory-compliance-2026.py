#!/usr/bin/env python3
"""validate-regulatory-compliance-2026.py

Validate a regulatory-compliance-2026 report JSON against the schema in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to report JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_SURFACE_TYPES = {"web", "ios", "android", "kiosk", "ebook", "embedded"}
ALLOWED_JURISDICTIONS = {"US", "EU", "ON", "US-FED", "UK", "AU", "JP"}
ALLOWED_REGULATIONS = {"ADA-Title-II", "EAA", "AODA", "Section-508", "UK-EQA", "AU-DDA"}
ALLOWED_WCAG_VERSIONS = {"2.0", "2.1", "2.2"}
ALLOWED_WCAG_LEVELS_REG = {"A", "AA", "AAA"}
ALLOWED_WCAG_LEVELS_STATEMENT = {"AA", "AAA"}
ALLOWED_SEVERITY = {"blocker", "high", "medium", "low"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
SC_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]

    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != "regulatory-compliance-2026":
            errs.append("__faion_header__.methodology must be 'regulatory-compliance-2026'")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != "report":
            errs.append("__faion_header__.produces must be 'report'")

    for k in ("report_date", "owner"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "report_date" in obj and not DATE_RE.match(str(obj["report_date"])):
        errs.append("report_date must be ISO YYYY-MM-DD")

    surfaces = obj.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        errs.append("surfaces must be non-empty list")
    else:
        for i, s in enumerate(surfaces):
            for k in ("id", "type", "url_or_bundle", "jurisdictions"):
                if k not in s:
                    errs.append(f"surfaces[{i}] missing {k}")
            if s.get("type") not in ALLOWED_SURFACE_TYPES:
                errs.append(f"surfaces[{i}].type invalid")
            jur = s.get("jurisdictions") or []
            if not isinstance(jur, list) or not jur:
                errs.append(f"surfaces[{i}].jurisdictions must be non-empty list")
            else:
                for j in jur:
                    if j not in ALLOWED_JURISDICTIONS:
                        errs.append(f"surfaces[{i}].jurisdictions has invalid {j}")

    regs = obj.get("regulations")
    if not isinstance(regs, list) or not regs:
        errs.append("regulations must be non-empty list")
    else:
        for i, r in enumerate(regs):
            for k in ("regulation", "wcag_version", "wcag_level", "deadline", "surfaces"):
                if k not in r:
                    errs.append(f"regulations[{i}] missing {k}")
            if r.get("regulation") not in ALLOWED_REGULATIONS:
                errs.append(f"regulations[{i}].regulation invalid")
            if r.get("wcag_version") not in ALLOWED_WCAG_VERSIONS:
                errs.append(f"regulations[{i}].wcag_version invalid")
            if r.get("wcag_level") not in ALLOWED_WCAG_LEVELS_REG:
                errs.append(f"regulations[{i}].wcag_level invalid")
            if "deadline" in r and not DATE_RE.match(str(r["deadline"])):
                errs.append(f"regulations[{i}].deadline must be ISO date")
            rs = r.get("surfaces")
            if not isinstance(rs, list) or not rs:
                errs.append(f"regulations[{i}].surfaces must be non-empty list")

    stmt = obj.get("statement_published")
    if not isinstance(stmt, dict):
        errs.append("statement_published must be object")
    else:
        for k in ("url", "last_updated", "wcag_version", "wcag_level", "feedback_channels", "methodology"):
            if k not in stmt:
                errs.append(f"statement_published missing {k}")
        if "wcag_version" in stmt and stmt["wcag_version"] not in ALLOWED_WCAG_VERSIONS:
            errs.append("statement_published.wcag_version invalid")
        if "wcag_level" in stmt and stmt["wcag_level"] not in ALLOWED_WCAG_LEVELS_STATEMENT:
            errs.append("statement_published.wcag_level invalid")
        if "last_updated" in stmt and not DATE_RE.match(str(stmt["last_updated"])):
            errs.append("statement_published.last_updated must be ISO date")
        fc = stmt.get("feedback_channels")
        if not isinstance(fc, list) or not fc:
            errs.append("statement_published.feedback_channels must be non-empty list")
        meth = stmt.get("methodology")
        if not isinstance(meth, dict):
            errs.append("statement_published.methodology must be object")
        else:
            for k in ("automated", "manual", "at_user"):
                if not isinstance(meth.get(k), bool):
                    errs.append(f"statement_published.methodology.{k} must be boolean")

    bl = obj.get("remediation_backlog", [])
    if not isinstance(bl, list):
        errs.append("remediation_backlog must be list")
    else:
        for i, item in enumerate(bl):
            for k in ("id", "wcag_sc", "surface", "severity", "owner"):
                if k not in item:
                    errs.append(f"remediation_backlog[{i}] missing {k}")
            if "wcag_sc" in item and not SC_RE.match(str(item["wcag_sc"])):
                errs.append(f"remediation_backlog[{i}].wcag_sc must be N.N.N")
            if "severity" in item and item["severity"] not in ALLOWED_SEVERITY:
                errs.append(f"remediation_backlog[{i}].severity invalid")

    if obj.get("overlay_widgets_disabled") is not True:
        errs.append("overlay_widgets_disabled must be true (overlay use is forbidden)")

    return errs


OK = {
    "__faion_header__": {"methodology": "regulatory-compliance-2026", "version": "1.1.0", "produces": "report"},
    "report_date": "2026-05-23",
    "owner": "a11y-lead@example.com",
    "surfaces": [{"id": "web", "type": "web", "url_or_bundle": "https://a.example.com", "jurisdictions": ["US"]}],
    "regulations": [{"regulation": "ADA-Title-II", "wcag_version": "2.1", "wcag_level": "AA", "deadline": "2026-04-24", "surfaces": ["web"]}],
    "statement_published": {
        "url": "https://example.com/a11y",
        "last_updated": "2026-05-15",
        "wcag_version": "2.2",
        "wcag_level": "AA",
        "feedback_channels": ["a11y@example.com"],
        "methodology": {"automated": True, "manual": True, "at_user": True},
    },
    "remediation_backlog": [{"id": "R-001", "wcag_sc": "1.4.3", "surface": "web", "severity": "high", "owner": "fe"}],
    "overlay_widgets_disabled": True,
}
BAD = {"report_date": "2026-05-23", "surfaces": [], "regulations": []}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
