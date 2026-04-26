#!/usr/bin/env python3
"""
signal-scorer.py — score market-trend signals on recency/evidence/applicability.
Drops signals below threshold before paying for Opus synthesis.

Usage: python signal-scorer.py signals.jsonl

JSONL row shape:
  {"trend": "...", "source": "URL", "published": "YYYY-MM-DD",
   "primary_source": bool, "citations": int, "applicability": 0-3,
   "region": "US|EU|APAC|global", "market_impl": "..."}
"""
import json, sys, datetime as dt

THRESHOLD = 5
TODAY = dt.date.today()


def score(sig: dict) -> dict:
    age_days = (TODAY - dt.date.fromisoformat(sig["published"])).days
    recency = 3 if age_days <= 30 else 2 if age_days <= 90 else 1 if age_days <= 180 else 0
    evidence = 3 if sig.get("primary_source") else 2 if sig.get("citations", 0) >= 3 else 1
    applicability = int(sig.get("applicability", 0))
    sig["score"] = recency + evidence + applicability
    return sig


def main(path: str) -> None:
    rows = [score(json.loads(line)) for line in open(path) if line.strip()]
    kept = sorted(
        [r for r in rows if r["score"] >= THRESHOLD],
        key=lambda r: r["score"],
        reverse=True,
    )
    print(f"# Trend signals (kept {len(kept)}/{len(rows)}, threshold={THRESHOLD})\n")
    print("| Score | Trend | Region | Source | Date | Market implication |")
    print("|-------|-------|--------|--------|------|--------------------|")
    for r in kept:
        print(
            f"| {r['score']} | {r['trend']} | {r.get('region', '?')} | "
            f"{r['source']} | {r['published']} | {r.get('market_impl', '')} |"
        )


if __name__ == "__main__":
    main(sys.argv[1])
