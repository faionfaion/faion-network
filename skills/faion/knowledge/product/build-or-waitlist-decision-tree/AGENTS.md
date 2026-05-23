# Build Or Waitlist Decision Tree

## Summary

**One-sentence:** Per-feature decision: build immediately, waitlist (validate via smoke page first), or decline — gated by stated demand, capacity, strategic fit, kill-criterion presence.

**One-paragraph:** Solo SaaS founders need a fast rule to handle 'can you add X?' asks. This methodology pins a decision tree: (1) does the ask have ≥3 distinct customer requests? if no → decline. (2) does the founder have capacity in the current sprint? if no → waitlist with smoke page. (3) does the feature align with the published roadmap? if no → decline (or escalate to roadmap review). (4) is there a kill-criterion drafted? if no → waitlist until drafted. Output: a single decision-record per ask with rationale + revisit date.

**Ефективно для:**

- Solo SaaS founder fielding 10+ feature requests per week.
- Indie maker balancing core product + audience asks.
- Tech-lead acting as PM with no dedicated triage process.
- Operator overwhelmed by sales-driven ad-hoc requests.

## Applies If (ALL must hold)

- Product has live paying users or active beta cohort.
- Feature request inflow ≥3/week.
- Founder owns the roadmap + backlog tracker.
- Founder can write a kill-criterion in under 5 minutes.

## Skip If (ANY kills it)

- Product is pre-launch — feature requests are noise.
- Roadmap is contractually frozen — all asks default to waitlist.
- Founder does not have capacity for any new builds — default to waitlist universally.
- Ask is a bug fix, not a feature — route to bug-fix flow.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature request log (≥30 days) | csv / ticket dump | support tool |
| Current sprint capacity (hours) | int | founder calendar |
| Roadmap reference | url / doc | roadmap tool |
| Smoke-page template | url / Notion | operator templates |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/anti-roadmap-template` | decline rationale + revisit triggers |
| `solo/product/distribution-first-ideation` | smoke-page validation |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-build-or-waitlist-decision-tree` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/build-or-waitlist-decision-tree.md` | Markdown skeleton for the decision-record artefact, matching content/02-output-contract.xml |
| `templates/build-or-waitlist-decision-tree.schema.json` | JSON Schema seed + filled fixture for the decision-record artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-build-or-waitlist-decision-tree.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[anti-roadmap-template]]`
- `[[demo-hypothesis-template]]`
- `[[friction-to-backlog]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
