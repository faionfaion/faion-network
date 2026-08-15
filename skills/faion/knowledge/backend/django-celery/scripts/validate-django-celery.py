#!/usr/bin/env python3
"""validate-django-celery.py

Validate the artefact produced by the django-celery methodology against the JSON
Schema embedded in content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run built-in OK + BAD fixtures
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED: tuple[str, ...] = ('task_name', 'business_key', 'idempotency', 'queue', 'max_retries', 'backoff_base_seconds', 'backoff_jitter', 'soft_time_limit', 'time_limit', 'dispatch_mode', 'dlq_strategy', 'dlq_queue', 'alerting_channel')
ENUMS: dict[str, list] = {'backoff_jitter': ['none', 'full', 'equal'], 'dispatch_mode': ['on_commit', 'outside_transaction'], 'idempotency': ['idempotency_key', 'db_upsert', 'check_before_act', 'natural_key'], 'dlq_strategy': ['dlq', 'failure_record', 'alert_only']}
TASK_NAME_RE = re.compile(r'^[a-z][a-z0-9_.]+$')
INT_BOUNDS: dict[str, tuple[int, int | None]] = {'max_retries': (0, 5), 'backoff_base_seconds': (1, None), 'soft_time_limit': (1, None), 'time_limit': (1, None)}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k, allowed in ENUMS.items():
        if k in obj and obj[k] not in allowed:
            errs.append(f"field {k!r} not in allowed values {allowed!r}; got {obj[k]!r}")
    if 'task_name' in obj and not TASK_NAME_RE.match(str(obj['task_name'])):
        errs.append("field 'task_name' must be dotted snake_case (^[a-z][a-z0-9_.]+$)")
    for k, (lo, hi) in INT_BOUNDS.items():
        if k not in obj:
            continue
        v = obj[k]
        if not isinstance(v, int) or isinstance(v, bool):
            errs.append(f"field {k!r} must be an integer; got {v!r}")
            continue
        if v < lo or (hi is not None and v > hi):
            bound = f"[{lo},{hi}]" if hi is not None else f">={lo}"
            errs.append(f"field {k!r} out of range {bound}; got {v!r}")
    return errs


OK = {'task_name': 'apps.payments.tasks.process_refund', 'business_key': 'refund_id', 'idempotency': 'idempotency_key', 'queue': 'payments', 'max_retries': 5, 'backoff_base_seconds': 2, 'backoff_jitter': 'full', 'retry_backoff': True, 'retry_jitter': True, 'soft_time_limit': 30, 'time_limit': 60, 'dispatch_mode': 'on_commit', 'dlq_strategy': 'dlq', 'dlq_queue': 'payments-dlq', 'alerting_channel': '#payments-oncall'}
BAD = {'task_name': 'apps.payments.tasks.process_refund', 'max_retries': 999}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-django-celery.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
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
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
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
