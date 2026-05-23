# Friction To Backlog

## Summary

**One-sentence:** Converts journey-map friction nodes into prioritised backlog tickets — each ticket carries the friction-id, expected metric impact, evidence count, owner — closing the loop from mapping to delivery.

**One-paragraph:** Mapping friction is the easy part; the hard part is converting the map into an actionable, prioritised backlog. This methodology pins a per-friction-node ticket structure: (a) friction-id (links back to map node), (b) expected metric impact (which KPI moves, by how much), (c) evidence count (interviews + analytics), (d) owner, (e) effort estimate. Tickets are prioritised by (impact × evidence) / effort. The map and the backlog are kept in sync via a weekly check.

**Ефективно для:**

- Solo PM with a friction map sitting in Figma unused.
- Indie operator with growing backlog and unclear UX priorities.
- Tech-lead translating UX research into engineering tickets.
- Designer + PM team handing off journey-map output to engineering.

## Applies If (ALL must hold)

- A friction map / journey map exists with ≥5 friction nodes named.
- Backlog tracker is owned by the PM.
- There is at least one KPI dashboard to ground impact estimates.
- Operator can commit to a weekly map↔backlog sync.

## Skip If (ANY kills it)

- No friction map exists — build the map first.
- Map has <5 friction nodes — overhead exceeds benefit.
- Team uses no-estimate flow — impact/effort ranking adds friction.
- Tickets are contractually fixed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Friction map / journey map | Figma / Miro / md | research repo |
| KPI dashboard reference | url | analytics |
| Backlog tracker URL | url | tracker |
| Customer-interview evidence | md | research repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/discovery-research-handoff-template` | evidence shape per friction |
| `solo/product/backlog-hygiene-cron-checklist` | weekly sync cadence |
| `solo/product/product-manager` | parent operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-friction-to-backlog` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/friction-to-backlog.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/friction-to-backlog.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-friction-to-backlog.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[backlog-hygiene-cron-checklist]]`
- `[[design-debt-vs-design-bet]]`
- `[[kano-prioritization]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
