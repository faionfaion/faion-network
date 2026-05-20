---
slug: golden-set-curation-and-maintenance
tier: pro
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Generic methodology for curating 50-200 hand-labelled I/O pairs for any AI feature, plus a discipline for growing the set from production incidents.
content_id: "90764cdc66941a1a"
tags: [ai, eval, golden-set, regression-test, incident-feedback, ml-ops]
---
# Golden Set Curation & Maintenance

## Summary

**One-sentence:** Generic methodology for curating 50-200 hand-labelled I/O pairs for any AI feature, plus a discipline for growing the set from production incidents.

**One-paragraph:** Every AI feature needs a small, hand-curated, version-controlled set of input/expected-output pairs that anchors all evaluations and regression tests. This methodology is RAG-agnostic — it applies to summarization, classification, extraction, agentic flows, anything. Mechanism: a stratified seeding protocol (cover happy path + failure-class buckets), explicit per-item metadata (intent, difficulty, expected-output, anti-output), an incident-driven growth rule (every page becomes a candidate golden item), a versioned promotion process, and a per-quarter drift audit that retires stale items. Primary output: a checked-in `golden/` dataset with per-item metadata that is the single source of truth for "did the model regress?".

## Applies If (ALL must hold)

- AI feature is shipped or near-shipping into a non-AI product
- feature has measurable correctness criteria (not just "vibes")
- team owns the model boundary (input + output schema)
- ≥ 1 production incident has occurred OR feature touches a regulated / customer-visible surface
- team is willing to spend ~ 1 engineer-week to seed the initial set

## Skip If (ANY kills it)

- pre-prototype feature with unstable schema — golden items will rot daily
- pure exploratory research with no production deployment plan
- LLM-judge-only eval pipeline already running for a feature where human label is more expensive than the cost of mistakes
- feature output is creative content with no consensus correctness (poem, brand copy)
- team uses a RAG-specific eval framework already covering golden-set discipline — use it instead

## Prerequisites (must be true before starting)

- input/output schema for the feature is stable (no breaking changes within the audit horizon)
- production logging captures inputs + outputs with PII-safe redaction
- incident channel exists (PagerDuty, Slack, ticketing) producing reviewable incident records
- version control with branch + PR review on the `golden/` directory
- per-feature owner accountable for golden-set quality

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/rag-eval-test-set-generation` | Optional pairing for RAG-flavored features |
| `geek/ai/ml-ops/eval-pipeline-design` | Receives the golden set as anchor dataset |
| `geek/ai/ml-engineer/incident-postmortem-ai-features` | Feeds incidents back as golden-set candidates |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: stratified seeding, anti-output required, incident-to-golden pipeline, quarterly drift audit, versioned promotion | ~1000 |
| `content/02-output-contract.xml` | essential | Per-item schema, metadata required keys, dataset-level metrics | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (overfitting to golden, label drift, easy-only items, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `seed_item_drafting` | sonnet | Generate candidate inputs covering failure-class buckets |
| `expected_output_authoring` | opus | Authoritative ground-truth; high-consequence |
| `anti_output_generation` | sonnet | Generate plausible-wrong outputs for tripwire eval |
| `incident_to_candidate_extraction` | sonnet | Read incident log, propose golden item |
| `drift_audit_classifier` | haiku | Tag each item: still_valid / schema_changed / retire |

## Templates

| File | Purpose |
|------|---------|
| `templates/golden-item-schema.json` | Per-item JSON schema with metadata fields |
| `templates/seeding-buckets.md` | Stratified bucket list (happy + failure classes) |
| `templates/incident-to-golden.md` | Conversion checklist from incident to golden candidate |
| `templates/drift-audit-checklist.md` | Quarterly review template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/coverage-report.py` | Per-bucket coverage matrix vs target distribution | Before promotion |
| `scripts/duplicate-detector.py` | Detect near-duplicate inputs across items | Pre-promotion |
| `scripts/eval-runner.py` | Run model against golden set + produce diff vs prior version | CI gate |

## Related

- parent skill: `pro/ai/ml-engineer/`
- peer methodologies: `rag-eval-test-set-generation`, `eval-pipeline-design`, `incident-postmortem-ai-features`
- external: [Eugene Yan, evals](https://eugeneyan.com/writing/llm-evaluators/) · [Hamel Husain, golden datasets](https://hamel.dev/blog/posts/evals/)
