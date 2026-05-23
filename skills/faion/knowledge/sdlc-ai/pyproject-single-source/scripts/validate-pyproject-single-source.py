#!/usr/bin/env python3
"""validate-pyproject-single-source.py — validate consolidated pyproject artefact.

Inputs:
    --file PATH       path to artefact JSON (parse pyproject.toml first via `python -c "import tomllib,json; print(json.dumps(tomllib.loads(open('pyproject.toml','rb').read())))"`)
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_TOP = ["build-system", "project", "tool", "no_legacy_companions"]
PROJECT_REQUIRED = ["name", "version", "requires-python", "dependencies"]

VALID_FIXTURE = {
    "build-system": {"requires": ["hatchling"], "build-backend": "hatchling.build"},
    "project": {"name": "my-pkg", "version": "0.1.0", "requires-python": ">=3.12", "dependencies": ["fastapi>=0.115"]},
    "tool": {"ruff": {"line-length": 100}, "pytest": {"ini_options": {"minversion": "9.0"}}},
    "no_legacy_companions": True,
}

INVALID_FIXTURE = {
    "build-system": {"requires": []},
    "project": {"name": "my-pkg"},
    "tool": {"ruff": {}},
    "no_legacy_companions": False,
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED_TOP:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    bs = obj.get("build-system", {})
    if not isinstance(bs, dict):
        errs.append("build-system: must be object")
    else:
        if "build-backend" not in bs:
            errs.append("build-system.build-backend: missing")
        reqs = bs.get("requires", [])
        if not isinstance(reqs, list) or len(reqs) < 1:
            errs.append("build-system.requires: must be non-empty array")
    project = obj.get("project", {})
    if not isinstance(project, dict):
        errs.append("project: must be object")
    else:
        for k in PROJECT_REQUIRED:
            if k not in project:
                errs.append(f"project.{k}: missing")
    tool = obj.get("tool", {})
    if not isinstance(tool, dict) or len(tool) < 2:
        errs.append("tool: must be object with >= 2 tables")
    if obj.get("no_legacy_companions") is not True:
        errs.append("no_legacy_companions: must be true (legacy files still present)")
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
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
