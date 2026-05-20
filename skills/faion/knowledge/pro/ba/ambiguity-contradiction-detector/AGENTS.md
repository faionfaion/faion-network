---
slug: ambiguity-contradiction-detector
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ambiguity Contradiction Detector: codified business-analysis practice that turns the recurring 'role-business-analyst/AI-assisted requirements discovery on a new outsource engagement' decision into a repeatable, auditable artefact.
content_id: "c6b1edce45b18fcc"
tags: [ambiguity-contradiction-detector, ba, pro]
---
# Ambiguity Contradiction Detector

## Summary

**One-sentence:** Ambiguity Contradiction Detector: codified business-analysis practice that turns the recurring 'role-business-analyst/AI-assisted requirements discovery on a new outsource engagement' decision into a repeatable, auditable artefact.

**One-paragraph:** Ambiguity Contradiction Detector addresses the gap identified by the role-business-analyst/AI-assisted requirements discovery on a new outsource engagement playbook: Brief calls this out as a core pain. Nothing in the corpus addresses scanning a PRD/spec for ambiguous modifiers (`fast`, `easy`, `secure`), contradictions across sections, missing actors, undefined units. Requirements-validation talks about validation criteria but not detection patterns. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

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
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-acceptance-criteria | ~900 |
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
| `templates/ambiguity-contradiction-detector.json` | JSON schema for the Ambiguity Contradiction Detector output contract |
| `templates/ambiguity-contradiction-detector.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ambiguity-contradiction-detector.py` | Enforce Ambiguity Contradiction Detector output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/`
- upstream playbook: `role-business-analyst/AI-assisted requirements discovery on a new outsource engagement`
