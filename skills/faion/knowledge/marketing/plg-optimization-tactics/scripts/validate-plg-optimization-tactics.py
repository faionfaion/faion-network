#!/usr/bin/env python3
"""validate-plg-optimization-tactics.py

Validate the ranked-backlog artefact for the plg-optimization-tactics methodology
against the schema in content/02-output-contract.xml.

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

BANNED_CTA = re.compile(r"(?i)(upgrade now|premium plan|get more features|unlock premium)")
STAGES = {"activation", "free-to-paid", "expansion"}
ICE_KEYS = {"impact", "confidence", "ease"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("funnel_stage", "baseline", "tactics", "generated_at"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("funnel_stage") not in STAGES:
        errs.append(f"funnel_stage must be one of {sorted(STAGES)}")
    baseline = obj.get("baseline") or {}
    for k in ("metric", "value", "as_of"):
        if k not in baseline:
            errs.append(f"baseline missing: {k}")
    tactics = obj.get("tactics") or []
    if not isinstance(tactics, list) or not tactics:
        errs.append("tactics must be non-empty array")
    for i, t in enumerate(tactics if isinstance(tactics, list) else []):
        for k in ("name", "hypothesis", "source_section", "ice", "instrumentation"):
            if k not in t:
                errs.append(f"tactics[{i}] missing: {k}")
        ice = t.get("ice") or {}
        if set(ice.keys()) & ICE_KEYS != ICE_KEYS:
            errs.append(f"tactics[{i}].ice missing keys: {ICE_KEYS - set(ice.keys())}")
        for k in ICE_KEYS & set(ice.keys()):
            v = ice[k]
            if not (isinstance(v, int) and 1 <= v <= 10):
                errs.append(f"tactics[{i}].ice.{k} must be int 1..10")
        cta = t.get("cta_text")
        if cta and BANNED_CTA.search(cta):
            errs.append(f"tactics[{i}].cta_text matches banned phrase: {cta!r}")
    return errs


OK = {
    "funnel_stage": "free-to-paid",
    "baseline": {"metric": "free_to_paid_30d_pct", "value": 4.2, "as_of": "2026-05-20"},
    "tactics": [
        {
            "name": "Prompt at 80% storage",
            "hypothesis": "Earlier prompt catches users before frustration.",
            "source_section": "upgrade-prompt-rules",
            "ice": {"impact": 7, "confidence": 7, "ease": 9},
            "instrumentation": "PostHog event upgrade_prompt_shown",
            "cta_text": "Teams like Acme save 10h/week on Team plan.",
        }
    ],
    "generated_at": "2026-05-23T10:00:00Z",
}
BAD = {"funnel_stage": "free-to-paid", "tactics": [{"name": "x", "cta_text": "Upgrade Now"}]}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
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
        sys.stderr.write(f"not a file: {p}\n"); return 2
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
