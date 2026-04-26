#!/usr/bin/env python3
"""emv.py — score a Markdown risk register, exit non-zero on critical untriaged risks.

Usage: python emv.py RISK-REGISTER.md

Parses table rows with columns: ID | Description | Category | P | I | Score | ...
P and I must be one of: VL, L, M, H, VH
Exits 1 if any row has Score >= 0.15 (High/Critical) and Status = Active.

P weights: VL=0.05, L=0.20, M=0.40, H=0.60, VH=0.85
I weights: VL=0.025, L=0.075, M=0.15, H=0.30, VH=0.50
"""
import re
import sys
import pathlib

P_WEIGHT = {"VL": 0.05, "L": 0.20, "M": 0.40, "H": 0.60, "VH": 0.85}
I_WEIGHT = {"VL": 0.025, "L": 0.075, "M": 0.15, "H": 0.30, "VH": 0.50}
CRIT_THRESHOLD = 0.15


def main(path: str) -> int:
    text = pathlib.Path(path).read_text()
    # Match table rows: | R-NN | ... | P | I | Score | ...
    pattern = r"\|\s*(R-\d+)\s*\|[^|]*\|[^|]*\|\s*([A-Z]{1,2})\s*\|\s*([A-Z]{1,2})\s*\|"
    crit = []
    for match in re.finditer(pattern, text):
        rid, p_str, i_str = match.group(1), match.group(2), match.group(3)
        p = P_WEIGHT.get(p_str)
        i = I_WEIGHT.get(i_str)
        if p is not None and i is not None:
            score = p * i
            if score >= CRIT_THRESHOLD:
                crit.append((rid, p_str, i_str, round(score, 4)))

    if crit:
        print("CRITICAL risks requiring immediate triage:")
        for rid, p_str, i_str, score in crit:
            print(f"  {rid}: P={p_str} I={i_str} score={score}")
        return 1
    print(f"OK — no critical risks above threshold {CRIT_THRESHOLD}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: emv.py RISK-REGISTER.md", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
