#!/usr/bin/env python3
"""validate-template-task.py — stdlib-only validator for the template-task output artefact.

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
    "task_id", "feature", "status", "objective",
    "acceptance_criteria", "files", "estimated_tokens", "traces_to",
]
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
TASK_ID = re.compile(r"^TASK_[0-9]{3}$")
AC_ID = re.compile(r"^AC-[0-9]+\.[0-9]+$")
FR_ID = re.compile(r"^FR-[0-9]+$")
AD_ID = re.compile(r"^AD-[0-9]+$")
STATUSES = {"todo", "in-progress", "done"}
ACTIONS = {"CREATE", "MODIFY", "DELETE"}
PLURAL_OWNERS = {"team", "we", "us", "ourselves", "everyone", "engineering"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
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
    tid = obj.get("task_id", "")
    if isinstance(tid, str) and tid and not TASK_ID.match(tid):
        errs.append(f"task_id not TASK_NNN: {tid!r}")
    st = obj.get("status", "")
    if isinstance(st, str) and st and st not in STATUSES:
        errs.append(f"status not in {sorted(STATUSES)}: {st!r}")
    obj_text = obj.get("objective", "")
    if isinstance(obj_text, str) and " and " in obj_text.lower():
        errs.append("objective contains 'and' linking verbs; split into two tasks (r2-single-responsibility)")
    et = obj.get("estimated_tokens", 0)
    if isinstance(et, int) and et > 100000:
        errs.append(f"estimated_tokens > 100000: {et} (r4-token-budget-realistic)")
    ac = obj.get("acceptance_criteria", [])
    if isinstance(ac, list):
        for i, c in enumerate(ac):
            if not isinstance(c, dict):
                errs.append(f"acceptance_criteria[{i}] not object")
                continue
            for k in ("id", "given", "when", "then"):
                if not c.get(k):
                    errs.append(f"acceptance_criteria[{i}].{k} missing/empty (r1-observable-ac)")
            cid = c.get("id", "")
            if cid and not AC_ID.match(cid):
                errs.append(f"acceptance_criteria[{i}].id not AC-N.N: {cid!r}")
    files = obj.get("files", [])
    if isinstance(files, list):
        for i, f in enumerate(files):
            if not isinstance(f, dict):
                errs.append(f"files[{i}] not object")
                continue
            if f.get("action") not in ACTIONS:
                errs.append(f"files[{i}].action not in {sorted(ACTIONS)}: {f.get('action')!r}")
            if not f.get("path"):
                errs.append(f"files[{i}].path missing/empty")
    traces = obj.get("traces_to", {})
    if isinstance(traces, dict):
        fr = traces.get("fr", [])
        ad = traces.get("ad", [])
        if not (isinstance(fr, list) and fr):
            errs.append("traces_to.fr missing or empty (r3-traces-to-spec)")
        else:
            for x in fr:
                if not (isinstance(x, str) and FR_ID.match(x)):
                    errs.append(f"traces_to.fr entry not FR-N: {x!r}")
        if not (isinstance(ad, list) and ad):
            errs.append("traces_to.ad missing or empty (r3-traces-to-spec)")
        else:
            for x in ad:
                if not (isinstance(x, str) and AD_ID.match(x)):
                    errs.append(f"traces_to.ad entry not AD-N: {x!r}")
    return errs


OK_JSON = (
    '{"artefact_id":"task-jwt-refresh-001","owner":"Ruslan Faion <ruslan@faion.net>",'
    '"version":"1.0.0","last_reviewed":"2026-05-23","task_id":"TASK_001",'
    '"feature":"jwt-refresh","status":"todo",'
    '"objective":"Add POST /api/v1/auth/refresh endpoint that rotates the refresh token.",'
    '"acceptance_criteria":[{"id":"AC-1.1","given":"valid refresh token",'
    '"when":"POST /api/v1/auth/refresh","then":"HTTP 200 with new access+refresh pair"}],'
    '"files":[{"action":"CREATE","path":"apps/auth/views/refresh.py"}],'
    '"estimated_tokens":45000,"traces_to":{"fr":["FR-3"],"ad":["AD-2"]}}'
)
BAD_JSON = (
    '{"owner":"team","task_id":"001","objective":"do stuff",'
    '"acceptance_criteria":[],"estimated_tokens":250000}'
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
