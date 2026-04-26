# Market Analysis

## Summary

Market analysis is the combined methodology for sizing a market (TAM/SAM/SOM), classifying trend timing, mapping the competitive landscape (15-20 named players with URLs), and producing a feature-gap matrix from the top 5 competitors. The core rule: run both top-down and bottom-up sizing; if they diverge more than 2x, flag it as a research gap rather than averaging. These four sub-methodologies share data sources and produce JSON-first outputs that feed downstream SDD artifacts.

## Why

Desk research without methodology produces TAM theatre (Gartner numbers inflated 3-10x), hallucinated competitors (invented product names), stale pricing (6-18 months behind live pages), and unfalsifiable trend-timing labels ("Early Majority" with no quantitative anchor). Separating the four passes into distinct subagent invocations keeps context windows small, enables JSON validation per pass, and makes the competitive matrix reproducible via competitor snapshots.

## When To Use

- Before writing a spec.md for a new product idea — produces SAM number and competitive whitespace
- When the GTM strategist or product manager needs a quantified opportunity ($X M SAM, Y% CAGR, Z named competitors)
- Quarterly competitor refresh: re-scrape pricing pages, changelogs, review sites for moves
- Pre-fundraise: investor decks need a defensible TAM and a feature matrix
- Niche viability scoring inside `niche-evaluation` flows — replaces guesses with sourced numbers

## When NOT To Use

- Single-customer custom builds with no market
- Pure technical or architecture research — route to `pro/dev/software-architect` instead
- Ideas fewer than 2 weeks from launch where research will not change the decision
- Highly regulated B2B niches (defense, medical devices) where public data is scarce — use primary expert interviews
- Working business where the decision is growth, not entry — switch to `growth-marketer` or `conversion-optimizer`

## Content

| File | What's inside |
|------|---------------|
| `content/01-sizing.xml` | TAM/SAM/SOM calculation methods, validation checks, and bottom-up enforcement rules |
| `content/02-trend-pass.xml` | Trend categories (macro/industry/micro), adoption curve, timing assessment, quantitative-anchor requirement |
| `content/03-competitor-discovery.xml` | Competitor types (direct/indirect/substitute/potential), mapping process, URL-evidence requirement, whitespace identification |
| `content/04-feature-matrix.xml` | Feature inventory across top 5 competitors, gap classification (table stakes/opportunity/validate), gap validation checklist |
| `content/05-antipatterns.xml` | Common mistakes and AI-agent gotchas: TAM theatre, hallucinated competitors, stale pricing, adoption-curve guessing |

## Templates

| File | Purpose |
|------|---------|
| `templates/market-sizing.md` | TAM/SAM/SOM sizing template with top-down and bottom-up sections |
| `templates/trend-analysis.md` | Trend analysis template with drivers, threats, and timing assessment |
| `templates/competitive-landscape.md` | Competitor landscape table with direct, indirect, and whitespace sections |
| `templates/feature-matrix.md` | Feature matrix and gap validation templates |
| `templates/competitors-snapshot.sh` | Bash script that freezes a competitor URL set into a dated snapshot folder via firecrawl |
