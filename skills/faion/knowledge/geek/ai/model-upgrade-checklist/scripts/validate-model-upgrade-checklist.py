#!/usr/bin/env python3
"""Validate output contract for model-upgrade-checklist artefact.

USAGE:
    validate-model-upgrade-checklist.py <input.json>   Validate a record.
    validate-model-upgrade-checklist.py --self-test    Run built-in fixture.
    validate-model-upgrade-checklist.py --help         Show this help.

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
    for k in ("artefact_id", "owner", "decision", "rationale", "inputs_used", "version", "last_reviewed", "current_model", "target_model", "eval_baseline_id", "rollout"):
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
    if c.get("current_model") == c.get("target_model") and c.get("current_model"):
        v.append("current_model must differ from target_model (rule r1: bound scope)")
    rollout = c.get("rollout") or {}
    if not rollout.get("kill_switch_armed"):
        v.append("rollout.kill_switch_armed must be true")
    if not rollout.get("stages"):
        v.append("rollout.stages must be non-empty")
    return v


def _self_test() -> int:
    good = {
        "artefact_id": "sonnet-4.5-to-4.6-q2-2026",
        "owner": "alice@example.com",
        "decision": "Upgrade Sonnet 4.5 → 4.6 behind canary",
        "rationale": "Per prompt-set-v3 and gold-eval-q2, latency improves with no quality regression.",
        "inputs_used": [
            {"name": "prompt-set-v3", "source": "repo://prompts/v3"},
            {"name": "gold-eval-q2", "source": "s3://eval/q2.jsonl"},
        ],
        "version": "1.0.0",
        "last_reviewed": date.today().isoformat(),
        "current_model": "claude-sonnet-4-5",
        "target_model": "claude-sonnet-4-6",
        "eval_baseline_id": "gold-eval-q2",
        "rollout": {"stages": ["shadow", "canary_5pct", "100pct"], "kill_switch_armed": True},
    }
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = dict(good); bad["owner"] = "team"
    assert any("plural" in x for x in validate(bad)), "should reject plural owner"
    bad = dict(good); bad["rollout"] = {"stages": [], "kill_switch_armed": False}
    out = validate(bad)
    assert any("kill_switch" in x for x in out), "should reject disarmed kill switch"
    assert any("stages" in x for x in out), "should reject empty stages"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-model-upgrade-checklist.py")
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
