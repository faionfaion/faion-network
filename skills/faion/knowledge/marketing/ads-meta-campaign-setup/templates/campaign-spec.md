<!--
purpose: Meta campaign launch spec Markdown skeleton.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-1200 tokens when loaded as context
variables:
  - name: campaign_name
    type: string
    required: true
    description: Campaign name following the naming convention below. It is the only thing that makes a report readable three months later, so build it from the convention rather than describing the idea.
  - name: objective
    type: enum
    required: true
    options: [awareness, traffic, engagement, leads, app_promotion, sales]
    description: The optimisation objective. Meta optimises for exactly what you pick - choosing traffic when you want purchases buys you clicks from people who never buy, and the numbers will look fine.
  - name: budget_model
    type: enum
    required: true
    options: [abo, cbo]
    description: Budget at ad-set level (abo) or campaign level (cbo). cbo only once you clear roughly 50 conversions per week; below that it starves the ad set that needed the data.
  - name: conversion_event
    type: string
    required: true
    description: The pixel event that counts as success - Purchase, Lead, CompleteRegistration. It must already be firing and verified before launch; an unfired event trains the algorithm on nothing.
  - name: daily_budget
    type: string
    required: true
    description: Daily spend per ad set, with currency. Learning phase needs roughly 50 conversions in 7 days - if your budget divided by your CPA does not reach that, the structure is wrong, not the creative.
  - name: primary_audience
    type: text
    required: true
    description: Who the first ad set targets and where the list came from - matched customer file, 1% lookalike of purchasers, interest stack. Name the source; "our audience" cannot be rebuilt after it breaks.
-->

# Meta Campaign Spec: {{campaign_name}}

## Objective
{{objective}}

## Budget model
{{budget_model}} — rationale: 50+ conversions per week is the threshold for cbo

## Ad sets (≤5)

| # | Name | Audience | Daily $ | Placement | Notes |
|---|------|----------|---------|-----------|-------|
| 1 | {{campaign_name}} | {{primary_audience}} | {{daily_budget}} | advantage_plus | |

## Conversion event
{{conversion_event}}

## Naming convention
[stage]_[product]_[audience]_[creative]_[yyyymmdd]

## Learning phase plan
- Target: 50 conv/wk per ad set within 14 days
- Hold structure for 7 days minimum
- Pause + diagnose at day 14 if still in learning
