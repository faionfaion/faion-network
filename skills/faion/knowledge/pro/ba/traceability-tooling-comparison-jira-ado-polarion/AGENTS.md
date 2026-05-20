---
slug: traceability-tooling-comparison-jira-ado-polarion
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "020db263f8a8e972"
summary: "Traceability Tooling Comparison Jira Ado Polarion: produces a versioned, owner-signed artefact that closes the gap 'role-business-analyst/Requirements traceability across the full project lifecycle'."
tags: [traceability-tooling-comparison-jira-ado-polarion, ba, pro]
---
# Traceability Tooling Comparison Jira Ado Polarion

## Summary

**One-sentence:** Traceability Tooling Comparison Jira Ado Polarion: produces a versioned, owner-signed artefact that closes the gap 'role-business-analyst/Requirements traceability across the full project lifecycle'.

**One-paragraph:** Addresses the gap surfaced by 'role-business-analyst/Requirements traceability across the full project lifecycle': BAs constantly inherit Jira / Azure DevOps / Polarion / Confluence trace setups they didn't design. Need a comparison + setup guide: link types, custom fields, trace gates, gotchas per tool. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a traceability tooling comparison jira ado polarion artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-business-analyst/Requirements traceability across the full project lifecycle' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working traceability tooling comparison jira ado polarion artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-business-analyst/Requirements traceability across the full project lifecycle' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/ba` | parent domain group — provides operating context for Traceability Tooling Comparison Jira Ado Polarion |

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
| `templates/traceability-tooling-comparison-jira-ado-polarion.json` | JSON schema for the Traceability Tooling Comparison Jira Ado Polarion output contract |
| `templates/traceability-tooling-comparison-jira-ado-polarion.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-traceability-tooling-comparison-jira-ado-polarion.py` | Enforce Traceability Tooling Comparison Jira Ado Polarion output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/`
- upstream playbook: `role-business-analyst/Requirements traceability across the full project lifecycle`
- pro/ba/role-business-analyst
