---
slug: vuln-triage-sla-template
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "45724abb5bae26d6"
summary: "Vuln Triage Sla Template: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Security testing program rollout'."
tags: [vuln-triage-sla-template, dev, pro]
---
# Vuln Triage Sla Template

## Summary

**One-sentence:** Vuln Triage Sla Template: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Security testing program rollout'.

**One-paragraph:** Addresses the gap surfaced by 'role-qa-engineer/Security testing program rollout': Severity matrix + SLA per tier + waiver expiry + audit log; everyone re-derives this from scratch. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a vuln triage sla template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-qa-engineer/Security testing program rollout' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working vuln triage sla template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-qa-engineer/Security testing program rollout' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Vuln Triage Sla Template |

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
| `templates/vuln-triage-sla-template.json` | JSON schema for the Vuln Triage Sla Template output contract |
| `templates/vuln-triage-sla-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vuln-triage-sla-template.py` | Enforce Vuln Triage Sla Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-qa-engineer/Security testing program rollout`
- pro/dev/role-qa-engineer
