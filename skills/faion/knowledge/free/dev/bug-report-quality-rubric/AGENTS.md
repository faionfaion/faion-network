---
slug: bug-report-quality-rubric
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Bug Report Quality Rubric: codified engineering practice that turns the recurring 'role-qa-engineer/Ship a QA program for an AI-powered product' decision into a repeatable, auditable artefact.
content_id: "17f240734aed34db"
tags: [bug-report-quality-rubric, dev, free]
---
# Bug Report Quality Rubric

## Summary

**One-sentence:** Bug Report Quality Rubric: codified engineering practice that turns the recurring 'role-qa-engineer/Ship a QA program for an AI-powered product' decision into a repeatable, auditable artefact.

**One-paragraph:** Bug Report Quality Rubric addresses the gap identified by the role-qa-engineer/Ship a QA program for an AI-powered product playbook: Cross-cutting QA basic with zero coverage. Should be free tier. A QA engineer files dozens of bugs a week; without a rubric (repro, expected, actual, environment, severity, priority, attachments, AI-context if AI feature) the team wastes cycles on triage. Especially important when bugs are about LLM outputs and need prompt/version/seed capture. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-qa-engineer/Ship a QA program for an AI-powered product OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == free or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-qa-engineer/Ship a QA program for an AI-powered product task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-detector-first | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/bug-report-quality-rubric.json` | JSON schema for the Bug Report Quality Rubric output contract |
| `templates/bug-report-quality-rubric.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bug-report-quality-rubric.py` | Enforce Bug Report Quality Rubric output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `free/dev/`
- upstream playbook: `role-qa-engineer/Ship a QA program for an AI-powered product`
