---
slug: alert-triage-decision-tree
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Alert Triage Decision Tree: codified AI-in-SDLC practice that turns the recurring 'p6-product-dev-team/Sentry / Datadog alert triage (in-hours)' decision into a repeatable, auditable artefact.
content_id: "917cb1734f137f39"
tags: [alert-triage-decision-tree, sdlc-ai, geek]
---
# Alert Triage Decision Tree

## Summary

**One-sentence:** Alert Triage Decision Tree: codified AI-in-SDLC practice that turns the recurring 'p6-product-dev-team/Sentry / Datadog alert triage (in-hours)' decision into a repeatable, auditable artefact.

**One-paragraph:** Alert Triage Decision Tree addresses the gap identified by the p6-product-dev-team/Sentry / Datadog alert triage (in-hours) playbook: We have inc-* runbook + read-only-investigation pages but no flat decision tree for the first 5 minutes after an alert fires (noise / dup / new / escalate). Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p6-product-dev-team/Sentry / Datadog alert triage (in-hours) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p6-product-dev-team/Sentry / Datadog alert triage (in-hours) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/sdlc-ai-operator` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned | ~900 |
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
| `templates/alert-triage-decision-tree.json` | JSON schema for the Alert Triage Decision Tree output contract |
| `templates/alert-triage-decision-tree.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-alert-triage-decision-tree.py` | Enforce Alert Triage Decision Tree output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/sdlc-ai/`
- upstream playbook: `p6-product-dev-team/Sentry / Datadog alert triage (in-hours)`
