#!/usr/bin/env python3
"""validate-dormant-lead-reactivation.py

Validate one reactivation sequence spec JSON against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to spec JSON
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
import re
import sys
from pathlib import Path

BANNED_OWNER = re.compile(r"^(team|we|us)$", re.I)
SPEC_ID = re.compile(r"^dlr-\d{4}q[1-4]-[a-z0-9-]+$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SEGMENTS = {"past-client", "lost-proposal", "nurture-lead"}
STALE_JURIS = {"EU", "UK", "CA"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("spec_id", "segment", "contacts", "touches", "owner", "version"):
        if k not in obj:
            errs.append(f"missing required: {k}")
    if not SPEC_ID.match(obj.get("spec_id", "")):
        errs.append("spec_id must match dlr-YYYYqN-<segment>")
    if obj.get("segment") not in SEGMENTS:
        errs.append(f"segment must be one of {sorted(SEGMENTS)}")
    owner = obj.get("owner", "")
    if not isinstance(owner, str) or len(owner) < 3:
        errs.append("owner missing or too short")
    elif BANNED_OWNER.match(owner.strip()):
        errs.append(f"owner is banned plural noun: {owner!r}")
    if not SEMVER.match(obj.get("version", "")):
        errs.append("version must be semver")
    touches = obj.get("touches") or []
    if not isinstance(touches, list) or not touches:
        errs.append("touches must be non-empty array")
    if isinstance(touches, list) and len(touches) > 3:
        errs.append("touches must be <=3 (rule max-3-touches)")
    for i, t in enumerate(touches if isinstance(touches, list) else []):
        for k in ("n", "channel", "subject", "body", "references_prior_interaction"):
            if k not in t:
                errs.append(f"touches[{i}].{k} missing")
        if t.get("references_prior_interaction") is not True:
            errs.append(f"touches[{i}].references_prior_interaction must be true (rule prior-context-reference)")
        if not t.get("body") or len(t.get("body", "")) < 40:
            errs.append(f"touches[{i}].body too short")
    contacts = obj.get("contacts") or []
    if not isinstance(contacts, list) or not contacts:
        errs.append("contacts must be non-empty array")
    for i, c in enumerate(contacts if isinstance(contacts, list) else []):
        for k in ("contact_id", "prior_interaction", "consent_jurisdiction", "consent_age_months"):
            if k not in c:
                errs.append(f"contacts[{i}].{k} missing")
        # consent-reconfirm rule
        if (c.get("consent_jurisdiction") in STALE_JURIS
                and isinstance(c.get("consent_age_months"), (int, float))
                and c["consent_age_months"] > 18):
            touch1 = touches[0] if touches else {}
            if not touch1.get("is_consent_reconfirmation"):
                errs.append(f"contacts[{i}] needs consent re-confirm but touch 1 isn't (rule consent-reconfirm-first-touch)")
    return errs


OK = {
    "spec_id": "dlr-2026q2-past-client", "segment": "past-client",
    "contacts": [{"contact_id": "c1", "prior_interaction": "Onboarding rebuild 2025-08", "consent_jurisdiction": "US", "consent_age_months": 10}],
    "touches": [
        {"n": 1, "channel": "email", "subject": "How's <project>?", "body": "x"*50, "references_prior_interaction": True},
        {"n": 2, "channel": "email", "subject": "Idea", "body": "y"*50, "references_prior_interaction": True},
        {"n": 3, "channel": "email", "subject": "Close", "body": "z"*50, "references_prior_interaction": True},
    ],
    "owner": "@ruslan", "version": "1.0.0",
}
BAD = {"spec_id": "dlr-x", "segment": "past-client", "owner": "team", "version": "1", "touches": [], "contacts": []}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write(f"ok rejected: {validate(OK)}\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
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
