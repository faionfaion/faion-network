#!/usr/bin/env python3
"""validate-architecture-decision-records.py — stdlib-only validator for the architecture-decision-records output artefact.

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

REQUIRED = ['artefact_id', 'owner', 'version', 'last_reviewed', 'adr_id', 'title', 'status', 'date', 'context', 'decision', 'consequences', 'alternatives_rejected']
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
PLURAL_OWNERS = {"team", "we", "us", "the team", "ourselves", "everyone", "engineering"}
STATUSES = {"Proposed", "Accepted", "Deprecated", "Superseded"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
        elif obj[k] in (None, ""):
            errs.append(f"required field is empty: {k}")
        elif isinstance(obj[k], (list, dict)) and not obj[k]:
            errs.append(f"required collection field is empty: {k}")
    # `operator` is accepted as an owner-key alias so artefacts written against
    # the older sdd contract still get the named-individual check applied.
    owner_key = "owner" if "owner" in obj else ("operator" if "operator" in obj else None)
    owner = obj.get(owner_key, "") if owner_key else ""
    if isinstance(owner, str) and owner.strip().lower() in PLURAL_OWNERS:
        errs.append("owner is plural pronoun / generic group; must be a named individual")
    v = obj.get("version", "")
    if isinstance(v, str) and v and not SEMVER.match(v):
        errs.append(f"version not semver: {v!r}")
    d = obj.get("last_reviewed", "")
    if isinstance(d, str) and d and not DATE.match(d):
        errs.append(f"last_reviewed not YYYY-MM-DD: {d!r}")
    # The three checks below close the gap both pre-merge validators shared:
    # the schema declared them, neither implementation enforced them.
    status = obj.get("status")
    if status is not None and status not in STATUSES:
        errs.append(f"status not in {sorted(STATUSES)} (r4-status-discipline); got {status!r}")
    alts = obj.get("alternatives_rejected")
    if isinstance(alts, list) and len(alts) < 2:
        errs.append(f"alternatives_rejected needs >=2 entries (r3-alternatives-required); got {len(alts)}")
    cons = obj.get("consequences")
    if isinstance(cons, dict):
        if not cons.get("positive"):
            errs.append("consequences.positive is empty (r7-consequences-both-signs)")
        if not cons.get("negative"):
            errs.append("consequences.negative is empty (r7-consequences-both-signs)")
    elif cons is not None:
        errs.append("consequences must be an object with 'positive' and 'negative' lists (r7)")
    if status == "Superseded" and not obj.get("superseded_by"):
        errs.append("status is Superseded but superseded_by is unset (r1-immutable-history)")
    return errs


OK_JSON = '{"artefact_id": "adr-auth-clerk-023", "owner": "Ruslan Faion <ruslan@faion.net>", "version": "1.0.0", "last_reviewed": "2026-05-23", "adr_id": "023", "title": "Adopt Clerk for identity", "status": "Accepted", "date": "2026-05-23", "context": "Auth0 pricing climbed; we need an alternative with SSO and decent UX.", "decision": "Adopt Clerk as the primary identity provider for new signups.", "consequences": {"positive": ["Cheaper at current MAU"], "negative": ["Vendor concentration on Clerk"]}, "alternatives_rejected": [{"option": "WorkOS", "reason": "Higher floor cost"}, {"option": "Stay on Auth0", "reason": "The pricing climb is the reason for the ADR"}], "supersedes": null, "superseded_by": null}'
BAD_JSON = '{"owner": "team", "status": "lgtm", "alternatives_rejected": []}'
# One-sided consequences and a single alternative: valid before the sdd merge,
# rejected after it. Guards r3 and r7 against silent regression.
ONE_SIDED_JSON = '{"artefact_id": "adr-x", "owner": "Ruslan Faion", "version": "1.0.0", "last_reviewed": "2026-05-23", "adr_id": "024", "title": "Something", "status": "Accepted", "date": "2026-05-23", "context": "A context paragraph long enough to clear the minimum length bar.", "decision": "We will do the thing we already did.", "consequences": {"positive": ["all upside"], "negative": []}, "alternatives_rejected": [{"option": "Do nothing", "reason": "no"}]}'


def self_test() -> int:
    ok = json.loads(OK_JSON)
    if validate(ok):
        sys.stderr.write("self-test FAIL: OK rejected: " + repr(validate(ok)) + "\n")
        return 1
    for name, blob in (("BAD", BAD_JSON), ("ONE_SIDED", ONE_SIDED_JSON)):
        if not validate(json.loads(blob)):
            sys.stderr.write(f"self-test FAIL: {name} accepted\n")
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
