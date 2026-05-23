#!/usr/bin/env python3
"""validate-solo-change-order-mini-contract.py

Validate a ChangeOrder JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to CO JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

CHANNELS = {"email", "chat", "signed_doc"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("co_id", "master_sow", "header", "scope_delta", "price_delta",
             "schedule_delta", "payment_terms_delta", "acceptance", "artefact"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    msa = obj["master_sow"]
    for k in ("name", "date", "identifier"):
        if not msa.get(k):
            errs.append(f"master_sow.{k} empty (rule: r1)")

    for d in ("scope_delta", "price_delta", "schedule_delta", "payment_terms_delta"):
        v = obj.get(d, "")
        if not v or v.strip().upper() == "TBD":
            errs.append(f"{d} empty or TBD (rule: r2)")

    a = obj["acceptance"]
    if a.get("channel") not in CHANNELS:
        errs.append("acceptance.channel invalid")

    art = obj["artefact"]
    if not art.get("immutable_link"):
        errs.append("artefact.immutable_link empty (rule: r5)")
    if a.get("reply_yes_captured") and not art.get("invoice_line_ref"):
        errs.append("artefact.invoice_line_ref required when YES captured")

    vh = obj.get("verbal_authorization_hours", 0)
    if vh > 8 and not a.get("reply_yes_captured"):
        errs.append(f"verbal_authorization_hours {vh} > 8 without YES (rule: r4)")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "co_id": "x",
    "master_sow": {"name": "", "date": "2026-04-12", "identifier": ""},
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01", "version": "0"},
    "scope_delta": "sure can add the export thing",
    "price_delta": "TBD",
    "schedule_delta": "",
    "payment_terms_delta": "later",
    "acceptance": {"reply_yes_captured": False, "captured_at": None, "channel": "email"},
    "artefact": {"immutable_link": "", "invoice_line_ref": ""},
    "verbal_authorization_hours": 24
}


def self_test() -> int:
    if SMOKE_OK_FILE.is_file():
        ok = json.loads(SMOKE_OK_FILE.read_text())
        ok["header"]["last_reviewed"] = dt.date.today().isoformat()
        errs = validate(ok)
        if errs:
            sys.stderr.write("smoke_ok rejected: " + "; ".join(errs) + "\n"); return 1
    if not validate(SMOKE_BAD):
        sys.stderr.write("smoke_bad accepted\n"); return 1
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
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
