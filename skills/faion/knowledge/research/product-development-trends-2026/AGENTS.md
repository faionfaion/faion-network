# Product Development Trends 2026

## Summary

**One-sentence:** Snapshot specialisation of trend research locked to 2026 signals (on-device LLM, agent-as-product, vibe-coding, privacy-first, sustainability), with hard freshness cutoff (no sources older than 18 months).

**One-paragraph:** Year-locked trend snapshot built on product-development-trends, scoped to the 2026 signal set: on-device LLM inference, agent-as-product paradigm, AI-native CRMs, privacy-first shifts post-DSA, vibe-coding, sustainability badges. Enforces an 18-month source-age cap and a 2025-Q4-to-2026-Q4 retrieval window.

**Ефективно для:**

- 2026 річний планувальний цикл - треба зафіксувати поточні trends.
- Перевірка чи 2024-2025 bets ще релевантні у 2026.
- Investor narrative '2026 trend posture'.
- Pricing / packaging оновлення в світлі 2026 signals.
- Hiring 2026 - під які trends ми скейлимо.

## Applies If (ALL must hold)

- 2026 annual planning cycle; lock current trend posture.
- Re-validation of 2024-2025 bets against 2026 signals.
- Investor narrative '2026 trend posture' section.
- Pricing / packaging refresh in light of 2026 signals.
- Hiring 2026 - under which trends do we scale headcount?

## Skip If (ANY kills it)

- Non-2026 cycles (use product-development-trends instead).
- Trends with no 2026-specific divergence (use the parent methodology).
- Pre-PMF startups with no users; trend bets are noise.
- Hardware companies where 2026 signals lag.
- Internal tools.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 2026 candidate trend list | markdown | PM + research team |
| Q4 2025 retrospective | markdown | previous trend cycle |
| Source-freshness check | automated | CI / WebFetch |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[product-development-trends]] | supplies the 4-axis scoring rubric this snapshot specialises |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `freshness-gate` | haiku | Reject sources older than 18 months. |
| `score-2026-signals` | sonnet | Apply 4-axis scoring to the 2026 candidate set. |
| `verdict-2026` | opus | Bet/monitor/ignore with 2026-specific kill criteria. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trend-brief-2026.md.j2` | 2026 trend brief skeleton with the 6 canonical 2026 trend buckets |
| `templates/trend-brief-2026.md` | 2026 trend brief skeleton with the 6 canonical 2026 trend buckets Generated from `templates/trend-brief-2026.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/collect-trends.py` | Pull 2026 source signals with freshness gate |
| `templates/score-signals.py` | Apply 4-axis scoring to 2026 candidates |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-development-trends-2026.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[product-development-trends]]
- [[trend-analysis]]
- [[competitive-intelligence]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/collect-trends.py`

```python
#!/usr/bin/env python3
"""
collect-trends.py — collect 2025-2026 trend evidence per axis using Exa.ai.

Usage: EXA_API_KEY=<key> python collect-trends.py [output.jsonl]

Output: JSONL where each line is:
  {"axis": str, "title": str, "url": str, "published": str, "score": float}

Requires: EXA_API_KEY environment variable.
Install: pip install requests (stdlib urllib used to avoid extra deps)
"""
import json
import os
import sys
import urllib.request

AXES = [
    "ai-augmented-ideation product development",
    "continuous-discovery product team cadence",
    "rapid-pivot product strategy quarterly",
    "cross-functional product team structure",
]

EXA_URL = "https://api.exa.ai/search"
KEY = os.environ.get("EXA_API_KEY", "")


def fetch_axis(axis: str) -> list[dict]:
    if not KEY:
        raise RuntimeError("EXA_API_KEY environment variable not set")
    body = json.dumps({
        "query": f"{axis} 2025 OR 2026",
        "num_results": 8,
        "start_published_date": "2025-01-01",
        "use_autoprompt": True,
    }).encode()
    req = urllib.request.Request(
        EXA_URL,
        data=body,
        headers={"x-api-key": KEY, "content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    return [
        {
            "axis": axis,
            "title": x.get("title", ""),
            "url": x.get("url", ""),
            "published": x.get("publishedDate", ""),
            "score": float(x.get("score", 0)),
        }
        for x in data.get("results", [])
    ]


def main() -> int:
    out_path = sys.argv[1] if len(sys.argv) > 1 else "trends.jsonl"
    total = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for axis in AXES:
            try:
                results = fetch_axis(axis)
                for row in results:
                    f.write(json.dumps(row) + "\n")
                    total += 1
                print(f"axis '{axis}': {len(results)} results", file=sys.stderr)
            except Exception as exc:
                print(f"ERROR axis '{axis}': {exc}", file=sys.stderr)
    print(f"Wrote {total} signals to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### `templates/score-signals.py`

```python
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
```
