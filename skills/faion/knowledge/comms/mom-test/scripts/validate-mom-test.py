#!/usr/bin/env python3
"""validate-mom-test.py

Validate the artefact for the mom-test methodology against the schema in
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
import sys
from pathlib import Path

REQUIRED = ['hypothesis', 'persona', 'questions', 'current_spend_question', 'signal_classifier_output']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    qs = obj.get("questions") or []
    import re
    open_pat = re.compile(r"^(Tell me|Walk me|How|What|When)")
    if not isinstance(qs, list) or len(qs) < 5:
        errs.append("questions must be list of >=5")
    else:
        for q in qs:
            if not open_pat.match(q):
                errs.append(f"non past-tense/current-state question: {q!r}")
    sco = obj.get("signal_classifier_output") or {}
    share = sco.get("interviewer_word_share")
    if share is not None and share > 0.20:
        errs.append("interviewer_word_share > 0.20")

    return errs


OK = {
    "hypothesis": "SMB retailers spend >4h/week reconciling inventory.",
    "persona": "SMB retailer, 10-50 staff, Shopify + spreadsheet.",
    "questions": [
        "Tell me about the last reconciliation.",
        "Walk me through your close routine.",
        "How long did it take?",
        "What happens when off?",
        "When did you last try to fix?"
    ],
    "current_spend_question": "What are you spending today on tools or staff time?",
    "signal_classifier_output": {
        "compliment_count": 1,
        "fact_count": 9,
        "commitment_count": 2,
        "interviewer_word_share": 0.17
    }
}
BAD = {
    "hypothesis": "x",
    "questions": [
        "Would you use it?"
    ]
}


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
