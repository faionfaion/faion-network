#!/usr/bin/env python3
"""benefits_status.py — realization % and RAG from measurements.yaml.

Usage: python benefits_status.py register.yaml measurements.yaml PERIOD
  PERIOD format: M1, M3, M6, Y1, Y2

register.yaml:
  benefits:
    - id: B-01
      baseline: 100   # null if not yet measured
      target: 200
      realization_curve:
        - period: M3
          expected: 0.30  # expected fraction of full benefit

measurements.yaml:
  measurements:
    - benefit_id: B-01
      period: M3
      actual: 145
      evidence_url: https://bi.example.com/report/123

RAG: GREEN if actual >= 90% of expected; YELLOW 70-90%; RED < 70%.
Exits 1 if any benefit is RED.
"""
import json
import sys
import yaml
import pathlib


def rag(actual_pct: float, expected_pct: float) -> str:
    if expected_pct == 0:
        return "N/A"
    ratio = actual_pct / expected_pct
    if ratio >= 0.90:
        return "GREEN"
    if ratio >= 0.70:
        return "YELLOW"
    return "RED"


def main(register_path: str, measurements_path: str, period: str) -> int:
    register = yaml.safe_load(pathlib.Path(register_path).read_text())
    measurements = yaml.safe_load(pathlib.Path(measurements_path).read_text())

    R = {b["id"]: b for b in register.get("benefits", [])}
    M = [m for m in measurements.get("measurements", []) if m["period"] == period]

    out = []
    has_red = False

    for m in M:
        b = R.get(m["benefit_id"])
        if not b:
            continue
        baseline = b.get("baseline")
        target = b.get("target")
        if baseline is None or target is None or target == baseline:
            out.append({"id": b["id"], "rag": "N/A", "note": "baseline or target missing"})
            continue

        curve_entry = next(
            (p for p in b.get("realization_curve", []) if p["period"] == period), None
        )
        expected_pct = curve_entry["expected"] if curve_entry else 0.0
        actual_pct = (m["actual"] - baseline) / (target - baseline)
        status = rag(actual_pct, expected_pct)
        if status == "RED":
            has_red = True

        out.append({
            "id": b["id"],
            "period": period,
            "actual_pct": round(actual_pct, 3),
            "expected_pct": expected_pct,
            "rag": status,
            "evidence": m.get("evidence_url"),
        })

    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 1 if has_red else 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: benefits_status.py register.yaml measurements.yaml PERIOD", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
