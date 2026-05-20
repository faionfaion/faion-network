---
slug: team-mode-cli-flag
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "0406eaa275de2269"
summary: "Team Mode Cli Flag: produces a versioned, owner-signed artefact that closes the gap 'p6-product-dev-team/Adopt faion org-wide and override with company patterns'."
tags: [team-mode-cli-flag, sdlc-ai, geek]
---
# Team Mode Cli Flag

## Summary

**One-sentence:** Team Mode Cli Flag: produces a versioned, owner-signed artefact that closes the gap 'p6-product-dev-team/Adopt faion org-wide and override with company patterns'.

**One-paragraph:** Addresses the gap surfaced by 'p6-product-dev-team/Adopt faion org-wide and override with company patterns': Meta-gap: faion CLI assumes a single user with personal preferences. Team usage needs `faion --team-config /etc/faion/team.yaml` or env `FAION_TEAM_OVERLAY=...` so the override resolution is consistent across 10 devs. Surfaces in CLI behavior, not just content Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a team mode cli flag artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p6-product-dev-team/Adopt faion org-wide and override with company patterns' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working team mode cli flag artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p6-product-dev-team/Adopt faion org-wide and override with company patterns' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/sdlc-ai` | parent domain group — provides operating context for Team Mode Cli Flag |

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
| `templates/team-mode-cli-flag.json` | JSON schema for the Team Mode Cli Flag output contract |
| `templates/team-mode-cli-flag.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-mode-cli-flag.py` | Enforce Team Mode Cli Flag output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/sdlc-ai/`
- upstream playbook: `p6-product-dev-team/Adopt faion org-wide and override with company patterns`
- geek/sdlc-ai/p6-product-dev-team
