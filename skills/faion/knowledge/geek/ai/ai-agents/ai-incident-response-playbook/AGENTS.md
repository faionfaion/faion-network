---
slug: ai-incident-response-playbook
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Operational runbook for ai incident response playbook — step-by-step actions, decision points, and escalation triggers ready to execute under stress.
content_id: "9f99865ef7b57428"
tags: [ai, runbook]
---
# AI Incident Response Playbook

## Summary

**One-sentence:** Operational runbook for ai incident response playbook — step-by-step actions, decision points, and escalation triggers ready to execute under stress.

**One-paragraph:** Operational runbook for ai incident response playbook — step-by-step actions, decision points, and escalation triggers ready to execute under stress. When an AI feature misbehaves in production, PMs co-own the response with eng. No playbook for triage + comms + rollback.

## Applies If (ALL must hold)

- You are on-call or directly responsible for the operational scenario covered by ai incident response playbook.
- The runbook is loaded BEFORE the incident (drill or pre-read) — not discovered during a page.
- Each step has an unambiguous owner, exit criterion, and elapsed-time budget.
- Decision branches name the input signal explicitly (metric, log line, alert ID).

## Skip If (ANY kills it)

- Investigative R&D where the goal is to learn, not restore service.
- Rare events with cost-of-staleness > cost-of-improvisation (annual close, novel breach).
- Vendor-owned systems where the action is 'call support and wait'.

## Prerequisites

- On-call rotation or paging path that loads this runbook on alert.
- Test/staging environment where each branch is exercisable.
- Last incident postmortem read; any open action item from it consumed.

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
| `step_execute` | haiku | Imperative action against named system |
| `branch_decision` | sonnet | Signal interpretation and route choice |
| `incident_writeup` | opus | Postmortem narrative with root cause |

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
