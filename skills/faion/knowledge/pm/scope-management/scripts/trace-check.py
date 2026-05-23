#!/usr/bin/env python3
"""trace-check.py — flag must-have requirements missing design/test coverage in RTM CSV.

CSV columns: id, priority, statement, design_ref, test_ref, status
Exit 1 if any gaps found, 0 if all must-haves are covered.

Usage: python trace-check.py rtm.csv
"""
import csv
import sys


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: trace-check.py <rtm.csv>")

    rows = list(csv.DictReader(open(sys.argv[1])))
    missing = []

    for r in rows:
        if r.get("priority", "").lower() == "must":
            gaps = []
            if not r.get("design_ref", "").strip():
                gaps.append("design_ref")
            if not r.get("test_ref", "").strip():
                gaps.append("test_ref")
            if gaps:
                missing.append((r["id"], gaps))

    if missing:
        print(f"GAP: {len(missing)} must-have requirement(s) missing coverage:")
        for req_id, gaps in missing:
            print(f"  {req_id}: missing {', '.join(gaps)}")
        sys.exit(1)

    print(f"OK: all {sum(1 for r in rows if r.get('priority','').lower()=='must')} "
          f"must-have requirements have design and test coverage.")


if __name__ == "__main__":
    main()
