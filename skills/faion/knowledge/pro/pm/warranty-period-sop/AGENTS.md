---
slug: warranty-period-sop
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "51268dcb2013dd80"
summary: "Warranty Period Sop: produces a versioned, owner-signed artefact that closes the gap 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)'."
tags: [warranty-period-sop, pm, pro]
---
# Warranty Period Sop

## Summary

**One-sentence:** Warranty Period Sop: produces a versioned, owner-signed artefact that closes the gap 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)'.

**One-paragraph:** Addresses the gap surfaced by 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)': Freelancers either swallow free post-launch fixes or fight over them. Need a defined warranty-window SOP: what's in, what's out, how to convert it into a retainer. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a warranty period sop artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working warranty period sop artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Warranty Period Sop |

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
| `templates/warranty-period-sop.json` | JSON schema for the Warranty Period Sop output contract |
| `templates/warranty-period-sop.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-warranty-period-sop.py` | Enforce Warranty Period Sop output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)`
- pro/pm/p3-technical-freelancer
