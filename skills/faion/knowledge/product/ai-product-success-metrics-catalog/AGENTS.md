# AI Product Success Metrics Catalog

## Summary

**One-sentence:** A catalogued, versioned, AI-specific success-metrics set (deflection rate, intervention rate, hallucination rate, time-to-correction, retention-on-AI-features) so AI-native PMs measure the right things instead of bolting CSAT onto every chatbot.

**One-paragraph:** Generic success-metrics-definition does not cover AI-specific KPIs. AI-native products fail silently when measured with the wrong yardstick: a chatbot with 90% CSAT can still be deflecting customers to dead ends, and a copilot can have 99% engagement while writing the same hallucinated SQL every day. This methodology pins the AI-specific catalog: deflection rate, intervention rate, hallucination rate (with manual audit floor), time-to-correction, and retention-on-AI-features. Every metric has a typed definition, an evidence source (transcript / log / metric), a named owner, semver + last_reviewed, and explicit grounding so no LLM-claim survives without provenance.

**Ефективно для:** AI-native PM, який запускає продукт із LLM-фічею і не хоче, щоб CSAT прикривав мовчазний відтік клієнтів.

## Applies If (ALL must hold)

- Product has at least one user-facing AI feature (chatbot, copilot, suggestion, summary, search rerank).
- Operator has access to per-session transcripts or interaction logs for the AI feature.
- Named owner (PM or AI PM) is accountable for the catalog.
- Output will feed an ongoing dashboard or weekly review, not a one-off slide.

## Skip If (ANY kills it)

- Pure non-AI product — use the generic success-metrics methodology instead.
- Greenfield prototype with no production users — defer until ≥50 sessions are available to baseline.
- Regulator-mandated KPI set (e.g. credit-scoring fairness) — defer to that mandate.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| AI feature inventory | YAML | product spec |
| Session transcripts | log / DB query | telemetry store |
| Manual audit sample | CSV | QA team |
| Named owner | role + person | product team |
| Dashboard / review forum | URL | product ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/product/product-manager` | Parent skill — provides the operating context. |
| `geek/ai-core/llm-evaluation` | Sibling that feeds the hallucination-audit floor. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: bound-scope, typed-input, named-owner, versioned, LLM-grounding | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Has-AI-feature gate + provenance branch | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_metric_definitions` | haiku | Template fill from feature inventory. |
| `compute_baselines` | sonnet | Per-metric judgment from sampled logs. |
| `audit_hallucination_floor` | opus | Cross-transcript synthesis; requires nuanced judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-product-success-metrics-catalog.json` | JSON schema for the catalog output contract. |
| `templates/ai-product-success-metrics-catalog.md` | Markdown skeleton with required metrics. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-product-success-metrics-catalog.py` | Enforce catalog contract (all 5 metrics present with definitions + sources, semver + last_reviewed, owner is person). | After catalog draft, before dashboard wiring. |

## Related

- [[ai-feature-de-risking]] — sibling AI-PM methodology consuming these metrics.
- [[ai-feature-trust-metrics]] — peer geek research methodology covering trust-specific axes.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether at least one user-facing AI feature exists. If no → skip. If yes but logs are unavailable → block until telemetry is wired. If yes + logs available → emit the catalog with grounded definitions.
