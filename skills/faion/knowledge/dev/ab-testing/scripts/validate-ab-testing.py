#!/usr/bin/env python3
"""validate-ab-testing.py

Validate an experiment-run artefact against the schema declared in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to experiment-run JSON
    --self-test       run built-in fixtures (OK + BAD)
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

EXP_ID_RE = re.compile(r"^EXP-[0-9]{3,6}$")
DECISIONS = {"ship", "kill", "extend", "invalid-srm", "invalid-underpowered"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("experiment_id", "hypothesis", "primary_metric", "design", "variants", "result", "decision"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "experiment_id" in obj and not EXP_ID_RE.match(str(obj["experiment_id"])):
        errs.append(f"experiment_id must match ^EXP-[0-9]{{3,6}}$: got {obj['experiment_id']!r}")
    variants = obj.get("variants") or {}
    if not isinstance(variants, dict) or len(variants) < 2:
        errs.append("variants must have >=2 entries")
    for name, v in (variants.items() if isinstance(variants, dict) else []):
        if not isinstance(v, dict):
            errs.append(f"variants.{name} not object")
            continue
        exp = v.get("exposures", 0)
        conv = v.get("conversions", 0)
        if conv > exp:
            errs.append(f"variants.{name}: conversions ({conv}) > exposures ({exp})")
    res = obj.get("result") or {}
    for k in ("lift", "wilson_ci_low", "wilson_ci_high", "z", "p_value", "srm_chi_square_p"):
        if k not in res:
            errs.append(f"result missing {k}")
    dec = obj.get("decision")
    if dec not in DECISIONS:
        errs.append(f"decision must be in {sorted(DECISIONS)}: got {dec!r}")
    # Cross-rules
    srm = res.get("srm_chi_square_p", 1.0)
    if isinstance(srm, (int, float)) and srm < 0.001 and dec == "ship":
        errs.append("ship with srm_chi_square_p < 0.001 (must be invalid-srm)")
    lo = res.get("wilson_ci_low")
    hi = res.get("wilson_ci_high")
    if dec == "ship" and isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
        if lo <= 0 <= hi:
            errs.append("ship while wilson CI spans zero")
    return errs


def _load_smoke():
    p = Path(__file__).resolve().parent.parent / "templates" / "_smoke-test.json"
    obj = json.loads(p.read_text())
    obj.pop("__faion_header__", None)
    return obj


def self_test() -> int:
    ok = _load_smoke()
    errs_ok = validate(ok)
    if errs_ok:
        sys.stderr.write(f"OK fixture rejected: {errs_ok}\n")
        return 1
    bad = json.loads(json.dumps(ok))
    bad["result"]["srm_chi_square_p"] = 0.0001
    if not validate(bad):
        sys.stderr.write("BAD fixture accepted\n")
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
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"cannot parse JSON: {e}\n")
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
