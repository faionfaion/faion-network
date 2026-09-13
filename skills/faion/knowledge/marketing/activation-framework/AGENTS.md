# Activation Framework

## Summary

**One-sentence:** Generates a 7-step activation diagnosis + remediation plan: event definition, baseline, funnel map, drop-off priorities, ICE-scored experiments.

**One-paragraph:** Generates a 7-step activation diagnosis + remediation plan: event definition, baseline, funnel map, drop-off priorities, ICE-scored experiments. Use it when signups приходять, але week-1 retention слабкий, bottleneck невідомий. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Signups приходять, але week-1 retention слабкий, bottleneck невідомий.
- Вибір або валідація activation event ('aha moment'), що корелює з D30 retention.
- Mapping funnel, інструментація відсутніх events, пріоритизація drop-offs.
- Побудова weekly activation dashboard + ICE-scored experiment backlog.

## Applies If (ALL must hold)

- An event table exists with per-user timestamps for signup and for the candidate activation events, plus an acquisition-channel attribute.
- At least four signup-week cohorts have closed, i.e. their last signup day plus the activation window is before the data cutoff.
- At least one cohort is 30 days old, so D30 retention can be compared for users who did and did not perform the candidate event.
- The team can run experiments against the funnel and score them with Impact, Confidence and Ease on a 1-10 integer scale.
- Signups arrive but week-1 or D30 retention is weak and the bottleneck step is unknown.

## Skip If (ANY kills it)

- No event table exists, or signup is not a tracked event: route to instrumentation work first; there is nothing to diagnose.
- The product is under four weeks old, so no four closed cohorts can exist: collect data, do not write a baseline from open cohorts.
- Activation is already defined, validated against retention and reported weekly on closed cohorts: use the experiment backlog only, not the full diagnosis.
- Retention is fine and the problem is acquisition volume or pricing: this framework optimises the signup-to-activation funnel, not traffic or revenue.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Event table | per-user rows: user_id, event name, timestamp, acquisition_channel | product analytics warehouse (Amplitude, Mixpanel, BigQuery export) |
| Signup-week cohorts with data cutoff | signup_week_start, signups, activated per week, YYYY-MM-DD cutoff | warehouse query over the event table |
| D30 retention by candidate event | two groups: users and D30 retention for performed vs not performed | retention query on one closed cohort |
| Funnel steps from signup to the candidate event | ordered list with the tracked event per step, or "none" | product team + event table |
| Experiment ideas | one line each with target step | growth team backlog |
| `templates/ice.py` | Python helper, `ice_score(impact, confidence, ease)` | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: single event with window, D30 validation, closed-cohort baseline, funnel-to-event mapping, absolute-loss ranking, ICE formula, experiment threshold, weekly dashboard | 1700 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the activation spec: one event with window_days, D30 validation with both groups, baseline over 4+ closed cohorts, event-mapped funnel with uninstrumented steps, drop-offs by absolute loss, ICE backlog with integer 1-10 scores and step/metric/baseline/threshold per experiment, weekly closed-cohort dashboard; valid and invalid specs; 8 forbidden patterns | ~4000 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 7 steps: name one event and window, validate against D30 on a closed cohort, closed-cohort baseline, map the funnel to events, rank drop-offs by users lost, score the backlog with ice.py, specify the weekly dashboard and validate | ~1500 |
| `content/05-examples.xml` | recommended | Complete spec for a B2B SaaS (project_created within 7 days, 46 vs 11 percent D30, four closed cohorts at 22 percent, one uninstrumented step, two ICE-scored experiments) with a note per value, plus the spec as usually written and what the validator prints | ~2200 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-activation-framework.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/activation-framework.spec.md.j2` | Markdown spec skeleton: activation event, D30 validation, closed-cohort baseline, funnel, drop-offs, ICE backlog, weekly dashboard |
| `templates/activation-framework.spec.md` | Markdown spec skeleton: activation event, D30 validation, closed-cohort baseline, funnel, drop-offs, ICE backlog, weekly dashboard. Generated from `templates/activation-framework.spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/activation-framework.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-activation-framework.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
