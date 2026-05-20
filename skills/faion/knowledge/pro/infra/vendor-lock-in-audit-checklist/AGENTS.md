---
slug: vendor-lock-in-audit-checklist
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "8e7692231d77e757"
summary: "Vendor Lock In Audit Checklist: produces a versioned, owner-signed artefact that closes the gap 'role-devops-engineer/Container vs serverless vs VM decision tree at architecture time'."
tags: [vendor-lock-in-audit-checklist, infra, pro]
---
# Vendor Lock In Audit Checklist

## Summary

**One-sentence:** Vendor Lock In Audit Checklist: produces a versioned, owner-signed artefact that closes the gap 'role-devops-engineer/Container vs serverless vs VM decision tree at architecture time'.

**One-paragraph:** Addresses the gap surfaced by 'role-devops-engineer/Container vs serverless vs VM decision tree at architecture time': Critical for P4 outsource (client handover, exit clauses) and P6 product (acquisition due-diligence). Currently no methodology systematizes lock-in scoring (proprietary services used, data export cost, IAM portability, IaC portability). Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a vendor lock in audit checklist artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-devops-engineer/Container vs serverless vs VM decision tree at architecture time' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working vendor lock in audit checklist artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-devops-engineer/Container vs serverless vs VM decision tree at architecture time' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infra` | parent domain group — provides operating context for Vendor Lock In Audit Checklist |

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
| `templates/vendor-lock-in-audit-checklist.json` | JSON schema for the Vendor Lock In Audit Checklist output contract |
| `templates/vendor-lock-in-audit-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-lock-in-audit-checklist.py` | Enforce Vendor Lock In Audit Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- upstream playbook: `role-devops-engineer/Container vs serverless vs VM decision tree at architecture time`
- pro/infra/role-devops-engineer
