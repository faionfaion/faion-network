# Substack vs Beehiiv vs ConvertKit vs Ghost

## Summary

**One-sentence:** Produces a versioned decision record picking one newsletter platform from {Substack, Beehiiv, ConvertKit, Ghost} based on revenue model, list size projection, owned-audience priority, and tech tole...

**One-paragraph:** Indie hackers need a fast pick-one decision matrix between Substack / Beehiiv / ConvertKit / Ghost. Newsletter-growth methodology assumes you already chose. This produces a 1-page decision record: weighted criteria, scores per vendor, recommendation, migration cost note. Bounded inputs → contract-checked transformation → versioned output downstream agents or humans can consume without re-deriving the rationale.

**Ефективно для:** first-time newsletter authors, founders considering migration from a current platform, agencies advising a client between options.

## Applies If (ALL must hold)

- Author is about to start a newsletter OR considering migration
- Author can commit to one platform for ≥6 months
- Author has a revenue intent (sub, sponsorship, lead-magnet)
- Author can name list-size projection at 6 / 12 months

## Skip If (ANY kills it)

- Author already has 10k+ subscribers — switching cost dominates rubric output
- Author needs B2B sequenced automation — pick MailerLite/Customer.io not the four here
- Author is on a self-hosted stack and rejects all SaaS

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Revenue model intent | enum {sub, sponsorship, lead-magnet, hybrid} | founder |
| List size projection 12mo | integer | founder estimate |
| Owned-audience priority (1-5) | integer | founder ranking |
| Tech tolerance (1-5) | integer | founder ranking |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[content-marketing]]` | Newsletter cadence + tone conventions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale and source | ~900 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Score vendors against criteria | sonnet | Rubric application. |
| Compute migration cost | sonnet | Arithmetic from vendor pricing. |
| Recommend in ambiguous cases | opus | Multi-criterion trade-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md.tmpl` | Decision record skeleton: inputs, scorecard, recommendation, migration cost, signature. |
| `templates/scorecard.md.tmpl` | 4-criteria × 4-vendor scorecard. |
| `templates/_smoke-test.md` | Filled example for indie hacker shipping paid sub newsletter. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-substack-beehiiv-pick.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `free/marketing/`
- `[[content-marketing]]`
- `[[growth-marketing]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether substack-beehiiv-pick applies: root question — "Is owned-audience priority ≥4 on the 1-5 scale?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
