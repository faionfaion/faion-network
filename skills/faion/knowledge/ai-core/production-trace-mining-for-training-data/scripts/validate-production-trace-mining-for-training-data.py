#!/usr/bin/env python3
"""Validate trace-mining-spec artefact.

USAGE:
    validate-production-trace-mining-for-training-data.py <input.json>
    validate-production-trace-mining-for-training-data.py --self-test
    validate-production-trace-mining-for-training-data.py --help

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

TRIG_KINDS = {"event", "threshold", "schedule"}
LABEL_MODES = {"heuristic", "llm_judge", "heuristic_plus_judge"}
SCHEME_RE = re.compile(r"^(git|warehouse|s3)://")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
FORBIDDEN_TRIGGERS = ("when needed", "as required", "ad hoc", "when it feels")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def validate(s: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(s, dict):
        return ["root must be object"]
    for k in ("artefact_id", "owner", "trigger", "scrub_spec_ref", "label_inference", "capabilities", "retention_days", "version", "last_reviewed"):
        if k not in s:
            v.append(f"missing required field: {k}")
    owner = (s.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        v.append(f"owner forbidden value {owner!r} (rule r4)")
    tr = s.get("trigger") or {}
    if tr.get("kind") not in TRIG_KINDS:
        v.append(f"trigger.kind must be one of {sorted(TRIG_KINDS)}")
    val = (tr.get("value") or "").lower()
    for bad in FORBIDDEN_TRIGGERS:
        if bad in val:
            v.append(f"trigger.value contains forbidden phrase {bad!r} (rule r1)")
    if not SCHEME_RE.match(s.get("scrub_spec_ref", "") or ""):
        v.append("scrub_spec_ref must be git://, warehouse://, or s3://")
    li = s.get("label_inference") or {}
    if li.get("mode") not in LABEL_MODES:
        v.append(f"label_inference.mode must be one of {sorted(LABEL_MODES)}")
    if not (li.get("rules_ref") or "").strip():
        v.append("label_inference.rules_ref must be non-empty (rule r3)")
    if not isinstance(s.get("capabilities"), list) or len(s.get("capabilities") or []) < 1:
        v.append("capabilities must be non-empty list")
    rd = s.get("retention_days")
    if not isinstance(rd, int) or rd < 1 or rd > 3650:
        v.append("retention_days out of range [1,3650]")
    if not SEMVER_RE.match(s.get("version", "") or ""):
        v.append("version must be semver")
    if not DATE_RE.match(s.get("last_reviewed", "") or ""):
        v.append("last_reviewed must be ISO date YYYY-MM-DD")
    return v


GOOD = {
    "artefact_id": "trace-mining-support-2026q2",
    "owner": "ruslan@faion.net",
    "trigger": {"kind": "schedule", "value": "monthly: 1st"},
    "scrub_spec_ref": "git://faion/specs/scrub.json",
    "label_inference": {"mode": "heuristic_plus_judge", "rules_ref": "git://faion/labels/x.yaml"},
    "capabilities": ["intent_classification"],
    "retention_days": 365,
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "artefact_id": "x",
    "owner": "team",
    "trigger": {"kind": "event", "value": "when needed"},
    "scrub_spec_ref": "",
    "label_inference": {"mode": "heuristic", "rules_ref": ""},
    "capabilities": [],
    "retention_days": -1,
    "version": "v1",
    "last_reviewed": "yesterday",
}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("owner" in x for x in bad)
    assert any("trigger.value" in x for x in bad)
    assert any("scrub_spec_ref" in x for x in bad)
    assert any("retention" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-production-trace-mining-for-training-data.py")
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
