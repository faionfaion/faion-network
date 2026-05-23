#!/usr/bin/env python3
"""validate-workflow-design-phase.py — stdlib-only validator for the workflow-design-phase output artefact.

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
    "feature", "status", "spec_ref", "decisions", "file_table", "fr_coverage",
]
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
AD_ID = re.compile(r"^AD-[0-9]+$")
REQ_ID = re.compile(r"^(FR|NFR)-[0-9]+$")
STATUSES = {"Draft", "Accepted", "Superseded"}
ACTIONS = {"CREATE", "MODIFY", "DELETE"}
PLURAL_OWNERS = {"team", "we", "us", "ourselves", "everyone", "engineering"}
VAGUE_PATHS = {"various", "tbd", "multiple", "many"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", [], {}):
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
    st = obj.get("status", "")
    if isinstance(st, str) and st and st not in STATUSES:
        errs.append(f"status not in {sorted(STATUSES)}: {st!r}")
    decisions = obj.get("decisions", [])
    if isinstance(decisions, list):
        for i, dec in enumerate(decisions):
            if not isinstance(dec, dict):
                errs.append(f"decisions[{i}] not object")
                continue
            did = dec.get("id", "")
            if not (isinstance(did, str) and AD_ID.match(did)):
                errs.append(f"decisions[{i}].id not AD-N: {did!r}")
            if not dec.get("chosen"):
                errs.append(f"decisions[{i}].chosen missing")
            rejected = dec.get("rejected", [])
            if not (isinstance(rejected, list) and rejected):
                errs.append(f"decisions[{i}].rejected empty (r2-ad-x-rejected-alternatives)")
            if not dec.get("rationale"):
                errs.append(f"decisions[{i}].rationale missing")
            sat = dec.get("satisfies", [])
            if not (isinstance(sat, list) and sat):
                errs.append(f"decisions[{i}].satisfies empty")
            else:
                for x in sat:
                    if not (isinstance(x, str) and REQ_ID.match(x)):
                        errs.append(f"decisions[{i}].satisfies entry not FR-N/NFR-N: {x!r}")
    ft = obj.get("file_table", [])
    if isinstance(ft, list):
        for i, row in enumerate(ft):
            if not isinstance(row, dict):
                errs.append(f"file_table[{i}] not object")
                continue
            if row.get("action") not in ACTIONS:
                errs.append(f"file_table[{i}].action not in {sorted(ACTIONS)}: {row.get('action')!r}")
            path = row.get("path", "")
            if not path:
                errs.append(f"file_table[{i}].path missing")
            elif isinstance(path, str) and path.strip().lower() in VAGUE_PATHS:
                errs.append(f"file_table[{i}].path is vague: {path!r} (r5-file-table-actionable)")
            scope = row.get("scope", "")
            if not (isinstance(scope, str) and len(scope) >= 5):
                errs.append(f"file_table[{i}].scope too short (≥5 chars required)")
    cov = obj.get("fr_coverage", {})
    if not (isinstance(cov, dict) and cov):
        errs.append("fr_coverage empty (r4-fr-coverage-complete)")
    return errs


OK_JSON = (
    '{"artefact_id":"design-jwt-refresh","owner":"Ruslan Faion <ruslan@faion.net>",'
    '"version":"1.0.0","last_reviewed":"2026-05-23","feature":"jwt-refresh",'
    '"status":"Accepted","spec_ref":".aidocs/features/in-progress/jwt-refresh/spec.md",'
    '"decisions":[{"id":"AD-2","chosen":"HS256 + rotation",'
    '"rejected":["RS256 overkill","no rotation"],'
    '"rationale":"HS256 simpler; rotation closes theft window.",'
    '"satisfies":["FR-3","NFR-2"]}],'
    '"file_table":[{"action":"CREATE","path":"apps/auth/views/refresh.py",'
    '"scope":"POST /auth/refresh view"}],"fr_coverage":{"FR-3":["AD-2"]}}'
)
BAD_JSON = (
    '{"owner":"team","status":"Draft",'
    '"decisions":[{"id":"AD-1","chosen":"use kafka","rejected":[],"satisfies":[]}],'
    '"file_table":[{"action":"MODIFY","path":"various","scope":"x"}],'
    '"fr_coverage":{}}'
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
