---
slug: vendor-management-pm
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "5e4810af6af65258"
summary: "Vendor Management Pm: produces a versioned, owner-signed artefact that closes the gap 'role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)'."
tags: [vendor-management-pm, pm, pro]
---
# Vendor Management Pm

## Summary

**One-sentence:** Vendor Management Pm: produces a versioned, owner-signed artefact that closes the gap 'role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)'.

**One-paragraph:** Addresses the gap surfaced by 'role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)': procurement-management has a vendor_score.py but no ongoing vendor-management methodology: cadence of vendor 1:1s, escalation paths, SLA tracking, vendor-of-record decisions, change-management when vendor team rotates. Critical for P4 PMs managing sub-vendors. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a vendor management pm artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working vendor management pm artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Vendor Management Pm |

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
| `templates/vendor-management-pm.json` | JSON schema for the Vendor Management Pm output contract |
| `templates/vendor-management-pm.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-management-pm.py` | Enforce Vendor Management Pm output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)`
- pro/pm/role-project-manager
