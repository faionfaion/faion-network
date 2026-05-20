---
slug: client-conventions-intake
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Client Conventions Intake: codified dev practice that turns the recurring 'role-software-developer/Feature from spec to production (3 weeks, P4 client-rules edition)' decision into a repeatable, auditable artefact.
content_id: "77ed0ff220efa280"
tags: [client-conventions-intake, dev, solo]
---
# Client Conventions Intake

## Summary

**One-sentence:** Client Conventions Intake: codified dev practice that turns the recurring 'role-software-developer/Feature from spec to production (3 weeks, P4 client-rules edition)' decision into a repeatable, auditable artefact.

**One-paragraph:** Client Conventions Intake addresses the gap surfaced by 'role-software-developer/Feature from spec to production (3 weeks, P4 client-rules edition)'. Outsource devs (P4) lose hours guessing each client's style, branch model, PR template, and review etiquette. A repeatable intake produces a per-engagement CONVENTIONS.md and makes AI-assisted coding stay in-style. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-software-developer/Feature from spec to production (3 weeks, P4 client-rules edition)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-software-developer/Feature from spec to production (3 weeks, P4 client-rules edition)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent role skill — provides the operating context for this methodology |

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
| `templates/client-conventions-intake.json` | JSON schema for the Client Conventions Intake output contract |
| `templates/client-conventions-intake.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-conventions-intake.py` | Enforce Client Conventions Intake output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/software-developer/`
- upstream playbook: `role-software-developer/Feature from spec to production (3 weeks, P4 client-rules edition)`
- methodology family: `solo/dev/` (gap-p2 batch, F-059-063)
