#!/usr/bin/env python3
"""Validate output contract for model-migration-checklist artefact.

USAGE:
    validate-model-migration-checklist.py <input.json>   Validate a record.
    validate-model-migration-checklist.py --self-test    Run built-in fixture.
    validate-model-migration-checklist.py --help         Show this help.

EXIT CODES:
    0 on pass
    1 on schema violation
    2 on usage error

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

PLURAL_OWNER = re.compile(r"^(team|we|us|engineering|the (team|squad|group))$", re.I)
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
STALE_DAYS = 90


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("artefact_id", "owner", "decision", "rationale", "inputs_used", "version", "last_reviewed", "from_model", "to_model", "eval_baseline_id"):
        if k not in c:
            v.append(f"missing required field: {k}")
    owner = (c.get("owner") or "").strip()
    if not owner:
        v.append("owner empty (rule r3)")
    elif PLURAL_OWNER.match(owner):
        v.append(f"owner is plural/generic: {owner!r} (rule r3)")
    rationale = c.get("rationale") or ""
    inputs = c.get("inputs_used") or []
    if isinstance(inputs, list) and rationale:
        names = [x.get("name", "") for x in inputs if isinstance(x, dict)]
        if names and not any(name and name in rationale for name in names):
            v.append("rationale must reference at least one input by name (rule r5)")
    if not inputs:
        v.append("inputs_used is empty (rule r2)")
    ver = c.get("version") or ""
    if not SEMVER.match(ver):
        v.append("version must be semver X.Y.Z (rule r4)")
    lr = c.get("last_reviewed")
    if lr:
        try:
            d = date.fromisoformat(lr)
            if date.today() - d > timedelta(days=STALE_DAYS):
                v.append(f"last_reviewed older than {STALE_DAYS} days (rule r4)")
        except ValueError:
            v.append("last_reviewed must be ISO-8601 date")
    if c.get("from_model") == c.get("to_model") and c.get("from_model"):
        v.append("from_model must differ from to_model (rule r1: bound scope)")
    if not c.get("eval_baseline_id"):
        v.append("eval_baseline_id required — without an eval, the migration has no gate")
    return v


def _self_test() -> int:
    good = {
        "artefact_id": "openai-to-anthropic-q2-2026",
        "owner": "alice@example.com",
        "decision": "Migrate gpt-4o → claude-sonnet-4-6 behind canary",
        "rationale": "Per prompt-set-v3 and gold-eval-q2, accuracy parity at lower cost.",
        "inputs_used": [
            {"name": "prompt-set-v3", "source": "repo://prompts/v3"},
            {"name": "gold-eval-q2", "source": "s3://eval/q2.jsonl"},
        ],
        "version": "1.0.0",
        "last_reviewed": date.today().isoformat(),
        "from_model": "gpt-4o",
        "to_model": "claude-sonnet-4-6",
        "eval_baseline_id": "gold-eval-q2",
    }
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = dict(good); bad["owner"] = "team"
    assert any("plural" in x for x in validate(bad)), "should reject plural owner"
    bad = dict(good); bad["from_model"] = "claude-sonnet-4-6"
    assert any("differ" in x for x in validate(bad)), "should reject same-model migration"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-model-migration-checklist.py")
    p.add_argument("path", nargs="?", help="JSON record to validate")
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
