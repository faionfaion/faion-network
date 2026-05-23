---
slug: founder-deal-kill-rule
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Rule-based deal-kill checklist for the Monday pipeline review — 5 numeric kill conditions (no-reply age, last-meeting age, missed milestone, budget-confirmed=false, champion-leave) auto-kill stale deals.
content_id: "112be39ce8f76dbc"
complexity: medium
produces: checklist
est_tokens: 3200
tags: [pipeline, deal-management, sales-ops, agency, founder-led-sales]
---
# Founder Deal Kill Rule

## Summary

**One-sentence:** Rule-based deal-kill checklist for the Monday pipeline review — 5 numeric kill conditions (no-reply age, last-meeting age, missed milestone, budget-confirmed=false, champion-leave) auto-kill stale deals.

**One-paragraph:** Founders / micro-agency leads hate killing deals because each one represents hope. Pipelines fill with zombies that block real attention. This methodology offloads the kill decision to a 5-rule checklist with numeric thresholds. Core rules: each kill condition is numeric (no-reply &gt; X days, last-meeting &gt; Y days, missed milestone, budget-confirmed=false at stage gate, champion left); when ≥2 conditions trip, deal auto-kills (moves to "dead" stage with reason logged); kill is reversible within 30 days; weekly pipeline review processes one batch (no per-deal debate); kills feed a quarterly retro to refine thresholds.

**Ефективно для:**

- Monday pipeline review — 15-30 minute deal triage.
- Founder-led sales — defers emotional reluctance to a rule.
- Micro-agency lead — same triage across 20-80 pipeline rows.
- Quarterly retro — kill log informs ICP + threshold updates.

## Applies If (ALL must hold)

- ≥20 pipeline rows where stale-vs-active is unclear.
- CRM tracks last-reply date + last-meeting date + budget-confirmed flag.
- Weekly pipeline review is a standing ritual.
- Owner has authority to kill deals (not committee).

## Skip If (ANY kills it)

- Tiny pipeline (&lt;10 deals) — manual review suffices.
- No CRM / no date tracking — fix data hygiene first.
- Enterprise sales with 12+ month sales cycles — different threshold needs.
- Single very-high-ACV deal that justifies bespoke attention.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pipeline CSV / CRM export | CSV / API | CRM |
| Per-deal: last-reply, last-meeting, budget-confirmed, champion status | fields | CRM |
| Threshold config (no-reply X days, last-meeting Y days) | YAML | own ops |
| Kill log (prior quarter) | report | own ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[founder-led-qualification-rubric]] | Upstream qualification feeds the pipeline. |
| [[late-invoice-dunning-sequence]] | Different shape; same numeric-threshold pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: numeric-thresholds, two-trip-auto-kill, reversible-30-days, batch-not-debate, retro-refines-thresholds | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for one kill-batch run + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: pull pipeline → apply rules → batch-kill → notify → log | 600 |
| `content/06-decision-tree.xml` | essential | Tree mapping deal state to kill / keep / escalate | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `apply-thresholds` | haiku | Numeric comparison. |
| `decide-edge-cases` | sonnet | Two-trip + champion-leave often needs judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/kill-batch.json` | JSON example of one weekly kill batch |
| `templates/thresholds.yaml` | Threshold config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-founder-deal-kill-rule.py` | Validate one kill-batch JSON | After weekly review, before CRM update |

## Related

- [[founder-led-qualification-rubric]]
- [[late-invoice-dunning-sequence]]
- [[experiment-verdict-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps deal state (numeric counters + champion status) to kill / keep / escalate, pinning the rule from `01-core-rules.xml`. Use it during the Monday review — bypassing turns the triage back into emotional debate.
