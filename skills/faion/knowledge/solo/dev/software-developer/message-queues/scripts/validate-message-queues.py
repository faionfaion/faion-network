#!/usr/bin/env python3
"""validate-message-queues.py

Validate the artefact for the message-queues methodology against the JSON Schema
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

REQUIRED = ["queue_name", "broker", "idempotency_strategy", "manual_ack", "dlq_name", "alert_endpoint", "max_retries", "schema_version"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    import re
    if 'queue_name' in obj and not re.match(r'^[a-z][a-z0-9_.-]+$', str(obj['queue_name'])):
        errs.append('queue_name must be lowercase with [a-z0-9_.-]')
    if 'broker' in obj and obj['broker'] not in ('rabbitmq', 'redis_streams', 'sqs', 'nats', 'kafka'):
        errs.append('broker not in enum')
    if 'idempotency_strategy' in obj and obj['idempotency_strategy'] not in ('idempotency_key', 'db_upsert', 'check_before_act', 'natural_key'):
        errs.append('idempotency_strategy not in enum')
    if 'max_retries' in obj and (not isinstance(obj['max_retries'], int) or obj['max_retries'] < 1 or obj['max_retries'] > 20):
        errs.append('max_retries must be int in [1,20]')
    if 'manual_ack' in obj and obj['manual_ack'] is not True:
        errs.append('manual_ack must be true')
    return errs


OK = {'queue_name': 'orders.events', 'broker': 'rabbitmq', 'idempotency_strategy': 'idempotency_key', 'manual_ack': True, 'dlq_name': 'orders.events.dlq', 'alert_endpoint': 'https://alert.example.com/dlq', 'max_retries': 5, 'schema_version': 2, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'queue_name': 'Orders Events', 'broker': 'custom', 'manual_ack': False, 'max_retries': 50}


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
