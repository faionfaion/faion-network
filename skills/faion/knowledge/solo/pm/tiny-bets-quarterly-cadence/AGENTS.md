---
slug: tiny-bets-quarterly-cadence
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "06b6aba45a349993"
summary: "Tiny Bets Quarterly Cadence: produces a versioned, owner-signed artefact that closes the gap 'p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year'."
tags: [tiny-bets-quarterly-cadence, pm, solo]
---
# Tiny Bets Quarterly Cadence

## Summary

**One-sentence:** Tiny Bets Quarterly Cadence: produces a versioned, owner-signed artefact that closes the gap 'p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year'.

**One-paragraph:** Addresses the gap surfaced by 'p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year': The 'tiny bets' / Tiny Seed cadence (quarterly bet selection + commit + cull) is the operating rhythm of the persona. faion lacks an explicit cadence methodology (vs. corporate sprint/quarter cadences). Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a tiny bets quarterly cadence artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working tiny bets quarterly cadence artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/pm` | parent domain group — provides operating context for Tiny Bets Quarterly Cadence |

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
| `templates/tiny-bets-quarterly-cadence.json` | JSON schema for the Tiny Bets Quarterly Cadence output contract |
| `templates/tiny-bets-quarterly-cadence.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tiny-bets-quarterly-cadence.py` | Enforce Tiny Bets Quarterly Cadence output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/pm/`
- upstream playbook: `p2-indie-hacker/Multi-product portfolio rotation: ship N small bets per year`
- solo/pm/p2-indie-hacker
