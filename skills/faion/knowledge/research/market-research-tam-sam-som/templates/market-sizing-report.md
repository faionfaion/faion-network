<!--
purpose: Full TAM/SAM/SOM report skeleton with triangulation
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~200-1500 tokens when loaded as context
variables:
  - name: market_name
    type: string
    required: true
    description: The market or niche being sized, narrow enough to argue about. "Project management software" is a category, not a market - the constraints below only mean something against a real one.
  - name: source
    type: text
    required: true
    description: Where the global figure comes from - publisher, report title, date and URL. Analyst numbers vary by multiples and are frequently circular; an unsourced TAM is a number somebody made up first.
  - name: geography_constraint
    type: string
    required: true
    description: The geography you can actually sell into and support, with the reason. Language, payment rails and support hours are constraints; "global" is what people write when they have not checked.
  - name: industry_constraint
    type: string
    required: true
    description: The industry or segment filter applied to reach SAM. Say what it excludes, not just what it includes - the exclusion is the part a reader can check against your product.
  - name: conversion_assumption
    type: text
    required: true
    description: The funnel assumptions behind SOM - visitors, signup rate, paid rate - and where each came from. This is the softest input in the document and the one that moves the answer most.
  - name: confidence
    type: enum
    required: true
    options: [high, medium, low]
    description: Your honest confidence in the SOM figure. If the three methods below disagree by more than about 3x, it is not high, however good the sources for each of them looked.
-->
# Market Sizing Report: {{market_name}}

## Executive Summary
- **TAM:** [$X]
- **SAM:** [$X]
- **SOM (3-year):** [X customers × $X/year = $X ARR]
- **Confidence:** {{confidence}}
- **Methods used:** Top-down, Bottom-up, Competitor-based

## TAM Calculation (Top-Down)

**Market:** {{market_name}}
**Source for the global figure:** {{source}}
**Growth rate:** [X% CAGR]

| Constraint | % of TAM | Value | Source |
|------------|----------|-------|--------|
| [Segment 1] | [X%] | [$X] | [URL] |
| [Segment 2] | [X%] | [$X] | [URL] |

**TAM = [$X]**

## SAM Calculation

| Constraint | % of TAM | Value |
|------------|----------|-------|
| Geography ({{geography_constraint}}) | [X%] | [$X] |
| Industry ({{industry_constraint}}) | [X%] | [$X] |
| Company size | [X%] | [$X] |

**SAM = TAM × [combined %] = [$X]**

## SOM Calculation (Bottom-Up)

**Target customers:**
- Source: [Census/Eurostat/Apollo] — [X] companies matching [firmographic criteria]
- Estimated reachable: [X]

**Conversion funnel:**

{{conversion_assumption}}

**SOM = [X customers × $X/year = $X ARR]**

## Triangulation

| Method | TAM | SAM | SOM | Confidence |
|--------|-----|-----|-----|------------|
| Top-down | [$X] | [$X] | [$X] | H/M/L |
| Bottom-up | [$X] | [$X] | [$X] | H/M/L |
| Competitor-based | [$X] | [$X] | [$X] | H/M/L |

**Spread:** [X]× — [OK / FLAG: investigate gap driver]

## Assumptions Ledger

| Assumption | Type | Value | Source |
|------------|------|-------|--------|
| [Name] | Hard/Soft | [value] | [URL or "estimate"] |

## Sources

| Source | URL | Accessed | Type |
|--------|-----|----------|------|
| [Name] | [URL] | [date] | Primary/Secondary |
