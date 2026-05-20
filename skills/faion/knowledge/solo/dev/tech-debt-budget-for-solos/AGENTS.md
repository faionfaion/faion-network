---
slug: tech-debt-budget-for-solos
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "d59cdbc293de01dc"
summary: "Tech Debt Budget For Solos: produces a versioned, owner-signed artefact that closes the gap 'p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)'."
tags: [tech-debt-budget-for-solos, dev, solo]
---
# Tech Debt Budget For Solos

## Summary

**One-sentence:** Tech Debt Budget For Solos: produces a versioned, owner-signed artefact that closes the gap 'p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)'.

**One-paragraph:** Addresses the gap surfaced by 'p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)': solo/dev/code-quality/tech-debt-management exists but reads like an enterprise framework. A solo needs a tight budget: 'one debt-reduction session per shipped feature' or 'cap debt items at N' — a small, lived rule, not a process. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a tech debt budget for solos artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working tech debt budget for solos artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/dev` | parent domain group — provides operating context for Tech Debt Budget For Solos |

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
| `templates/tech-debt-budget-for-solos.json` | JSON schema for the Tech Debt Budget For Solos output contract |
| `templates/tech-debt-budget-for-solos.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-budget-for-solos.py` | Enforce Tech Debt Budget For Solos output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/`
- upstream playbook: `p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)`
- solo/dev/p1-solo-saas-builder
