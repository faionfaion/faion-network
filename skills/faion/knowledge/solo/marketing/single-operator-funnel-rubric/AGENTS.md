---
slug: single-operator-funnel-rubric
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a Friday-pulse rubric with four locked stages (visit → signup → paid → retained), one named evidence source per stage, capped at 20 minutes — one BROKEN_STAGE per week."
content_id: "8a087eb8a2016947"
complexity: light
produces: rubric
est_tokens: 3000
tags: [funnel, solo, metrics, rubric, weekly]
---

# Single Operator Funnel Rubric

## Summary

**One-sentence:** Produces a Friday-pulse rubric with four locked stages (visit → signup → paid → retained), one named evidence source per stage, capped at 20 minutes — one BROKEN_STAGE per week.

**Ефективно для:** Solo founders running their entire revenue funnel solo, with no analytics team, who keep skipping diagnosis because the conventional rubrics assume staffing they do not have.

**One-paragraph:** Solo founders need to diagnose where the funnel breaks but conventional rubrics assume a marketing team plus a product analyst plus a BI tool. The single-operator rubric maps each stage to one acceptable evidence source the founder already has (Plausible, Stripe, Postgres count) and refuses stages the founder cannot measure honestly. The output is a single 20-minute Friday pulse that compounds week-over-week and surfaces the broken stage before MRR damage.

## Applies If (ALL must hold)

- A one-person operator runs the entire revenue funnel (no analytics support).
- The product has a measurable signup event AND a paid conversion event.
- The founder can spare a recurring 20-minute Friday slot.

## Skip If (ANY kills it)

- The team has a dedicated analytics person — use a full funnel report instead.
- Pre-revenue product with no paid event yet — switch to activation-only rubric.
- Local/offline funnel where stages can't be wired to digital evidence.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| read-access to visits source (Plausible / GA / Cloudflare) | URL + token | self-managed |
| read-access to signup source (Postgres / Auth provider) | DB or API | self-managed |
| read-access to paid source (Stripe / billing) | API key | Stripe dashboard |
| retained-cohort query | SQL string | internal data dictionary |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/solo-x-analytics-review` | Adjacent solo metrics rhythm. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `pull_weekly_counts` | haiku | Bounded SQL/API fetch. |
| `compute_wow_deltas` | haiku | Pure arithmetic. |
| `tag_broken_stage` | sonnet | Judgement call — pick a single stage. |

## Templates

| File | Purpose |
|---|---|
| `templates/single-operator-funnel-rubric.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/single-operator-funnel-rubric.md` | Markdown skeleton with the required fields. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-single-operator-funnel-rubric.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[solo-x-analytics-review]] — paired weekly rhythm.
- [[utm-taxonomy-discipline]] — feeds clean visit-source attribution.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
