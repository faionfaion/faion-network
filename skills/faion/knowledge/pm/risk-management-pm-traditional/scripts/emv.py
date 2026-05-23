#!/usr/bin/env python3
"""emv.py

Score a Markdown risk register and exit non-zero if any active row has
score >= 0.15 (High/Critical). P and I must be one of: VL, L, M, H, VH.

Inputs:
    --file PATH       path to RISK-REGISTER.md
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = OK (no critical untriaged risks)
    1 = critical risks present
    2 = usage / unreadable

P weights: VL=0.05, L=0.20, M=0.40, H=0.60, VH=0.85
I weights: VL=0.025, L=0.075, M=0.15, H=0.30, VH=0.50
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

P_WEIGHT = {"VL": 0.05, "L": 0.20, "M": 0.40, "H": 0.60, "VH": 0.85}
I_WEIGHT = {"VL": 0.025, "L": 0.075, "M": 0.15, "H": 0.30, "VH": 0.50}
CRIT_THRESHOLD = 0.15
ROW_RE = re.compile(
    r"\|\s*(R-\d+)\s*\|[^|]*\|[^|]*\|\s*([A-Z]{1,2})\s*\|\s*([A-Z]{1,2})\s*\|"
)

FIXTURE_OK = "| R-001 | desc | people | L | L | 0.04 |"
FIXTURE_CRIT = "| R-002 | desc | people | H | H | 0.18 |"


def score(text: str) -> list[tuple[str, str, str, float]]:
    crit: list[tuple[str, str, str, float]] = []
    for m in ROW_RE.finditer(text):
        rid, p_str, i_str = m.group(1), m.group(2), m.group(3)
        p = P_WEIGHT.get(p_str)
        i = I_WEIGHT.get(i_str)
        if p is None or i is None:
            continue
        s = p * i
        if s >= CRIT_THRESHOLD:
            crit.append((rid, p_str, i_str, round(s, 4)))
    return crit


def self_test() -> int:
    if score(FIXTURE_OK):
        sys.stderr.write("self-test FAIL: OK fixture flagged\n")
        return 1
    if not score(FIXTURE_CRIT):
        sys.stderr.write("self-test FAIL: CRIT fixture missed\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="register markdown path")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixture")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    crit = score(p.read_text())
    if crit:
        sys.stdout.write("CRITICAL risks requiring immediate triage:\n")
        for rid, p_s, i_s, s in crit:
            sys.stdout.write(f"  {rid}: P={p_s} I={i_s} score={s}\n")
        return 1
    sys.stdout.write(f"OK no critical risks above threshold {CRIT_THRESHOLD}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
