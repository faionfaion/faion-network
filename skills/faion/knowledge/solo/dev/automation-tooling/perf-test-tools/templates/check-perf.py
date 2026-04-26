#!/usr/bin/env python3
"""check-perf.py — fail CI if k6 thresholds miss.
Usage: python check-perf.py results.json
Input: k6 JSON output file (k6 run --out json=results.json)
Output: exit 0 if thresholds pass, exit 1 with details if they fail.
"""
import json
import sys
import pathlib

LIMITS = {
    "http_req_duration.p(95)": 500,   # ms
    "http_req_failed.rate": 0.01,      # fraction
}


def main():
    data = [
        json.loads(line)
        for line in pathlib.Path(sys.argv[1]).read_text().splitlines()
        if line.strip()
    ]
    metrics: dict[str, list[float]] = {}
    for entry in data:
        if entry.get("type") == "Point":
            m = entry["metric"]
            metrics.setdefault(m, []).append(entry["data"]["value"])

    failed = []
    for key, limit in LIMITS.items():
        name, *agg = key.split(".")
        values = metrics.get(name, [])
        if not values:
            failed.append(f"{key}: no samples")
            continue
        if agg and agg[0].startswith("p("):
            pct = float(agg[0][2:-1]) / 100
            v = sorted(values)[int(len(values) * pct)]
        else:
            v = sum(values) / len(values)
        if v > limit:
            failed.append(f"{key}={v:.2f} > limit={limit}")

    if failed:
        print("PERF FAIL:")
        for f in failed:
            print(f"  {f}")
        sys.exit(1)
    print("PERF OK")


if __name__ == "__main__":
    main()
