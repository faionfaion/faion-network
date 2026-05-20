---
slug: contract-testing-consumer-driven
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Contract Testing Consumer Driven: codified dev practice that turns the recurring 'role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops' decision into a repeatable, auditable artefact.
content_id: "238c3e9d37ff437d"
tags: [contract-testing-consumer-driven, dev, pro]
---
# Contract Testing Consumer Driven

## Summary

**One-sentence:** Contract Testing Consumer Driven: codified dev practice that turns the recurring 'role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops' decision into a repeatable, auditable artefact.

**One-paragraph:** Contract Testing Consumer Driven addresses the gap surfaced by 'role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops'. Faion has api-contract-first (design-time spec) but nothing for run-time consumer-driven contracts (Pact, Spring Cloud Contract). For any microservice or multi-team product (P4 outsource + P6 product team), CDC is the modern alternative to fragile cross-service E2E. Closest existing geek/sdlc-ai/test-consumer-contract-from-spec is for AI agents writing contracts, not a QA engineer adopting Pact. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/contract-testing-consumer-driven.json` | JSON schema for the Contract Testing Consumer Driven output contract |
| `templates/contract-testing-consumer-driven.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contract-testing-consumer-driven.py` | Enforce Contract Testing Consumer Driven output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/software-developer/`
- upstream playbook: `role-qa-engineer/Modernize a 2018-era QA suite into AI-augmented test ops`
- methodology family: `pro/dev/` (gap-p2 batch, F-059-063)
