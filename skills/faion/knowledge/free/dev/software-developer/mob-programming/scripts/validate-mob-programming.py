#!/usr/bin/env python3
"""validate-mob-programming.py — validate a mob-session checklist against the output schema.

Usage:
    validate-mob-programming.py --checklist file.json
    validate-mob-programming.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(data: dict) -> list[dict]:
    v: list[dict] = []
    done = data.get("done", "")
    if not (10 <= len(done) <= 200):
        v.append({"rule": "rule:r4", "message": f"done length {len(done)} not in [10,200]"})
    rot = data.get("rotationMinutes")
    if not isinstance(rot, int) or not 5 <= rot <= 10:
        v.append({"rule": "rule:r3", "message": f"rotationMinutes={rot} not in [5,10]"})
    roster = data.get("roster", [])
    if not 3 <= len(roster) <= 6:
        v.append({"rule": "skip", "message": f"roster size {len(roster)} not in [3,6]"})
    if not data.get("retroPlanned"):
        v.append({"rule": "rule:r6", "message": "retroPlanned is false/missing"})
    return v


def self_test() -> int:
    good = {"done": "Refactor PaymentService to use new fixture; tests green.",
            "rotationMinutes": 7, "roster": ["A", "B", "C", "D"],
            "parkingLot": [], "retroPlanned": True}
    assert not validate(good)
    bad = {"done": "x", "rotationMinutes": 30, "roster": ["A"], "retroPlanned": False}
    assert validate(bad)
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checklist", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.checklist:
        ap.error("--checklist required")
        return 2
    data = json.loads(args.checklist.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
