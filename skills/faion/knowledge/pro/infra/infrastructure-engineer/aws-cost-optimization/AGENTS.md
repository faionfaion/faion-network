---
slug: aws-cost-optimization
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Quarterly FinOps report: Cost Explorer drill-down by tag + Savings Plan coverage + Graviton coverage + Spot adoption + Instance Scheduler + rightsizing recommendations, signed by a named owner against pinned thresholds."
content_id: "13510d643fa9f890"
complexity: deep
produces: report
est_tokens: 5000
tags: [aws, cost, finops, graviton, spot, reserved, infra]
---
# AWS Cost Optimization

## Summary

**One-sentence:** Quarterly FinOps report: Cost Explorer drill-down by tag + Savings Plan coverage + Graviton coverage + Spot adoption + Instance Scheduler + rightsizing recommendations, signed by a named owner against pinned thresholds.

**One-paragraph:** Quarterly FinOps report: Cost Explorer drill-down by tag + Savings Plan coverage + Graviton coverage + Spot adoption + Instance Scheduler + rightsizing recommendations, signed by a named owner against pinned thresholds. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- AWS monthly spend ≥ $5k OR org policy requires quarterly FinOps review.
- Cost Explorer + Cost & Usage Report (CUR) ingestion is enabled.
- Resources are tagged with Project / Environment / Owner / ManagedBy.

## Skip If (ANY kills it)

- Monthly spend < $1k — overhead does not pay back.
- Tags missing on > 30% of resources — fix tagging first; FinOps drill-down depends on it.
- AWS budget already < forecast for 4 consecutive quarters with no growth — optimisation has diminishing return.

**Ефективно для:**

- Команди з AWS spend ≥ $5k/міс які хочуть зменшити витрати на 20-40%.
- Quarterly FinOps cadence з named owner.
- Команди де Cost Explorer / CUR не аналізується регулярно.
- Аудит-ready середовища з вимогою FinOps звітності.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev` | Parent role context. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from header + section list. |
| `populate-evidence` | sonnet | Per-row evidence link + summary judgment. |
| `outcome-synthesis` | opus | Cross-cycle synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Report skeleton with frontmatter + sections + evidence anchors per row. |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-cost-optimization.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
