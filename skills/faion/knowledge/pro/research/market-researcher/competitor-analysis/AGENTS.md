# Competitor Analysis

## Summary

Competitor analysis is the systematic study of businesses competing for the same customers, structured as a SWOT-grid + market-share estimation + portfolio scorecard workflow. The market-researcher variant produces defensible board-ready artifacts — share in 5% buckets, per-SWOT-cell citation URLs, strategic-group maps with pre-committed axes — rather than feature-level positioning advice.

## Why

Without a structured framework, teams either ignore competitors or obsess over them without evidence. SWOT cells fabricated from brand familiarity rather than sourced observations lead to false confidence in competitive position. Forcing one citation URL per SWOT cell, rounding share to 5% buckets, and running a devil's-advocate pass eliminates the most common failure modes and produces artifacts that hold up in investor due diligence.

## When To Use

- Annual strategy review: scoring 8-15 named competitors on a SWOT grid as input to a board or strategy deck.
- Market-share estimation: producing defensible "X holds ~N% of category Y" claims from public proxies.
- Portfolio benchmarking: comparing a product line against 3-7 incumbents on a fixed quarterly scorecard.
- M&A or partnership shortlist: ranking acquisition targets by SWOT fit and relative strategic-group position.
- Investor due diligence: evidence-backed competitor matrix for a Series A/B deck.
- Win-loss debrief input: cross-referencing lost deals with competitor SWOT.

## When NOT To Use

- Single-feature spec or pricing-page rewrite — use the researcher variant; SWOT/share is overkill.
- Pre-MVP idea triage with no named competitors — use idea-generation-methods or niche-evaluation first.
- Real-time competitive monitoring — SWOT is a snapshot; use Klue/Crayon for live tracking.
- Regulated/enterprise-only categories where market share is locked behind Gartner/IDC reports — agents will fabricate share numbers; buy the report.
- Hyperlocal markets (single city, single B2B niche under 50 buyers) — public proxies do not exist.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Five-step framework: identify (direct/indirect/future), map landscape, analyze dimensions, find gaps, define differentiation |
| `content/02-swot-and-share.xml` | SWOT rules (one citation per cell), share-estimation rules (5% buckets, proxy triangulation), devil's-advocate pass, portfolio scorecard |
| `content/03-examples-and-antipatterns.xml` | Note-taking app and email marketing examples, common mistakes, AI-agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/competitor-report.md` | Full competitor analysis report: market overview, competitor map, detailed analysis, positioning matrix, gap analysis, differentiation, monitoring plan |
| `templates/competitor-snapshot.md` | Quick one-page competitor snapshot with strengths, weaknesses, opportunity |
| `templates/market-share-proxy.sh` | Bash script assembling SimilarWeb + Crunchbase + GitHub share-estimation proxies into a quarterly CSV |
