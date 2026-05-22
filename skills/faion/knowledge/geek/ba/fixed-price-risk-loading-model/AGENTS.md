---
slug: fixed-price-risk-loading-model
tier: geek
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a fixed-price risk loading model: risk-register-to-buffer translation, contingency tiers, hidden-cost classes, and a defensible bid number with explicit risk-pricing reasoning per category."
content_id: "2cbe4dbd626a03a3"
complexity: deep
produces: spec
est_tokens: 4500
tags: [ba, fixed-price, pricing, risk, p4-outsource, geek]
---

# Fixed-Price Risk Loading Model

## Summary

**One-sentence:** Produces a fixed-price risk loading model: risk-register-to-buffer translation, contingency tiers, hidden-cost classes, and a defensible bid number with explicit risk-pricing reasoning per category.

**Ефективно для:** BAs / sales engineers pricing fixed-price engagements; commercial leads defending bid margins to procurement; partners pricing P4 outsource engagements.

**One-paragraph:** This methodology pins the recurring decision around "fixed-price-risk-loading-model" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Engagement is fixed-price (not T&M).
- Risk register exists OR can be built.
- Bid number is defensible against procurement.
- Owner exists for the model.

## Skip If (ANY kills it)

- Engagement is T&M — loading model does not apply.
- Bid is volume-only with no risk premium negotiated.
- Standardised price-list product with no scope-risk variance.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Risk register (likelihood × impact) | CSV | BA / delivery |
| Historical loading ratios | spreadsheet | finance |
| Engagement scope | Markdown spec | BA |
| Bid owner | handle / email | commercial |
| Procurement constraints | Markdown | commercial |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[fixed-price-vs-tm-cr-pricing-playbook]]` | change-request flow runs after bid signed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_loading_table` | haiku | Mechanical template fill. |
| `synthesize_buffer` | sonnet | Per-class buffer judgment. |
| `escalate_margin` | opus | Cross-class margin decision. |

## Templates

| File | Purpose |
|------|---------|
| `templates/fixed-price-risk-loading-model.json` | JSON Schema for the Fixed-Price Risk Loading Model output contract |
| `templates/fixed-price-risk-loading-model.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a fixed-price-risk-loading-model record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fixed-price-risk-loading-model.py` | Enforce the Fixed-Price Risk Loading Model output contract | After subagent returns, before downstream consumer reads |

## Related

- [[fixed-price-vs-tm-cr-pricing-playbook]] — adjacent change-request playbook.
- [[compliance-traceability-pack]] — when risk is regulatory.
- [[ai-enabled-business-analysis]] — parent BA methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
