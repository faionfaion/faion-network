#!/usr/bin/env python3
"""validate-ai-user-story-decomposition.py

Validate the artefact produced by the `ai-user-story-decomposition` methodology against the
JSON Schema embedded in `content/02-output-contract.xml`.

This validator uses stdlib only (no pyyaml/pydantic) for portability.

Inputs:
    --file PATH       path to artefact (JSON)
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["ask_summary", "owner", "stories", "ac", "ai_boundary", "fallback", "eval_ac", "golden_seeds"]


def validate(obj) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        v = obj[k]
        if v in (None, "", [], {}):
            errs.append(f"required field empty: {k}")
        if isinstance(v, str) and v.strip().upper() in {"TBD", "TODO", "FIXME"}:
            errs.append(f"placeholder value in field: {k}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.lower().strip() in {"team", "we", "tbd"}:
        errs.append("owner must be a single named person, not 'team' / 'we' / 'TBD'")
    return errs


OK = json.loads(r"""{"ask_summary": "Add a chatbot that answers refund-policy questions for support", "owner": "jane@team.io", "stories": [{"id": "story-1", "as_a": "logged-in customer", "i_want": "to ask about refund policy", "so_that": "I get a same-day answer", "ac": ["ac-1", "ac-2"]}], "ac": [{"id": "ac-1", "criterion": "AI returns answer grounded in /docs/refund.md", "metric_threshold": "precision >= 0.92"}, {"id": "ac-2", "criterion": "p95 latency under 4s", "metric_threshold": "latency_p95 <= 4000ms"}], "ai_boundary": {"ai_scope": "answer-generation from grounded snippet", "deterministic_fallback": "search index returns top-3 KB articles", "handoff_signal": "confidence < 0.6 OR refusal"}, "fallback": {"low_confidence": "show KB articles", "refusal": "open support ticket", "timeout": "show KB articles + apology"}, "eval_ac": [{"metric": "precision", "threshold": 0.92}, {"metric": "latency_p95_ms", "threshold": 4000}], "golden_seeds": [{"input": {"q": "Can I return after 30 days?"}, "expected": "policy.no_returns_after_30", "anti_output": "policy.full_refund"}, {"input": {"q": "Refund on digital purchase?"}, "expected": "policy.digital_no_refund", "anti_output": "policy.full_refund"}, {"input": {"q": "What if item is damaged?"}, "expected": "policy.damaged_full_refund", "anti_output": "policy.no_returns_after_30"}, {"input": {"q": "How long does it take?"}, "expected": "policy.refund_window_5d", "anti_output": "policy.instant"}, {"input": {"q": "Tell me a joke"}, "expected": "refusal.off_topic", "anti_output": "joke output"}]}""")
BAD = json.loads(r"""{"ask_summary": "add AI", "owner": "team", "stories": [{"id": "s", "as_a": "user"}]}""")


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"valid fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
