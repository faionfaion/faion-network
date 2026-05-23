#!/usr/bin/env python3
"""cpm.py

Compute critical path from a CSV activity list and print activities on
the critical path along with total project duration.

CSV columns (header required): id, predecessors (semicolon-separated), duration

Inputs:
    --file PATH       CSV path
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = ok
    1 = cycle or invalid input
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import defaultdict
from pathlib import Path

FIXTURE = """id,predecessors,duration
A01,,3
A02,A01,6
A03,A02,1
A04,A01,2
A05,A04;A03,1
"""


def cpm(rows: list[dict[str, str]]) -> tuple[float, list[str]]:
    dur = {r["id"]: float(r["duration"]) for r in rows}
    pred: dict[str, list[str]] = defaultdict(list)
    succ: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        rid = r["id"]
        preds = [p for p in r["predecessors"].split(";") if p.strip()]
        for p in preds:
            pred[rid].append(p)
            succ[p].append(rid)
    # topological sort
    indeg = {rid: len(pred[rid]) for rid in dur}
    order: list[str] = []
    queue = [rid for rid in dur if indeg[rid] == 0]
    while queue:
        n = queue.pop(0)
        order.append(n)
        for s in succ[n]:
            indeg[s] -= 1
            if indeg[s] == 0:
                queue.append(s)
    if len(order) != len(dur):
        raise ValueError("cycle detected")
    es: dict[str, float] = {rid: 0.0 for rid in dur}
    ef: dict[str, float] = {rid: 0.0 for rid in dur}
    for n in order:
        es[n] = max((ef[p] for p in pred[n]), default=0.0)
        ef[n] = es[n] + dur[n]
    project_end = max(ef.values())
    lf = {rid: project_end for rid in dur}
    ls = {rid: 0.0 for rid in dur}
    for n in reversed(order):
        if succ[n]:
            lf[n] = min(ls[s] for s in succ[n])
        ls[n] = lf[n] - dur[n]
    critical = [rid for rid in order if abs(es[rid] - ls[rid]) < 1e-9]
    return project_end, critical


def self_test() -> int:
    rows = list(csv.DictReader(io.StringIO(FIXTURE)))
    dur, crit = cpm(rows)
    if abs(dur - 11.0) > 1e-9 or crit != ["A01", "A02", "A03", "A05"]:
        sys.stderr.write(f"self-test FAIL: got dur={dur}, crit={crit}\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="CSV activity list path")
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
    rows = list(csv.DictReader(p.open()))
    try:
        dur, crit = cpm(rows)
    except ValueError as e:
        sys.stderr.write(f"error: {e}\n")
        return 1
    sys.stdout.write(f"project_duration={dur}\n")
    sys.stdout.write(f"critical_path={','.join(crit)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
