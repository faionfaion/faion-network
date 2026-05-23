#!/usr/bin/env python3
"""validate-java-spring-async.py

Validate the async-config manifest for the java-spring-async methodology against
the JSON Schema declared in 02-output-contract.xml.

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

REQUIRED = ["executors", "async_methods", "task_decorator_installed", "graceful_shutdown"]


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    execs = obj.get("executors") or []
    if not isinstance(execs, list) or len(execs) < 1:
        errs.append("executors must be non-empty list")
    for i, e in enumerate(execs):
        if not str(e.get("name", "")):
            errs.append(f"executors[{i}].name must be non-empty")
        if e.get("rejected_execution_handler") != "CallerRunsPolicy":
            errs.append(f"executors[{i}].rejected_execution_handler must be 'CallerRunsPolicy'")
        if not isinstance(e.get("core_pool_size"), int) or e.get("core_pool_size", 0) < 1:
            errs.append(f"executors[{i}].core_pool_size must be positive integer")
        if not isinstance(e.get("queue_capacity"), int) or e.get("queue_capacity", 0) < 1:
            errs.append(f"executors[{i}].queue_capacity must be positive integer (bounded)")
    methods = obj.get("async_methods") or []
    if not isinstance(methods, list) or len(methods) < 1:
        errs.append("async_methods must be non-empty list")
    for i, m in enumerate(methods):
        if not str(m.get("executor", "")):
            errs.append(f"async_methods[{i}].executor must be non-empty")
        if not str(m.get("returns", "")).startswith("CompletableFuture"):
            errs.append(f"async_methods[{i}].returns must start with 'CompletableFuture'")
    if obj.get("task_decorator_installed") is not True:
        errs.append("task_decorator_installed must be true")
    gs = obj.get("graceful_shutdown") or {}
    if gs.get("wait_for_tasks") is not True:
        errs.append("graceful_shutdown.wait_for_tasks must be true")
    if not isinstance(gs.get("await_termination_seconds"), int) or gs.get("await_termination_seconds", 0) < 10:
        errs.append("graceful_shutdown.await_termination_seconds must be >= 10")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "executors": [{"name": "emailExecutor", "rejected_execution_handler": "CallerRunsPolicy", "core_pool_size": 4, "queue_capacity": 256}],
    "async_methods": [{"class": "com.acme.notif.EmailService", "method": "send", "executor": "emailExecutor", "returns": "CompletableFuture<Void>"}],
    "task_decorator_installed": True,
    "graceful_shutdown": {"wait_for_tasks": True, "await_termination_seconds": 30},
    "forbidden_patterns_found": [],
}
BAD = {
    "executors": [{"name": "", "rejected_execution_handler": "AbortPolicy", "core_pool_size": 0, "queue_capacity": 0}],
    "async_methods": [{"class": "com.acme.EmailService", "method": "send", "executor": "", "returns": "void"}],
    "task_decorator_installed": False,
    "graceful_shutdown": {"wait_for_tasks": False, "await_termination_seconds": 0},
    "forbidden_patterns_found": ["self-invocation"],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
