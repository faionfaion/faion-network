#!/usr/bin/env python3
"""validate-surveys.py

Validate the artefact for the surveys methodology against the schema in
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
INSTRUMENTS = {'nps', 'sus', 'seq', 'custom', 'csat'}
SCALES = {'binary', 'open-text', 'likert-1-5', 'nps-0-10', 'likert-1-7'}
CHANNELS = {'panel', 'in-app', 'email', 'intercept'}
TESTS = {'chi2', 'none', 'anova', 't-test'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'surveys':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'config':
            errs.append("__faion_header__.produces mismatch")
    if 'research_question' not in obj:
        errs.append(f"missing required field: " + 'research_question')
    if 'instrument' not in obj:
        errs.append(f"missing required field: " + 'instrument')
    if 'items' not in obj:
        errs.append(f"missing required field: " + 'items')
    if 'sampling' not in obj:
        errs.append(f"missing required field: " + 'sampling')
    if 'analysis_plan' not in obj:
        errs.append(f"missing required field: " + 'analysis_plan')


    rq = obj.get("research_question") or ""
    if not isinstance(rq, str) or len(rq) < 20:
        errs.append("research_question too short")
    instr = obj.get("instrument") or []
    if not isinstance(instr, list) or not instr:
        errs.append("instrument must be non-empty list")
    items = obj.get("items") or []
    if not isinstance(items, list) or not items:
        errs.append("items must be non-empty list")
    for i, it in enumerate(items):
        t = it.get("text") or ""
        if " and " in t.lower():
            errs.append("items[" + str(i) + "] may be double-barreled (contains 'and')")
        for bad in ("amazing", "awful", "shouldn't we", "best ever"):
            if bad in t.lower():
                errs.append("items[" + str(i) + "] contains leading wording: " + bad)
        sc = it.get("scale")
        if sc not in SCALES:
            errs.append("items[" + str(i) + "].scale invalid")
        if sc and sc.startswith("likert") and not it.get("labels"):
            errs.append("items[" + str(i) + "] likert without labels")
    samp = obj.get("sampling") or {}
    tn = samp.get("target_n")
    if not isinstance(tn, int) or tn < 30:
        errs.append("sampling.target_n must be >=30")
    ch = samp.get("channels") or []
    if not isinstance(ch, list) or not ch:
        errs.append("sampling.channels must be non-empty list")
    ap = obj.get("analysis_plan") or {}
    if "significance_test" not in ap:
        errs.append("analysis_plan.significance_test missing")

    return errs


OK = {'__faion_header__': {'methodology': 'surveys', 'version': '1.1.0', 'produces': 'config'}, 'research_question': 'Did the new onboarding flow improve first-week feature adoption?', 'instrument': ['nps', 'seq'], 'items': [{'id': 'q1', 'text': 'How likely are you to recommend the product to a colleague?', 'scale': 'nps-0-10', 'labels': ['0=not at all', '10=extremely']}, {'id': 'q2', 'text': 'How easy was completing the onboarding tutorial?', 'scale': 'likert-1-5', 'labels': ['1=very difficult', '2=difficult', '3=neither', '4=easy', '5=very easy']}], 'sampling': {'target_n': 400, 'channels': ['in-app', 'email'], 'fielding_window_days': 14, 'response_rate_target_pct': 25}, 'analysis_plan': {'cross_tabs': ['plan_tier', 'tenure_days'], 'weighting': 'tenure-balanced', 'significance_test': 't-test'}}
BAD = {'research_question': 'About product?', 'items': [{'id': 'q1', 'text': 'Rate the speed and accuracy', 'scale': 'likert-1-5'}], 'sampling': {'target_n': 10, 'channels': []}}


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
