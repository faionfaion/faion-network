#!/usr/bin/env python3
"""prio_method_and_wsjf.py — pick method + score WSJF if SAFe context.
Inputs:
  context.json   {item_count, release_or_backlog, has_effort_estimates,
                  has_kano_survey, has_reach_baseline, is_regulated,
                  is_safe_pi}
  items.csv      req_id, title, ub_value, time_crit, risk_oppty, job_size
Output: markdown to stdout (method decision + WSJF rank if applicable).
"""
import sys, json, csv


def pick(c: dict) -> str | None:
    if c.get("release_or_backlog") == "release":
        return "moscow"
    if c.get("is_safe_pi"):
        return "wsjf"
    if c.get("has_kano_survey"):
        return "kano"
    if c.get("has_reach_baseline") and c.get("item_count", 0) >= 30:
        return "rice"
    if c.get("is_regulated"):
        return "weighted_sum"
    if c.get("item_count", 0) < 30:
        return "value_effort"
    return None


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)

    ctx = json.load(open(sys.argv[1]))
    method = pick(ctx)
    print(f"# Prioritization Method Selection")
    print(f"- method: **{method or 'NONE — collect missing data first'}**")

    if method != "wsjf":
        sys.exit(0)

    if len(sys.argv) < 3:
        print("WSJF selected but no items.csv provided"); sys.exit(1)

    rows = list(csv.DictReader(open(sys.argv[2])))
    for r in rows:
        cod = float(r["ub_value"]) + float(r["time_crit"]) + float(r["risk_oppty"])
        js = max(float(r["job_size"]), 1.0)  # floor prevents tiny-job domination
        r["wsjf"] = cod / js
    rows.sort(key=lambda r: -float(r["wsjf"]))

    print("\n## WSJF Rank (CoD = UBV + TC + RR-OE; Job Size floored at 1)\n")
    print("| # | Req ID | UBV | TC | RR-OE | JS | WSJF |")
    print("|---|--------|-----|----|-------|----|------|")
    for i, r in enumerate(rows, 1):
        print(f"| {i} | {r['req_id']} | {r['ub_value']} | {r['time_crit']} | "
              f"{r['risk_oppty']} | {r['job_size']} | {float(r['wsjf']):.2f} |")


if __name__ == "__main__":
    main()
