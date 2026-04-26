#!/usr/bin/env python3
"""integration_status.py — emit GREEN/YELLOW/RED per knowledge area from integrated/plan.yaml.

Input:  YAML file with a metrics: {} block containing numeric values per key.
Output: colour-coded status table + overall status.
Exit:   1 if overall is RED (wire to CI for alerting).

Usage:  python integration_status.py [path/to/integrated/plan.yaml]
"""
from __future__ import annotations
import pathlib
import sys
import yaml

THRESHOLDS: dict[str, list[tuple[float, str]]] = {
    "schedule_slip_days":  [(0, "GREEN"), (5, "YELLOW"), (15, "RED")],
    "budget_overrun_pct":  [(0.00, "GREEN"), (0.05, "YELLOW"), (0.10, "RED")],
    "open_high_risks":     [(0, "GREEN"), (2, "YELLOW"), (5, "RED")],
    "scope_change_pct":    [(0.00, "GREEN"), (0.10, "YELLOW"), (0.20, "RED")],
    "defect_rate_pct":     [(0.00, "GREEN"), (0.05, "YELLOW"), (0.10, "RED")],
}


def status_for(value: float, ladder: list[tuple[float, str]]) -> str:
    label = ladder[0][1]
    for threshold, lbl in ladder:
        if value >= threshold:
            label = lbl
    return label


def main(path: str = "integrated/plan.yaml") -> int:
    plan = yaml.safe_load(pathlib.Path(path).read_text())
    metrics = plan.get("metrics", {})
    print(f"{'Area':<22} {'Value':>10}  Status")
    print("-" * 42)
    overall = "GREEN"
    rank = {"GREEN": 0, "YELLOW": 1, "RED": 2}
    for area, ladder in THRESHOLDS.items():
        if area not in metrics:
            print(f"{area:<22} {'MISSING':>10}  RED")
            overall = "RED"
            continue
        v = float(metrics[area])
        s = status_for(v, ladder)
        print(f"{area:<22} {v:>10.2f}  {s}")
        if rank[s] > rank[overall]:
            overall = s
    print("-" * 42)
    print(f"{'OVERALL':<22} {'':>10}  {overall}")
    return 0 if overall != "RED" else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
