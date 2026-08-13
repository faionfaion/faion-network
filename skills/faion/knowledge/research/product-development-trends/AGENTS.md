# Product Development Trends

## Summary

**One-sentence:** Scores emerging trends on a 4-axis rubric (signal strength + adoption velocity + revenue alignment + decay risk) producing a quarterly trend brief with explicit 'bet / monitor / ignore' verdicts.

**One-paragraph:** Systematic quarterly trend research that filters hype: each candidate trend is scored on 4 axes (signal strength, adoption velocity, revenue alignment, decay risk), classified as bet / monitor / ignore, and traced back to >=3 independent sources (one academic / filing, one practitioner, one market signal). Output: trend-brief.md with the picks + rationale + kill-criteria per bet.

**Ефективно для:**

- Quarterly strategy review: куди йти у наступному кварталі.
- Roadmap-планування: чи варто інвестувати в AI / on-device / privacy / etc.
- Investor update з 'trend snapshot' секцією.
- Hiring rationale: під який trend ми наймаємо.
- Newsletter / content marketing: серія 'trend digest'.

## Applies If (ALL must hold)

- Quarterly strategy review on where to bet next.
- Roadmap planning: AI / on-device / privacy / sustainability / etc.
- Investor update with a 'trend snapshot' section.
- Hiring rationale: under which trend are we adding headcount?
- Content marketing 'trend digest' series.

## Skip If (ANY kills it)

- Acute delivery cycle (next sprint) - trends are quarterly+.
- Crisis mode (revenue cliff, outage) - solve the crisis first.
- Pure execution org with no R&D budget.
- Niche internal tool where outside trends do not apply.
- When the only goal is to add a buzzword to the deck.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Candidate trend list | markdown | PM + research team |
| Product positioning doc | markdown | marketing |
| Quarterly revenue target | currency | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[trend-analysis]] | supplies the raw signal sources that this methodology scores |

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
| `signal-pull` | haiku | Mechanical pull of academic / filings / practitioner sources. |
| `score-axes` | sonnet | Score signal strength + velocity + alignment + decay. |
| `verdict-bet-monitor-ignore` | opus | Strategic verdict + kill criteria per bet. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trend-brief.md` | Quarterly trend brief skeleton with bet/monitor/ignore tables |
| `templates/score-signals.py` | Score a candidate trend across 4 axes; print JSON |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-development-trends.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[product-development-trends-2026]]
- [[trend-analysis]]
- [[competitive-intelligence]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/score-signals.py`

```python
#!/usr/bin/env python3
"""
score-signals.py — score trend signals on recency, evidence, applicability; filter weak ones.

Usage: python score-signals.py signals.jsonl [threshold]

Input JSONL fields (per line):
  trend: str
  source: str (URL)
  published: str (YYYY-MM-DD)
  primary_source: bool
  citations: int
  applicability: int (0-3, set by human reviewer before running)

Output: markdown table sorted by score desc; signals below threshold omitted.
Default threshold: 5 (max possible: 9)
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
    primary = bool(sig.get("primary_source", False))
    citations = int(sig.get("citations", 0))
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
                try:
                    rows.append(score(json.loads(line)))
                except json.JSONDecodeError as exc:
                    print(f"SKIP malformed line: {exc}", file=sys.stderr)

    kept = [r for r in rows if r["score"] >= THRESHOLD]
    kept.sort(key=lambda r: r["score"], reverse=True)

    print(f"# Trend signals — kept {len(kept)}/{len(rows)} (threshold={THRESHOLD})\n")
    print("| Score | Trend | Source | Published |")
    print("|-------|-------|--------|-----------|")
    for r in kept:
        trend = r.get("trend", r.get("axis", "—"))[:60]
        source = r.get("source", r.get("url", "—"))
        print(f"| {r['score']} | {trend} | {source} | {r.get('published', '—')[:10]} |")

    if not kept:
        print("\n*(No signals met threshold — lower threshold or collect more signals)*")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <signals.jsonl> [threshold]", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
```
