# Trend Analysis

## Summary

**One-sentence:** Multi-source signal aggregation (search interest + research papers + funding + GitHub stars + social) producing a trend score (0-100) and decay-curve estimate; rejects single-source narratives.

**One-paragraph:** Authoring methodology for trend analysis. Aggregates 5 signal classes (search interest, research-paper count, funding rounds, GitHub stars, social mentions) into a composite score 0-100; fits a 4-quarter decay curve; flags hype cycles vs structural trends. Refuses single-source trend narratives ('Twitter is buzzing about X').

**Ефективно для:**

- Quarterly trend brief - треба порівняти 3-5 candidate trends.
- Investor deck slide 'why now' з кількісними signals.
- Hiring / R&D rationale: підтвердити trend перед інвестицією.
- Content marketing: серія 'trend digest' з consistent методологією.
- Кваліфікація 'is this hype or structural?'.

## Applies If (ALL must hold)

- Quarterly trend brief comparing 3-5 candidate trends.
- Investor deck 'why now' slide backed by quantitative signals.
- Hiring / R&D rationale: confirm a trend before investing.
- Content marketing 'trend digest' with consistent methodology.
- Qualifying 'is this hype or structural?' on a candidate.

## Skip If (ANY kills it)

- Acute delivery cycle (next sprint).
- Trends with no quantitative signal yet (too early).
- Trends fully covered by an authoritative report (just cite it).
- Internal-only research with no decision attached.
- When the only goal is to fill a newsletter section.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Candidate trend list | markdown | PM / research |
| Tooling access | Google Trends API + Crossref + Crunchbase + GitHub + X/Reddit | data ops |
| Score rubric | from product-development-trends | previous cycle |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[product-development-trends]] | consumes the trend scores this methodology emits |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `signal-pull` | haiku | Mechanical pull of search/paper/funding/stars/social signals. |
| `normalize-and-score` | sonnet | Normalize across signal classes; compute composite 0-100. |
| `decay-fit` | sonnet | Fit 4-quarter decay curve; flag hype vs structural. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trend-report.md.j2` | Trend report skeleton (signals + score + decay + verdict) |
| `templates/trend-report.md` | Trend report skeleton (signals + score + decay + verdict) Generated from `templates/trend-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/trend-signals.py` | Pull + normalize the 5 signal classes; emit JSON |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trend-analysis.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[product-development-trends]]
- [[product-development-trends-2026]]
- [[competitive-intelligence]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/trend-signals.py`

```python
# trend_signals.py — minimal multi-source trend collector
# Input: trend term as CLI argument
# Output: JSON with signals from Google Trends, HN Algolia, GitHub
# Usage: python trend_signals.py "AI agents"
import json, datetime as dt, sys
from pytrends.request import TrendReq
import requests


def google_trends(term: str) -> dict:
    p = TrendReq()
    p.build_payload([term], timeframe="today 12-m")
    df = p.interest_over_time()
    if df.empty:
        return {"yoy_pct": None, "last": None, "source": "google_trends"}
    last, first = df[term].iloc[-1], df[term].iloc[0]
    yoy = None if first == 0 else round((last - first) / first * 100, 1)
    return {"yoy_pct": yoy, "last": int(last), "source": "google_trends"}


def hn_hits(term: str) -> dict:
    since = int(dt.datetime.now().timestamp()) - 2592000  # 30 days
    r = requests.get(
        "https://hn.algolia.com/api/v1/search",
        params={"query": term, "tags": "story",
                "numericFilters": f"created_at_i>{since}"},
    ).json()
    return {"hits_30d": r.get("nbHits", 0), "source": "hacker_news"}


def gh_repos(term: str) -> dict:
    since = (dt.date.today() - dt.timedelta(days=180)).isoformat()
    r = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": f"{term} created:>{since}", "sort": "stars", "order": "desc"},
    ).json()
    items = r.get("items") or [{}]
    return {
        "new_repos_180d": r.get("total_count", 0),
        "top_stars": items[0].get("stargazers_count", 0),
        "source": "github",
    }


def collect(term: str) -> dict:
    return {
        "term": term,
        "ts": dt.datetime.utcnow().isoformat() + "Z",
        "signals": [google_trends(term), hn_hits(term), gh_repos(term)],
    }


if __name__ == "__main__":
    term = sys.argv[1] if len(sys.argv) > 1 else "AI agents"
    print(json.dumps(collect(term), indent=2))
```
