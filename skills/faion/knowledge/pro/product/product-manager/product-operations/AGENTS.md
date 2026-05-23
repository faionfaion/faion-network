---
slug: product-operations
tier: pro
group: product
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: PM-side RACI contract with an existing Product Ops function: consumes canonical artefacts, hands off scaled-org ceremonies, never duplicates instrumentation Product Ops owns.
content_id: "489513fbdd9ac9ef"
complexity: medium
produces: config
est_tokens: 4900
tags: [product-operations, product-manager, raci, governance, hand-off]
---
# Product Operations (PM-side)

## Summary

**One-sentence:** PM-side RACI contract with an existing Product Ops function: consumes canonical artefacts, hands off scaled-org ceremonies, never duplicates instrumentation Product Ops owns.

**One-paragraph:** Written RACI per artefact (tracking-plan, OKR cascade, voice-of-customer, launch readiness); PM consumes canonical stores rather than rebuilding them; scaled PM-invented ceremonies hand off to Product Ops; explicit escalation path for disputes. Output: pm-ops-contract markdown + RACI YAML.

**Ефективно для:**

- PM onboarding в org з existing Product Ops функцією.
- Кілька PM-ів просять inconsistent artefacts — route через Product Ops canonical store.
- Pre-board prep — consume Product Ops outputs замість re-derive.
- PM пропонує нову ceremony — hand off до Product Ops для scaling.

## Applies If (ALL must hold)

- PM onboarding into an org with an existing Product Ops function — needs explicit RACI.
- Multiple PMs requesting inconsistent artifacts — route through Product Ops canonical store.
- Preparing a board/exec/portfolio review — consume Product Ops outputs.
- PM proposes a new ceremony — hand off to Product Ops to ship org-wide.
- PM receives a Product Ops insight and needs to convert it into a discovery or kill decision.

## Skip If (ANY kills it)

- No Product Ops function exists — use solo product-operations methodology.
- <=2 PM team where overhead exceeds benefit.
- Consultancy / services with no recurring product surface.
- Existing RACI <=90 days old without org change.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product Ops charter | doc | Head of Product Ops |
| Artefact inventory | list of canonical artefacts | Product Ops |
| PM cohort | list of PMs | org chart |
| Escalation path baseline | doc | Head of Product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-management]] | Provides the stakeholder register that informs RACI roles. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: explicit RACI, canonical-store consumption, scaled-ceremony hand-off, no-duplicate instrumentation, named escalation | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for pm-ops-contract | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: parallel store, scaled PM-ceremony, ad-hoc instrumentation, escalation ambiguity | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: charter -> RACI -> canonical map -> ceremony handoff -> escalation | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on Product Ops presence + PM count | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `raci-author` | sonnet | Draft the RACI from PM + ProductOps charters. |
| `contract-audit` | haiku | Mechanical check of canonical-store consumption. |
| `escalation-memo` | sonnet | Write the escalation path with named owners. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pm-ops-contract.md` | PM-ops contract skeleton with RACI + canonical map + escalation. |
| `templates/pm-ops-contract-check.sh` | Check that PM artefacts use canonical-store outputs (no parallel). |
| `templates/raci.yaml` | RACI YAML skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-operations.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[stakeholder-management]]
- [[product-analytics]]
- [[release-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
