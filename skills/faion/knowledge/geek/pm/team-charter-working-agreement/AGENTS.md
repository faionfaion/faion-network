---
slug: team-charter-working-agreement
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "194a41a24e76350a"
summary: "Team Charter Working Agreement: produces a versioned, owner-signed artefact that closes the gap 'p6-product-dev-team/Adopt faion org-wide and override with company patterns'."
tags: [team-charter-working-agreement, pm, geek]
---
# Team Charter Working Agreement

## Summary

**One-sentence:** Team Charter Working Agreement: produces a versioned, owner-signed artefact that closes the gap 'p6-product-dev-team/Adopt faion org-wide and override with company patterns'.

**One-paragraph:** Addresses the gap surfaced by 'p6-product-dev-team/Adopt faion org-wide and override with company patterns': `team-development` covers Tuckman stages but there is no concrete artifact: a 1-page team charter (mission, decision rights, working hours, AI-tool usage policy, code-review SLA, on-call rotation rules). This is the single most-cited missing doc on Y-Combinator/HN threads about scaling a product team past 5 people Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a team charter working agreement artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p6-product-dev-team/Adopt faion org-wide and override with company patterns' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working team charter working agreement artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p6-product-dev-team/Adopt faion org-wide and override with company patterns' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/pm` | parent domain group — provides operating context for Team Charter Working Agreement |

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
| `templates/team-charter-working-agreement.json` | JSON schema for the Team Charter Working Agreement output contract |
| `templates/team-charter-working-agreement.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-charter-working-agreement.py` | Enforce Team Charter Working Agreement output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- upstream playbook: `p6-product-dev-team/Adopt faion org-wide and override with company patterns`
- geek/pm/p6-product-dev-team
