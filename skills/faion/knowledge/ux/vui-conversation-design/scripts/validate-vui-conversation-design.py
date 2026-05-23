#!/usr/bin/env python3
"""validate-vui-conversation-design.py

Validate the artefact for the vui-conversation-design methodology against the schema in
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
        if hdr.get("methodology") != 'vui-conversation-design':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'spec':
            errs.append("__faion_header__.produces mismatch")
    if 'states' not in obj:
        errs.append(f"missing required field: " + 'states')
    if 'reprompt_cap' not in obj:
        errs.append(f"missing required field: " + 'reprompt_cap')
    if 'noise_test_conditions' not in obj:
        errs.append(f"missing required field: " + 'noise_test_conditions')


    states = obj.get("states") or []
    if not isinstance(states, list) or len(states) < 2:
        errs.append("states must have >=2")
    for i, s in enumerate(states):
        for k in ("allowed_intents", "voice_script", "screen_prompt", "no_match_handler", "ambiguous_handler"):
            if k not in s:
                errs.append("states[" + str(i) + "] missing " + k)
        vs = s.get("voice_script") or ""
        if len(vs) > 100:
            errs.append("states[" + str(i) + "].voice_script > 100 chars")
    if obj.get("reprompt_cap") != 3:
        errs.append("reprompt_cap must be 3")
    nt = obj.get("noise_test_conditions") or []
    if not isinstance(nt, list) or len(nt) < 3:
        errs.append("noise_test_conditions must have >=3")

    return errs


OK = {'__faion_header__': {'methodology': 'vui-conversation-design', 'version': '1.1.0', 'produces': 'spec'}, 'states': [{'id': 'ask-date', 'allowed_intents': ['provide-date'], 'voice_script': 'Which date works for you?', 'screen_prompt': 'Select a date below or say one out loud.', 'no_match_handler': "reprompt-1: 'I didn't catch that.'", 'ambiguous_handler': 'ask user to disambiguate'}, {'id': 'confirm', 'allowed_intents': ['confirm', 'deny'], 'voice_script': 'Book for Tuesday at 3 PM. Confirm?', 'screen_prompt': 'Confirm booking for Tuesday at 3 PM (Yes / No)', 'no_match_handler': "reprompt-1: 'Say yes or cancel.'", 'ambiguous_handler': "reprompt: 'Sorry, was that yes or cancel?'"}], 'reprompt_cap': 3, 'noise_test_conditions': ['quiet', 'ambient', 'kitchen']}
BAD = {'states': [{'id': 'x', 'voice_script': 'Please proceed to provide the date for your appointment booking confirmation'}], 'reprompt_cap': 7, 'noise_test_conditions': ['quiet']}


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
