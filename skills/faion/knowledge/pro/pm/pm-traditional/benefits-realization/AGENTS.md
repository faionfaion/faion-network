---
slug: benefits-realization
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Tracks whether a project's promised business outcomes materialise after delivery via named owner, baseline, target, realisation curve at M1/M3/M6/Y1/Y2, and RAG status.
content_id: "042a8ae182270abf"
complexity: medium
produces: report
est_tokens: 4900
tags: [benefits, outcomes, measurement, roi, post-launch]
---
# Benefits Realization

## Summary

**One-sentence:** Tracks whether a project's promised business outcomes materialise after delivery via named owner, baseline, target, realisation curve at M1/M3/M6/Y1/Y2, and RAG status.

**One-paragraph:** Tracks whether a project's promised business outcomes materialise after delivery via named owner, baseline, target, realisation curve at M1/M3/M6/Y1/Y2, and RAG status. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-benefits-realization.py` enforces the output contract.

**Ефективно для:**

- Capital programs and transformation initiatives with quantitative benefits.
- Portfolios where post-launch measurement informs next funding round.
- Public-sector / regulated programs requiring benefit reporting (NHS, GDS, EU).
- ERP / CRM / cloud migrations with documented benefit claims.
- M&A integrations with synergy realisation in the deal thesis.

## Applies If (ALL must hold)

- Business case promised quantitative benefits (revenue, cost saving, NPS, cycle time).
- Each benefit has a named business-stakeholder owner (not the PM).
- Baseline measurement + target are documented before go-live.

## Skip If (ANY kills it)

- Pre-PMF startup — benefit hypothesis itself is unstable.
- Pure R&D / option-creating projects where value is learning.
- Indirect / strategic benefits only — track qualitatively.
- Tactical one-off projects under $50k — measurement cost > insight.
- No named benefit owner — tracking is theatre.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Benefits register | YAML | PM + benefit owner |
| Pre-launch baseline | metric snapshot | data team |
| Realisation curve | M1/M3/M6/Y1/Y2 expected % | benefit owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[project-closure]] | closure formalises hand-off to benefits tracking |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-register` | sonnet | Judgement: distinguish outputs from outcomes from benefits. |
| `compute-rag` | haiku | Mechanical actual / expected → RAG. |
| `analyse-deviation` | sonnet | Root-cause: adoption gap, training, external factor, overpromise. |

## Templates

| File | Purpose |
|------|---------|
| `templates/benefits-register.md` | Benefits-register template with owner, baseline, target, metric source per row |
| `templates/realization-report.md` | Periodic realisation report template with RAG status per benefit |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-benefits-realization.py` | Validate the report artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[project-closure]]
- [[earned-value-management]]
- [[lessons-learned]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

