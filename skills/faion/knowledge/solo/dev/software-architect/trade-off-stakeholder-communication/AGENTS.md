---
slug: trade-off-stakeholder-communication
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Architecture trade-offs must be communicated differently to executives, product managers, engineers, and operations.
content_id: "2c039ea157acff50"
tags: [stakeholder-communication, trade-off, adr, documentation, architecture]
---
# Trade-off Communication and Documentation

## Summary

**One-sentence:** Architecture trade-offs must be communicated differently to executives, product managers, engineers, and operations.

**One-paragraph:** Architecture trade-offs must be communicated differently to executives, product managers, engineers, and operations. Every significant decision requires structured documentation covering context, evaluated options, criteria and weights, identified trade-offs, risks and mitigations, and decision rationale. Stakeholder surprise — trade-offs discovered in production — is the most costly failure mode.

## Applies If (ALL must hold)

- Writing the "Consequences" section of any ADR — to enumerate explicit gain/loss pairs.
- Presenting a technology or architecture decision to non-technical stakeholders (executives, product).
- Generating an ADR from a decision matrix or ATAM analysis.
- Stakeholder review before committing to a Type-1 irreversible decision.
- Post-implementation review — communicating whether predicted trade-offs materialized.

## Skip If (ANY kills it)

- Type-2 reversible small-scope decisions — a brief ADR comment is sufficient; full stakeholder communication creates noise.
- When stakeholders have not been identified yet — agents will invent generic personas and the output looks plausible but binds nobody.

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
