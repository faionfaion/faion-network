#!/usr/bin/env python3
"""rtm_coverage.py — audit requirements traceability matrix coverage.

Input:  scope/rtm.yaml
        requirements:
          - id: FR-01
            design: design/auth.md
            build: src/auth.py
            test: tests/test_auth.py
            status: accepted  # or: in-progress, pending
Output: coverage report; exits 1 if any requirement lacks design or test link.
"""
import sys
import yaml
import pathlib


def main(path: str = "scope/rtm.yaml") -> int:
    data = yaml.safe_load(pathlib.Path(path).read_text())
    items = data.get("requirements", [])
    total = len(items)
    if not total:
        print("No requirements.")
        return 0

    has_design = sum(1 for r in items if r.get("design"))
    has_build = sum(1 for r in items if r.get("build"))
    has_test = sum(1 for r in items if r.get("test"))
    has_accept = sum(1 for r in items if r.get("status") == "accepted")

    def pct(n: int) -> float:
        return 100 * n / total

    print(f"total    {total}")
    print(f"design   {has_design}/{total} ({pct(has_design):.0f}%)")
    print(f"build    {has_build}/{total} ({pct(has_build):.0f}%)")
    print(f"test     {has_test}/{total} ({pct(has_test):.0f}%)")
    print(f"accepted {has_accept}/{total} ({pct(has_accept):.0f}%)")

    gaps = [r["id"] for r in items if not r.get("design") or not r.get("test")]
    if gaps:
        print(f"\nGAPS (missing design or test): {', '.join(gaps)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
