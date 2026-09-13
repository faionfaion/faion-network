# North Star Metric

## Summary

**One-sentence:** Generates an NSM decision record: candidate metrics, value-equation, retention/revenue correlation, chosen NSM + input metrics tree.

**One-paragraph:** Generates an NSM decision record: candidate metrics, value-equation, retention/revenue correlation, chosen NSM + input metrics tree. Use it when teams misaligned на тому, що означає 'успіх'. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Teams misaligned на тому, що означає 'успіх'.
- Marketing / product / sales optimize у різних напрямах.
- OKR tree потребує root metric.
- Acquisition spend scaling — потрібна validation NSM lift.

## Applies If (ALL must hold)

- At least 8 weeks of per-account usage events and retention (or paid conversion) are queryable in a warehouse or analytics tool.
- The product has a nameable core value event (project completed, message sent inside a team, night booked) that can be counted per user, account or team over a window.
- Product, marketing and sales each bring a candidate metric and accept being scored on the same five criteria.
- Each input metric can be assigned to a team that can move it within a quarter, and a dashboard exists where the current NSM value can be published.
- The organisation accepts exactly one NSM with revenue kept as the outcome it is validated against, not as the NSM.

## Skip If (ANY kills it)

- No per-account usage and retention data exists yet: instrument the core events first and return with eight weeks of cohorts.
- The sponsor has already fixed the NSM as MRR, signups, pageviews or undifferentiated MAU and will not score alternatives.
- The team wants two North Stars or a primary plus a secondary; the methodology adopts one and places the rest as inputs or rejections.
- Nobody will own input metrics or accept a yearly review with a series-break rule for redefinitions.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Usage event data | per-account rows of core value events with timestamps, unit (user, account, team) and internal or test markers, at least 8 weeks | product analytics warehouse |
| Retention or paid-conversion data | per-account week-N retention or conversion flag for the same cohort | warehouse or billing system |
| Candidate metrics | at least three proposals, one per stakeholder group, each mappable to what it counts | product, marketing, sales |
| Team map | which team owns breadth, depth, frequency and efficiency levers, with current values | product and growth leads |
| Previous NSM record | reference and definition, when one exists | decision-record store |
| `templates/north-star-metric.adr.md.j2`, `templates/nsm-definition.md.j2` | record skeleton; definition sheet | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: NSM counts value delivered, computable definition, candidates scored on five criteria, cohort validation against retention, single NSM, input metrics tree, gaming guards, change is a new record | 2400 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the NSM record: 3+ candidates scored on five criteria with totals, one chosen value-event NSM (highest or explained), computable definition with events, unit, window, threshold, exclusions and dashboard, above-vs-below cohort validation with rates and delta, runner-ups placed or rejected, 3-5 owned input metrics, gaming vectors with guards, change control with series break and yearly review; valid and invalid records; 8 forbidden patterns | 5150 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 950 |
| `content/04-procedure.xml` | essential | 8 steps: confirm event and retention data, generate and score candidates, choose one NSM and place runner-ups, write the computable definition, validate against retention, decompose into input metrics, name gaming vectors and guards, set change control and validate | 1650 |
| `content/05-examples.xml` | recommended | Complete record for a team project tool (weekly teams completing a project chosen at 24/25, 4,200-team cohort 0.62 vs 0.21, three runner-ups placed, four owned inputs, three gaming guards, review in 360 days) with a note per value, plus an MRR-as-NSM record and what the validator prints | 2450 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-north-star-metric.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/north-star-metric.adr.md.j2` | ADR-style decision record skeleton |
| `templates/north-star-metric.adr.md` | ADR-style decision record skeleton Generated from `templates/north-star-metric.adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/north-star-metric.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

| `templates/nsm-definition.md.j2` | North Star Metric definition sheet — calculation, justification, current state, input metrics |
| `templates/nsm-definition.md` | North Star Metric definition sheet — calculation, justification, current state, input metrics Generated from `templates/nsm-definition.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-north-star-metric.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
