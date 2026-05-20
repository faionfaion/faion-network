---
slug: wtp-survey-questionnaire
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "37f5a10a7c38c4ec"
summary: "Wtp Survey Questionnaire: produces a versioned, owner-signed artefact that closes the gap 'role-product-manager/Pricing experiment, hypothesis to result'."
tags: [wtp-survey-questionnaire, research, pro]
---
# Wtp Survey Questionnaire

## Summary

**One-sentence:** Wtp Survey Questionnaire: produces a versioned, owner-signed artefact that closes the gap 'role-product-manager/Pricing experiment, hypothesis to result'.

**One-paragraph:** Addresses the gap surfaced by 'role-product-manager/Pricing experiment, hypothesis to result': survey-design exists generically; PMs need a ready-to-run Van Westendorp / Gabor-Granger questionnaire + scoring sheet. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a wtp survey questionnaire artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-product-manager/Pricing experiment, hypothesis to result' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working wtp survey questionnaire artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-product-manager/Pricing experiment, hypothesis to result' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/research` | parent domain group — provides operating context for Wtp Survey Questionnaire |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/wtp-survey-questionnaire.json` | JSON schema for the Wtp Survey Questionnaire output contract |
| `templates/wtp-survey-questionnaire.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wtp-survey-questionnaire.py` | Enforce Wtp Survey Questionnaire output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/research/`
- upstream playbook: `role-product-manager/Pricing experiment, hypothesis to result`
- pro/research/role-product-manager
