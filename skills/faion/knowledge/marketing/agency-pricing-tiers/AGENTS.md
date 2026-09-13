# Agency Pricing Tiers

## Summary

**One-sentence:** Playbook step: constructs good/better/best agency service tiers so the 'best' is the actual margin tier and the middle anchors the buyer.

**One-paragraph:** Playbook step: constructs good/better/best agency service tiers so the 'best' is the actual margin tier and the middle anchors the buyer. Use it when agency продає 1-tier engagement і втрачає upsell + price-anchor. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Agency продає 1-tier engagement і втрачає upsell + price-anchor.
- Good/better/best tier construction — best має найвищу margin.
- Mid-tier anchoring через price gap distribution (3 / 5 / 8 множник).
- Scope-up procedure mid-engagement задокументована.

## Applies If (ALL must hold)

- The agency sells a repeatable service to a defined ICP and currently offers it as a single engagement.
- Delivery cost per deliverable is known: estimated hours from past engagements, a loaded hourly cost, and pass-through costs.
- The deliverables can be listed with quantities and turnaround times, so tiers can nest as strict supersets.
- One deliverable the ICP needs for its outcome can be withheld from the entry tier as the fence.
- Someone at the agency can be named as approver for mid-engagement scope changes.

## Skip If (ANY kills it)

- Work is bespoke per client with no repeatable deliverable list: price per proposal, not as tiers.
- Delivery cost is unknown: cost the service first; the margin rule cannot be checked.
- The buyer is procurement-led with a fixed rate card and no choice of scope: a ladder has nothing to anchor.
- The agency wants a fourth priced tier or a "discuss" band between tiers: this methodology holds exactly three.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Deliverable list with hours | deliverable, quantity, turnaround days, estimated hours | timesheets from the last three engagements |
| Loaded hourly cost | one number in the agency's currency | finance |
| Pass-through costs per tier | tools, ad-platform fees, per month | finance / ops |
| ICP and its outcome | one sentence naming who buys and what result they need | agency positioning doc |
| Target price of the middle tier | number in the agency's currency | founders / current engagement price |
| Approver for scope changes | role name | agency org chart |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: three priced tiers, best has highest margin, 3/5/8 gaps, nested supersets, fenced good and complete better, scope-up procedure, discount by scope, present best first | 1700 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the ladder: three ordered tiers with price, delivery cost and gross margin, nested deliverables with quantity and turnaround, 3 / 5 / 8 band or gap justification, the fence, better as default, best-first presentation, scope-up and concession rules, rollout steps; valid and invalid ladders; 8 forbidden patterns | ~4050 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 7 steps: list nested deliverables, cost each tier, set prices on 3 / 5 / 8, compute margin and check best leads, name the fence and default, write scope-up and concession rules, publish best-first and validate | ~1450 |
| `content/05-examples.xml` | recommended | Complete 3,000 / 5,000 / 8,000 EUR ladder (best at 54.5 percent margin, conversion tracking as the fence, scope-up procedure, three rollout steps) with a note per value, plus the ladder as usually built and what the validator prints | ~2300 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-agency-pricing-tiers.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/agency-pricing-tiers.playbook-step.md.j2` | Markdown rate-sheet skeleton: three costed tiers with margin, nested deliverables, fence and default, presentation, scope-up, concessions, rollout steps |
| `templates/agency-pricing-tiers.playbook-step.md` | Markdown rate-sheet skeleton: three costed tiers with margin, nested deliverables, fence and default, presentation, scope-up, concessions, rollout steps. Generated from `templates/agency-pricing-tiers.playbook-step.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/agency-pricing-tiers.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-pricing-tiers.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
