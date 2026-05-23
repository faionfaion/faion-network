#!/usr/bin/env python3
"""validate-accessibility.py

Validate an a11y-report against the schema declared in content/02-output-contract.xml.

Inputs:
    --file PATH       path to a11y-report JSON
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

SCREEN_ID_RE = re.compile(r"^A11Y-[A-Z0-9-]{2,40}$")
WCAG_LEVELS = {"A", "AA", "AAA"}
VERDICTS = {"pass", "fail"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("screen_id", "url", "wcag_level", "checks", "axe", "verdict"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "screen_id" in obj and not SCREEN_ID_RE.match(str(obj["screen_id"])):
        errs.append(f"screen_id must match ^A11Y-[A-Z0-9-]{{2,40}}$: got {obj['screen_id']!r}")
    if obj.get("wcag_level") not in WCAG_LEVELS:
        errs.append(f"wcag_level must be in {sorted(WCAG_LEVELS)}: got {obj.get('wcag_level')!r}")
    if obj.get("verdict") not in VERDICTS:
        errs.append(f"verdict must be in {sorted(VERDICTS)}: got {obj.get('verdict')!r}")

    checks = obj.get("checks") or {}
    for k in ("semantic", "aria", "keyboard", "contrast"):
        if k not in checks:
            errs.append(f"checks missing {k}")

    axe = obj.get("axe") or {}
    for k in ("critical", "serious", "moderate", "minor"):
        v = axe.get(k)
        if not isinstance(v, int) or v < 0:
            errs.append(f"axe.{k} must be non-negative int")

    # cross-rules
    verdict = obj.get("verdict")
    if verdict == "pass":
        if axe.get("critical", 0) > 0:
            errs.append("verdict=pass with axe.critical > 0 (axe-zero-critical)")
        for c in ("semantic", "aria", "keyboard", "contrast"):
            blk = checks.get(c) or {}
            if blk.get("pass") is False:
                errs.append(f"verdict=pass with checks.{c}.pass=false")
        sem = checks.get("semantic") or {}
        if sem.get("div_buttons", 0) > 0:
            errs.append("checks.semantic.div_buttons > 0 (semantic-first)")
        kb = checks.get("keyboard") or {}
        if kb.get("traps", 0) > 0:
            errs.append("checks.keyboard.traps > 0 (keyboard-completeness)")

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
    bad["axe"]["critical"] = 2
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
