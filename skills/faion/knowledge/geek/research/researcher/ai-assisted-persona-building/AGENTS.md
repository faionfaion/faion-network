---
slug: ai-assisted-persona-building
tier: geek
group: research
domain: researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A three-stage pipeline for building data-driven personas from behavioral analytics data: Haiku ingests and normalizes event exports; Opus identifies cluster boundaries with silhouette validation; Sonnet generates persona narratives, JTBD maps, and pain-point summaries.
content_id: "73260ac58e8f8236"
tags: [personas, clustering, behavioral-data, jtbd, user-research]
---
# AI-Assisted Persona Building

## Summary

**One-sentence:** A three-stage pipeline for building data-driven personas from behavioral analytics data: Haiku ingests and normalizes event exports; Opus identifies cluster boundaries with silhouette validation; Sonnet generates persona narratives, JTBD maps, and pain-point summaries.

**One-paragraph:** A three-stage pipeline for building data-driven personas from behavioral analytics data: Haiku ingests and normalizes event exports; Opus identifies cluster boundaries with silhouette validation; Sonnet generates persona narratives, JTBD maps, and pain-point summaries. A mandatory human gate sits between clustering and narrative generation — the researcher names and validates clusters before the agent writes about them.

## Applies If (ALL must hold)

- Building initial personas from existing behavioral data (analytics, CRM, interview transcripts).
- Updating stale personas when new behavioral data or cohort segments emerge.
- Generating JTBD statements from clustered behavioral patterns.
- Automating persona refresh as part of a recurring monthly or quarterly pipeline.

## Skip If (ANY kills it)

- When no actual user data exists — without data the result is a synthetic persona, not a data-driven one.
- As a final deliverable without team validation — AI clusters need human labeling and context.
- When the user base is too homogeneous — clustering adds overhead without insight gain.
- High-stakes segmentation (pricing tiers, feature gating) without statistical validation of cluster stability.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/research/researcher/`
