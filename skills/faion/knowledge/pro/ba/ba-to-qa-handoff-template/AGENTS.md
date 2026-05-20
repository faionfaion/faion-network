---
slug: ba-to-qa-handoff-template
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ba to Qa Handoff Template: codified business-analysis practice that turns the recurring 'role-business-analyst/AI-assisted requirements discovery on a new outsource engagement' decision into a repeatable, auditable artefact.
content_id: "a2fff6d098434d44"
tags: [ba-to-qa-handoff-template, ba, pro]
---
# Ba to Qa Handoff Template

## Summary

**One-sentence:** Ba to Qa Handoff Template: codified business-analysis practice that turns the recurring 'role-business-analyst/AI-assisted requirements discovery on a new outsource engagement' decision into a repeatable, auditable artefact.

**One-paragraph:** Ba to Qa Handoff Template addresses the gap identified by the role-business-analyst/AI-assisted requirements discovery on a new outsource engagement playbook: BA→Dev handoff is THE moment outsource engagements break. Corpus has no template covering: business context, in-scope/out-of-scope, dependencies, NFR table, AC pack, traceability anchors, open questions, decision log links, glossary link. Without a canonical handoff template, devs reinvent every sprint and BAs absorb the blame. / Mirror of the dev handoff. QA needs: AC pack, test-data hints, edge cases, NFR thresholds, regulatory anchors, expected error states, rollback criteria. Today the corpus assumes QA derives this themselves from the AC doc — they don't, especially on regulated work. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-business-analyst/AI-assisted requirements discovery on a new outsource engagement OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-business-analyst/AI-assisted requirements discovery on a new outsource engagement task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

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
| `templates/ba-to-qa-handoff-template.json` | JSON schema for the Ba to Qa Handoff Template output contract |
| `templates/ba-to-qa-handoff-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-to-qa-handoff-template.py` | Enforce Ba to Qa Handoff Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/`
- upstream playbook: `role-business-analyst/AI-assisted requirements discovery on a new outsource engagement`
