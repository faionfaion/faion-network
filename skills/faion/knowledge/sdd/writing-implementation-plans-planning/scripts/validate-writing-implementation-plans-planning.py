#!/usr/bin/env python3
"""validate-writing-implementation-plans.py — stdlib-only validator for the writing-implementation-plans output artefact.

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
    "feature", "status", "design_ref",
    "tasks", "waves", "critical_path", "risks", "rollout", "rollback",
]
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
TASK_ID = re.compile(r"^TASK_[0-9]{3}$")
AD_ID = re.compile(r"^AD-[0-9]+$")
STATUSES = {"Draft", "Accepted", "Superseded"}
PLURAL_OWNERS = {"team", "we", "us", "ourselves", "everyone", "engineering"}


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
    task_ids: set[str] = set()
    tasks = obj.get("tasks", [])
    if isinstance(tasks, list):
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                errs.append(f"tasks[{i}] not object")
                continue
            tid = t.get("id", "")
            if not (isinstance(tid, str) and TASK_ID.match(tid)):
                errs.append(f"tasks[{i}].id not TASK_NNN: {tid!r}")
            else:
                task_ids.add(tid)
            if not t.get("title"):
                errs.append(f"tasks[{i}].title missing")
            files = t.get("files", [])
            if not (isinstance(files, list) and files):
                errs.append(f"tasks[{i}].files empty (r2-tasks-from-file-table)")
            et = t.get("est_tokens", 0)
            if not isinstance(et, int):
                errs.append(f"tasks[{i}].est_tokens not int")
            elif et > 100000:
                errs.append(f"tasks[{i}].est_tokens > 100000: {et} (r3-wave-token-budget)")
            traces = t.get("traces_to", {})
            ad = traces.get("ad", []) if isinstance(traces, dict) else []
            if not (isinstance(ad, list) and ad):
                errs.append(f"tasks[{i}].traces_to.ad empty (r2-tasks-from-file-table)")
            else:
                for x in ad:
                    if not (isinstance(x, str) and AD_ID.match(x)):
                        errs.append(f"tasks[{i}].traces_to.ad entry not AD-N: {x!r}")
    waves = obj.get("waves", [])
    seen_in_waves: set[str] = set()
    if isinstance(waves, list):
        for i, w in enumerate(waves):
            if not isinstance(w, dict):
                errs.append(f"waves[{i}] not object")
                continue
            wt = w.get("tasks", [])
            for tid in wt if isinstance(wt, list) else []:
                if not (isinstance(tid, str) and TASK_ID.match(tid)):
                    errs.append(f"waves[{i}].tasks contains malformed id: {tid!r}")
                elif tid not in task_ids:
                    errs.append(f"waves[{i}].tasks references unknown task: {tid}")
                else:
                    seen_in_waves.add(tid)
    cp = obj.get("critical_path", [])
    if isinstance(cp, list):
        for tid in cp:
            if not (isinstance(tid, str) and TASK_ID.match(tid)):
                errs.append(f"critical_path entry malformed: {tid!r}")
            elif tid not in task_ids:
                errs.append(f"critical_path references unknown task: {tid}")
    rollback = obj.get("rollback", "")
    if isinstance(rollback, str) and len(rollback) < 10:
        errs.append("rollback empty or too short (r5-rollout-and-rollback)")
    rollout = obj.get("rollout", "")
    if isinstance(rollout, str) and len(rollout) < 10:
        errs.append("rollout empty or too short (r5-rollout-and-rollback)")
    return errs


OK_JSON = (
    '{"artefact_id":"plan-jwt-refresh","owner":"Ruslan Faion <ruslan@faion.net>",'
    '"version":"1.0.0","last_reviewed":"2026-05-23","feature":"jwt-refresh",'
    '"status":"Accepted",'
    '"design_ref":".aidocs/features/in-progress/jwt-refresh/design.md",'
    '"tasks":[{"id":"TASK_001","title":"Add refresh view + rotation logic",'
    '"files":["apps/auth/views/refresh.py"],"est_tokens":45000,'
    '"depends_on":[],"traces_to":{"ad":["AD-2"]}},'
    '{"id":"TASK_002","title":"Wire URL + integration tests",'
    '"files":["apps/auth/urls.py"],"est_tokens":30000,'
    '"depends_on":["TASK_001"],"traces_to":{"ad":["AD-2"]}}],'
    '"waves":[{"n":1,"tasks":["TASK_001"]},{"n":2,"tasks":["TASK_002"]}],'
    '"critical_path":["TASK_001","TASK_002"],'
    '"risks":["Token-rotation race under concurrent refresh"],'
    '"rollout":"Feature-flagged behind FF_JWT_REFRESH; canary at 5% for 24h.",'
    '"rollback":"Disable FF_JWT_REFRESH; fallback remains live 7 days."}'
)
BAD_JSON = (
    '{"owner":"team","status":"Draft","design_ref":"x",'
    '"tasks":[{"id":"TASK_001","title":"do everything","files":["various"],'
    '"est_tokens":250000,"depends_on":[],"traces_to":{"ad":[]}}],'
    '"waves":[],"critical_path":[],"risks":["x"],"rollout":"","rollback":""}'
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
