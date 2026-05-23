---
slug: solution-assessment
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a post-implementation review comparing delivered solution against baselined requirements, value drivers, and KPIs with explicit gap callouts.
content_id: "d41944e3752727f6"
complexity: medium
produces: report
est_tokens: 4300
tags: [ba, solution-assessment, post-implementation, kpi, value]
---
# Solution Assessment

## Summary

**One-sentence:** Produces a post-implementation review comparing delivered solution against baselined requirements, value drivers, and KPIs with explicit gap callouts.

**One-paragraph:** Produces a post-implementation review comparing delivered solution against baselined requirements, value drivers, and KPIs with explicit gap callouts. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Post-launch (≥1 cycle live) — sponsor хоче evidence що delivery дала обіцяну value.
- Engagement closure/renewal — assessment як вхід у наступний контракт.
- Defect/incident pattern свідчить про scope misalignment — треба ретроспектива.
- KPI fall-short — треба корінь причини і roadmap fix'ів.

## Applies If (ALL must hold)

- Solution has been live for ≥1 cycle of usage data.
- Sponsor needs evidence that the delivery achieved promised value.
- Engagement closure or renewal — assessment input is mandatory.
- Defect / incident pattern suggests scope was misaligned.

## Skip If (ANY kills it)

- Solution is too new (< 4 weeks live) for assessment data.
- No baseline was captured pre-launch — assessment has no comparison anchor.
- Solution is being retired — assessment is replaced by sunset-decision artefact.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Baselined requirements + KPIs | Output of requirements-documentation + roadmap | BA / PM |
| Post-launch usage data | Analytics / telemetry | data team |
| Support / incident data | Ticketing system | ops |
| Stakeholder feedback | Surveys / interviews | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[data-driven-requirements]] | post-launch metrics replay original evidence |
| [[requirements-validation]] | validation report is the assessment baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect-post-launch-data` | haiku | Mechanical extraction from configured sources. |
| `compute-deltas` | sonnet | Match actual KPI vs baseline; compute gap. |
| `write-report` | opus | Synthesise narrative under political pressure. |

## Templates

| File | Purpose |
|------|---------|
| `templates/post-implementation-review.md` | PIR document skeleton. |
| `templates/solution-assessment-report.md` | Detailed assessment report with KPI table + gap callouts. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solution-assessment.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[data-driven-requirements]]
- [[requirements-validation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
