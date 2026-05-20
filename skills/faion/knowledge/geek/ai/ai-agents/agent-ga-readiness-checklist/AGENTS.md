---
slug: agent-ga-readiness-checklist
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Concrete operating checklist covering agent ga readiness checklist — the small set of items a practitioner runs every cycle so nothing high-leverage gets skipped.
content_id: "ef51138693ee957f"
tags: [agent, ai, checklist]
---
# Agent GA Readiness Checklist

## Summary

**One-sentence:** Concrete operating checklist covering agent ga readiness checklist — the small set of items a practitioner runs every cycle so nothing high-leverage gets skipped.

**One-paragraph:** Concrete operating checklist covering agent ga readiness checklist — the small set of items a practitioner runs every cycle so nothing high-leverage gets skipped. Geek-tier builders ship to small numbers of paying customers. They need a hardened checklist (auth, rate-limits, billing, eval bar, runbook, rollback) before flipping pilot → GA. Right now this is buried in vendor blog posts.

## Applies If (ALL must hold)

- You operate the recurring activity addressed by agent ga readiness checklist at least once per cycle (weekly, sprint, quarter, or annual).
- You have authority to act on each item — checklist items without owners or budget are deferred.
- Skipped items must be auditable: a written reason replaces the action.
- Time-box: full pass completes within the cycle window (e.g., 30-90 min for weekly, 1-2 days for annual).

## Skip If (ANY kills it)

- One-off events with no recurrence — checklist value is in the rhythm.
- Activities without a named owner — items will not be done, only ticked.
- Teams running a more granular checklist already — adding a meta-layer creates conflict.

## Prerequisites

- Calendar slot dedicated to the cycle (recurring meeting / focus block).
- Read-access to the source systems each item inspects (analytics, billing, repo).
- Last cycle's output filed where current cycle can compare year-over-year.

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
| `checklist_dry_run` | haiku | Template walk, no judgment needed |
| `anomaly_flag` | sonnet | Compare current cycle vs prior, flag deltas |
| `decision_synthesis` | opus | Consolidate flags into a corrective-action list |

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
