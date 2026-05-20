---
slug: threat-model-lite-workshop
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "2ee157ca5886079e"
summary: "Threat Model Lite Workshop: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Security testing program rollout'."
tags: [threat-model-lite-workshop, dev, pro]
---
# Threat Model Lite Workshop

## Summary

**One-sentence:** Threat Model Lite Workshop: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Security testing program rollout'.

**One-paragraph:** Addresses the gap surfaced by 'role-qa-engineer/Security testing program rollout': Full STRIDE is heavy; product teams need a 'threat-model lite' 90-minute workshop pattern QAs can facilitate. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a threat model lite workshop artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-qa-engineer/Security testing program rollout' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working threat model lite workshop artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-qa-engineer/Security testing program rollout' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Threat Model Lite Workshop |

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
| `templates/threat-model-lite-workshop.json` | JSON schema for the Threat Model Lite Workshop output contract |
| `templates/threat-model-lite-workshop.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-threat-model-lite-workshop.py` | Enforce Threat Model Lite Workshop output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-qa-engineer/Security testing program rollout`
- pro/dev/role-qa-engineer
