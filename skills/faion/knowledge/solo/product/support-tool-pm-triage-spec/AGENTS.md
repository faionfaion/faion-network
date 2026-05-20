---
slug: support-tool-pm-triage-spec
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "94108ffdce9cf2c5"
summary: "Support Tool Pm Triage Spec: produces a versioned, owner-signed artefact that closes the gap 'role-product-manager/Customer feedback triage from Intercom/Pylon'."
tags: [support-tool-pm-triage-spec, product, solo]
---
# Support Tool Pm Triage Spec

## Summary

**One-sentence:** Support Tool Pm Triage Spec: produces a versioned, owner-signed artefact that closes the gap 'role-product-manager/Customer feedback triage from Intercom/Pylon'.

**One-paragraph:** Addresses the gap surfaced by 'role-product-manager/Customer feedback triage from Intercom/Pylon': PMs spend hours weekly inside Intercom/Pylon/Zendesk but there is no tier-appropriate spec for tag schemes, escalation rules, or weekly digests. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a support tool pm triage spec artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-product-manager/Customer feedback triage from Intercom/Pylon' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working support tool pm triage spec artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-product-manager/Customer feedback triage from Intercom/Pylon' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product` | parent domain group — provides operating context for Support Tool Pm Triage Spec |

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
| `templates/support-tool-pm-triage-spec.json` | JSON schema for the Support Tool Pm Triage Spec output contract |
| `templates/support-tool-pm-triage-spec.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-support-tool-pm-triage-spec.py` | Enforce Support Tool Pm Triage Spec output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/product/`
- upstream playbook: `role-product-manager/Customer feedback triage from Intercom/Pylon`
- solo/product/role-product-manager
