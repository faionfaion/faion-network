# PMF Rubric for Solos

## Summary

**One-sentence:** Scores a solo-founder product on six PMF dimensions (very-disappointed %, retention curve, organic pull, willingness-to-pay, founder-confidence, runway-fit) and outputs a PMF rubric report with verdict.

**One-paragraph:** Scores a solo-founder product on six PMF dimensions (very-disappointed %, retention curve, organic pull, willingness-to-pay, founder-confidence, runway-fit) and outputs a PMF rubric report with verdict. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Post-MVP solo founder hunting for product/market fit signal.
- Pre-funding discussion: show pre-PMF status with concrete dimensions, not vibes.
- Quarterly PMF re-check: scoring drift signals when to double-down vs pivot.
- Pre-pivot gate (see pivot-vs-quit): rubric score below threshold triggers pivot review.

## Applies If (ALL must hold)

- Product launched ≥2 months ago and has ≥10 active users.
- Survey instrument ('how disappointed if this disappeared') can be deployed.
- Retention curve calculable from existing event log.
- Founder available for weekly user calls during the scoring window.

## Skip If (ANY kills it)

- Pre-launch or < 10 users — scoring is noise.
- Cannot deploy survey to users — PMF signal incomplete.
- Founder time-locked in client work — scoring will be skipped half-way.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Very-disappointed survey results | survey export with ≥30 responses | Typeform / Tally |
| Retention cohort data | cohort table week-1 through week-12 | warehouse |
| Organic acquisition share | % of signups from search / referral | analytics |
| Willingness-to-pay signal | % who paid OR pre-paid | Stripe / billing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥6 testable rules with rationale + source incl. `skip-this-methodology` | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-pmf-rubric-for-solos` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pmf-rubric-for-solos.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[pivot-vs-quit-decision-template]]
- [[freelancer-to-saas-time-box]]
- [[north-star-metric-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
