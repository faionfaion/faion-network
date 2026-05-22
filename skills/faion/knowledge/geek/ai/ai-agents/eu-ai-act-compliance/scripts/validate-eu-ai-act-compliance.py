#!/usr/bin/env python3
"""validate-eu-ai-act-compliance.py

Purpose:
    Validate a risk-classification report against the schema in
    content/02-output-contract.xml: risk tier is one of four enums, articles
    follow the `Article N` pattern, reviewer sign-off block exists.

Inputs:
    --file PATH      Risk-classification JSON
    --self-test      Validate the built-in smoke fixture

Outputs:
    Stdout: validation report
    Exit 0 on pass, 1 on failure, 2 on usage error.

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RISK_TIER = {"unacceptable", "high", "limited", "minimal"}
ARTICLE_RE = re.compile(r"^Article \d+(\(\d+\))?$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if obj.get("risk_tier") not in RISK_TIER:
        errs.append(f"risk_tier: {obj.get('risk_tier')!r} not in {sorted(RISK_TIER)}")
    articles = obj.get("applicable_articles")
    if not isinstance(articles, list) or not articles:
        errs.append("applicable_articles: must be non-empty list")
    else:
        for i, a in enumerate(articles):
            if not isinstance(a, str) or not ARTICLE_RE.match(a):
                errs.append(f"applicable_articles[{i}]: {a!r} does not match 'Article N' pattern")
    rationale = obj.get("rationale")
    if not isinstance(rationale, str) or len(rationale) < 20:
        errs.append("rationale: must be string >= 20 chars")
    if not isinstance(obj.get("requires_conformity_assessment"), bool):
        errs.append("requires_conformity_assessment: must be boolean")
    sign = obj.get("reviewer_signoff")
    if not isinstance(sign, dict):
        errs.append("reviewer_signoff: required mapping missing")
    else:
        if not sign.get("reviewer_id"):
            errs.append("reviewer_signoff.reviewer_id: missing")
        if not ISO_RE.match(sign.get("signed_at", "")):
            errs.append("reviewer_signoff.signed_at: must be ISO-8601 UTC (YYYY-MM-DDThh:mm:ssZ)")
    return errs


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--file", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    target = SMOKE if args.self_test else args.file
    if target is None:
        p.error("either --file or --self-test must be given")
    if not target.exists():
        sys.stdout.write(f"FAIL: file not found: {target}\n")
        return 1
    obj = json.loads(target.read_text(encoding="utf-8"))
    obj = {k: v for k, v in obj.items() if not k.startswith("_")}
    errs = validate(obj)
    if errs:
        sys.stdout.write(f"FAIL: {target}\n")
        for e in errs:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write(f"OK: {target}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
