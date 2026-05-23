#!/usr/bin/env python3
"""validate-team-mode-cli-flag.py

Validate the config artefact for the team-mode-cli-flag methodology against the schema
in `content/02-output-contract.xml`.

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
import re
import sys
from pathlib import Path

REQUIRED = ['version', 'last_reviewed', 'signed_by', 'signature', 'overrides']
SCHEMA_PROPS = {'version': {'pattern': '^\\d+\\.\\d+\\.\\d+$'}, 'signature': {'pattern': '^[A-Za-z0-9+/=]{40,}$'}}


def _check_property(name, value, spec, errs):
    if spec is None or not isinstance(spec, dict):
        return
    if "const" in spec and value != spec["const"]:
        errs.append(f"field {name} must equal const {spec['const']!r}, got {value!r}")
    if "enum" in spec and value not in spec["enum"]:
        errs.append(f"field {name} must be one of {spec['enum']!r}, got {value!r}")
    if "minimum" in spec and isinstance(value, (int, float)) and value < spec["minimum"]:
        errs.append(f"field {name} below minimum {spec['minimum']}")
    if "maximum" in spec and isinstance(value, (int, float)) and value > spec["maximum"]:
        errs.append(f"field {name} above maximum {spec['maximum']}")
    if "minItems" in spec and isinstance(value, list) and len(value) < spec["minItems"]:
        errs.append(f"field {name} has fewer than {spec['minItems']} items")
    if "minLength" in spec and isinstance(value, str) and len(value) < spec["minLength"]:
        errs.append(f"field {name} shorter than {spec['minLength']} chars")
    if "pattern" in spec and isinstance(value, str) and not re.search(spec["pattern"], value):
        errs.append(f"field {name} fails pattern {spec['pattern']}")


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k, spec in SCHEMA_PROPS.items():
        if k in obj:
            _check_property(k, obj[k], spec, errs)
    return errs


OK = {'version': '1.2.0', 'last_reviewed': '2026-05-10', 'signed_by': 'ops@acme.com', 'signature': 'MEUCIQDxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'overrides': {'model_whitelist': ['claude-opus', 'claude-sonnet'], 'mcp_allowlist': ['pact', 'github']}}
BAD = {'version': '1.2', 'signed_by': 'we', 'overrides': {}}


def self_test() -> int:
    ok_errs = validate(OK)
    if ok_errs:
        sys.stderr.write(f"ok rejected: {ok_errs}\n")
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
