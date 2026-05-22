---
slug: ai-assisted-backlog-deduplication
tier: geek
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "End-to-end playbook for AI-assisted backlog deduplication — embeddings cluster, human review, merged/closed/kept decisions logged with traceability."
content_id: "d8f664856a7a354a"
complexity: medium
produces: playbook-step
est_tokens: 3600
tags: [ai, playbook, backlog, deduplication, embeddings]
---
# Ai Assisted Backlog Deduplication

## Summary

**One-sentence:** End-to-end playbook for AI-assisted backlog deduplication — embeddings cluster, human review, merged/closed/kept decisions logged with traceability.

**One-paragraph:** End-to-end playbook for AI-assisted backlog deduplication — embeddings cluster, human review, merged/closed/kept decisions logged with traceability. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** Product/PM-у з backlog >300 items — щоб дублі знаходились автоматично, але рішення лишалось людським.

## Applies If (ALL must hold)

- Backlog has >= 300 items across >= 6 months of accumulation.
- Embeddings provider is available (OpenAI, Cohere, local model).
- A named PM owns the backlog and will sign off on merge/close decisions.
- Tracker supports bulk updates (Jira API, Linear API).

## Skip If (ANY kills it)

- Backlog < 100 items — manual review is cheaper than the pipeline.
- No tracker API — manual cleanup remains the only option.
- Team treats backlog as append-only memory — duplication is an explicit feature.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Backlog export | CSV/JSON | Jira / Linear |
| Embeddings API key | secret | OpenAI / Cohere / local |
| Owner sign-off path | approval workflow | PM tooling |
| Duplicate-threshold calibration set | labelled CSV | manual sample of 50 |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/pm-agile/ai-assisted-velocity-anomaly-detection` | Companion AI-assist pipeline; shares the same prompt-injection guards. |
| `geek/pm/project-manager/ai-pm-tool-integration-recipes` | Tracker integration boilerplate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `embed-and-cluster` | haiku | Pure pipeline call — no judgement. |
| `threshold-calibration` | sonnet | Bounded judgement against labelled set. |
| `merge-decision-write-up` | opus | Cross-item synthesis for PM sign-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.py` | Python skeleton: load backlog → embed → cluster → emit review CSV → apply approved merges. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-assisted-backlog-deduplication.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[ai-assisted-velocity-anomaly-detection]]
- [[ai-pm-tool-integration-recipes]]
- [[exception-driven-standup-protocol]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to run the dedupe pipeline (>=300 items + embeddings + owner + 50-label calibration), block until calibration exists, or skip (small backlog). Run before any embed call costs money.
