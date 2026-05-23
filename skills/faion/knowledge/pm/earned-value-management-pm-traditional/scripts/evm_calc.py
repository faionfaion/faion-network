#!/usr/bin/env python3
"""evm_calc.py — deterministic EVM index computation from YAML inputs.

Usage: python evm_calc.py baseline.yaml actuals.yaml

baseline.yaml:
  bac: 100000
  pv_curve:
    "2024-03": 50000
    "2024-04": 75000
  work_packages:
    - id: WP-1.1
      budget: 30000
      earning_rule: "0/100"

actuals.yaml:
  period_end: "2024-03"
  actual_cost_to_date: 55000
  work_packages:
    - id: WP-1.1
      pct_complete: 1.0   # 0/100 rule: 0.0 or 1.0
      accepted: true

Output: JSON with BAC, PV, EV, AC, SV, CV, SPI, CPI, EAC, ETC, VAC, TCPI.
Exits 1 if SPI < 0.85 or CPI < 0.85 (RED threshold).
"""
import json
import sys
import yaml
import pathlib


def main(baseline_path: str, actuals_path: str) -> int:
    B = yaml.safe_load(pathlib.Path(baseline_path).read_text())
    A = yaml.safe_load(pathlib.Path(actuals_path).read_text())

    BAC = float(B["bac"])
    period = A["period_end"]
    PV = float(B["pv_curve"][period])
    AC = float(A["actual_cost_to_date"])

    # Build work-package index from baseline
    wp_budget = {wp["id"]: float(wp["budget"]) for wp in B.get("work_packages", [])}

    # EV = sum of budget * pct_complete for accepted work packages only
    EV = 0.0
    for wp in A.get("work_packages", []):
        if wp.get("accepted", False):
            budget = wp_budget.get(wp["id"], 0.0)
            EV += budget * float(wp.get("pct_complete", 0.0))

    SV = EV - PV
    CV = EV - AC
    SPI = EV / PV if PV else None
    CPI = EV / AC if AC else None
    EAC = BAC / CPI if CPI else None
    ETC = (EAC - AC) if EAC is not None else None
    VAC = (BAC - EAC) if EAC is not None else None
    TCPI = (BAC - EV) / (BAC - AC) if (BAC - AC) != 0 else None

    out = {
        "period_end": period,
        "BAC": BAC,
        "PV": PV,
        "EV": round(EV, 2),
        "AC": AC,
        "SV": round(SV, 2),
        "CV": round(CV, 2),
        "SPI": round(SPI, 4) if SPI is not None else None,
        "CPI": round(CPI, 4) if CPI is not None else None,
        "EAC": round(EAC, 2) if EAC is not None else None,
        "ETC": round(ETC, 2) if ETC is not None else None,
        "VAC": round(VAC, 2) if VAC is not None else None,
        "TCPI": round(TCPI, 4) if TCPI is not None else None,
    }
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")

    # Exit 1 on RED threshold
    red = (SPI is not None and SPI < 0.85) or (CPI is not None and CPI < 0.85)
    return 1 if red else 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: evm_calc.py baseline.yaml actuals.yaml", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
