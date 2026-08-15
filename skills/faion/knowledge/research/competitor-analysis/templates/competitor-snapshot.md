<!--
purpose: Single-competitor snapshot template for parallel sub-tasks
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~200-1500 tokens when loaded as context
variables:
  - name: competitor_name
    type: string
    required: true
    description: The competitor as they name themselves. One per snapshot - a snapshot covering "the incumbents" cannot be updated when exactly one of them changes its pricing.
  - name: url
    type: string
    required: true
    description: The exact URL you actually read, not the homepage. Pricing lives on different paths per region and per currency; a reader has to be able to re-check the same page you did.
  - name: date
    type: string
    required: true
    description: The date you read those pages, ISO. Competitor pages change weekly and an undated snapshot gets quoted for a year as though it were still true.
  - name: primary_market
    type: string
    required: true
    description: The region or segment they actually serve, judged from their pricing currencies and case studies rather than from their claim to be global.
  - name: pricing_basis
    type: text
    required: true
    description: How you normalised their prices - "effective monthly, one user, billed monthly, tax excluded". Without a stated basis the table below compares numbers that were never comparable.
  - name: our_opportunity
    type: text
    required: true
    description: What specifically you could do better, tied to a weakness with a source. If you cannot point at a review or a missing capability, this section is wishful thinking with a heading.
-->
# {{competitor_name}} Snapshot

**Website:** {{url}}
**Fetched:** {{date}}
**Founded:** [Year or "unknown"]
**Employees:** [~X or "unknown"]
**Funding:** [$X (source: URL) or "unknown"]
**Primary market:** {{primary_market}}

## Product

**What it does:** [1 sentence]

**Core features:**
- [feature]
- [feature]

**Missing features (from reviews):**
- [feature — source: URL]

## Pricing

Basis for comparison: {{pricing_basis}}

| Tier | Effective price on that basis | Source |
|------|-------------------------------|--------|
| Free | $0 | [URL] |
| [Tier] | [$X] | [URL] |

**Footnotes found:** [annual lock-in? seat minimums? transaction fees?]

## Positioning

**Headline:** "[their headline]"
**Target audience:** [who]

## Strengths

1. [X — source: URL]
2. [X]

## Weaknesses

1. [X — source: review URL]
2. [X]

## Opportunity for Us

{{our_opportunity}}
