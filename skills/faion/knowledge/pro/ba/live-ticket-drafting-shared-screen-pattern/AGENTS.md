---
slug: live-ticket-drafting-shared-screen-pattern
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Live Ticket Drafting Shared Screen Pattern: codified ba practice that turns the recurring 'p4-outsource-specialist/JIRA ticket scoping session with client PM' decision into a repeatable, auditable artefact.
content_id: "a60e1a79984ec958"
tags: [live-ticket-drafting-shared-screen-pattern, ba, pro]
---
# Live Ticket Drafting Shared Screen Pattern

## Summary

**One-sentence:** Live Ticket Drafting Shared Screen Pattern: codified ba practice that turns the recurring 'p4-outsource-specialist/JIRA ticket scoping session with client PM' decision into a repeatable, auditable artefact.

**One-paragraph:** Live Ticket Drafting Shared Screen Pattern addresses the gap identified by the p4-outsource-specialist/JIRA ticket scoping session with client PM playbook: Elicitation methodologies exist but the specific pattern of drafting the ticket on screen during the call (vs taking notes and editing later) is a separate, distinct skill with very different stakeholder dynamics. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p4-outsource-specialist/JIRA ticket scoping session with client PM OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p4-outsource-specialist/JIRA ticket scoping session with client PM task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/live-ticket-drafting-shared-screen-pattern.json` | JSON schema for the Live Ticket Drafting Shared Screen Pattern output contract |
| `templates/live-ticket-drafting-shared-screen-pattern.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-live-ticket-drafting-shared-screen-pattern.py` | Enforce Live Ticket Drafting Shared Screen Pattern output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/business-analyst/`
- upstream playbook: `p4-outsource-specialist/JIRA ticket scoping session with client PM`
