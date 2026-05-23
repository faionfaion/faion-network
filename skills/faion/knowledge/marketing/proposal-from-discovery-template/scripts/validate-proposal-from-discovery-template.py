#!/usr/bin/env python3
"""validate-proposal-from-discovery-template.py

Validate a filled proposal-from-discovery-template artefact against the
schema declared in `content/02-output-contract.xml`.

Inputs:
    --file PATH       path to artefact JSON file
    --self-test       run built-in fixtures (pass + fail) and report
    --help            print this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
OPTION_NAMES = {"light", "standard", "outcome-based"}


def _err(errs: list[str], msg: str) -> None:
    errs.append(msg)


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]

    # Header
    header = obj.get("header")
    if not isinstance(header, dict):
        _err(errs, "header: missing or not an object")
    else:
        for k in ("version", "owner", "last_reviewed", "client", "title"):
            if k not in header:
                _err(errs, f"header.{k}: missing")
        v = header.get("version", "")
        if v and not SEMVER.match(v):
            _err(errs, f"header.version: not semver ({v!r})")
        d = header.get("last_reviewed", "")
        if d and not ISO_DATE.match(d):
            _err(errs, f"header.last_reviewed: not ISO date ({d!r})")
        owner = header.get("owner", "")
        if isinstance(owner, str) and owner.strip().lower() in {"team", "we", "us", ""}:
            _err(errs, f"header.owner: not a named human ({owner!r})")
        title = header.get("title", "")
        if isinstance(title, str) and not (8 <= len(title) <= 120):
            _err(errs, "header.title: length must be 8..120")

    # Discovery inputs
    di = obj.get("discovery_inputs")
    if not isinstance(di, dict):
        _err(errs, "discovery_inputs: missing or not an object")
    else:
        pain = di.get("pain", "")
        if not isinstance(pain, str) or len(pain) < 30:
            _err(errs, "discovery_inputs.pain: must be string >=30 chars")
        if "budget_signal" not in di:
            _err(errs, "discovery_inputs.budget_signal: missing")
        links = di.get("evidence_links", [])
        if not isinstance(links, list) or len(links) < 1:
            _err(errs, "discovery_inputs.evidence_links: must be non-empty list")

    # Options
    opts = obj.get("options", [])
    if not isinstance(opts, list) or len(opts) != 3:
        _err(errs, f"options: must be exactly 3 entries (got {len(opts) if isinstance(opts, list) else 'N/A'})")
    else:
        names_seen = set()
        for i, opt in enumerate(opts):
            if not isinstance(opt, dict):
                _err(errs, f"options[{i}]: not an object")
                continue
            for k in ("name", "scope", "price", "duration_weeks"):
                if k not in opt:
                    _err(errs, f"options[{i}].{k}: missing")
            n = opt.get("name", "")
            if n not in OPTION_NAMES:
                _err(errs, f"options[{i}].name: must be one of {sorted(OPTION_NAMES)} (got {n!r})")
            if n in names_seen:
                _err(errs, f"options[{i}].name: duplicate ({n!r})")
            names_seen.add(n)
            scope = opt.get("scope", "")
            if isinstance(scope, str) and len(scope) < 20:
                _err(errs, f"options[{i}].scope: must be >=20 chars")
            dw = opt.get("duration_weeks")
            if isinstance(dw, int) and not (1 <= dw <= 52):
                _err(errs, f"options[{i}].duration_weeks: must be 1..52")

    # Actions
    acts = obj.get("actions", [])
    if not isinstance(acts, list) or len(acts) < 1:
        _err(errs, "actions: must be non-empty list")
    else:
        for i, a in enumerate(acts):
            if not isinstance(a, dict):
                _err(errs, f"actions[{i}]: not an object")
                continue
            for k in ("owner", "due_date", "action"):
                if k not in a:
                    _err(errs, f"actions[{i}].{k}: missing")
            dd = a.get("due_date", "")
            if dd and not ISO_DATE.match(dd):
                _err(errs, f"actions[{i}].due_date: not ISO date ({dd!r})")

    return errs


_OK_FIXTURE = {
    "header": {
        "version": "1.0.0",
        "owner": "Anna Schmidt",
        "last_reviewed": "2026-05-23",
        "client": "Acme Corp",
        "title": "Acme — payment-funnel rebuild proposal",
    },
    "discovery_inputs": {
        "pain": "Checkout p95 latency 1.4s; 18% Stripe retry rate; revenue leak ~$8k/week.",
        "budget_signal": "Confirmed $25-50k Q3.",
        "evidence_links": ["https://drive.acme.com/calls/2026-05-21.md"],
    },
    "options": [
        {"name": "light", "scope": "Stripe retry tuning + latency budget", "price": 6500, "duration_weeks": 2},
        {"name": "standard", "scope": "Light + p95 rebuild + retry policy roll-out", "price": 18000, "duration_weeks": 6},
        {"name": "outcome-based", "scope": "Standard with success fee on retry-rate ≤6%", "price": 12000, "duration_weeks": 6},
    ],
    "actions": [
        {"owner": "Anna Schmidt", "due_date": "2026-05-26", "action": "Send PDF"},
    ],
}

_BAD_FIXTURE = {
    "header": {"version": "1", "owner": "team", "last_reviewed": "yesterday"},
    "options": [{"name": "standard"}],
}


def self_test() -> int:
    ok_errs = validate(_OK_FIXTURE)
    if ok_errs:
        sys.stderr.write(f"self-test FAIL: OK fixture rejected: {ok_errs}\n")
        return 1
    bad_errs = validate(_BAD_FIXTURE)
    if not bad_errs:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
