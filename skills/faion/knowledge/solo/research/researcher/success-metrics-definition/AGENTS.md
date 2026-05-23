---
slug: success-metrics-definition
tier: solo
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a success-metrics spec (1 north-star + \u22645 AARRR KPIs + targets + baselines + vanity-flagged exclusions) so the team measures what drives business outcomes, not what's easy to count."
content_id: "113bd2fd9ab39969"
complexity: medium
produces: spec
est_tokens: 4100
tags: [metrics, kpis, north-star, aarrr, measurement]
---

# Success Metrics Definition

## Summary

**One-sentence:** Produces a success-metrics spec (1 north-star + ≤5 AARRR KPIs + targets + baselines + vanity-flagged exclusions) so the team measures what drives business outcomes, not what's easy to count.

**Ефективно для:** Solo PMs whose dashboard fills with vanity metrics (pageviews, signups) that don't move the revenue needle.

**One-paragraph:** Teams measure the wrong things or too many things. This methodology pins one north-star metric to a business goal, partitions ≤5 supporting KPIs across the AARRR funnel (acquisition / activation / retention / referral / revenue), sets actionable targets with baselines, and explicitly flags vanity metrics for exclusion. Output is consumed by mvp-instrumentation-checklist and outcome-based-roadmaps.

## Applies If (ALL must hold)

- New product or feature launch needs measurement baseline.
- Existing dashboards are crowded with metrics nobody acts on.
- Team disagrees on which metric should drive prioritisation.
- Quarterly OKR cycle needs measurable key results.

## Skip If (ANY kills it)

- Pre-product: no traffic to measure.
- Compliance-only metrics (uptime SLA, regulatory) — outside AARRR scope.
- Team smaller than one — no need for shared dashboards.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| business goal statement | string | founder |
| current funnel data | csv/dashboard export | analytics |
| instrumentation status | checklist | engineer |
| prior quarter targets | spec | previous run |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/mvp-instrumentation-checklist` | Downstream — consumes metric definitions to instrument. |
| `solo/product/product-manager/okr-setting` | Downstream — KPIs feed into OKR key results. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/success-metrics-definition.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/success-metrics-definition.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-success-metrics-definition.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[mvp-instrumentation-checklist]] — related methodology.
- [[okr-setting]] — related methodology.
- [[outcome-based-roadmaps]] — related methodology.
- [[use-case-mapping]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
