#!/usr/bin/env python3
"""validate-python-web-frameworks.py — Validate a python-web-frameworks decision-record.

Inputs:
  - <record.json>  Path to the decision-record JSON file.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - record validates.
  1 - record violates schema.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FRAMEWORKS = {"django", "fastapi", "flask"}
RULES = {"r1-django-when-admin", "r2-fastapi-when-async", "r3-flask-when-small"}
RULE_TO_FRAMEWORK = {
    "r1-django-when-admin": "django",
    "r2-fastapi-when-async": "fastapi",
    "r3-flask-when-small": "flask",
}
DOWNSTREAM_RE = re.compile(r"^[a-z0-9-]+(/[a-z0-9-]+)*$")
ADR_RE = re.compile(r"^framework = (django|fastapi|flask)$")

VALID_FIXTURE = {
    "framework": "django",
    "triggered_by_rule": "r1-django-when-admin",
    "rationale": "Admin/CMS surface drives the schedule; django.admin saves ~2 sprints.",
    "non_functional_drivers": ["admin"],
    "downstream_methodologies": ["django-models", "django-api"],
    "adr_line": "framework = django",
}
INVALID_FIXTURE = {
    "framework": "litestar",
    "triggered_by_rule": "gut",
    "rationale": "fast",
    "downstream_methodologies": [],
    "adr_line": "use litestar",
}


def validate(rec: dict) -> list[str]:
    out: list[str] = []
    required = ["framework", "triggered_by_rule", "rationale", "downstream_methodologies", "adr_line"]
    for k in required:
        if k not in rec:
            out.append(f"missing required key: {k}")
    if out:
        return out
    if rec["framework"] not in FRAMEWORKS:
        out.append(f"framework not in {sorted(FRAMEWORKS)}")
    if rec["triggered_by_rule"] not in RULES:
        out.append(f"triggered_by_rule not in {sorted(RULES)}")
    if rec["triggered_by_rule"] in RULE_TO_FRAMEWORK and rec["framework"] != RULE_TO_FRAMEWORK[rec["triggered_by_rule"]]:
        out.append("rule/framework mismatch")
    if not isinstance(rec["rationale"], str) or len(rec["rationale"]) < 40:
        out.append("rationale must be >= 40 chars")
    downstream = rec["downstream_methodologies"]
    if not isinstance(downstream, list) or not downstream:
        out.append("downstream_methodologies must be non-empty list")
    else:
        for ds in downstream:
            if not DOWNSTREAM_RE.match(str(ds)):
                out.append(f"downstream slug invalid: {ds!r}")
        # framework consistency
        if rec.get("framework") == "django":
            if not any(str(s).startswith("django-") for s in downstream):
                out.append("django framework chosen but no django-* downstream methodologies listed")
        if rec.get("framework") == "fastapi":
            if not any("fastapi" in str(s) or "async" in str(s) for s in downstream):
                out.append("fastapi framework chosen but no fastapi/async downstream methodologies listed")
    if not ADR_RE.match(str(rec.get("adr_line", ""))):
        out.append(f"adr_line must match {ADR_RE.pattern!r}")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid fixture rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    path = Path(argv[1])
    if not path.is_file():
        sys.stderr.write(f"not a file: {path}\n")
        return 2
    try:
        rec = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(rec)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
