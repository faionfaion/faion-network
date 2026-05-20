---
slug: solo-incident-triage-checklist
tier: solo
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Bedside 4-step triage checklist a solo operator runs in the first 15 minutes of a prod incident — before paging anyone, before diving into logs, before posting to status.
content_id: "ebb7eeb34bcc8000"
tags: [solo-incident-triage-checklist, infra, solo]
---
# Solo Incident Triage Checklist

## Summary

**One-sentence:** A 4-step kept-by-the-bedside checklist that a solo operator runs in the first 15 minutes of a production incident, before any deep debugging.

**One-paragraph:** Solo operators have no team to delegate to during an incident — there is no SRE on call, no Slack war room, no second pair of eyes. This methodology fixes the recurring "panic-first" failure mode by reducing the first 15 minutes to four deterministic actions: stop the bleed, snapshot state, set a hard deadline, then debug. It complements `solo/infra/server-craft/health-checks-autoheal` (which covers automated recovery primitives); this is the human-in-the-loop layer that sits on top.

## Applies If (ALL must hold)

- production user-facing service is degraded or down
- the operator is the only human responder
- no automatic rollback has fired (or rollback failed)
- elapsed time since alert < 15 minutes

## Skip If (ANY kills it)

- the incident is already past the 15-minute window — switch to incident-management methodology, not triage
- auto-recovery (health-checks-autoheal) already resolved the alert — log and move on
- the "incident" is a feature request or a known-issue ticket misrouted as a page

## Prerequisites

- a single bookmarked status URL (Plausible / UptimeRobot / Better Stack)
- write-access to a one-line incident log file (`~/incidents/YYYY-MM-DD.md`)
- runbook for the top-3 known failure modes (DB down, deploy bad, third-party API out)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft` | parent infra skill — host/service shape |
| `solo/infra/one-person-rollback-runbook` | downstream — invoked if step-1 says "roll back" |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: stop-bleed-first, snapshot-before-fix, 15-min-deadline, single-incident-log, no-fix-without-evidence | ~900 |

## Related

- parent skill: `solo/infra/server-craft`
- upstream playbook: `p1-solo-saas-builder/Solo prod incident response (no team safety net)`
- sibling: `solo/infra/one-person-rollback-runbook`
