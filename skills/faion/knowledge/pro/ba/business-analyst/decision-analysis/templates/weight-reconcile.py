#!/usr/bin/env python3
"""weight-reconcile.py — aggregate per-stakeholder weight CSVs, flag dissent.

Each input CSV must have columns: stakeholder, criterion, weight
(weights per stakeholder should sum to 1.0 within each file).

Flags rows where σ > 0.05 OR absolute range > 0.20 as requiring reconciliation.

Usage: python weight-reconcile.py weights/finance.csv weights/security.csv ... > reconcile.md
"""
import sys
import csv
import statistics
import collections


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("Usage: weight-reconcile.py weights/*.csv")

    per: dict[str, list[tuple[str, float]]] = collections.defaultdict(list)

    for f in sys.argv[1:]:
        try:
            for row in csv.DictReader(open(f)):
                per[row["criterion"]].append((row["stakeholder"], float(row["weight"])))
        except (KeyError, ValueError) as e:
            sys.exit(f"{f}: {e} — expected columns: stakeholder, criterion, weight")

    print("# Weight Reconciliation\n")
    print("| Criterion | Mean | Sigma | Range | Reconcile? | Stakeholders |")
    print("|-----------|------|-------|-------|------------|--------------|")

    needs_reconcile = []
    for crit, rows in sorted(per.items()):
        ws = [w for _, w in rows]
        mean = statistics.mean(ws)
        sd = statistics.stdev(ws) if len(ws) > 1 else 0.0
        rng_val = max(ws) - min(ws)
        flag = "YES" if sd > 0.05 or rng_val > 0.20 else "no"
        if flag == "YES":
            needs_reconcile.append(crit)
        who = ", ".join(f"{s}={w:.2f}" for s, w in rows)
        print(f"| {crit} | {mean:.2f} | {sd:.2f} | {min(ws):.2f}-{max(ws):.2f} | {flag} | {who} |")

    print()
    if needs_reconcile:
        print(f"**{len(needs_reconcile)} criteria require reconciliation before locking weights:**")
        for c in needs_reconcile:
            print(f"- {c}")
        print("\nConvene a 30-minute reconciliation session for these criteria only.")
        print("Lock weights after reconciliation: record weight_locked_at and weight_setter per criterion.")
        sys.exit(1)
    else:
        print("All criteria within acceptable variance. Weights may be locked.")


if __name__ == "__main__":
    main()
