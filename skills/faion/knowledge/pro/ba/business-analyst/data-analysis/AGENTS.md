---
slug: data-analysis
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Data Analysis in the BA context identifies what data the business needs, how it is structured, where it comes from and goes, its quality characteristics, and the rules governing it.
content_id: "29ca58ceccac3e3f"
tags: [data, data-analysis, data-dictionary, data-quality, requirements]
---
# Data Analysis — Requirements Discovery and Quality Assessment

## Summary

**One-sentence:** Data Analysis in the BA context identifies what data the business needs, how it is structured, where it comes from and goes, its quality characteristics, and the rules governing it.

**One-paragraph:** Data Analysis in the BA context identifies what data the business needs, how it is structured, where it comes from and goes, its quality characteristics, and the rules governing it. The process runs five steps: identify data needs, define data elements, create a data model (conceptual → logical → physical), analyze data quality across six dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness), and define data rules (validation, derivation, default, constraint, uniqueness). Output is a data dictionary and data requirements document linked to the specification.

## Applies If (ALL must hold)

- Pre-spec discovery: profiling existing tables to convert a vague stakeholder assertion into a quantified requirement.
- Sizing a candidate feature: running counts to confirm population, frequency, and business value before backlog entry.
- Reconciling conflicting stakeholder data reports by reading both definitions and running a third query.
- Generating evidence packs for steering committees with sourced numbers and definition footnotes.
- Hand-off contract with the data team: drafting a data-request.md instead of an open-ended Slack ask.

## Skip If (ANY kills it)

- Statistical inference or A/B testing analysis — that is analytics-engineer territory; BA stops at descriptive statistics and basic segmentation.
- Production data pipeline authoring — BA writes throwaway exploratory SQL; promotion to dbt models requires engineering review.
- Direct write access to source systems — BA queries are read-only.
- Heavily regulated PII data without a DPIA — BA exploration on raw data is a compliance breach; require synthetic/redacted environments.
- Replacing a certified source-of-truth metric with an ad-hoc calculation — reference it, never recompute.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/ba/business-analyst/`
