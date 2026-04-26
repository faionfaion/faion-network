#!/usr/bin/env python3
"""benefits-track.py — pull current metric values vs target, emit JSON status.

Reads benefits_register.yaml; supports source_system: looker | csv.
Computes % realized and status (on_track if >= 70%, else at_risk).

Usage:
    LOOKER_BASE=https://company.looker.com LOOKER_TOKEN=xxx \\
    python benefits-track.py benefits_register.yaml

Output: JSON array with actual, pct_realized, status per benefit.
"""
import json
import os
import sys
import yaml
import csv as csv_mod


def fetch_looker(b: dict) -> float | None:
    import requests
    url = f"{os.environ['LOOKER_BASE']}/api/4.0/queries/{b['query_id']}/run/json"
    r = requests.get(url, headers={"Authorization": f"token {os.environ['LOOKER_TOKEN']}"})
    r.raise_for_status()
    return float(r.json()[0][b["metric"]])


def fetch_csv(b: dict) -> float | None:
    with open(b["path"]) as f:
        rows = list(csv_mod.DictReader(f))
    return float(rows[-1][b["metric"]]) if rows else None


SOURCES = {"looker": fetch_looker, "csv": fetch_csv}


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "benefits_register.yaml"
    reg = yaml.safe_load(open(path))
    out = []

    for b in reg:
        fetcher = SOURCES.get(b.get("source_system", ""))
        if fetcher is None:
            out.append({**b, "actual": None, "status": "no_fetcher"})
            continue
        try:
            actual = fetcher(b)
        except Exception as e:
            out.append({**b, "actual": None, "status": f"error: {e}"})
            continue

        baseline = b["baseline_value"]
        target = b["target_value"]
        delta = target - baseline
        pct = (actual - baseline) / delta if delta else 0.0
        out.append({
            **b,
            "actual": actual,
            "pct_realized": round(pct, 3),
            "status": "on_track" if pct >= 0.7 else "at_risk",
        })

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
