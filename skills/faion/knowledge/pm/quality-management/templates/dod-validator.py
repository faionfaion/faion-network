#!/usr/bin/env python3
"""dod_validator.py — minimal PR DoD gate.

Runs the must items from quality/dod.yaml against the current codebase.
Exit 1 if any must item fails — wire to CI pre-merge check.

Usage:  python dod_validator.py [path/to/dod.yaml]
Requires: pytest, coverage, ruff, gitleaks installed and in PATH.
"""
from __future__ import annotations
import json
import subprocess
import sys
import yaml
import pathlib


def run(cmd: str) -> int:
    return subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def coverage_pct() -> float:
    r = subprocess.run(
        ["coverage", "report", "--format=total"],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


CHECKS = {
    "dod-002": ("tests_pass", lambda: run("pytest -q") == 0),
    "dod-003": ("coverage_80", lambda: coverage_pct() >= 80),
    "dod-006": ("lint_clean", lambda: run("ruff check .") == 0),
    "dod-004": ("no_secrets", lambda: run("gitleaks detect --no-banner") == 0),
}


def main(dod_path: str = "quality/dod.yaml") -> int:
    dod = yaml.safe_load(pathlib.Path(dod_path).read_text())
    must_ids = {
        item["id"]
        for section in dod.get("items", {}).values()
        for item in section
        if item.get("priority") == "must" and item.get("gate") in ("pre-merge", "pre-commit")
    }
    results = []
    for item_id, (name, check_fn) in CHECKS.items():
        if item_id not in must_ids:
            continue
        passed = check_fn()
        results.append({"item": item_id, "name": name, "pass": passed})
    print(json.dumps(results, indent=2))
    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
