---
slug: team-conventions-as-code
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "34629d3793205a48"
summary: "Team Conventions As Code: produces a versioned, owner-signed artefact that closes the gap 'role-software-developer/Make Production Readiness a PR-Level Concern'."
tags: [team-conventions-as-code, dev, pro]
---
# Team Conventions As Code

## Summary

**One-sentence:** Team Conventions As Code: produces a versioned, owner-signed artefact that closes the gap 'role-software-developer/Make Production Readiness a PR-Level Concern'.

**One-paragraph:** Addresses the gap surfaced by 'role-software-developer/Make Production Readiness a PR-Level Concern': Pro tier expects 'team patterns' (DDD/CQRS/microservices) without naming the meta-pattern: encode the team's conventions as enforceable rules (custom ESLint rules, ruff plugins, CODEOWNERS, danger.js, conventional-commits hook, AGENTS.md as machine-readable). Right now lint floor lives at geek/sdlc-ai/ and is out of tier reach. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a team conventions as code artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-software-developer/Make Production Readiness a PR-Level Concern' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working team conventions as code artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-software-developer/Make Production Readiness a PR-Level Concern' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Team Conventions As Code |

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
| `templates/team-conventions-as-code.json` | JSON schema for the Team Conventions As Code output contract |
| `templates/team-conventions-as-code.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-conventions-as-code.py` | Enforce Team Conventions As Code output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-software-developer/Make Production Readiness a PR-Level Concern`
- pro/dev/role-software-developer
