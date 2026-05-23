---
slug: trend-analysis
tier: pro
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Multi-source signal aggregation (search interest + research papers + funding + GitHub stars + social) producing a trend score (0-100) and decay-curve estimate; rejects single-source narratives.
content_id: "092655a085ae568b"
complexity: medium
produces: report
est_tokens: 4600
tags: [trends, signals, decay-curve, horizon-scan]
---
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
| `templates/trend-report.md` | Trend report skeleton (signals + score + decay + verdict) |
| `templates/trend-signals.py` | Pull + normalize the 5 signal classes; emit JSON |

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
