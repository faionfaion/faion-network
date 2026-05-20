---
slug: tm-to-fp-conversion-playbook
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "e2d86d55f1cadac7"
summary: "Tm To Fp Conversion Playbook: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)'."
tags: [tm-to-fp-conversion-playbook, pm, pro]
---
# Tm To Fp Conversion Playbook

## Summary

**One-sentence:** Tm To Fp Conversion Playbook: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)'.

**One-paragraph:** Addresses the gap surfaced by 'p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)': A common but undocumented commercial transition. faion has scope-management and change-control but no end-to-end T&M-to-FP conversion playbook with the data audit + estimate + reserves recipe. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a tm to fp conversion playbook artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working tm to fp conversion playbook artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Tm To Fp Conversion Playbook |

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
| `templates/tm-to-fp-conversion-playbook.json` | JSON schema for the Tm To Fp Conversion Playbook output contract |
| `templates/tm-to-fp-conversion-playbook.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tm-to-fp-conversion-playbook.py` | Enforce Tm To Fp Conversion Playbook output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)`
- pro/pm/p4-outsource-specialist
