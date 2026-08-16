<!--

purpose: Full TAM/SAM/SOM report skeleton with triangulation
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~200-1500 tokens when loaded as context
-->


# Market Sizing Report: <market_name>

## Executive Summary
- **TAM:** [$X]
- **SAM:** [$X]
- **SOM (3-year):** [X customers × $X/year = $X ARR]
- **Confidence:** <confidence>
- **Methods used:** Top-down, Bottom-up, Competitor-based

## TAM Calculation (Top-Down)

**Market:** <market_name>
**Source for the global figure:** <source>
**Growth rate:** <x_cagr>

| Constraint | % of TAM | Value | Source |
|------------|----------|-------|--------|
| <segment_1> | [X%] | [$X] | [URL] |
| <segment_2> | [X%] | [$X] | [URL] |

**TAM = [$X]**

## SAM Calculation

| Constraint | % of TAM | Value |
|------------|----------|-------|
| Geography (<geography_constraint>) | [X%] | [$X] |
| Industry (<industry_constraint>) | [X%] | [$X] |
| Company size | [X%] | [$X] |

**SAM = TAM × <combined> = [$X]**

## SOM Calculation (Bottom-Up)

**Target customers:**
- Source: <census_eurostat_apollo> — [X] companies matching <firmographic_criteria>
- Estimated reachable: [X]

**Conversion funnel:**

<conversion_assumption>

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
| [Name] | Hard/Soft | <value> | [URL or "estimate"] |

## Sources

| Source | URL | Accessed | Type |
|--------|-----|----------|------|
| [Name] | [URL] | <date> | Primary/Secondary |
