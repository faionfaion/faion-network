# purpose: Apply 4-axis scoring to 2026 candidates
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1500 tokens when loaded as context
#!/usr/bin/env python3
"""
score-signals.py — score trend signals on recency, evidence, applicability; drop weak ones.

Usage: python score-signals.py signals.jsonl [threshold]

Input JSONL fields (per line):
  trend: str
  source: str (URL)
  published: str (YYYY-MM-DD)
  primary_source: bool
  citations: int
  applicability: int (0-3, set by human reviewer)

Output: markdown table of kept signals, sorted by score descending.
Default threshold: 5 (max score: 9)
"""
import json
import sys
import datetime as dt

THRESHOLD = int(sys.argv[2]) if len(sys.argv) > 2 else 5
TODAY = dt.date.today()


def score(sig: dict) -> dict:
    published_str = sig.get("published", "")
    try:
        age_days = (TODAY - dt.date.fromisoformat(published_str[:10])).days
    except ValueError:
        age_days = 999
    recency = 3 if age_days <= 30 else 2 if age_days <= 90 else 1 if age_days <= 180 else 0
    citations = int(sig.get("citations", 0))
    primary = bool(sig.get("primary_source", False))
    evidence = 3 if primary else 2 if citations >= 3 else 1
    applicability = min(3, max(0, int(sig.get("applicability", 0))))
    total = recency + evidence + applicability
    return {**sig, "score": total, "recency": recency, "evidence_score": evidence}


def main(path: str) -> None:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(score(json.loads(line)))

    kept = [r for r in rows if r["score"] >= THRESHOLD]
    kept.sort(key=lambda r: r["score"], reverse=True)

    print(f"# Trend signals — kept {len(kept)}/{len(rows)} (threshold={THRESHOLD})\n")
    print("| Score | Trend | Source | Published | Recency | Evidence |")
    print("|-------|-------|--------|-----------|---------|----------|")
    for r in kept:
        trend = r.get("trend", r.get("axis", "—"))[:60]
        source = r.get("source", r.get("url", "—"))
        print(
            f"| {r['score']} | {trend} | {source} "
            f"| {r.get('published', '—')[:10]} "
            f"| {r['recency']} | {r['evidence_score']} |"
        )

    if not kept:
        print("\n*(No signals met the threshold — lower threshold or collect more evidence)*")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <signals.jsonl> [threshold]", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
