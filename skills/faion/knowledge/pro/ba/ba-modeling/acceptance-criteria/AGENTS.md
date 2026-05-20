---
slug: acceptance-criteria
tier: pro
group: ba
domain: ba-modeling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Acceptance criteria (AC) define the exact conditions a requirement must satisfy to be accepted as complete.
content_id: "96fc82f8dbdd8592"
tags: [acceptance-criteria, spec, testing, bdd, gherkin]
---
# Acceptance Criteria

## Summary

**One-sentence:** Acceptance criteria (AC) define the exact conditions a requirement must satisfy to be accepted as complete.

**One-paragraph:** Acceptance criteria (AC) define the exact conditions a requirement must satisfy to be accepted as complete. Each criterion is testable, behaviour-level, and carries a stable ID (AC-FEATURE-NN) that cross-references spec.md, test-plan.md, PR description, CI report, and changelog. Two formats: Given/When/Then (Gherkin/BDD) for user-facing behaviour, and rule-based checklists for system constraints.

## Applies If (ALL must hold)

- Authoring AC for SDD spec.md files before a coding subagent picks up the task.
- Translating a freeform user story or stakeholder note into testable criteria.
- Generating regression scenarios from a bug report so the fix has a definition-of-done gate before merge.
- Splitting an oversized story: when AC count exceeds 7 per story, that is the slicing signal.
- Wiring AC to executable specs (Gherkin to Cucumber / Behave / Playwright) so BA review and CI share one artifact.

## Skip If (ANY kills it)

- Pure spike / research tasks where the outcome is a learning, not a behaviour.
- Throwaway prototypes or demos with a lifespan under one sprint.
- UX-only changes where verification is subjective (visual polish, brand tone).
- Operational runbook changes (server tweaks, cron edits) — use smoke checks instead.
- Negotiation-heavy external contracts where AC ossify before scope is stable.

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

- parent skill: `pro/ba/ba-modeling/`
