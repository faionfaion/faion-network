#!/usr/bin/env python3
"""Validate corpus-discovery-report artefact.

USAGE:
    validate-rag-corpus-discovery-interview.py <input.json>
    validate-rag-corpus-discovery-interview.py --self-test
    validate-rag-corpus-discovery-interview.py --help

EXIT CODES:
    0 valid
    1 schema violation
    2 usage / unreadable

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
TS_RE = re.compile(r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$")
URL_RE = re.compile(r"^(https?://|s3://)")
LEADING_PHRASES = ("would you", "do you think you would", "wouldn't you", "do you usually", "what would you do if")
LABELS = {"hypothesis", "finding"}
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def validate(s: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(s, dict):
        return ["root must be object"]
    for k in ("artefact_id", "owner", "guide_prompts", "interviews", "quotes", "findings", "version", "last_reviewed"):
        if k not in s:
            v.append(f"missing required field: {k}")
    owner = (s.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        v.append(f"owner forbidden value {owner!r}")
    gp = s.get("guide_prompts")
    if not isinstance(gp, list) or not (5 <= len(gp) <= 9):
        v.append("guide_prompts must have 5..9 entries")
    if isinstance(gp, list):
        for i, p in enumerate(gp):
            pl = (p or "").lower()
            for lp in LEADING_PHRASES:
                if lp in pl:
                    v.append(f"guide_prompts[{i}] uses leading phrase {lp!r} (rule r2)")
    interviews = s.get("interviews")
    if not isinstance(interviews, list) or len(interviews) < 5:
        v.append("interviews must have ≥5 entries (rule r1)")
    if isinstance(interviews, list):
        for i, it in enumerate(interviews):
            if not isinstance(it, dict):
                v.append(f"interviews[{i}] must be object")
                continue
            if it.get("consent_recorded") is not True:
                v.append(f"interviews[{i}].consent_recorded must be true (rule r5)")
            if not URL_RE.match(it.get("recording_url") or ""):
                v.append(f"interviews[{i}].recording_url must be https:// or s3:// (rule r3)")
    quotes = s.get("quotes")
    if not isinstance(quotes, list) or len(quotes) < 5:
        v.append("quotes must have ≥5 entries (rule r4)")
    if isinstance(quotes, list):
        for i, q in enumerate(quotes):
            if not isinstance(q, dict):
                v.append(f"quotes[{i}] must be object")
                continue
            if not TS_RE.match(q.get("timestamp") or ""):
                v.append(f"quotes[{i}].timestamp must be HH:MM:SS (rule r4)")
            if not (q.get("transcript_id") or "").strip():
                v.append(f"quotes[{i}].transcript_id required (rule r4)")
    findings = s.get("findings")
    if not isinstance(findings, list) or len(findings) < 1:
        v.append("findings must be non-empty")
    if isinstance(findings, list):
        for i, f in enumerate(findings):
            if not isinstance(f, dict):
                v.append(f"findings[{i}] must be object")
                continue
            if f.get("label") not in LABELS:
                v.append(f"findings[{i}].label must be hypothesis|finding")
            eids = f.get("evidence_quote_ids") or []
            if f.get("label") == "finding":
                tids = {(eid.split("@")[0] if "@" in eid else eid) for eid in eids}
                if len(tids) < 2:
                    v.append(f"findings[{i}] labelled finding but evidence from <2 transcripts (rules r1,r4)")
    if not SEMVER_RE.match(s.get("version", "") or ""):
        v.append("version must be semver")
    if not DATE_RE.match(s.get("last_reviewed", "") or ""):
        v.append("last_reviewed must be ISO YYYY-MM-DD")
    return v


GOOD = {
    "artefact_id": "corpus-discovery-support-bot-2026q2",
    "owner": "ruslan@faion.net",
    "guide_prompts": [
        "Walk me through the last time you looked up a customer policy.",
        "Show me where the answer actually lives in your tools today.",
        "Tell me about a time the answer was wrong or stale.",
        "Describe how you decide which source to trust.",
        "Which document classes are licensed for embedding?",
    ],
    "interviews": [
        {"transcript_id": f"t{i}", "recording_url": f"s3://faion-research/2026q2/t{i}.m4a", "consent_recorded": True, "interviewee_role": "support-lead"}
        for i in range(1, 6)
    ],
    "quotes": [
        {"transcript_id": f"t{i}", "timestamp": "00:05:00", "text": f"quote {i}"}
        for i in range(1, 6)
    ],
    "findings": [
        {"id": "f1", "label": "finding", "evidence_quote_ids": ["t1@00:05:00", "t2@00:05:00"]},
        {"id": "f2", "label": "hypothesis", "evidence_quote_ids": ["t3@00:05:00"]},
    ],
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "artefact_id": "x",
    "owner": "team",
    "guide_prompts": ["would you pay for this?"],
    "interviews": [{"transcript_id": "t1", "recording_url": "x", "consent_recorded": False, "interviewee_role": "x"}],
    "quotes": [],
    "findings": [],
    "version": "v1",
    "last_reviewed": "yesterday",
}


def _self_test() -> int:
    errs = validate(GOOD)
    assert errs == [], f"happy failed: {errs}"
    bad = validate(BAD)
    assert any("interviews" in x for x in bad)
    assert any("consent" in x for x in bad)
    assert any("leading" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-rag-corpus-discovery-interview.py")
    p.add_argument("path", nargs="?")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
