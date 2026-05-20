---
slug: cost-model-spreadsheet-template
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "1ee506a6eea311eb"
summary: Canonical cloud cost-model spreadsheet template (compute, storage, egress, NAT, observability, backup) with per-cloud variants — replaces re-building the same sheet from scratch for every architecture proposal.
tags: [cost-modelling, architecture, finops, software-architect, capacity-planning]
---
# Cost-Model Spreadsheet Template

## Summary

**One-sentence:** A canonical multi-cloud cost-model template (AWS / GCP / Azure / Hetzner / DO) covering compute, storage, egress, NAT, observability, backup, and the line items architects routinely forget — so a Greenfield architecture proposal lands with a defensible cost sheet instead of an under-estimated bill.

**One-paragraph:** Software architects re-invent the same cost spreadsheet on every Greenfield or scale-event project. The result: a) line items missed (NAT gateway, observability log storage, S3 egress, KMS request fees, NAT data-processing fees, etc.), b) different teams use different unit assumptions for the same architecture, c) "we'll just add 20% buffer" hides large structural mismatches. This methodology pins a template with five top-level categories (Compute / Storage / Network / Operations / Buffer) decomposed into ~30 named line items, plus a per-cloud unit-rate reference, plus the four assumption fields every line must populate (unit, monthly volume, monthly cost, source link). Output: a sheet (Excel/Sheets/CSV) the architect submits alongside the architecture decision record.

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

- Architecture decision record (ADR) draft with the components named.
- Estimated traffic shape (req/sec peak, average), data growth rate (GB/month).
- Target SLA + RTO/RPO (drives backup + multi-AZ cost).
- Cloud provider(s) confirmed.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/architecture-decision-records` | The cost-model is attached to an ADR. |
| `pro/dev/software-architect/capacity-planning-pre-launch` | Traffic estimates flow from there. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: complete line items, assumptions explicit, cloud unit-rate sourced, scenarios, buffer policy | ~1000 |
| `content/02-output-contract.xml` | essential | Sheet structure, required tabs, sign-off block | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: missing egress, ignored NAT, observability storage, buffer-as-cover | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decompose-architecture-to-line-items` | sonnet | Map ADR components to the standard category line items |
| `populate-unit-rates` | haiku | Look up provider pricing per line |
| `scenario-stress-test` | opus | Compute low/expected/high cases with cross-line dependencies |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-model.xlsx` | The master template with tabs: assumptions, lines, summary, scenarios |
| `templates/per-cloud-rates/` | Unit-rate reference per provider |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/lines-vs-architecture-check.py` | Compares ADR component list vs filled line items; flags missing | Pre-submit |

## Related

- parent skill: `pro/dev/software-architect/`
- peer methodology: `architecture-decision-records`, `capacity-planning-pre-launch`, `finops-baseline`
- external: [Vantage cloud pricing](https://www.vantage.sh/) · [AWS Pricing Calculator](https://calculator.aws/) · [GCP Pricing Calculator](https://cloud.google.com/products/calculator)
