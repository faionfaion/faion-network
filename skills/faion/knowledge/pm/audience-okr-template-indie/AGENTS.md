# Audience OKR Template (Indie)

## Summary

**One-sentence:** Quarterly OKR template scoped to a single audience segment for indie founders: one Objective, 3 measurable Key Results, weekly check-in cadence.

**One-paragraph:** Cuts the corporate OKR ritual down to indie scale: one audience segment, one Objective, 3 measurable Key Results (one growth, one engagement, one retention), weekly check-in. Output is a versioned spec that survives the next quarter's planning meeting.

**Ефективно для:**

- Indie founder serving 1-2 distinct audience segments who keeps shipping features for 'users' in general. Forces one Objective per segment per quarter and 3 measurable KRs — kills shotgun roadmap drift.

## Applies If (ALL must hold)

- Founder serves ≥1 audience segment with ≥10 paid or active users
- Quarterly planning happens (formal or informal)
- ≥1 measurable metric per segment exists (signups, MRR, retention, NPS)

## Skip If (ANY kills it)

- Pre-product phase with <10 active users — too early for OKRs
- Enterprise PM workflow with formal corporate OKR system
- Single-customer consulting work — use client-1pager instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Audience segment definition (persona, ICP, channel) | doc | marketing |
| Current quarter baseline metrics for the segment | table | analytics |
| Last 2 quarters of metrics history | CSV | analytics export |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/pm/burndown-diagnosis-cheatsheet` | Peer methodology — diagnoses OKR slippage mid-quarter. |
| `solo/marketing/seo-manager` | Peer methodology — provides growth-side input for one of the 3 KRs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-audience-okr-template-indie` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-audience-okr-template-indie` | haiku | Schema check + threshold checks; deterministic. |
| `review-audience-okr-template-indie` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audience-okr-template-indie.json` | JSON skeleton conforming to the output contract schema. |
| `templates/audience-okr-template-indie.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/audience-okr-template-indie.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/audience-okr-template-indie.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-audience-okr-template-indie.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[burndown-diagnosis-cheatsheet]]
- [[capacity-fit-calculator]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/audience-okr-template-indie.json`

```json
{
  "artefact_id": "okr-indie-2026-q2",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "segment": "solo-founder-paid",
  "quarter": "2026-Q2",
  "objective": "Make solo-founder paid tier the obvious upgrade after free trial",
  "key_results": [
    {
      "id": "kr1",
      "type": "growth",
      "metric": "trial\u2192paid",
      "target": 0.25,
      "current": 0.18,
      "status": "on-track"
    },
    {
      "id": "kr2",
      "type": "engagement",
      "metric": "weekly active %",
      "target": 0.6,
      "current": 0.42,
      "status": "at-risk"
    },
    {
      "id": "kr3",
      "type": "retention",
      "metric": "M2 retention",
      "target": 0.8,
      "current": 0.7,
      "status": "on-track"
    }
  ],
  "check_in_day": "Monday",
  "grading_date": "2026-06-30",
  "owner": "@ruslan"
}
```
