# Activation Metrics

## Summary

**One-sentence:** Generates an activation metrics report: activation rate, time-to-activation, segmented funnel, D30 correlation table for the chosen event.

**One-paragraph:** Generates an activation metrics report: activation rate, time-to-activation, segmented funnel, D30 correlation table for the chosen event. Use it when weekly звіт по activation rate з segmentation по acquisition channel. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Weekly звіт по activation rate з segmentation по acquisition channel.
- Time-to-activation distribution за фіксованим window (наприклад 7d).
- D30 retention lift table для candidate activation events.
- Funnel step conversion з абсолютними та відносними drops.

## Applies If (ALL must hold)

- An activation event and window are already defined (from activation-framework) and the event is tracked per user with timestamps.
- A signup table gives every signup in the period, so the rate's denominator is all signups, not a later funnel step.
- The reporting period can be closed: the last signup date plus the window is on or before the data cutoff.
- A first-touch acquisition channel is stored per signup, or the report can state that segmentation is unavailable.
- The report is produced on a cadence (weekly) with the same window and cohort definition as the previous period.

## Skip If (ANY kills it)

- No activation event is defined: run activation-framework first; there is nothing to measure.
- Only a count of users at a later step exists and the signup total cannot be obtained: no rate can be reported.
- The question is which event should be activation, not how the chosen one performs: that is the framework's D30 validation, not this report.
- The period is a single day or an in-flight experiment read-out: use the experiment's own analysis, not the weekly cohort report.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Activation definition | event name (snake_case) + window in days | activation-framework spec |
| Signup table | user_id, signup_timestamp, first-touch channel | product database or warehouse |
| Event table | user_id, event name, timestamp for the activation event and every funnel step | product analytics warehouse (Amplitude, Mixpanel, BigQuery export) |
| Data cutoff and previous period | YYYY-MM-DD cutoff; previous period start/end with the same window | the reporting calendar |
| Sample floor | integer signups per channel | growth team convention |
| Release log for the period | change name + release date, A/B result if any | product team changelog |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: signup denominator, fixed window and closed cohorts, channel segmentation, quantile time-to-activation, D30 lift table, funnel absolute and relative drops, metric units, findings cite metrics | 1800 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the report: event and window, closed period and cutoff, signups_total as denominator, metrics with units and per-channel rates with a low-sample floor, time-to-activation quantiles, D30 lift table with sizes, funnel with both drops, findings citing metric and period; valid and invalid reports; 8 forbidden patterns | ~4450 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 7 steps: fix event, window and closed period; aggregate rate against all signups; segment by channel with a floor; time-to-activation quantiles; D30 lift table; funnel with both drops; findings and validation | ~1400 |
| `content/05-examples.xml` | recommended | Complete April report (0.223 against 5,335 signups, four channel rates with one low-sample flag, partial metric for the open week, median 1.4 hours, March D30 table, five-step funnel, three findings) with a note per value, plus the usual report and what the validator prints | ~2350 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-activation-metrics.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/activation-metrics.report.md.j2` | Markdown report skeleton: definition and closed period, metrics table with units and channel rates, time-to-activation quantiles, D30 lift, funnel with both drops, findings |
| `templates/activation-metrics.report.md` | Markdown report skeleton: definition and closed period, metrics table with units and channel rates, time-to-activation quantiles, D30 lift, funnel with both drops, findings. Generated from `templates/activation-metrics.report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/activation-metrics.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |
| `templates/activation-funnel-analysis.md.j2` | Weekly activation-funnel working analysis — definition, current performance, drop-off, this week's experiment. |
| `templates/activation-funnel-analysis.md` | Weekly activation-funnel working analysis — definition, current performance, drop-off, this week's experiment. Generated from `templates/activation-funnel-analysis.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-activation-metrics.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
