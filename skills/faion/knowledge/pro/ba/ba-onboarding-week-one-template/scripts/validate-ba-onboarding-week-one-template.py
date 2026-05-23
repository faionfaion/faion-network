#!/usr/bin/env python3
"""validate-ba-onboarding-week-one-template.py

Validate a week-one-pack manifest against 02-output-contract.xml.

Inputs:
    --file PATH       path to manifest JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid; 1 = invalid; 2 = usage / unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

WEEK_RANGE = re.compile(r"^\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}$")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("project_name", "ba_name", "week_range", "files", "signoff"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not WEEK_RANGE.match(obj.get("week_range", "")):
        errs.append("week_range must match YYYY-MM-DD/YYYY-MM-DD")
    files = obj.get("files", {})
    inv = files.get("inventory_md", {})
    if inv.get("row_count", 0) < 1:
        errs.append("files.inventory_md.row_count < 1 (rule r1)")
    sm = files.get("stakeholders_md", {})
    if sm.get("approve_authority_count", 0) < 1:
        errs.append("files.stakeholders_md.approve_authority_count < 1 (rule r2)")
    gl = files.get("glossary_md", {})
    if gl.get("term_count", 0) < 15:
        errs.append("files.glossary_md.term_count < 15 (rule r3)")
    pr = files.get("processes_md", {})
    if not pr.get("diagram_files"):
        errs.append("files.processes_md.diagram_files empty (rule r4)")
    rs = files.get("risks_md", {})
    if rs.get("gap_count", 0) < 5 or rs.get("risk_count", 0) < 5:
        errs.append("files.risks_md gap_count/risk_count < 5 (rule r5)")
    so = obj.get("signoff", {})
    if not (so.get("engagement_manager_name") or "").strip():
        errs.append("signoff.engagement_manager_name empty (rule r5)")
    return errs


OK_FIXTURE = {
    "project_name": "x", "ba_name": "Maria Lopes", "week_range": "2026-05-18/2026-05-22",
    "files": {
        "inventory_md": {"path": "i.md", "row_count": 20},
        "stakeholders_md": {"path": "s.md", "named_rows": 8, "approve_authority_count": 2},
        "glossary_md": {"path": "g.md", "term_count": 18},
        "processes_md": {"path": "p.md", "diagram_files": ["p.svg"]},
        "risks_md": {"path": "r.md", "gap_count": 5, "risk_count": 5},
    },
    "signoff": {"engagement_manager_name": "Pedro Silva", "signoff_ts": "2026-05-22T17:00:00Z"},
}
BAD_FIXTURE = {"project_name": "x", "ba_name": "x", "week_range": "x", "files": {}, "signoff": {}}


def self_test() -> int:
    if validate(OK_FIXTURE):
        sys.stderr.write("OK rejected\n"); return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("BAD accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
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
