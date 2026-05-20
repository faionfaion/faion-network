---
slug: tracker-ai-triage-classify-route
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Pipe every inbound bug or request through a six-step triage agent before any human picks it up: classify type (bug/story/epic/task/spike), score severity with an attached SLA timer (blocker/critical/major/minor), dedupe against the last 1000 issues by title+body cosine similarity, apply /area/*, /component/*, /lang/* labels, route to the CODEOWNERS-derived team, and assign to the least-loaded engineer on that team.
content_id: "d29c5e53e5f77aab"
tags: [triage, issue-tracker, ai-agent, classification, routing]
---
# AI Triage, Classify, and Route Inbound Issues

## Summary

**One-sentence:** Pipe every inbound bug or request through a six-step triage agent before any human picks it up: classify type (bug/story/epic/task/spike), score severity with an attached SLA timer (blocker/critical/major/minor), dedupe against the last 1000 issues by title+body cosine similarity, apply /area/*, /component/*, /lang/* labels, route to the CODEOWNERS-derived team, and assign to the least-loaded engineer on that team.

**One-paragraph:** Pipe every inbound bug or request through a six-step triage agent before any human picks it up: classify type (bug/story/epic/task/spike), score severity with an attached SLA timer (blocker/critical/major/minor), dedupe against the last 1000 issues by title+body cosine similarity, apply /area/*, /component/*, /lang/* labels, route to the CODEOWNERS-derived team, and assign to the least-loaded engineer on that team. Severity = blocker MUST require an on-call confirmation before the SLA timer arms; everything else is auto-routed. The agent emits a single comment listing every classification it applied so the assignee can dispute any field with one reaction.

## Applies If (ALL must hold)

- High-volume inbound queues over ~50 issues per week where manual triage is the documented bottleneck.
- Linear's Triage Intelligence or Jira's AI Backlog can be the drop-in implementation rather than a custom build.
- Multi-team monorepos that already maintain CODEOWNERS — routing piggybacks on the same matrix.
- Teams with at least three months of historical issue + assignment data so the routing model has a non-cold-start.

## Skip If (ANY kills it)

- Small teams (under five engineers) where the cost of triage agent setup exceeds manual work.
- Domains where misclassification has security or legal consequences without specialist review.
- Cold-start projects: under three months of history yields routing accuracy too low to act on without human review.
- Single-repo solo projects — every issue is self-routed by definition.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
