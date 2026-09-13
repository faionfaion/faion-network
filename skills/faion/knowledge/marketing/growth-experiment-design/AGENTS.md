# Growth Experiment Design

## Summary

**One-sentence:** Generates a one-page growth experiment doc: hypothesis, ICE score, control group, instrumentation playback, sample size, write-up template.

**One-paragraph:** Generates a one-page growth experiment doc: hypothesis, ICE score, control group, instrumentation playback, sample size, write-up template. Use it when team запускає >=2 growth experiments/quarter. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Team запускає >=2 growth experiments/quarter.
- Product має >=5,000 MAU (sample-size threshold).
- Analytics owner може провести pre-flight review.
- Feature-flag платформа активна (LaunchDarkly / Statsig / Unleash).

## Applies If (ALL must hold)

- A feature-flag platform (LaunchDarkly, Statsig, Unleash, GrowthBook, Optimizely or an internal one) can assign variants by deterministic hashing on a user or account id.
- The product has at least 5,000 monthly active users, so a minimum effect on the primary metric can be reached within eight weeks.
- The analytics destination records an exposure event and the primary and guardrail metric events with an experiment id and variant id.
- The team has written ICE scoring criteria and a shared experiment log where every run, including losers, is written up.
- An analytics owner can run the instrumentation playback and the SRM check before results are read.

## Skip If (ANY kills it)

- Assignment can only be by session, device, time period or geography without randomisation: the result is an observation, not an experiment, and this spec must not be written for it.
- Eligible traffic is so low that the minimum detectable effect needs more than eight weeks even at 50/50 and the hypothesis cannot be redesigned for a larger effect or a proxy metric.
- The change cannot be held behind a flag with a concurrent control (a pricing change for everyone, a legal or compliance change).
- The team runs fewer than two experiments a quarter and has no backlog to rank: write a plain test plan, the ICE and velocity machinery buys nothing.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Baseline rate of the primary metric | rate over the last four closed weeks, with eligible daily traffic for the segment | product analytics warehouse (BigQuery, Amplitude, Mixpanel) |
| Event catalogue | exposure and metric event names as they land in the analytics destination | analytics owner |
| ICE scoring criteria | one document, written once for the team, with what 1 and 10 mean for Impact, Confidence and Ease | growth team (`ice.criteria_ref`) |
| Prior experiment log | shared log with decision, effect, guardrails and SRM per past run | growth team |
| Flag platform configuration | platform name, hash key, variant allocation | feature-flag platform admin |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: falsifiable hypothesis with effect size, one primary metric plus guardrails, ICE before build, sample size before launch, fixed stop date and SRM check, flag-randomised control, instrumentation playback, write-up for every experiment | 2300 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the experiment spec: hypothesis with one metric and a minimum effect, three guardrail categories with stop thresholds, ICE with cited confidence, sample size at alpha 0.05 / power 0.8 with 1-8 whole weeks, flag assignment on user_id with a control, exposure at variant_seen and a playback, fixed stop date and SRM gate, write-up within seven days; valid and invalid specs; 9 forbidden patterns | 5100 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 1250 |
| `content/04-procedure.xml` | essential | 8 steps: falsifiable hypothesis, guardrails, ICE before build, sample size and whole-week duration, flag assignment with control, instrumentation playback, stop date and SRM gate, write-up and validate | 1950 |
| `content/05-examples.xml` | recommended | Complete spec for a checkout trust-badge test (4.2 percent baseline, 5 percent MDE, 143,000 per variant over 3 weeks, Statsig on user_id, SRM p 0.41, shipped at 6.8 percent) with a note per value, plus the spec as usually written and what the validator prints | 2100 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 950 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-growth-experiment-design.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-experiment-design.spec.md.j2` | Markdown spec skeleton with 5-line header |
| `templates/growth-experiment-design.spec.md` | Markdown spec skeleton with 5-line header Generated from `templates/growth-experiment-design.spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/growth-experiment-design.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-experiment-design.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
