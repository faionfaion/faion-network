# Solo Incident Triage Checklist

## Summary

**One-sentence:** Generates a one-page incident-triage checklist for a solo operator — assess, contain, communicate, fix, learn — gated by a named on-call owner.

**One-paragraph:** Solo incident response without a checklist devolves into panicked tab-switching. This methodology pins five phases: ASSESS (what's broken, who's affected), CONTAIN (stop the bleeding — rollback or feature-flag off), COMMUNICATE (status page + customer comms in 15 min), FIX (root cause + verified deploy), LEARN (blameless postmortem inside 72h). Output: an IncidentReport.

**Ефективно для:**

- Solo operator who has stared at logs for 40 minutes without acting.
- Live outage where a status update should have gone out 20 minutes ago.
- Cascading failures where the wrong thing was rolled back first.
- Postmortem culture where lessons get lost between incidents.

## Applies If (ALL must hold)

- Live production incident — users impacted or service degraded.
- Operator is the only on-call.
- Decision must be made between rollback, feature-flag, and forward-fix.
- Postmortem expected (paying customers OR ≥ 1h downtime).

## Skip If (ANY kills it)

- Pre-launch hobby project with no real users.
- Internal-only tooling — incident severity is low.
- Already mid-incident on a different playbook — finish the active one first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Status page or comms channel | URL | operator setup |
| Rollback procedure for the current version | doc path | deploy plan |
| Feature-flag toggle inventory | list | operator config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| solo-deploy-checklist | Rollback procedure comes from the deploy plan. |
| monitoring-logging | Detection surface + log paths. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-named-on-call, r2-comms-within-15min, r3-contain-before-fix, r4-blameless-postmortem, r5-no-untested-forward-fix | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Solo Incident Triage Checklist artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: tab-switching-no-action, silent-incident, forward-fix-on-prod, postmortem-skipped | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `assess-impact` | sonnet | Per-incident scoping with stakes. |
| `draft-comms` | sonnet | Customer-facing language; balance honesty + signal. |
| `compose-postmortem` | opus | High-stakes synthesis — root cause + actions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-incident-triage-checklist.json` | IncidentReport JSON skeleton. |
| `templates/solo-incident-triage-checklist.md` | Markdown triage checklist for live use. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-incident-triage-checklist.py` | Validate IncidentReport JSON against the schema. | Post-incident before closing. |

## Related

- [[solo-deploy-checklist]]
- [[monitoring-logging]]
- [[health-checks-autoheal]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
