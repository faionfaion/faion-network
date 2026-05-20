---
slug: audit-grade-code-review-checklist
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Audit Grade Code Review Checklist: codified engineering practice that turns the recurring 'p4-outsource-specialist/Audit-grade code review for compliance client' decision into a repeatable, auditable artefact.
content_id: "c3de641ae3155590"
tags: [audit-grade-code-review-checklist, dev, pro]
---
# Audit Grade Code Review Checklist

## Summary

**One-sentence:** Audit Grade Code Review Checklist: codified engineering practice that turns the recurring 'p4-outsource-specialist/Audit-grade code review for compliance client' decision into a repeatable, auditable artefact.

**One-paragraph:** Audit Grade Code Review Checklist addresses the gap identified by the p4-outsource-specialist/Audit-grade code review for compliance client playbook: Existing code-review methodologies are at solo/team scale. None addresses the 'this PR may be evidence in a regulator audit' lens specific to banking/health/payments outsourcing. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p4-outsource-specialist/Audit-grade code review for compliance client OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p4-outsource-specialist/Audit-grade code review for compliance client task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned | ~900 |
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
| `templates/audit-grade-code-review-checklist.json` | JSON schema for the Audit Grade Code Review Checklist output contract |
| `templates/audit-grade-code-review-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-audit-grade-code-review-checklist.py` | Enforce Audit Grade Code Review Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `p4-outsource-specialist/Audit-grade code review for compliance client`
