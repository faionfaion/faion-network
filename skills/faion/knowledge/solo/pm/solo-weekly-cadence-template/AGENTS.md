---
slug: solo-weekly-cadence-template
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Sunday-review + Monday-prime weekly cadence template tailored for a one-operator product — fixed artifacts, memory hooks, time-boxed.
content_id: "9cf9ffcb9b424b82"
tags: [solo-weekly-cadence-template, pm, solo]
---
# Solo Weekly Cadence Template

## Summary

**One-sentence:** A Sunday-review + Monday-prime weekly cadence for a one-operator SaaS or solo practice — fixed artifacts (week-note + next-week-plan), explicit memory hooks, hard time-box.

**One-paragraph:** Existing `weekly-review-solo` methodologies state intent ("review the week") but leave the artifact set vague, so the ritual drifts and dies. This template fixes (a) the exact two artifacts produced each week, (b) the four mandatory inputs reviewed, (c) the memory-hook step that connects this week's decisions back to last week's plan, and (d) a 60-minute total time-box split 30/30 between Sunday review and Monday prime. Optimised for the case where the operator is also the engineer, the marketer, and the support team.

## Applies If (ALL must hold)

- the operator is solo (no team to broadcast to)
- the product or practice is live (i.e. there is "last week" data worth reviewing)
- the operator is in week ≥4 of running the product or practice
- weekend availability allows a 30-minute Sunday slot

## Skip If (ANY kills it)

- the operator is on holiday / parental leave — pause cadence rather than half-ass it
- product is pre-launch with no users — switch to a build-week cadence
- the operator works in a team that already runs a Monday standup (use that)
- cadence has been skipped 3 weeks in a row — restart, don't try to "catch up"

## Prerequisites

- a single weekly-note file template (Notion / Obsidian / markdown)
- access to the KPI dashboard from `solo/product/solo-kpi-dashboard-template`
- a backlog or todo list with last-week's plan items
- 60 minutes of uninterrupted time between Sunday and Monday morning

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager` | parent skill |
| `solo/product/solo-kpi-dashboard-template` | source for the metrics block of the weekly note |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: two-artifacts-only, four-mandatory-inputs, memory-hook-required, 60-min-time-box, no-catchup-restart | ~1000 |

## Related

- parent skill: `solo/pm/project-manager`
- upstream playbook: `p1-solo-saas-builder/Sunday roadmap & week-shaping ritual`
- sibling: `solo/product/solo-kpi-dashboard-template`
