#!/usr/bin/env python3
"""Validate output contract for python-pytest-fixtures.

USAGE:
    validate-python-pytest-fixtures.py <input.json>        Validate a JSON artefact.
    validate-python-pytest-fixtures.py --self-test         Run built-in fixture.
    validate-python-pytest-fixtures.py --help              Show this help.

EXIT CODES:
    0 on pass
    1 on schema violation
    2 on usage error

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = ['fixtures_scoped_narrowly', 'teardown_via_yield', 'no_autouse_on_heavy', 'factory_for_parametrised']


def validate(payload: dict) -> list[str]:
    violations: list[str] = []
    if not isinstance(payload, dict):
        return ["root must be a JSON object"]
    for f in REQUIRED_FIELDS:
        if f not in payload:
            violations.append(f"missing required field: {f}")
            continue
        if not isinstance(payload[f], bool):
            violations.append(f"field {f!r} must be boolean, got {type(payload[f]).__name__}")
        elif payload[f] is False:
            violations.append(f"gate failed: {f} is false")
    extra = set(payload) - set(REQUIRED_FIELDS)
    if extra:
        violations.append(f"unexpected fields: {sorted(extra)}")
    return violations


def _self_test() -> int:
    fixture = {f: True for f in REQUIRED_FIELDS}
    assert validate(fixture) == [], "happy path should pass"
    bad = dict(fixture)
    first = REQUIRED_FIELDS[0]
    bad[first] = False
    violations = validate(bad)
    assert any(first in v for v in violations), "should detect false gate"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="validate-python-pytest-fixtures.py")
    parser.add_argument("path", nargs="?", help="JSON artefact to validate")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        parser.print_help()
        return 2
    payload = json.loads(Path(args.path).read_text())
    violations = validate(payload)
    if violations:
        for v in violations:
            sys.stdout.write(f"VIOLATION: {v}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
