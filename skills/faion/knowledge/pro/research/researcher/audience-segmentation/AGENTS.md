# Audience Segmentation

## Summary

A 5-step methodology for dividing a potential market into distinct, scored groups using 2-3 dimensions drawn from observed data (demographic, behavioral, psychographic, needs-based). Produces a scored segment matrix and a target-strategy decision. Outputs `audience-segmentation.md` in `.aidocs/product_docs/`.

## Why

"Everyone is my customer" leads to messaging that resonates with nobody and marketing spend diffused across channels. Behavioral and needs-based segmentation — as opposed to pure demographic slicing — consistently outperforms for messaging work because it captures what users do and what they need, not just who they are. A weighted scoring model forces the team to commit to one primary segment until there is enough revenue to address more.

## When To Use

- Pre-launch: deciding which single segment gets the MVP.
- Post-launch with mixed signals (high churn in 30% of cohort, high NPS in 50%) — segment to find actual ICP.
- Repositioning a stalled product where "everyone" messaging tests failed.
- Pricing tier design when usage data shows two or more behavioral clusters.
- Channel allocation when paid spend is diffuse without a clear winner.
- B2B GTM when sales calls reveal distinct buyer types with different objections.

## When NOT To Use

- TAM under ~5k addressable accounts — further segmentation starves each segment of evidence.
- First 10 paying customers — too few data points; run `pain-points` and `problem-validation` first.
- Pure infra/dev tools where the buyer is "any engineer with this stack" — use `niche-evaluation`.
- Dimensions chosen from gut alone with no interview/CRM/analytics data backing them.
- One-off campaigns where the segment is already given by the brief.

## Content

| File | What's inside |
|------|---------------|
| `content/01-criteria.xml` | Four segmentation criteria types (demographic, behavioral, psychographic, needs-based) with use-case guidance |
| `content/02-process.xml` | 5-step segmentation process: gather data, pick dimensions, create segments, score, select target strategy |
| `content/03-examples.xml` | CRM tool and online course examples; common mistakes table |
| `content/04-gotchas.xml` | Hallucinated segments, score inflation, dimension drift, confusing personas with segments, human-in-the-loop gates |

## Templates

| File | Purpose |
|------|---------|
| `templates/segmentation-analysis.md` | Full segmentation analysis skeleton: dimensions, segment profiles with scoring table, comparison matrix, implications |
| `templates/segment-profile-card.md` | Single segment profile card: demographics, behaviors, needs, messaging, reach, size |
| `templates/segment-candidates.py` | KMeans clustering harness: turns a user CSV into candidate behavioral segments with silhouette scoring |
