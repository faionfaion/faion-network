---
slug: deliverability-incident-runbook
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Deliverability Incident Runbook: codified marketing practice that turns the recurring 'role-growth-marketing/Lifecycle email send + post-send analytics (per send)' decision into a repeatable, auditable artefact.
content_id: "10e1cd1c6b6bbebf"
tags: [deliverability-incident-runbook, marketing, pro]
---
# Deliverability Incident Runbook

## Summary

**One-sentence:** Deliverability Incident Runbook: codified marketing practice that turns the recurring 'role-growth-marketing/Lifecycle email send + post-send analytics (per send)' decision into a repeatable, auditable artefact.

**One-paragraph:** Deliverability Incident Runbook addresses the gap surfaced by 'role-growth-marketing/Lifecycle email send + post-send analytics (per send)'. When unsub / spam spikes, marketers panic-Google. Need a runbook: SPF/DKIM check, ESP reputation, segment isolate, throttle send. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-growth-marketing/Lifecycle email send + post-send analytics (per send)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-growth-marketing/Lifecycle email send + post-send analytics (per send)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent role skill — provides the operating context for this methodology |

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
| `synthesize_decision` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/deliverability-incident-runbook.json` | JSON schema for the Deliverability Incident Runbook output contract |
| `templates/deliverability-incident-runbook.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-deliverability-incident-runbook.py` | Enforce Deliverability Incident Runbook output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- upstream playbook: `role-growth-marketing/Lifecycle email send + post-send analytics (per send)`
- methodology family: `pro/marketing/` (gap-p2 batch, F-059-063)
