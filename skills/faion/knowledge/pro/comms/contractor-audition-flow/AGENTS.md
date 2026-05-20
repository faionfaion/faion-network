---
slug: contractor-audition-flow
tier: pro
group: comms
domain: comms
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Contractor Audition Flow: codified comms practice that turns the recurring 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies' decision into a repeatable, auditable artefact.
content_id: "ceb7302b80c21219"
tags: [contractor-audition-flow, comms, pro]
---
# Contractor Audition Flow

## Summary

**One-sentence:** Contractor Audition Flow: codified comms practice that turns the recurring 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies' decision into a repeatable, auditable artefact.

**One-paragraph:** Contractor Audition Flow addresses the gap surfaced by 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies'. hr-recruiter/recruiting-process and structured-interview-design assume W-2 hiring funnels. Agencies need a contractor-specific audition flow: paid trial task spec, scoring rubric, ramp-onto-real-client criteria, kill-criteria. Conflating it with employee interviewing produces 6-week hiring loops the agency can't afford. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies' task (last 30 days of activity)
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
| `templates/contractor-audition-flow.json` | JSON schema for the Contractor Audition Flow output contract |
| `templates/contractor-audition-flow.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contractor-audition-flow.py` | Enforce Contractor Audition Flow output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/comms/hr-recruiter/`
- upstream playbook: `p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies`
- methodology family: `pro/comms/` (gap-p2 batch, F-059-063)
