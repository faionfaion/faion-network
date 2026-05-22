---
slug: ai-in-project-management
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Framework for applying AI to project risk scoring, schedule variance analysis, resource capacity forecasting, and stakeholder digest generation.
content_id: "221f19eb9bde100c"
tags: [ai-pm, project-management, risk-management, automation, agile]
---
# AI in Project Management

## Summary

**One-sentence:** Framework for applying AI to project risk scoring, schedule variance analysis, resource capacity forecasting, and stakeholder digest generation.

**One-paragraph:** Framework for applying AI to project risk scoring, schedule variance analysis, resource capacity forecasting, and stakeholder digest generation. Anchor: PMBOK 8 AI Appendix and DORA 2025 Productivity Paradox — AI boosts individual task velocity but organizational throughput stays flat until bottlenecks in review/deploy are addressed.

## Applies If (ALL must hold)

- Risk register needs automated scoring across sprint data (staleness, dependent-task count, owner response rate).
- Stakeholder reports require synthesis from multiple sources (Jira, GitHub, budget sheets).
- Schedule variance must run continuously, not just at milestones.
- Resource allocation decisions need capacity forecasting across 3+ team members.
- Post-mortems need pattern extraction from historical project data.
- Project risk register needs automated scoring and trend analysis across sprint data.

## Skip If (ANY kills it)

- Projects with fewer than 3 people: overhead exceeds benefit.
- Decisions carrying legal/contractual weight: require full human sign-off with audit trail.
- Teams without baseline PM tooling (Jira/Linear/GitHub): AI has nothing to feed on.
- Highly political one-off decisions where stakeholder dynamics dominate data signals.
- Project has fewer than 3 people — overhead exceeds benefit.
- Decisions carry legal or contractual weight — AI recommendations need full human sign-off with audit trail.
- Team lacks baseline PM tooling (Jira/Linear/GitHub) — AI has nothing to feed on.

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

- parent skill: `geek/pm/pm-agile/`
