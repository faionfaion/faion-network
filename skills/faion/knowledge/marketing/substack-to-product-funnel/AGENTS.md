# Substack-to-Product Funnel

## Summary

**One-sentence:** Produces a Substack-to-product funnel spec (paid tier as soft-product, recommendation network, cross-posts, hard-product CTA) that newsletter-growth doesn't cover.

**Ефективно для:** Solo authors on Substack who treat the paid tier as a tip jar and miss the recommendation-network + cross-post mechanics that compound to a hard product.

**One-paragraph:** Substack-specific monetization mechanics — paid tier as a soft-product, recommendation network swaps, cross-posts with peers, deferred hard-product CTAs — are a distinct discipline newsletter-growth doesn't cover. This methodology produces a per-publication spec naming the soft-product (paid tier benefit), the recommendation partners, the cross-post cadence, and the hard-product CTA wired into post #4 of the welcome sequence. Output is consumed by the Substack admin + email-funnel builder.

## Applies If (ALL must hold)

- Newsletter is hosted on Substack (not Beehiiv / Ghost / ConvertKit).
- ≥500 free subscribers exist or a credible 8-week path to 500.
- A hard product (paid SaaS / book / course) exists or is on roadmap.
- Operator can ship a paid tier with a real benefit (not just gratitude).

## Skip If (ANY kills it)

- Hosted off Substack — recommendation network unavailable.
- <500 subs AND no credible growth path — funnel needs a base.
- Operator unwilling to sell — paid tier without product won't compound.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Substack pub URL + admin access | URL | operator |
| paid tier benefit definition (≥1 concrete delivery) | string | founder decision |
| ≥3 recommendation partners agreed | list of pub URLs | outreach |
| hard product URL + pricing | URL + price | founder decision |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/newsletter-growth` | Adjacent newsletter discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~700 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_paid_tier_benefit_copy` | sonnet | Soft-product positioning. |
| `plan_recommendation_swaps` | sonnet | Per-instance outreach choreography. |
| `audit_funnel_for_hard_cta` | opus | End-to-end funnel review for leaks. |

## Templates

| File | Purpose |
|---|---|
| `templates/substack-to-product-funnel.json` | JSON Schema for the output contract. |
| `templates/substack-to-product-funnel.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-substack-to-product-funnel.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[twitter-x-monetization-thread-to-product]] — adjacent solo funnel.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
