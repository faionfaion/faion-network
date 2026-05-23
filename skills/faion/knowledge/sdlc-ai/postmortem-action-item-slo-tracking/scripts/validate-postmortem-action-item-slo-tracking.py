#!/usr/bin/env python3
"""validate-postmortem-action-item-slo-tracking.py — validate the ledger artefact.

Inputs:
    --file PATH       path to artefact (JSON; markdown ledger can be parsed first)
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_TOP = ["owner", "review_cadence", "retention_months", "entries"]
ENTRY_REQUIRED = ["id", "ts", "owner", "hypothesis_or_event", "evidence_link", "outcome", "next", "slo_class", "slo_due"]
CADENCE_ENUM = {"weekly", "biweekly", "monthly"}
SLO_ENUM = {"P1", "P2", "P3"}

VALID_FIXTURE = {
    "owner": {"person": "ruslan", "role": "SRE lead"},
    "review_cadence": "weekly",
    "retention_months": 24,
    "entries": [
        {
            "id": 1,
            "ts": "2026-05-12T09:30:00Z",
            "owner": "ruslan",
            "hypothesis_or_event": "INC-441 prod 500s after Redis upgrade",
            "evidence_link": "https://github.com/org/repo/issues/441",
            "outcome": "pending",
            "next": "Add max-connections alert at 80%",
            "slo_class": "P1",
            "slo_due": "2026-05-26",
        }
    ],
}

INVALID_FIXTURE = {
    "owner": {"person": "team-sre", "role": "team alias"},
    "review_cadence": "ad-hoc",
    "retention_months": 6,
    "entries": [{"id": 1, "ts": "2026-05-12T09:30:00Z", "hypothesis_or_event": "TBD"}],
}

TEAM_ALIAS_MARKERS = ("@", "team-", "team_", "alias", "channel")


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED_TOP:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    owner = obj.get("owner", {})
    if not isinstance(owner, dict) or "person" not in owner or "role" not in owner:
        errs.append("owner: must be object with person + role")
    else:
        person = (owner.get("person") or "").lower()
        if any(m in person for m in TEAM_ALIAS_MARKERS):
            errs.append("owner.person: team alias forbidden — use a named individual")
    cad = obj.get("review_cadence")
    if cad not in CADENCE_ENUM:
        errs.append(f"review_cadence: {cad!r} not in {sorted(CADENCE_ENUM)}")
    rm = obj.get("retention_months")
    if not isinstance(rm, int) or rm < 12:
        errs.append("retention_months: must be integer >= 12")
    entries = obj.get("entries", [])
    if not isinstance(entries, list):
        errs.append("entries: must be array")
    else:
        for i, e in enumerate(entries):
            for k in ENTRY_REQUIRED:
                if k not in e:
                    errs.append(f"entries[{i}]: missing {k}")
            if e.get("slo_class") not in SLO_ENUM and "slo_class" in e:
                errs.append(f"entries[{i}].slo_class: not in {sorted(SLO_ENUM)}")
            ev = e.get("evidence_link", "")
            if not isinstance(ev, str) or len(ev) < 1:
                errs.append(f"entries[{i}].evidence_link: must be non-empty string")
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
