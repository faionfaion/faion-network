# Risk Management

## Summary

**One-sentence:** Identify threats and opportunities, rate by P×I, assign named owner with observable triggers, plan responses, monitor weekly. 'Accept' requires contingency budget = EMV.

**One-paragraph:** Identify threats and opportunities, rate by probability and impact, assign named owners with observable triggers, plan responses, and monitor weekly. Every risk must have a named owner (a person, not 'the team') and explicit triggers — observable signals that convert abstract risk into an actionable event. 'Accept' is not a free pass; it requires a contingency budget line equal to the risk's EMV. Risk that materialises becomes an Issue and leaves the register; double-tracking inflates the register and hides what is in flight.

**Ефективно для:**

- Project initiation: build initial risk register before charter sign-off
- Stage-gate reviews: refresh probability/impact and trigger statuses
- Pre-launch (T-2 weeks): focused launch-risk pass with rollback plans
- High-uncertainty domains: new tech, new vendor, regulatory change

## Applies If (ALL must hold)

- Project initiation: build initial risk register before charter sign-off
- Stage-gate reviews: refresh probability/impact and trigger statuses
- Pre-launch (T-2 weeks): focused launch-risk pass with rollback plans
- After incidents: feed lessons back as new risks for similar projects
- High-uncertainty domains: new technology, new vendor, regulatory change

## Skip If (ANY kills it)

- Trivial internal task (1 person, under 1 week, no external dependency)
- Pure agile teams with strong incremental delivery — use 'top 5' sticky list
- Crisis already in progress — switch to incident response; add lessons after

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Charter | Markdown | sponsor + PM |
| WBS | YAML | scope baseline |
| Prior lessons | YAML | lessons-learned archive |
| Vendor list | YAML | procurement |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[risk-register]] | Register schema and scoring scales |
| [[project-integration]] | Risk reviews feed integrated status |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: track-opportunities-too, named-owner-with-trigger, contingency-for-accept, source-quote-required, weekly-15min-review | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-candidates` | sonnet | Brainstorm with quoted-source rule |
| `rate-and-deduplicate` | sonnet | P×I assignment with rationale per rating |
| `compute-emv` | haiku | Deterministic arithmetic in script |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-register.md` | Risk register table: ID, category, P, I, score, response, owner, trigger, status |
| `templates/risk-response-plan.md` | Individual risk response plan with prevention steps and fallback actions |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/risk-score.py` | Compute Score and EMV from risks.yaml using deterministic P×I matrix | Weekly register review |
| `scripts/validate-risk-management.py` | Validate risk register invariants (named owner, trigger observable, Accept has contingency) | Pre-commit; CI |

## Related

- parent skill: `pro/pm/project-manager/`
- [[risk-register]]
- [[project-integration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
