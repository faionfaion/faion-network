#!/usr/bin/env python3
"""validate-vui-market-context.py

Validate the artefact for the vui-market-context methodology against the schema in
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
USE_CASES = {'kiosk', 'app-embedded', 'ivr', 'smart-home'}
PLATFORMS = {'bixby', 'custom-llm', 'matter', 'home-assistant', 'google-assistant', 'alexa', 'siri'}
ACCESS = {'partial', 'closed', 'restricted', 'open'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'vui-market-context':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'decision-record':
            errs.append("__faion_header__.produces mismatch")
    if 'decision_date' not in obj:
        errs.append(f"missing required field: " + 'decision_date')
    if 'use_case' not in obj:
        errs.append(f"missing required field: " + 'use_case')
    if 'scoring' not in obj:
        errs.append(f"missing required field: " + 'scoring')
    if 'recommendation' not in obj:
        errs.append(f"missing required field: " + 'recommendation')


    if obj.get("use_case") not in USE_CASES:
        errs.append("use_case invalid")
    scoring = obj.get("scoring") or []
    if not isinstance(scoring, list) or len(scoring) < 2:
        errs.append("scoring must contain >=2 platforms")
    for i, s in enumerate(scoring):
        if s.get("platform") not in PLATFORMS:
            errs.append("scoring[" + str(i) + "].platform invalid")
        if s.get("developer_access") not in ACCESS:
            errs.append("scoring[" + str(i) + "].developer_access invalid")
        if not s.get("evidence_sources"):
            errs.append("scoring[" + str(i) + "].evidence_sources missing")
    if obj.get("use_case") == "smart-home":
        plats = [s.get("platform") for s in scoring]
        rec = obj.get("recommendation") or {}
        fbs = rec.get("fallback") or []
        if not any(p in ("matter", "home-assistant") for p in plats + fbs + [rec.get("primary")]):
            errs.append("smart-home use_case must include matter or home-assistant in scoring or recommendation")
    rec = obj.get("recommendation") or {}
    if rec.get("primary") not in PLATFORMS:
        errs.append("recommendation.primary invalid")
    if not rec.get("fallback"):
        errs.append("recommendation.fallback must be non-empty")
    if len(str(rec.get("rationale", ""))) < 40:
        errs.append("recommendation.rationale must be >=40 chars")
    if not rec.get("lock_in_risk_notes"):
        errs.append("recommendation.lock_in_risk_notes must be non-empty")

    return errs


OK = {'__faion_header__': {'methodology': 'vui-market-context', 'version': '1.1.0', 'produces': 'decision-record'}, 'decision_date': '2026-05-23', 'use_case': 'smart-home', 'scoring': [{'platform': 'matter', 'install_base': 4, 'developer_access': 'open', 'distribution': 5, 'evidence_sources': ['Matter spec 1.3 (2025)', 'CSA 2025 update']}, {'platform': 'alexa', 'install_base': 5, 'developer_access': 'restricted', 'distribution': 3, 'evidence_sources': ['Amazon 2025 dev portal']}, {'platform': 'home-assistant', 'install_base': 3, 'developer_access': 'open', 'distribution': 4, 'evidence_sources': ['HA 2025 release notes']}], 'recommendation': {'primary': 'matter', 'fallback': ['home-assistant'], 'rationale': 'Matter is consumed by Alexa/Google/Apple; primary gives multi-vendor reach with open access. Home Assistant fallback covers prosumers.', 'lock_in_risk_notes': ['Matter v1.x ecosystem still maturing; expect feature gaps for advanced devices.']}}
BAD = {'decision_date': '2026-05-23', 'use_case': 'smart-home', 'scoring': [{'platform': 'alexa', 'install_base': 5, 'developer_access': 'open', 'distribution': 3, 'evidence_sources': ['2022 Alexa stats']}], 'recommendation': {'primary': 'alexa'}}


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
