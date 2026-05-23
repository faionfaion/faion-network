---
slug: cost-model-spreadsheet-template
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a defensible multi-cloud cost-model spreadsheet covering compute / storage / network / operations / buffer with sourced unit rates and 0.5x/1x/2x scenarios.
content_id: "6a229e0ef11f16f9"
complexity: deep
produces: spec
est_tokens: 4500
tags: [cost-model, finops, architecture, capacity-planning]
---
# Cost-Model Spreadsheet Template

## Summary

**One-sentence:** Produces a defensible multi-cloud cost-model spreadsheet covering compute / storage / network / operations / buffer with sourced unit rates and 0.5x/1x/2x scenarios.

**One-paragraph:** Software architects re-invent the same cost spreadsheet on every Greenfield or scale-event project, and the same line items get missed every time (NAT gateway data-processing, S3 egress, observability log storage, KMS request fees). This methodology pins a template with five top-level categories (Compute / Storage / Network / Operations / Buffer) decomposed into ~30 named line items, plus a per-cloud unit-rate reference, plus the four assumption fields every line populates (unit, monthly volume, monthly cost, source link). Output: a sheet that lands with the architecture decision record.

**Ефективно для:**

- Greenfield архітектурного proposal — потрібен defensible cost sheet для budget owner.
- коли архітектор постійно перебудовує ту саму spreadsheet з нуля на кожному проєкті.
- multi-cloud sizing (AWS / GCP / Azure / Hetzner) із NAT, egress, observability вартостями.
- Capacity expansion або migration estimate, де потрібен 0.5x / 1x / 2x scenario bracket.

## Applies If (ALL must hold)

- Architect is producing a Greenfield architecture proposal, capacity expansion plan, or platform-migration estimate.
- Target cloud(s) identified.
- Architecture has at least one each of compute + storage + ingress; the model is not useful for pure SaaS-stitching projects.
- Sign-off is required from a budget owner (CTO, COO, finance).

## Skip If (ANY kills it)

- Pure prototype with no production cost expectations (single dev env on personal credits).
- Cost is dominated by a single SaaS subscription (Snowflake, Datadog) — use the per-vendor pricing calculator and skip the spreadsheet.
- Project will use existing committed-spend with marginal incremental cost — model only the marginal items.
- Finance team already has a corporate model — extend theirs, don't fork.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Architecture decision record (ADR) draft | Markdown | architect |
| Traffic shape | req/sec peak + average | product / load tests |
| Data growth rate | GB/month | analytics |
| Cloud provider + region | string | architect |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/architecture-decision-records` | the cost model is attached to an ADR |
| `pro/dev/software-architect/capacity-planning-pre-launch` | traffic estimates flow from there |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r1-complete-line-items) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/05-examples.xml` | medium | One full worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decompose-architecture-to-line-items` | sonnet | Map ADR components to standard category line items |
| `populate-unit-rates` | haiku | Lookup provider pricing per line |
| `scenario-stress-test` | opus | Compute 0.5x/1x/2x cases with cross-line dependencies |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Cost model markdown skeleton with 5 categories |
| `templates/skeleton.json` | JSON schema for the cost model artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cost-model-spreadsheet-template.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[architecture-decision-records]]
- [[capacity-planning-pre-launch]]
- [[finops-baseline]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Cost-Model Spreadsheet Template methodology when in doubt about scope or fit.
