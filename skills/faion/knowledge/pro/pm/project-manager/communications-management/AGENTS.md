---
slug: communications-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured who-what-when-how matrix (comms/plan.
content_id: "1fd0695dcdc612d7"
tags: [communications, stakeholder, status-reporting, meeting-management, decision-log]
---
# Communications Management

## Summary

**One-sentence:** A structured who-what-when-how matrix (comms/plan.

**One-paragraph:** A structured who-what-when-how matrix (comms/plan.yaml) that maps every stakeholder to their information need, delivery channel, cadence, and owner. Status report colour (GREEN/YELLOW/RED) derives from quantitative schedule and budget thresholds, not PM judgment. Decisions are never stored in chat — they are logged in a versioned decision record. The plan self-monitors via a weekly audit script that opens issues for overdue communications.

## Applies If (ALL must hold)

- New projects where stakeholder count is above 5 and you need a written matrix before kickoff.
- Distributed or async-first teams where missed updates are the dominant failure mode.
- Regulated programs (SOX, HIPAA, GDPR, MDR) requiring traceable, dated, signed-off communications.
- "Drowning in Slack/email" situations: consolidate channels and kill duplicate updates.
- Multi-vendor engagements with formal status cadences and escalation paths required by contract.

## Skip If (ANY kills it)

- Solo founders or 2-3-person startups pre-PMF — matrix overhead exceeds value; a single Slack channel works.
- Crisis or incident response — runbooks and on-call rotations replace this; do not retrofit during P0.
- Short spikes under 2 weeks — agree on channel verbally, skip the artifact.
- When stakeholders refuse classification or the political situation is too fluid to commit to a cadence.

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

- parent skill: `pro/pm/project-manager/`
