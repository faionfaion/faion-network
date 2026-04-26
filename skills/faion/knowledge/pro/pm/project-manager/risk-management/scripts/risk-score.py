#!/usr/bin/env python3
"""risk-score.py — compute Score and EMV from a risks.yaml file.

YAML schema per risk:
  id, title, probability (L|M|H), impact (L|M|H),
  type (threat|opportunity), impact_usd (optional float)

Outputs sorted risk table (by EMV desc, then score).

Usage: python risk-score.py risks.yaml
"""
import sys
import yaml

SCORES = {
    ("L", "L"): "low",  ("L", "M"): "low",  ("L", "H"): "med",
    ("M", "L"): "low",  ("M", "M"): "med",  ("M", "H"): "high",
    ("H", "L"): "med",  ("H", "M"): "high", ("H", "H"): "crit",
}
P_NUM = {"L": 0.10, "M": 0.30, "H": 0.60}
SCORE_ORDER = {"crit": 4, "high": 3, "med": 2, "low": 1}


def score(risks: list) -> list:
    out = []
    for r in risks:
        p = r.get("probability", "M").upper()
        i = r.get("impact", "M").upper()
        sc = SCORES.get((p, i), "?")
        emv = None
        if "impact_usd" in r:
            emv = round(P_NUM.get(p, 0) * r["impact_usd"])
        out.append({**r, "score": sc, "emv_usd": emv})
    return sorted(out, key=lambda x: (-(x["emv_usd"] or 0), -SCORE_ORDER.get(x["score"], 0)))


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: risk-score.py risks.yaml")

    data = yaml.safe_load(open(sys.argv[1]))
    scored = score(data)

    print(f"{'ID':<8} {'Score':<6} {'EMV ($)':<10} {'P':<4} {'I':<4} Title")
    print("-" * 70)
    for r in scored:
        emv_str = f"${r['emv_usd']:,}" if r["emv_usd"] is not None else "—"
        print(f"{r['id']:<8} {r['score']:<6} {emv_str:<10} "
              f"{r.get('probability','?'):<4} {r.get('impact','?'):<4} {r['title']}")


if __name__ == "__main__":
    main()
