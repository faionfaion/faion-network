---
slug: contractor-onboarding-runbook
tier: pro
group: comms
domain: comms
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Contractor Onboarding Runbook: codified comms practice that turns the recurring 'p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks)' decision into a repeatable, auditable artefact.
content_id: "6093c1b77dd5e73c"
tags: [contractor-onboarding-runbook, comms, pro]
---
# Contractor Onboarding Runbook

## Summary

**One-sentence:** Contractor Onboarding Runbook: codified comms practice that turns the recurring 'p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Contractor Onboarding Runbook addresses the gap surfaced by 'p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks)'. onboarding-30-day exists for FT employees; agencies need a contractor-specific runbook covering access, IP, paired-shadow, and day-30 review. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter` | parent role skill — provides the operating context for this methodology |

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
| `templates/contractor-onboarding-runbook.json` | JSON schema for the Contractor Onboarding Runbook output contract |
| `templates/contractor-onboarding-runbook.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contractor-onboarding-runbook.py` | Enforce Contractor Onboarding Runbook output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/comms/hr-recruiter/`
- upstream playbook: `p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks)`
- methodology family: `pro/comms/` (gap-p2 batch, F-059-063)
