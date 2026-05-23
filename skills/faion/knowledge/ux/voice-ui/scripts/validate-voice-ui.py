#!/usr/bin/env python3
"""validate-voice-ui.py

Validate the artefact for the voice-ui methodology against the schema in
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
PLATFORMS = {'alexa', 'ivr', 'siri', 'custom-llm', 'google-actions'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'voice-ui':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'spec':
            errs.append("__faion_header__.produces mismatch")
    if 'platform' not in obj:
        errs.append(f"missing required field: " + 'platform')
    if 'intents' not in obj:
        errs.append(f"missing required field: " + 'intents')
    if 'barge_in' not in obj:
        errs.append(f"missing required field: " + 'barge_in')


    if obj.get("platform") not in PLATFORMS:
        errs.append("platform invalid")
    intents = obj.get("intents") or []
    if not isinstance(intents, list) or not intents:
        errs.append("intents must be non-empty list")
    for i, it in enumerate(intents):
        utt = it.get("sample_utterances") or []
        if len(utt) < 3:
            errs.append("intents[" + str(i) + "].sample_utterances must have >=3")
        prompt = it.get("prompt") or ""
        if len(prompt) > 100:
            errs.append("intents[" + str(i) + "].prompt > 100 chars")
        el = it.get("error_ladder") or []
        if len(el) != 3:
            errs.append("intents[" + str(i) + "].error_ladder must have exactly 3 tiers")
        if it.get("irreversible") is True and not it.get("confirmation_prompt"):
            errs.append("intents[" + str(i) + "] irreversible without confirmation_prompt")
    if obj.get("barge_in") is not True:
        errs.append("barge_in must be true")

    return errs


OK = {'__faion_header__': {'methodology': 'voice-ui', 'version': '1.1.0', 'produces': 'spec'}, 'platform': 'custom-llm', 'intents': [{'name': 'schedule-appointment', 'sample_utterances': ['book a meeting Tuesday at 3', 'schedule for tomorrow morning', 'set up an appointment'], 'slots': [{'name': 'datetime', 'type': 'datetime'}], 'prompt': 'When should I schedule it?', 'error_ladder': ["I didn't catch the time. Try again?", "You can say something like 'Tuesday at 3 PM'.", 'Let me hand off to a human.'], 'irreversible': False}, {'name': 'send-payment', 'sample_utterances': ['send $50 to Alice', 'pay Bob fifty bucks', 'transfer $100 to mom'], 'slots': [{'name': 'amount', 'type': 'currency'}, {'name': 'recipient', 'type': 'contact'}], 'prompt': 'Send $50 to Alice. Confirm?', 'error_ladder': ['Say yes to confirm, or cancel.', "You can say 'yes' or 'cancel'.", 'Cancelling. Try again from the start.'], 'irreversible': True, 'confirmation_prompt': 'Yes / Cancel'}], 'barge_in': True}
BAD = {'platform': 'custom-llm', 'intents': [{'name': 'pay', 'sample_utterances': ['pay'], 'prompt': 'I will now proceed to process your payment immediately', 'error_ladder': ["didn't catch"]}], 'barge_in': False}


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
