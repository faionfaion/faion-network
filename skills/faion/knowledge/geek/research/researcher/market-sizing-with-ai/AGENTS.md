# Market Sizing with AI

## Summary

AI-assisted TAM/SAM/SOM estimation using top-down and bottom-up triangulation, with explicit assumption documentation and confidence ratings per data point. Both paths must run independently; result is accepted only when they are within 2-3x of each other.

## Why

Finger-in-the-air market estimates lack credibility and cannot be stress-tested. Triangulation with two independent models raises confidence; requiring citations and confidence ratings forces honest calibration and surfaces data staleness before estimates are presented externally.

## When To Use

- Early-stage TAM/SAM/SOM validation before an investor deck or strategic decision.
- Triangulating conflicting market estimates from multiple sources.
- Generating a bottom-up model from known unit economics (ICP count, ACV, churn).
- Stress-testing existing market assumptions when entering a new segment.

## When NOT To Use

- Sole input for a fundraising pitch without primary source validation — LLMs hallucinate market figures.
- Nascent markets (under 3 years old) with no industry reports — AI-synthesized data lacks grounding.
- When regulatory or geographic precision is critical (e.g., healthcare TAM per country) — estimates too coarse.
- High-stakes M&A diligence — hire a research analyst; speed does not justify precision loss.

## Content

| File | What's inside |
|------|---------------|
| `content/01-triangulation.xml` | Top-down and bottom-up method rules, tool landscape, confidence rating system. |
| `content/02-agent-workflow.xml` | Haiku/Sonnet/Opus pipeline, prompt patterns, gotchas, best practices. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bottom-up-calc.py` | Python function: ICP count × adoption × ACV → TAM with 3-yr projection. |
| `templates/sizing-prompt.txt` | Three-step TAM/SAM/SOM prompt with triangulation and confidence output. |
