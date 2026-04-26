#!/usr/bin/env python3
"""poc_runner.py — minimal POC scenario harness for PM tool evaluation.

Vendor adapters live in adapters/<vendor>.py and implement:
    create_issue() -> str (issue ID)
    transition(issue_id: str) -> None
    search(query: str) -> list[dict]
    fire_webhook() -> None

Usage:
    python3 poc_runner.py --vendor jira --config config/jira.json
    python3 poc_runner.py --vendor linear --config config/linear.json
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import time


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vendor", required=True, help="e.g. jira, linear, gitlab")
    ap.add_argument("--config", required=True, help="JSON path with creds + project")
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    adapter = importlib.import_module(f"adapters.{args.vendor}").Adapter(cfg)

    results: dict[str, dict] = {}
    for step in ("create_issue", "transition", "search", "fire_webhook"):
        t0 = time.perf_counter()
        try:
            getattr(adapter, step)()
            results[step] = {
                "ok": True,
                "ms": int((time.perf_counter() - t0) * 1000),
            }
        except Exception as exc:  # noqa: BLE001
            results[step] = {"ok": False, "error": str(exc)}

    json.dump({"vendor": args.vendor, "steps": results}, sys.stdout, indent=2)
    print()
    failed = [s for s, r in results.items() if not r["ok"]]
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
