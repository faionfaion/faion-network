---
slug: vendor-risk-assessment-template
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "268b9b9fd721d391"
summary: "Vendor Risk Assessment Template: produces a versioned, owner-signed artefact that closes the gap 'p6-product-dev-team/SOC2 / GDPR audit prep (annual)'."
tags: [vendor-risk-assessment-template, pm, geek]
---
# Vendor Risk Assessment Template

## Summary

**One-sentence:** Vendor Risk Assessment Template: produces a versioned, owner-signed artefact that closes the gap 'p6-product-dev-team/SOC2 / GDPR audit prep (annual)'.

**One-paragraph:** Addresses the gap surfaced by 'p6-product-dev-team/SOC2 / GDPR audit prep (annual)': Procurement-management is generic; SaaS teams need a SOC2-aligned vendor-risk template covering subprocessors, DPA, data-residency questions. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a vendor risk assessment template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p6-product-dev-team/SOC2 / GDPR audit prep (annual)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working vendor risk assessment template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p6-product-dev-team/SOC2 / GDPR audit prep (annual)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/pm` | parent domain group — provides operating context for Vendor Risk Assessment Template |

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
| `templates/vendor-risk-assessment-template.json` | JSON schema for the Vendor Risk Assessment Template output contract |
| `templates/vendor-risk-assessment-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-risk-assessment-template.py` | Enforce Vendor Risk Assessment Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- upstream playbook: `p6-product-dev-team/SOC2 / GDPR audit prep (annual)`
- geek/pm/p6-product-dev-team
