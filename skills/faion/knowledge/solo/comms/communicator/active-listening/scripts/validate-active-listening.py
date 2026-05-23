#!/usr/bin/env python3
"""validate-active-listening.py

Validate the RASA interview-script artefact against the schema in
02-output-contract.xml.

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

REQUIRED = [
    "goal",
    "interviewee_profile",
    "receive_opener",
    "appreciate_phrases",
    "summarize_starters",
    "ask_questions",
    "reflective_prompts",
    "silence_cue",
]
OPEN_OPENER = re.compile(r"^(What|How|Tell me|Walk me|Describe|Help me understand|In what way)")
REFLECT_ANCHOR = re.compile(r"(sounds like|seems like|I hear that)")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    qs = obj.get("ask_questions") or []
    if not isinstance(qs, list) or len(qs) < 5:
        errs.append("ask_questions must be list of >=5")
    else:
        for q in qs:
            if not isinstance(q, str) or not OPEN_OPENER.match(q):
                errs.append(f"closed/forbidden opener: {q!r}")
    ss = obj.get("summarize_starters") or []
    if not isinstance(ss, list) or len(ss) < 3:
        errs.append("summarize_starters must be list of >=3")
    rp = obj.get("reflective_prompts") or []
    if not isinstance(rp, list) or len(rp) < 1:
        errs.append("reflective_prompts must be list of >=1")
    else:
        for r in rp:
            if not REFLECT_ANCHOR.search(r):
                errs.append(f"reflective prompt missing anchor: {r!r}")
    return errs


OK = {
    "goal": "Understand why deployment takes 4 hours.",
    "interviewee_profile": "DevOps lead, skeptical of new tooling.",
    "receive_opener": "I'll close the laptop for the next 30 minutes.",
    "appreciate_phrases": ["I see.", "Go on."],
    "summarize_starters": [
        "So if I understand you...",
        "What I'm hearing is...",
        "Let me play that back...",
    ],
    "ask_questions": [
        "Walk me through what happens after the export.",
        "How does the current process affect mornings?",
        "What does a good day with this look like?",
        "Tell me about the last time it broke.",
        "In what way would you change it?",
    ],
    "reflective_prompts": ["It sounds like you're frustrated because the same step breaks weekly."],
    "silence_cue": "Pause 3-5 seconds after each answer.",
}
BAD = {"goal": "x", "ask_questions": ["Is the system slow?", "Do you like it?"]}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"ok rejected: {errs_ok}\n")
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
