---
slug: ai-leverage-estimation-model
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Per-task-class AI productivity multiplier (1.0x–5x) applied to bottom-up effort estimates so senior-dev quotes reflect real shipped throughput, not pre-AI baselines.
content_id: "1221f287805ee357"
complexity: medium
produces: rubric
est_tokens: 4200
tags: [ai, leverage, estimation, multiplier, pm]
---
# AI Leverage Estimation Model

## Summary

**One-sentence:** Per-task-class AI productivity multiplier (1.0x–5x) applied to bottom-up effort estimates so senior-dev quotes reflect real shipped throughput, not pre-AI baselines.

**One-paragraph:** Existing cost-estimation methodologies (PERT, three-point) assume pre-AI productivity. Senior contractors now ship 2–5x on glue code, scaffold, and tests, and 1.0–1.2x on regulated or novel-domain work. No mainstream methodology quantifies the per-task-class multiplier; senior devs under- or over-quote accordingly. This rubric classifies each WBS leaf into one of six task-classes, assigns a defended multiplier band, and emits a leverage-adjusted estimate plus an audit trail naming the evidence per multiplier.

**Ефективно для:**

- Senior contractors quoting fixed-price or T&M work where AI use is real but unmeasured.
- Agencies re-baselining their delivery rate cards after 6+ months of AI tooling adoption.
- PMOs replacing pre-AI estimation curves with measured per-task-class throughput.
- Founders comparing "AI-augmented insourcing" vs "outsource to senior contractor with AI".

## Applies If (ALL must hold)

- WBS / leaf-task decomposition exists or can be produced from the brief.
- Operator has shipped ≥ 3 comparable tasks in the last 90 days with AI tooling and can produce throughput data per task-class.
- The estimate will be consumed by a named decision-maker (founder, PMO lead, client buyer) with a deadline.
- Deviation between estimated and actual throughput will be logged in a retro for future calibration.

## Skip If (ANY kills it)

- Pre-AI baselines unknown and operator has no comparable past delivery — no anchor to multiply against.
- Highly novel domain where AI tooling has not been tested (regulated medical, formal verification) — assume 1.0x and use PERT instead.
- Single-shot research spike < 4 hours — overhead exceeds value; budget time, not effort.
- Buyer rejects multiplier disclosure — fall back to plain PERT and absorb leverage as margin.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| WBS leaves | list of named tasks with success criteria | scope brief / planning session |
| Past throughput log | CSV with task-class + planned-hours + actual-hours | operator's last 90 days timesheet or commit log |
| Task-class taxonomy | enum {glue, scaffold, tests, business-logic, regulated, novel} | this methodology's `templates/task-class-taxonomy.md` |
| Buyer deadline | ISO date | engagement brief |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cost-estimation]] | PERT three-point baseline this rubric multiplies against |
| [[lessons-learned]] | Retro loop that closes calibration |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: task-class-mandatory, multiplier-band-not-point, evidence-cited, deviation-logged, retro-feedback, skip-this-methodology | 950 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: vanity-multiplier, single-point-instead-of-band, no-evidence-citation, no-retro-loop | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: decompose → classify → multiply → audit → calibrate | 850 |
| `content/06-decision-tree.xml` | essential | Apply / skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decompose-wbs` | haiku | Mechanical leaf-task extraction from brief. |
| `classify-task` | sonnet | Judgment on glue vs business-logic boundary. |
| `assign-multiplier` | sonnet | Pull evidence from throughput log; defend band. |
| `audit-and-calibrate` | opus | Cross-engagement synthesis of drift signals. |

## Templates

| File | Purpose |
|------|---------|
| `templates/leverage-estimate.json` | JSON skeleton conforming to the output contract |
| `templates/task-class-taxonomy.md` | The 6 task-classes with definition + example boundary cases |
| `templates/retro-log.md` | Per-engagement deviation log with planned-vs-actual per task-class |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-leverage-estimation-model.py` | Validate a leverage-estimate JSON against the output contract | Pre-commit on the estimate artefact; before sending to buyer |

## Related

- [[cost-estimation]]
- [[earned-value-management]]
- [[predictive-analytics-pm]]
- [[lessons-learned]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps three observable signals (past-throughput-available, task-novel-or-regulated, buyer-accepts-multiplier-disclosure) to either apply the rubric, fall back to PERT, or skip entirely. Each leaf references a rule from `01-core-rules.xml`.
