"""
Count support tickets by category from a CSV export.
Expects CSV with at least columns: id, category, subject.
Outputs weekly volume summary to stdout.

Usage:
  python ticket-patterns.py tickets_export.csv
"""
import csv
import sys
from collections import Counter


def ticket_summary(csv_path: str) -> None:
    tickets = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
    if not tickets:
        print("No tickets found.")
        return

    counts: Counter = Counter(t.get("category", "unknown") for t in tickets)
    total = len(tickets)

    print("## Weekly Support Volume")
    for cat, n in counts.most_common():
        print(f"  {cat}: {n} ({100 * n / total:.0f}%)")
    print(f"\nTotal: {total}")

    # Flag categories over 20% threshold
    for cat, n in counts.items():
        if n / total > 0.20 and cat == "how-to":
            print(f"\nWARNING: how-to tickets at {100 * n / total:.0f}% — review UX for related features")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ticket-patterns.py <csv_path>")
        sys.exit(1)
    ticket_summary(sys.argv[1])
