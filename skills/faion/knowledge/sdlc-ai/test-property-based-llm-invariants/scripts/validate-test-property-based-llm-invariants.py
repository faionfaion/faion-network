#!/usr/bin/env python3
"""validate-test-property-based-llm-invariants.py

Validate the code artefact for the test-property-based-llm-invariants methodology against the schema
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

REQUIRED = ['function_under_test', 'language', 'library', 'invariants', 'function_purity_verified']
SCHEMA_PROPS = {'language': {'enum': ['python', 'typescript', 'rust', 'haskell', 'scala', 'other']}, 'library': {'enum': ['hypothesis', 'fast-check', 'proptest', 'scalacheck', 'quickcheck', 'other']}, 'invariants': {'minItems': 1}, 'function_purity_verified': {'const': True}}


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


OK = {'function_under_test': 'src/encoders.py:rle_encode', 'language': 'python', 'library': 'hypothesis', 'invariants': [{'family': 'round-trip', 'statement': 'rle_decode(rle_encode(x)) == x', 'source_citation': "docstring line 3: 'encodes / decodes are inverses'", 'seed': 42}, {'family': 'idempotence', 'statement': 'rle_encode(rle_encode(x).bytes) == rle_encode(x)', 'source_citation': 'type signature: takes bytes, returns Encoded(bytes)', 'seed': 4242}], 'function_purity_verified': True}
BAD = {'function_under_test': 'src/utils.py:save_to_db', 'language': 'python', 'library': 'hypothesis', 'invariants': [{'family': 'round-trip', 'statement': 'save then load returns same', 'source_citation': '', 'seed': None}], 'function_purity_verified': False}


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
