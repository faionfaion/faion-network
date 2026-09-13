# Growth Loops

## Summary

**One-sentence:** Generates a growth-loop spec (input -> action -> output -> fuel-back) with stage metrics, friction map, and steady-state projection.

**One-paragraph:** Generates a growth-loop spec (input -> action -> output -> fuel-back) with stage metrics, friction map, and steady-state projection. Use it when funnel-only thinking буксує на cac payback — потрібен loop. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Funnel-only thinking буксує на CAC payback — потрібен loop.
- Existing user behaviour produces fuel for new users.
- Час відстежити loop steady-state >=90d.
- Stable instrumentation per loop stage (acquisition / action / output).

## Applies If (ALL must hold)

- Existing user behaviour produces an output (invitation, shared document, public content, listing) and an event is already tracked where that output becomes a new input in the same unit.
- Stage transitions from input to action to output to fuel-back can each be measured from instrumented events with a date and a sample size, or the team is willing to flag the missing ones as assumptions.
- At least 90 days of history, or the willingness to model that long, so the projection covers three full cycles at the measured cycle time.
- Blended CAC and payback are known for the current mix, and loop-sourced users can be separated through the fuel-back event rather than a channel label.
- Activation and 30-day retention (or index and traffic share for content) are reported per cohort, so a quality guardrail on loop output can be set numerically.

## Skip If (ANY kills it)

- No user output ever becomes a new input: the design is a funnel, and a funnel methodology or CAC-payback work answers the question.
- The fuel-back event is not instrumented and cannot be within the engagement: instrument it first; a spec built on an assumed closure rate compounds an invented number.
- The team wants a viral coefficient headline for a fundraising deck rather than a payback answer: k without cycle time, decay and a guardrail is exactly what this methodology refuses to produce.
- Three loop types are to be summed into one efficiency figure: pick the primary loop and run this once per loop, never blended.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Event table for the four stages | per-user events with timestamps: input, action, output and fuel-back event names as they land in analytics | product analytics warehouse (BigQuery, Amplitude, Mixpanel) |
| Stage conversion query results | numerator, denominator, value, measurement date and sample size per transition | warehouse query over the event table |
| Cycle-time distribution | median days from input event to fuel-back event per cohort | warehouse query |
| CAC and payback baseline | blended CAC and payback months for the last 90 days, with and without users attributed by the fuel-back event | finance or growth analytics |
| Cohort activation and D30 retention | loop-sourced cohort versus baseline cohort, same window | retention query |
| `templates/growth-loop-design.md.j2` | working canvas for the flow, metrics table and bottleneck before the spec is written | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: loop closes output into input, one primary loop type, measured stage rates, k and cycle time, 90-day cohort projection with decay, bottleneck-first friction map, CAC payback with and without loop, quality guardrail | 2200 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the loop spec: four stages closed by a fuel-back event in the input unit, one primary loop type, three measured-or-flagged stage metrics, k as their product with cycle time and the amplifier reading, a 90-day three-cycle cohort projection with decay, bottleneck-first friction map, CAC payback with and without loop, numeric quality guardrail; valid and invalid specs; 8 forbidden patterns | 4950 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 1150 |
| `content/04-procedure.xml` | essential | 8 steps: name the stages and the fuel-back event, declare the loop type, measure the stage transitions, compute k and cycle time, project cohorts with decay over 90 days, map the bottleneck and rank experiments, compute CAC payback with and without loop, set the quality guardrail and validate | 1700 |
| `content/05-examples.xml` | recommended | Complete spec for a document-sharing viral loop (k 0.13 from 0.45 x 2.4 x 0.12, 9-day cycle, 1.15 multiplier, 120-day projection with 5 percent saturation, view-page bottleneck, payback 14.2 to 12.4 months, D30 guardrail within) with a note per value, plus the same loop as usually drawn and what the validator prints | 2350 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-growth-loops.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-loops.spec.md.j2` | Markdown spec skeleton with 5-line header |
| `templates/growth-loops.spec.md` | Markdown spec skeleton with 5-line header Generated from `templates/growth-loops.spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/growth-loops.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |
| `templates/growth-loop-design.md.j2` | Single growth-loop design working canvas — flow, per-step metrics, bottleneck, optimization experiments. |
| `templates/growth-loop-design.md` | Single growth-loop design working canvas — flow, per-step metrics, bottleneck, optimization experiments. Generated from `templates/growth-loop-design.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-loops.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
