#!/usr/bin/env python3
"""validate-django-celery.py

Validate the artefact for the django-celery methodology against the JSON Schema
in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
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
import sys
from pathlib import Path

REQUIRED = ["task_name", "queue", "idempotency", "max_retries", "soft_time_limit", "time_limit", "dlq_strategy"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    import re
    if 'task_name' in obj and not re.match(r'^[a-z][a-z0-9_.]+$', str(obj['task_name'])):
        errs.append('task_name must be dotted snake_case')
    if 'max_retries' in obj and (not isinstance(obj['max_retries'], int) or obj['max_retries'] < 0 or obj['max_retries'] > 10):
        errs.append('max_retries must be int in [0,10]')
    if 'idempotency' in obj and obj['idempotency'] not in ('idempotency_key', 'db_upsert', 'check_before_act', 'natural_key'):
        errs.append('idempotency not in enum')
    if 'dlq_strategy' in obj and obj['dlq_strategy'] not in ('dlq', 'failure_record', 'alert_only'):
        errs.append('dlq_strategy not in enum')
    return errs


OK = {'task_name': 'app.payments.send_receipt_email', 'queue': 'emails', 'idempotency': 'idempotency_key', 'max_retries': 3, 'retry_backoff': True, 'retry_jitter': True, 'soft_time_limit': 30, 'time_limit': 60, 'dlq_strategy': 'dlq'}
BAD = {'task_name': 'SendEmail', 'max_retries': 99}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
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
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
