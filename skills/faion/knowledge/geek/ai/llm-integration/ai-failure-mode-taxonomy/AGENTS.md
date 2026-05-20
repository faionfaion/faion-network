---
slug: ai-failure-mode-taxonomy
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Shared vocabulary and decision tree for ai failure mode taxonomy — assigns every observed instance to one labelled class so postmortems and dashboards aggregate cleanly.
content_id: "7ec5cf66b4969a56"
tags: [ai, taxonomy]
---
# AI Failure Mode Taxonomy

## Summary

**One-sentence:** Shared vocabulary and decision tree for ai failure mode taxonomy — assigns every observed instance to one labelled class so postmortems and dashboards aggregate cleanly.

**One-paragraph:** Shared vocabulary and decision tree for ai failure mode taxonomy — assigns every observed instance to one labelled class so postmortems and dashboards aggregate cleanly. Reusable taxonomy (knowledge gap, reasoning gap, format gap, style gap, safety gap, latency gap) to triage AI feature failures and pick the right remediation.

## Applies If (ALL must hold)

- You triage incidents, issues, or failures and need a shared label set per ai failure mode taxonomy.
- Labels feed dashboards or postmortems — consistent classification matters more than perfect labels.
- Mis-classification cost (wrong remediation path) is bounded — labels are not safety-critical.
- Taxonomy is versioned; new categories require explicit approval, not ad-hoc creation.

## Skip If (ANY kills it)

- Failure modes that are still being discovered — premature labels lock in wrong categories.
- Pre-incident exercises with no real data yet — interview-driven, not taxonomy-driven.
- Single-incident retros where one-off detail matters more than aggregation.

## Prerequisites

- Initial label set drafted from ≥10 historical instances.
- Owner who can approve new categories without weekly meeting overhead.
- Tagging tool that lets re-labelling happen without losing history.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `single_instance_classify` | haiku | Fast label assignment from pre-existing taxonomy |
| `taxonomy_review` | sonnet | Detect misuse, propose new categories |
| `policy_update` | opus | Re-shape taxonomy when drift exceeds threshold |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `geek/ai/llm-integration/`
- peer methodologies: see siblings under `geek/ai/llm-integration/`
- external: industry references cited inline in `content/01-core-rules.xml`
