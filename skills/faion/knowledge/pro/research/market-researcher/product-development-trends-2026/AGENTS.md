# Product Development Trends 2026 (Quarterly Pulse)

## Summary

A recurring observability job — not a one-shot research deliverable — that keeps the four product-development trend buckets (AI-augmented ideation, continuous customer feedback, rapid pivots, cross-functional teams) grounded in dated primary sources. Each quarter a market-researcher subagent pulls signals from Stack Overflow Survey, GitHub Octoverse, ThoughtWorks Radar, State of DevOps, and Gartner, scores each bucket on a state × confidence rubric, and writes a dated snapshot that feeds roadmap and GTM positioning.

## Why

The four trend bullets are 2024-vintage consultancy talking points that age fast without re-verification. LLM training data lags real markets by 6-18 months, so any agent asked "is X still a trend?" answers yes by default. A scored snapshot with state ∈ {accepted/contested/declining/emerging}, confidence ∈ [0,1], and ≥2 dated primary sources per bucket makes the trend claims falsifiable rather than vibes.

## When To Use

- Quarterly refresh of roadmap macro-assumptions — re-validate that the chosen process is still the 2026 norm.
- Onboarding a new founder/PM agent into the faion-net stack as orientation on expected delivery style.
- GTM/positioning copy review — checking that messaging references current trends, not 2022 talking points.
- As input to idea-generation-methods or business-model-planning when justifying which delivery model the niche assumes.
- Pulse-check before kicking off a large feature: confirm the team's loop matches "AI-augmented ideation → continuous feedback → rapid pivot".

## When NOT To Use

- Concrete competitor study — use competitor-analysis or competitive-intelligence.
- Sizing the market — use market-research-tam-sam-som.
- Picking a methodology to actually run a feature — use pm-agile, sdd, or continuous-discovery.
- Generating a product roadmap — this is an input, not a producer; route output into product-manager.
- Regulated/compliance-heavy products (medical, finance) where waterfall + traceability is a feature.
- Hardware, B2G, or fixed-scope contracted work — "rapid pivots" is hostile to those contracts.

## Content

| File | What's inside |
|------|---------------|
| `content/01-trend-buckets.xml` | Four trend buckets with state/confidence rubric, snapshot schema, quarterly diff-to-ticket workflow |
| `content/02-rules-and-gotchas.xml` | Source-freshness rules, survivorship in "days not weeks" claim, greenwashing guard, duplicate-doc confusion, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/trend-snapshot.json` | JSON snapshot schema: 4 buckets with state, confidence, sources (≥2, dated), delta_vs_last |
| `templates/trend-snapshot-validate.sh` | Validates snapshot JSON: 4 buckets, valid state, confidence range, ≥2 sources, no stale sources (>365d) |
