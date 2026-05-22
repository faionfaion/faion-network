#!/usr/bin/env python3
"""validate-mocking-strategies.py — validate per-collaborator double-choice records.

Usage:
    validate-mocking-strategies.py --record records.json
    validate-mocking-strategies.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ALLOWED = {"dummy", "stub", "spy", "mock", "fake"}


def validate(records: list) -> list[dict]:
    v: list[dict] = []
    if not isinstance(records, list):
        return [{"rule": "schema", "message": "records must be an array"}]
    for i, r in enumerate(records):
        for k in ("collaborator", "doubleType", "patchTarget", "rationale"):
            if k not in r:
                v.append({"rule": "schema", "index": i, "message": f"missing {k}"})
        if r.get("doubleType") not in ALLOWED:
            v.append({"rule": "rule:r1", "index": i, "message": f"bad doubleType: {r.get('doubleType')!r}"})
        if len(r.get("rationale", "")) < 15:
            v.append({"rule": "rule:r4", "index": i, "message": "rationale too short"})
    return v


def self_test() -> int:
    good = [{"collaborator": "x.f", "doubleType": "stub", "patchTarget": "app.x",
             "isAsync": False, "rationale": "Need a state-returning collaborator only."}]
    assert not validate(good)
    bad = [{"collaborator": "x", "doubleType": "wrong", "patchTarget": "x", "rationale": "m"}]
    v = validate(bad)
    assert any("rule:r1" in x["rule"] for x in v)
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--record", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.record:
        ap.error("--record required")
        return 2
    data = json.loads(args.record.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
