<!--
purpose: Canonical AI product success metrics catalog skeleton.
consumes: feature inventory + session transcripts + manual audit sample.
produces: A versioned, owner-signed AI-KPI catalog.
depends-on: ../scripts/validate-ai-product-success-metrics-catalog.py.
token-budget-impact: ~500 tokens when filled.
-->

---
artefact_id: "<product-slug>-ai-metrics"
owner: "ai-pm:<person>"
version: "1.0.0"
last_reviewed: "2026-05-22"
inputs_used:
  - name: "Feature inventory"
    source: "<path-or-url>"
  - name: "Audit sample"
    source: "<path-to-csv>"
---

# AI Product Success Metrics — <product>

## Deflection rate

- Definition: percentage of sessions resolved by the AI without human escalation.
- Source: <log table / dashboard URL>
- Baseline: <%>

## Intervention rate

- Definition: percentage of sessions where a human had to step in.
- Source: <log table>
- Baseline: <%>

## Hallucination rate

- Definition: percentage of AI responses containing factually incorrect or unsupported claims (manual audit of N=100 sample).
- Source: <audit-sample-link>
- Baseline: <%>

## Time-to-correction

- Definition: median minutes between a wrong AI output and the corrected one (after user / human intervention).
- Source: <log table>
- Baseline: <minutes>

## Retention on AI features

- Definition: 28-day return rate of users who triggered the AI feature at least once.
- Source: <retention dashboard>
- Baseline: <%>

## Decisions / Actions / Next review

- <decision 1>
- Next review: <ISO date, ≤90 days>
