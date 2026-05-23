#!/usr/bin/env python3
"""validate-jenkins-pipeline-patterns.py

Validate the code artefact for the jenkins-pipeline-patterns methodology against the
schema in 02-output-contract.xml.

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

REQUIRED = ["syntax", "options", "agent_strategy", "shared_libraries"]


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("syntax") != "declarative":
        errs.append("syntax must be declarative")
    opts = obj.get("options", {})
    if not opts.get("timeout_minutes"):
        errs.append("options.timeout_minutes required > 0")
    if not opts.get("disableConcurrentBuilds"):
        errs.append("options.disableConcurrentBuilds must be true")
    if not opts.get("timestamps"):
        errs.append("options.timestamps must be true")
    ag = obj.get("agent_strategy", {})
    if ag.get("kind") == "kubernetes" and not ag.get("pod_resources_set"):
        errs.append("agent_strategy.pod_resources_set must be true on kubernetes")
    libs = obj.get("shared_libraries", [])
    for i, lib in enumerate(libs):
        if not lib.get("version_pinned"):
            errs.append(f"shared_libraries[{i}].version_pinned must be true")
        if not lib.get("dedicated_repo"):
            errs.append(f"shared_libraries[{i}].dedicated_repo must be true")
    branches = obj.get("parallel_branches", [])
    for i, b in enumerate(branches):
        if not b.get("workspace_isolated"):
            errs.append(f"parallel_branches[{i}].workspace_isolated must be true")
    return errs


OK = {
    "syntax": "declarative",
    "options": {
        "timeout_minutes": 30,
        "buildDiscarder_keep": 50,
        "disableConcurrentBuilds": True,
        "timestamps": True,
        "ansiColor": True,
    },
    "agent_strategy": {"kind": "kubernetes", "pod_resources_set": True},
    "shared_libraries": [
        {"name": "platform", "version_pinned": True, "dedicated_repo": True}
    ],
    "parallel_branches": [
        {"name": "unit-tests", "workspace_isolated": True},
        {"name": "integration-tests", "workspace_isolated": True},
    ],
}
BAD = {
    "syntax": "scripted",
    "options": {"timeout_minutes": 0, "disableConcurrentBuilds": False, "timestamps": False},
    "agent_strategy": {"kind": "kubernetes", "pod_resources_set": False},
    "shared_libraries": [{"name": "platform", "version_pinned": False, "dedicated_repo": False}],
    "parallel_branches": [{"name": "unit-tests", "workspace_isolated": False}],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
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
