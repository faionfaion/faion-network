---
slug: alert-to-fix-incident-loop
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Alert to Fix Incident Loop: codified engineering practice that turns the recurring 'role-software-developer/Sentry/Datadog alert → bugfix → ship' decision into a repeatable, auditable artefact.
content_id: "38f8ab6000507b53"
tags: [alert-to-fix-incident-loop, dev, solo]
---
# Alert to Fix Incident Loop

## Summary

**One-sentence:** Alert to Fix Incident Loop: codified engineering practice that turns the recurring 'role-software-developer/Sentry/Datadog alert → bugfix → ship' decision into a repeatable, auditable artefact.

**One-paragraph:** Alert to Fix Incident Loop addresses the gap identified by the role-software-developer/Sentry/Datadog alert → bugfix → ship playbook: api-monitoring-* methodologies live at pro tier and are observability-focused. A solo-tier 'one alert end-to-end' playbook is missing — this is daily work in P4/P6. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-software-developer/Sentry/Datadog alert → bugfix → ship OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-software-developer/Sentry/Datadog alert → bugfix → ship task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-blameless | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/alert-to-fix-incident-loop.json` | JSON schema for the Alert to Fix Incident Loop output contract |
| `templates/alert-to-fix-incident-loop.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-alert-to-fix-incident-loop.py` | Enforce Alert to Fix Incident Loop output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/`
- upstream playbook: `role-software-developer/Sentry/Datadog alert → bugfix → ship`
- external: [Allspaw 2012](https://www.kitchensoap.com/2012/10/25/on-being-a-senior-engineer/) · [Google SRE Postmortem chapter](https://sre.google/sre-book/postmortem-culture/)
