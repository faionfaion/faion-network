#!/usr/bin/env python3
"""Validate output contract for model-eval-control-bands artefact.

USAGE:
    validate-model-eval-control-bands.py <input.json>  Validate a record.
    validate-model-eval-control-bands.py --self-test   Run built-in fixture.
    validate-model-eval-control-bands.py --help        Show this help.

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
    for k in ("artefact_id", "owner", "decision", "rationale", "inputs_used", "version", "last_reviewed", "bands"):
        if k not in c:
            v.append(f"missing required field: {k}")
    owner = (c.get("owner") or "").strip()
    if not owner:
        v.append("owner empty (rule r3)")
    elif PLURAL_OWNER.match(owner):
        v.append(f"owner is plural/generic: {owner!r} (rule r3, fm-02)")
    rationale = c.get("rationale") or ""
    inputs = c.get("inputs_used") or []
    if isinstance(inputs, list) and rationale:
        names = [x.get("name", "") for x in inputs if isinstance(x, dict)]
        if names and not any(name and name in rationale for name in names):
            v.append("rationale must reference at least one input by name (rule r5, fm-03)")
    if not inputs:
        v.append("inputs_used is empty (rule r2, fm-01)")
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
    bands = c.get("bands") or []
    if not bands:
        v.append("bands must be non-empty")
    for i, b in enumerate(bands if isinstance(bands, list) else []):
        if not isinstance(b, dict):
            v.append(f"bands[{i}] must be object")
            continue
        for f in ("metric", "lower", "upper"):
            if f not in b:
                v.append(f"bands[{i}].{f} missing")
        if "lower" in b and "upper" in b and b["upper"] <= b["lower"]:
            v.append(f"bands[{i}] upper <= lower")
    return v


def _self_test() -> int:
    good = {
        "artefact_id": "ds1-bands",
        "owner": "sre-bot-ondemand@example.com",
        "decision": "Adopt bands for production v3",
        "rationale": "Based on metric-series-1 30-day variance, bands tightened by 10% to surface drift.",
        "inputs_used": [{"name": "metric-series-1", "source": "s3://obs/series.csv"}],
        "version": "1.0.0",
        "last_reviewed": date.today().isoformat(),
        "bands": [{"metric": "accuracy", "lower": 0.85, "upper": 0.92, "alerting": "page"}],
    }
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = dict(good); bad["owner"] = "team"
    assert any("plural" in x for x in validate(bad)), "should reject plural owner"
    bad = dict(good); bad["rationale"] = "Looks good."
    assert any("rationale" in x for x in validate(bad)), "should require input name in rationale"
    bad = dict(good); bad["last_reviewed"] = (date.today() - timedelta(days=120)).isoformat()
    assert any("last_reviewed" in x for x in validate(bad)), "should reject stale"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-model-eval-control-bands.py")
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
