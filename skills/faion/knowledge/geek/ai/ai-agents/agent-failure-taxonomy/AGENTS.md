---
slug: agent-failure-taxonomy
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Shared vocabulary and decision tree for agent failure taxonomy — assigns every observed instance to one labelled class so postmortems and dashboards aggregate cleanly.
content_id: "f0b9b19a7254aee5"
tags: [agent, ai, taxonomy]
---
# Agent Failure Taxonomy

## Summary

**One-sentence:** Shared vocabulary and decision tree for agent failure taxonomy — assigns every observed instance to one labelled class so postmortems and dashboards aggregate cleanly.

**One-paragraph:** Shared vocabulary and decision tree for agent failure taxonomy — assigns every observed instance to one labelled class so postmortems and dashboards aggregate cleanly. Without a shared vocabulary (hallucination vs reasoning-shortfall vs tool-misuse vs context-overflow vs injection vs drift) postmortems are ad-hoc and regression evals are not reusable across teams. P7's strategic-AI-narrative requires faion to own this taxonomy before competitors do.

## Applies If (ALL must hold)

- You triage incidents, issues, or failures and need a shared label set per agent failure taxonomy.
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
| `geek/ai/ai-agents/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

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

- parent skill: `geek/ai/ai-agents/`
- peer methodologies: see siblings under `geek/ai/ai-agents/`
- external: industry references cited inline in `content/01-core-rules.xml`
