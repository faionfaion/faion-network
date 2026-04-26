#!/usr/bin/env python3
"""calculate-confidence.py — Compute confidence score from gate results.

Usage:
    python calculate-confidence.py gate-report.md
    python calculate-confidence.py gate-report.md --threshold 90
    python calculate-confidence.py --help

Output:
    Confidence score (0-100) printed to stdout.
    Exit code 0 if score >= threshold, 1 if below.
"""

import argparse
import re
import sys


GATE_WEIGHTS = {
    "L1": 0.15,
    "L2": 0.25,
    "L3": 0.20,
    "L4": 0.20,
    "L5": 0.10,
    "L6": 0.10,
}


def parse_gate_report(path: str) -> dict[str, float]:
    """Parse gate-report.md and return {gate_id: pass_rate} dict."""
    scores: dict[str, float] = {}
    try:
        with open(path) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(2)

    # Match lines like: | L2 | Unit Tests | 8/10 | 80% | PASS |
    pattern = re.compile(r"\|\s*(L[1-6])\s*\|[^|]+\|[^|]+\|\s*(\d+)%\s*\|")
    for match in pattern.finditer(content):
        gate_id = match.group(1)
        pct = int(match.group(2))
        scores[gate_id] = pct / 100.0

    return scores


def calculate_confidence(scores: dict[str, float]) -> float:
    """Compute weighted confidence score (0-100)."""
    total_weight = 0.0
    weighted_sum = 0.0

    for gate_id, weight in GATE_WEIGHTS.items():
        if gate_id in scores:
            weighted_sum += scores[gate_id] * weight
            total_weight += weight

    if total_weight == 0:
        return 0.0

    # Normalize to account for missing gates
    return (weighted_sum / total_weight) * 100.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate SDD confidence score")
    parser.add_argument("report", help="Path to gate-report.md")
    parser.add_argument(
        "--threshold",
        type=float,
        default=90.0,
        help="Minimum score to proceed (default: 90)",
    )
    args = parser.parse_args()

    scores = parse_gate_report(args.report)

    if not scores:
        print("ERROR: No gate scores found in report. Check format.", file=sys.stderr)
        sys.exit(2)

    confidence = calculate_confidence(scores)

    print(f"Gate scores:")
    for gate_id in sorted(scores):
        weight = GATE_WEIGHTS.get(gate_id, 0)
        print(f"  {gate_id}: {scores[gate_id]*100:.0f}% (weight {weight:.0%})")

    print(f"\nConfidence score: {confidence:.1f}%")
    print(f"Threshold: {args.threshold}%")

    if confidence >= args.threshold:
        print(f"PROCEED: confidence {confidence:.1f}% >= threshold {args.threshold}%")
        sys.exit(0)
    else:
        delta = args.threshold - confidence
        print(
            f"BLOCK: confidence {confidence:.1f}% is {delta:.1f}% below threshold",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
