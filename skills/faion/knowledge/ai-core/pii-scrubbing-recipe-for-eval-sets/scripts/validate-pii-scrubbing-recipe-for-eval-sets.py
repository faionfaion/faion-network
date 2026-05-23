#!/usr/bin/env python3
"""Validate pii-scrub-spec artefact for the pii-scrubbing-recipe-for-eval-sets methodology.

USAGE:
    validate-pii-scrubbing-recipe-for-eval-sets.py <input.json>   Validate artefact.
    validate-pii-scrubbing-recipe-for-eval-sets.py --self-test    Run built-in fixtures.
    validate-pii-scrubbing-recipe-for-eval-sets.py --help         Show this help.

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

MODES = {"regex_only", "regex_plus_ml", "ml_plus_human_review"}
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def validate(s: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(s, dict):
        return ["root must be object"]
    for k in ("artefact_id", "owner", "scrub_strategy", "consent_label_field", "retention_days", "inputs_used", "version", "last_reviewed"):
        if k not in s:
            v.append(f"missing required field: {k}")
    owner = (s.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        v.append(f"owner forbidden value {owner!r} (rule r3)")
    sc = s.get("scrub_strategy") or {}
    if sc.get("mode") not in MODES:
        v.append(f"scrub_strategy.mode must be one of {sorted(MODES)}")
    if not isinstance(sc.get("rules"), list) or len(sc.get("rules") or []) < 1:
        v.append("scrub_strategy.rules must be non-empty list")
    rd = s.get("retention_days")
    if not isinstance(rd, int) or rd < 1 or rd > 3650:
        v.append("retention_days out of range [1,3650]")
    iu = s.get("inputs_used")
    if not isinstance(iu, list) or len(iu) < 1:
        v.append("inputs_used must be non-empty list (rule r5)")
    if isinstance(iu, list):
        for i, row in enumerate(iu):
            if not isinstance(row, dict) or "name" not in row or "source" not in row:
                v.append(f"inputs_used[{i}] must be object with name+source")
    if not SEMVER_RE.match(s.get("version", "") or ""):
        v.append("version must be semver (rule r4)")
    if not DATE_RE.match(s.get("last_reviewed", "") or ""):
        v.append("last_reviewed must be ISO date YYYY-MM-DD (rule r4)")
    return v


GOOD = {
    "artefact_id": "eval-set-prod-2026q2",
    "owner": "ruslan@faion.net",
    "scrub_strategy": {"mode": "regex_plus_ml", "rules": ["email", "phone", "credit_card"]},
    "consent_label_field": "user.consent.eval_v1",
    "retention_days": 365,
    "inputs_used": [{"name": "traffic_sample", "source": "warehouse://prod.traffic_2026q2"}],
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "artefact_id": "x",
    "owner": "team",
    "scrub_strategy": {"mode": "regex_only", "rules": []},
    "consent_label_field": "f",
    "retention_days": 99999,
    "inputs_used": [],
    "version": "v1",
    "last_reviewed": "yesterday",
}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy path failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("owner" in x for x in bad), "should flag owner"
    assert any("inputs_used" in x for x in bad), "should flag inputs_used"
    assert any("retention" in x for x in bad), "should flag retention"
    assert any("version" in x for x in bad), "should flag version"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-pii-scrubbing-recipe-for-eval-sets.py")
    p.add_argument("path", nargs="?", help="JSON artefact to validate")
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
