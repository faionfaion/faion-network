#!/usr/bin/env python3
"""validate-vpat-acr-template.py

Validate the artefact for the vpat-acr-template methodology against the schema in
02-output-contract.xml.

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

REQUIRED = ['product', 'version', 'vpat_edition', 'scope', 'rows', 'signed_by']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    ed = obj.get("vpat_edition") or ""
    if not ed.startswith("2.5"):
        errs.append(f"vpat_edition must be 2.5+, got {ed!r}")
    rows = obj.get("rows") or []
    for r in rows:
        st = r.get("status")
        if st in ("Partially Supports", "Does Not Support"):
            if not r.get("remarks"):
                errs.append(f"row {r.get('sc')!r} status={st!r} but remarks empty")

    return errs


OK = {   'product': 'FaionApp',
    'version': '2.4.0',
    'vpat_edition': '2.5 INT 2024',
    'scope': 'Marketing site + authenticated dashboard; mobile web only.',
    'rows': [   {   'sc': '1.4.3 Contrast (Minimum)',
                    'status': 'Supports',
                    'evaluation_method': 'automated (axe-core) + manual',
                    'remarks': 'All text meets 4.5:1; large text 3:1.'},
                {   'sc': '2.4.11 Focus Not Obscured (Minimum)',
                    'status': 'Supports',
                    'evaluation_method': 'manual keyboard + 1.4x zoom',
                    'remarks': 'Sticky header does not clip focus.'},
                {   'sc': '2.5.8 Target Size (Minimum)',
                    'status': 'Partially Supports',
                    'evaluation_method': 'manual + automated layout audit',
                    'remarks': 'Compare-table checkbox 20×20px; fix scheduled for v2.4.1.'},
                {   'sc': '3.3.8 Accessible Authentication (Minimum)',
                    'status': 'Supports',
                    'evaluation_method': 'manual + AT (NVDA)',
                    'remarks': 'Passkey + magic-link alternatives provided.'}],
    'signed_by': {'name': 'Olena Z.', 'role': 'Accessibility Lead', 'date': '2026-05-15'}}
BAD = {'product': 'x', 'vpat_edition': '2.3'}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"ok rejected: {errs_ok}\n")
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
