---
slug: model-eval-control-bands
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Model Eval Control Bands: codified ai practice that turns the recurring 'role-ml-engineer/Daily eval-suite run + drift triage' decision into a repeatable, auditable artefact.
content_id: "ec3dec70176b13aa"
tags: [model-eval-control-bands, ai, geek]
---
# Model Eval Control Bands

## Summary

**One-sentence:** Model Eval Control Bands: codified ai practice that turns the recurring 'role-ml-engineer/Daily eval-suite run + drift triage' decision into a repeatable, auditable artefact.

**One-paragraph:** Model Eval Control Bands addresses the gap identified by the role-ml-engineer/Daily eval-suite run + drift triage playbook: Eval methodologies define metrics but not how to set + maintain control bands so drift is detectable without false alarms. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-ml-engineer/Daily eval-suite run + drift triage OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-ml-engineer/Daily eval-suite run + drift triage task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer` | parent role skill — provides the operating context for this methodology |

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
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/model-eval-control-bands.json` | JSON schema for the Model Eval Control Bands output contract |
| `templates/model-eval-control-bands.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-model-eval-control-bands.py` | Enforce Model Eval Control Bands output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/ml-engineer/`
- upstream playbook: `role-ml-engineer/Daily eval-suite run + drift triage`
