---
slug: agent-kill-switch-design
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Safety control design for agent kill switch design — the kill, isolate, and rollback paths tested before any production exposure.
content_id: "d5fe7d2addd146f7"
tags: [agent, ai, safety]
---
# Agent Kill Switch Design

## Summary

**One-sentence:** Safety control design for agent kill switch design — the kill, isolate, and rollback paths tested before any production exposure.

**One-paragraph:** Safety control design for agent kill switch design — the kill, isolate, and rollback paths tested before any production exposure. How to design and test a runtime kill switch for an agent (per-tenant, global, per-tool). Required for production rollout but absent.

## Applies If (ALL must hold)

- You expose or operate the system covered by agent kill switch design to non-internal users (customers, paying or pilot).
- Failure of the safety control results in user-visible damage (cost, data, trust).
- Pre-prod verification of the control is feasible and budgeted.
- Roll-forward and roll-back paths are both tested, not just documented.

## Skip If (ANY kills it)

- Internal-only, dev-tier tools with no external blast radius.
- Trivially reversible actions (DRAFT-only outputs, dry-run flags) where safety is implicit.
- Cost of safety control > expected loss times probability over the next 90 days.

## Prerequisites

- Audit log of operations the control gates (one-way street: every privileged action observable).
- Drill scheduled — control verified at least once outside an incident.
- Roll-forward + roll-back contracts written and dry-run.

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
| `control_invocation` | haiku | Tool call to kill / quarantine / freeze |
| `postcontrol_audit` | sonnet | Verify control effects in logs |
| `policy_iteration` | opus | Tune thresholds based on drill outcomes |

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
