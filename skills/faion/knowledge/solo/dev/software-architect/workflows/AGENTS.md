---
slug: workflows
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Seven repeatable workflow types for architecture activities: system design, architecture review, ADR creation, technology evaluation, ATAM/CBAM assessment, migration planning (Strangler Fig), and design-document review.
content_id: "5855a9b1517a6537"
tags: [architecture, workflows, adr, design-review, technology-evaluation]
---
# Architecture Workflows

## Summary

**One-sentence:** Seven repeatable workflow types for architecture activities: system design, architecture review, ADR creation, technology evaluation, ATAM/CBAM assessment, migration planning (Strangler Fig), and design-document review.

**One-paragraph:** Seven repeatable workflow types for architecture activities: system design, architecture review, ADR creation, technology evaluation, ATAM/CBAM assessment, migration planning (Strangler Fig), and design-document review. Each workflow is a named pipeline of steps; agents run them as role-specialized subagent chains — clarifier, designer, critic, documenter — with state materialized to disk between steps.

## Applies If (ALL must hold)

- Standardizing repeated architecture activities across a team: pick one workflow per artifact type and stop inventing new review forms.
- Onboarding: gives a new architect a checklist instead of tribal knowledge.
- Multi-stakeholder decisions where the workflow ceremony (readouts, async review) is itself the deliverable.
- Audit-grade documentation where you must show "we followed an evaluation method."

## Skip If (ANY kills it)

- One-person, one-decision contexts — workflow ceremony costs more than the decision value.
- Pure code-level refactors — use design-pattern methodologies instead.
- Tight time-boxed prototypes — the workflows assume room for review cycles.

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

- parent skill: `solo/dev/software-architect/`
