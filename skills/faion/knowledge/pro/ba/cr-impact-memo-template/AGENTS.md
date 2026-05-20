---
slug: cr-impact-memo-template
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Cr Impact Memo Template: codified ba practice that turns the recurring 'role-business-analyst/Change-request impact assessment' decision into a repeatable, auditable artefact.
content_id: "1df4e10e5b9fce27"
tags: [cr-impact-memo-template, ba, pro]
---
# Cr Impact Memo Template

## Summary

**One-sentence:** Cr Impact Memo Template: codified ba practice that turns the recurring 'role-business-analyst/Change-request impact assessment' decision into a repeatable, auditable artefact.

**One-paragraph:** Cr Impact Memo Template addresses the gap surfaced by 'role-business-analyst/Change-request impact assessment'. Outsource BAs (P4) handle CRs constantly; a one-page memo template tied to gap analysis closes a frequent friction. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-business-analyst/Change-request impact assessment' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-business-analyst/Change-request impact assessment' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

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
| `templates/cr-impact-memo-template.json` | JSON schema for the Cr Impact Memo Template output contract |
| `templates/cr-impact-memo-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cr-impact-memo-template.py` | Enforce Cr Impact Memo Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/business-analyst/`
- upstream playbook: `role-business-analyst/Change-request impact assessment`
- methodology family: `pro/ba/` (gap-p2 batch, F-059-063)
