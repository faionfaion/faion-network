#!/usr/bin/env python3
"""validate-vui-accessibility-inclusivity.py

Validate the artefact for the vui-accessibility-inclusivity methodology against the schema in
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
        if hdr.get("methodology") != 'vui-accessibility-inclusivity':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'report':
            errs.append("__faion_header__.produces mismatch")
    if 'wer_per_slice' not in obj:
        errs.append(f"missing required field: " + 'wer_per_slice')
    if 'fairness_gap_pct' not in obj:
        errs.append(f"missing required field: " + 'fairness_gap_pct')
    if 'prompts' not in obj:
        errs.append(f"missing required field: " + 'prompts')
    if 'transcript_available' not in obj:
        errs.append(f"missing required field: " + 'transcript_available')
    if 'non_voice_fallback' not in obj:
        errs.append(f"missing required field: " + 'non_voice_fallback')


    wps = obj.get("wer_per_slice") or []
    if not isinstance(wps, list) or len(wps) < 3:
        errs.append("wer_per_slice must have >=3 slices")
    for i, w in enumerate(wps):
        if not isinstance(w.get("n"), int) or w.get("n", 0) < 30:
            errs.append("wer_per_slice[" + str(i) + "].n must be >=30")
    fg = obj.get("fairness_gap_pct")
    if not isinstance(fg, (int, float)) or fg > 10:
        errs.append("fairness_gap_pct must be <=10 (current: " + str(fg) + ")")
    prompts = obj.get("prompts") or []
    for i, p in enumerate(prompts):
        gl = p.get("grade_level")
        if not isinstance(gl, (int, float)) or gl > 8:
            errs.append("prompts[" + str(i) + "].grade_level must be <=8")
    if obj.get("transcript_available") is not True:
        errs.append("transcript_available must be true")
    if obj.get("non_voice_fallback") is not True:
        errs.append("non_voice_fallback must be true")

    return errs


OK = {'__faion_header__': {'methodology': 'vui-accessibility-inclusivity', 'version': '1.1.0', 'produces': 'report'}, 'wer_per_slice': [{'slice': 'native-en', 'wer_pct': 6.5, 'n': 100}, {'slice': 'non-native-en', 'wer_pct': 14.2, 'n': 80}, {'slice': '65+', 'wer_pct': 10.8, 'n': 50}], 'fairness_gap_pct': 7.7, 'prompts': [{'id': 'p1', 'text': 'When should I schedule it?', 'grade_level': 5.4}], 'transcript_available': True, 'non_voice_fallback': True}
BAD = {'wer_per_slice': [{'slice': 'all', 'wer_pct': 8, 'n': 100}], 'fairness_gap_pct': 20, 'prompts': [{'id': 'p1', 'text': 'Please confirm establishment of account', 'grade_level': 14}], 'transcript_available': False, 'non_voice_fallback': False}


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
