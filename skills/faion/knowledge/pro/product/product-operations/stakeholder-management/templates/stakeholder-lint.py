#!/usr/bin/env python3
# purpose: Lint stakeholder register for missing owners/cadence/attitude
# consumes: stakeholder-register.md path
# produces: exit 0 if clean; exit 1 with violation list
# depends-on: stdlib (re)
# token-budget-impact: low

import argparse, re, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", type=str)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        sample = "| name | high | high | supporter | ruslan | weekly |\n"
        ok = bool(re.search(r"\|\s*(supporter|neutral|resistor)\s*\|", sample))
        sys.stdout.write(f"self-test pass={ok}\n"); sys.exit(0 if ok else 1)
    if not a.file:
        sys.stderr.write("--file required\n"); sys.exit(2)
    text = open(a.file).read()
    viol = []
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line or line.lower().startswith("| name"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6:
            viol.append(f"too few cells: {line[:60]}"); continue
        attitude = cells[3].lower()
        owner = cells[4]
        cadence = cells[5].lower()
        if attitude not in ("supporter", "neutral", "resistor"):
            viol.append(f"attitude '{attitude}' invalid in: {line[:60]}")
        if not owner or owner.lower() == "tbd":
            viol.append(f"owner missing in: {line[:60]}")
        if cadence not in ("weekly", "biweekly", "monthly", "quarterly"):
            viol.append(f"cadence '{cadence}' invalid in: {line[:60]}")
    for v in viol:
        sys.stderr.write(f"VIOLATION: {v}\n")
    sys.exit(1 if viol else 0)

if __name__ == "__main__":
    main()
