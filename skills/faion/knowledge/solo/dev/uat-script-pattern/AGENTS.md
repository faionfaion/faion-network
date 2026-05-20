---
slug: uat-script-pattern
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "8198df9471d531ae"
summary: "Uat Script Pattern: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Major release QA cycle: regression + smoke + UAT'."
tags: [uat-script-pattern, dev, solo]
---
# Uat Script Pattern

## Summary

**One-sentence:** Uat Script Pattern: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Major release QA cycle: regression + smoke + UAT'.

**One-paragraph:** Addresses the gap surfaced by 'role-qa-engineer/Major release QA cycle: regression + smoke + UAT': UAT scripts often regress to ad-hoc Google Docs; need a repeatable script template tied to acceptance criteria + sign-off log. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a uat script pattern artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-qa-engineer/Major release QA cycle: regression + smoke + UAT' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working uat script pattern artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-qa-engineer/Major release QA cycle: regression + smoke + UAT' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/dev` | parent domain group — provides operating context for Uat Script Pattern |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/uat-script-pattern.json` | JSON schema for the Uat Script Pattern output contract |
| `templates/uat-script-pattern.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-uat-script-pattern.py` | Enforce Uat Script Pattern output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/`
- upstream playbook: `role-qa-engineer/Major release QA cycle: regression + smoke + UAT`
- solo/dev/role-qa-engineer
