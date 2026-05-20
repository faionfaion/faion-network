---
slug: trust-boundary-diff-helper
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3eb44b8d7f4ff4f9"
summary: "Trust Boundary Diff Helper: produces a versioned, owner-signed artefact that closes the gap 'role-software-architect/Security review of a new dependency or service edge'."
tags: [trust-boundary-diff-helper, dev, pro]
---
# Trust Boundary Diff Helper

## Summary

**One-sentence:** Trust Boundary Diff Helper: produces a versioned, owner-signed artefact that closes the gap 'role-software-architect/Security review of a new dependency or service edge'.

**One-paragraph:** Addresses the gap surfaced by 'role-software-architect/Security review of a new dependency or service edge': When a PR adds a new external call or auth surface, architects need a quick diff against existing trust boundaries. Missing. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a trust boundary diff helper artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-software-architect/Security review of a new dependency or service edge' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working trust boundary diff helper artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-software-architect/Security review of a new dependency or service edge' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Trust Boundary Diff Helper |

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
| `templates/trust-boundary-diff-helper.json` | JSON schema for the Trust Boundary Diff Helper output contract |
| `templates/trust-boundary-diff-helper.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trust-boundary-diff-helper.py` | Enforce Trust Boundary Diff Helper output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-software-architect/Security review of a new dependency or service edge`
- pro/dev/role-software-architect
