<!--
purpose: Markdown skeleton for an authored RAG canary rollout plan (human-readable).
consumes: target_version + baseline_version + golden_eval_id + rubric_id + cost budget
produces: filled-in plan matching the JSON schema sibling file
depends-on: content/02-output-contract.xml
token-budget-impact: 0 — template
-->

# RAG Canary Rollout Plan — `<feature_id>`

- **Target:** `<target_version>`
- **Baseline:** `<baseline_version>`
- **Golden eval suite:** `<golden_eval.suite_id>`
- **Online rubric:** `<online_quality.rubric_id>`

## Curve

| Step | Percent | Hold | Min samples |
|---|---|---|---|
| 1 | 1% | 24h | 200 |
| 2 | 5% | 24h | 1000 |
| 3 | 25% | 48h | 5000 |
| 4 | 100% | 168h soak | continuous |

## Gates per step

- Golden eval primary metric: **no regression**
- Secondary metrics: max regression 5%
- p95 latency: max delta +20%
- Online composite score: ≥ `<floor>`

## Kill switch

- Criteria (≥4): `<list>`
- Atomic flip: **true** (in-memory routing; no deploy)
- Last rehearsed: `<YYYY-MM-DD>` (≤90 days)
