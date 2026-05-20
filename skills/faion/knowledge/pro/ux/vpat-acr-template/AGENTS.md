---
slug: vpat-acr-template
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "55e7c0b45dfbe7f9"
summary: "Vpat Acr Template: produces a versioned, owner-signed artefact that closes the gap 'role-ux-ui-designer/Accessibility audit and remediation program (6 weeks)'."
tags: [vpat-acr-template, ux, pro]
---
# Vpat Acr Template

## Summary

**One-sentence:** Vpat Acr Template: produces a versioned, owner-signed artefact that closes the gap 'role-ux-ui-designer/Accessibility audit and remediation program (6 weeks)'.

**One-paragraph:** Addresses the gap surfaced by 'role-ux-ui-designer/Accessibility audit and remediation program (6 weeks)': Regulatory deliverables (VPAT/ACR) are evidence packaging for legal/ADA — no faion methodology covers the artifact format. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a vpat acr template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-ux-ui-designer/Accessibility audit and remediation program (6 weeks)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working vpat acr template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-ux-ui-designer/Accessibility audit and remediation program (6 weeks)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/ux` | parent domain group — provides operating context for Vpat Acr Template |

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
| `templates/vpat-acr-template.json` | JSON schema for the Vpat Acr Template output contract |
| `templates/vpat-acr-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vpat-acr-template.py` | Enforce Vpat Acr Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ux/`
- upstream playbook: `role-ux-ui-designer/Accessibility audit and remediation program (6 weeks)`
- pro/ux/role-ux-ui-designer
