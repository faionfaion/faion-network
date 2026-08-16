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
| `templates/substack-to-product-funnel.md.j2` | Markdown skeleton with the required fields. |
| `templates/substack-to-product-funnel.md` | Markdown skeleton with the required fields. Generated from `templates/substack-to-product-funnel.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-substack-to-product-funnel.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[twitter-x-monetization-thread-to-product]] — adjacent solo funnel.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/substack-to-product-funnel.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/substack-to-product-funnel.json",
  "title": "Substack-to-Product Funnel Output Contract",
  "type": "object",
  "required": [
    "operator",
    "publication_url",
    "paid_tier",
    "recommendation_partners",
    "cross_post_cadence",
    "welcome_sequence",
    "hard_product_url",
    "hard_product_cta_text",
    "kpi_set",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "operator": {
      "type": "string",
      "description": "named publication owner"
    },
    "publication_url": {
      "type": "string",
      "description": "Substack URL"
    },
    "paid_tier": {
      "type": "object",
      "description": "{name, monthly_price, annual_price, concrete_benefit}"
    },
    "recommendation_partners": {
      "type": "array",
      "description": "\u22653 publications with URL + agreement_at",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "cross_post_cadence": {
      "type": "object",
      "description": "{per_month, partner_rotation}"
    },
    "welcome_sequence": {
      "type": "array",
      "description": "5 emails; email 4 carries the hard-product CTA",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "hard_product_url": {
      "type": "string",
      "description": "URL"
    },
    "hard_product_cta_text": {
      "type": "string",
      "description": "\u2264140 chars"
    },
    "kpi_set": {
      "type": "object",
      "description": "{free_subs, paid_subs, hard_product_conversions, recommendation_inflow}"
    },
    "version": {
      "type": "string",
      "description": "semver"
    },
    "last_reviewed": {
      "type": "string",
      "description": "ISO date",
      "format": "date"
    }
  },
  "additionalProperties": true
}
```

### `templates/_smoke-test.json`

```json
{
  "operator": "sample-operator",
  "publication_url": "sample-publication_url",
  "paid_tier": {
    "key": "value"
  },
  "recommendation_partners": [
    {
      "key": "value"
    }
  ],
  "cross_post_cadence": {
    "key": "value"
  },
  "welcome_sequence": [
    {
      "key": "value"
    }
  ],
  "hard_product_url": "sample-hard_product_url",
  "hard_product_cta_text": "sample-hard_product_cta_text",
  "kpi_set": {
    "key": "value"
  },
  "version": "sample-version",
  "last_reviewed": "2026-05-23"
}
```
