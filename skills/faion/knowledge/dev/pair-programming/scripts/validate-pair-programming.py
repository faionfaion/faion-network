#!/usr/bin/env python3
"""validate-pair-programming.py — validate pair-session protocol JSON.

Usage:
    validate-pair-programming.py --protocol file.json
    validate-pair-programming.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MODES = {"classic", "ping-pong", "strong-style", "tour-guide"}


def validate(d: dict) -> list[dict]:
    v: list[dict] = []
    if d.get("mode") not in MODES:
        v.append({"rule": "rule:r4", "message": f"mode {d.get('mode')!r} not in canonical set"})
    roster = d.get("roster", [])
    if len(roster) != 2:
        v.append({"rule": "schema", "message": f"roster must have 2 entries"})
    pom = d.get("pomodoroMinutes")
    if not isinstance(pom, int) or not 20 <= pom <= 30:
        v.append({"rule": "rule:r5", "message": f"pomodoroMinutes={pom} not in [20,30]"})
    has_ai = any(p.get("isAI") for p in roster)
    if has_ai and not d.get("humanIsDriverIfAINavigator", False):
        v.append({"rule": "rule:r2", "message": "AI in roster but humanIsDriverIfAINavigator is not true"})
    return v


def self_test() -> int:
    good = {"mode": "strong-style",
            "roster": [{"name": "R", "isAI": False}, {"name": "C", "isAI": True}],
            "pomodoroMinutes": 25, "humanIsDriverIfAINavigator": True,
            "sessionMdPath": "x.md"}
    assert not validate(good)
    bad = {"mode": "X", "roster": [], "pomodoroMinutes": 60}
    assert validate(bad)
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--protocol", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.protocol:
        ap.error("--protocol required")
        return 2
    d = json.loads(args.protocol.read_text(encoding="utf-8"))
    v = validate(d)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
