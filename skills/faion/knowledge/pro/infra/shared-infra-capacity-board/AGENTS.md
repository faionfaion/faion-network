---
slug: shared-infra-capacity-board
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Shared Infra Capacity Board — a weekly cross-team artefact that surfaces upcoming demand on shared Kafka, Redis, DB, and similar resources before it becomes a fight.
content_id: "801b390f3067ccc5"
tags: [shared-infra-capacity-board, infra, pro]
---
# Shared Infra Capacity Board

## Summary

**One-sentence:** A weekly board (Confluence page, Notion DB, or simple repo file) where every team posts its 4-week demand projection for shared infra resources, so the architects' sync turns capacity fights into priority decisions with data.

**One-paragraph:** Cross-team architects routinely fight over shared infra — Kafka topics, Redis memory, primary DB connections, K8s node groups — because each team plans capacity in isolation and only discovers the conflict at deploy time. The shared-infra-capacity-board codifies a weekly surfacing ritual: every team posts (a) the resource they will lean on, (b) the projected delta, (c) the date they need it, (d) the owner. The board feeds the weekly architecture sync; conflicts surface a week in advance, not at incident time.

## Applies If (ALL must hold)

- ≥3 teams share at least one piece of infrastructure (Kafka, Redis, DB cluster, K8s node pool, search cluster, etc.)
- a weekly architecture sync (or equivalent ceremony) exists and is attended by team leads or architects
- teams have rough numerical projections of demand (RPS, topic count, connection count, memory)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the org runs one team per resource — no sharing means no contention to surface
- shared infra has auto-scaling capacity well beyond projected demand (the board adds bureaucracy without value)
- there is no weekly forum to feed; without a decision-making consumer the board rots

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | 5 testable rules: required fields, weekly cadence, owner accountability, conflict-resolution path, archive policy |

## Related

- upstream playbook: `role-software-architect/Cross-team architecture sync (weekly)`
- parent skill: `pro/infra/`
