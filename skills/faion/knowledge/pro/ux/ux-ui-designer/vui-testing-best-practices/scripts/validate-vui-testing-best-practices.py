#!/usr/bin/env python3
"""validate-vui-testing-best-practices.py

Validate the artefact for the vui-testing-best-practices methodology against the schema in
content/02-output-contract.xml.

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

VER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'vui-testing-best-practices':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'config':
            errs.append("__faion_header__.produces mismatch")
    if 'layers' not in obj:
        errs.append(f"missing required field: " + 'layers')
    if 'subgroup_buckets' not in obj:
        errs.append(f"missing required field: " + 'subgroup_buckets')
    if 'stress_conditions' not in obj:
        errs.append(f"missing required field: " + 'stress_conditions')
    if 'user_test_n' not in obj:
        errs.append(f"missing required field: " + 'user_test_n')
    if 'completion_metric' not in obj:
        errs.append(f"missing required field: " + 'completion_metric')
    if 'seeds_locked' not in obj:
        errs.append(f"missing required field: " + 'seeds_locked')


    layers = obj.get("layers") or []
    if sorted(layers) != ["integration", "stress", "unit", "user"]:
        errs.append("layers must be exactly [unit, integration, user, stress]")
    sb = obj.get("subgroup_buckets") or []
    if not isinstance(sb, list) or len(sb) < 2:
        errs.append("subgroup_buckets must have >=2")
    sc = obj.get("stress_conditions") or []
    if not isinstance(sc, list) or len(sc) < 3:
        errs.append("stress_conditions must have >=3")
    utn = obj.get("user_test_n")
    if not isinstance(utn, int) or utn < 5:
        errs.append("user_test_n must be >=5")
    if obj.get("completion_metric") != "completion_at_attempt_N":
        errs.append("completion_metric must be completion_at_attempt_N")
    if obj.get("seeds_locked") is not True:
        errs.append("seeds_locked must be true")

    return errs


OK = {'__faion_header__': {'methodology': 'vui-testing-best-practices', 'version': '1.1.0', 'produces': 'config'}, 'layers': ['unit', 'integration', 'user', 'stress'], 'subgroup_buckets': ['accent', 'age', 'gender'], 'stress_conditions': ['kitchen-noise', 'multi-speaker', 'accented-speech'], 'user_test_n': 8, 'completion_metric': 'completion_at_attempt_N', 'seeds_locked': True}
BAD = {'layers': ['unit'], 'subgroup_buckets': [], 'stress_conditions': ['quiet'], 'user_test_n': 3, 'completion_metric': 'binary', 'seeds_locked': False}


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
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
