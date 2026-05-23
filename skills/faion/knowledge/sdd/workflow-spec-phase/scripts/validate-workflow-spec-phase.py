#!/usr/bin/env python3
"""validate-workflow-spec-phase.py — stdlib-only validator for the workflow-spec-phase output artefact.

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

REQUIRED = [
    "artefact_id", "owner", "version", "last_reviewed",
    "feature", "status",
    "functional_requirements", "non_functional_requirements",
    "in_scope", "out_of_scope", "success_criteria", "glossary",
]
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
FR_ID = re.compile(r"^FR-[0-9]+$")
NFR_ID = re.compile(r"^NFR-[0-9]+$")
STATUSES = {"Draft", "Accepted", "Superseded"}
PLURAL_OWNERS = {"team", "we", "us", "ourselves", "everyone", "engineering"}
SOFT_PHRASES = ("should be nice", "would be great", "nice to have", "kinda")
ADJECTIVE_ONLY = {"useful", "smooth", "nice", "good", "great"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
        elif k != "non_functional_requirements" and obj[k] in (None, "", [], {}):
            errs.append(f"empty required field: {k}")
    owner = obj.get("owner", "")
    if isinstance(owner, str) and owner.strip().lower() in PLURAL_OWNERS:
        errs.append("owner is plural pronoun / generic group; must be a named individual")
    v = obj.get("version", "")
    if isinstance(v, str) and v and not SEMVER.match(v):
        errs.append(f"version not semver: {v!r}")
    d = obj.get("last_reviewed", "")
    if isinstance(d, str) and d and not DATE.match(d):
        errs.append(f"last_reviewed not YYYY-MM-DD: {d!r}")
    st = obj.get("status", "")
    if isinstance(st, str) and st and st not in STATUSES:
        errs.append(f"status not in {sorted(STATUSES)}: {st!r}")
    frs = obj.get("functional_requirements", [])
    if isinstance(frs, list):
        for i, fr in enumerate(frs):
            if not isinstance(fr, dict):
                errs.append(f"functional_requirements[{i}] not object")
                continue
            fid = fr.get("id", "")
            if not (isinstance(fid, str) and FR_ID.match(fid)):
                errs.append(f"functional_requirements[{i}].id not FR-N: {fid!r}")
            stmt = fr.get("statement", "")
            if not isinstance(stmt, str) or len(stmt) < 10:
                errs.append(f"functional_requirements[{i}].statement too short")
            else:
                low = stmt.lower()
                if "shall" not in low and "must" not in low:
                    errs.append(f"functional_requirements[{i}].statement lacks SHALL/MUST (r1-fr-testable-and-numbered)")
                if any(p in low for p in SOFT_PHRASES):
                    errs.append(f"functional_requirements[{i}].statement contains soft language (r1-fr-testable-and-numbered)")
    nfrs = obj.get("non_functional_requirements", [])
    if isinstance(nfrs, list):
        for i, nfr in enumerate(nfrs):
            if not isinstance(nfr, dict):
                continue
            nid = nfr.get("id", "")
            if nid and not NFR_ID.match(nid):
                errs.append(f"non_functional_requirements[{i}].id not NFR-N: {nid!r}")
    oos = obj.get("out_of_scope", [])
    if isinstance(oos, list) and len(oos) < 2:
        errs.append(f"out_of_scope has {len(oos)} entries; need ≥2 (r2-scope-explicit-out)")
    sc = obj.get("success_criteria", [])
    if isinstance(sc, list):
        for i, c in enumerate(sc):
            if isinstance(c, str) and c.strip().lower() in ADJECTIVE_ONLY:
                errs.append(f"success_criteria[{i}] is adjective-only: {c!r} (r3-success-criteria-measurable)")
    return errs


OK_JSON = (
    '{"artefact_id":"spec-jwt-refresh","owner":"Ruslan Faion <ruslan@faion.net>",'
    '"version":"1.0.0","last_reviewed":"2026-05-23","feature":"jwt-refresh","status":"Draft",'
    '"functional_requirements":[{"id":"FR-3","statement":"System SHALL rotate the refresh token on every successful POST /api/v1/auth/refresh."}],'
    '"non_functional_requirements":[{"id":"NFR-2","statement":"Refresh endpoint p95 latency SHALL be under 200ms at 100 RPS."}],'
    '"in_scope":["JWT refresh endpoint","rotation logic"],'
    '"out_of_scope":["OAuth federation","session-based fallback"],'
    '"success_criteria":["p95 latency < 200ms at 100 RPS","≥99% successful refresh over 7 days"],'
    '"glossary":{"refresh token":"Long-lived token used to obtain a new short-lived access token."}}'
)
BAD_JSON = (
    '{"owner":"team","status":"Accepted",'
    '"functional_requirements":[{"id":"1","statement":"system should be nice"}],'
    '"non_functional_requirements":[],'
    '"in_scope":["everything"],"out_of_scope":[],'
    '"success_criteria":["useful"],"glossary":{}}'
)


def self_test() -> int:
    ok = json.loads(OK_JSON)
    res = validate(ok)
    if res:
        sys.stderr.write("self-test FAIL: OK rejected: " + repr(res) + "\n")
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
