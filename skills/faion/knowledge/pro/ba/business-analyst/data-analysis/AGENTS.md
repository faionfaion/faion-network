# Data Analysis

## Summary

Data Analysis in the BA context identifies what data the business needs, how it is structured, where it comes from and goes, its quality characteristics, and the rules governing it. The process runs five steps: identify data needs, define data elements, create a data model (conceptual → logical → physical), analyze data quality across six dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness), and define data rules (validation, derivation, default, constraint, uniqueness). Output is a data dictionary and data requirements document linked to the specification.

## Why

Without data analysis, systems are built on conflicting definitions — Sales and Finance report different churn numbers because nobody aligned on the definition. Data quality issues that surface late cause integration failures and rework. Missing data requirements lead to post-launch migrations. The six-dimension quality scorecard provides a measurable, testable basis for data acceptance criteria.

## When To Use

- Pre-spec discovery: profiling existing tables to convert a vague stakeholder assertion into a quantified requirement.
- Sizing a candidate feature: running counts to confirm population, frequency, and business value before backlog entry.
- Reconciling conflicting stakeholder data reports by reading both definitions and running a third query.
- Generating evidence packs for steering committees with sourced numbers and definition footnotes.
- Hand-off contract with the data team: drafting a `data-request.md` instead of an open-ended Slack ask.

## When NOT To Use

- Statistical inference or A/B testing analysis — that is analytics-engineer territory; BA stops at descriptive statistics and basic segmentation.
- Production data pipeline authoring — BA writes throwaway exploratory SQL; promotion to dbt models requires engineering review.
- Direct write access to source systems — BA queries are read-only.
- Heavily regulated PII data without a DPIA — BA exploration on raw data is a compliance breach; require synthetic/redacted environments.
- Replacing a certified source-of-truth metric with an ad-hoc calculation — reference it, never recompute.

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Data analysis components, five-step process, data element attributes, data modeling levels, quality dimensions table, data rules taxonomy. |
| `content/02-examples.xml` | Customer entity example with attribute table and business rules; data quality findings example; antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/data-dictionary.md` | Data dictionary template: entity description, attribute table (name/definition/type/format/required/values/rules), relationships, business rules. |
| `templates/data-requirements.md` | Data requirements template: entities, attributes, derived data, quality requirements, volumes, integration, security. |
| `templates/data-quality-assessment.md` | Data quality assessment template: per-dimension findings with score, status, and recommendations. |
