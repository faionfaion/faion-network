# Idea Generation

## Summary

A methodology for systematically generating viable business ideas using 7 frameworks: Skills Inventory, Pain Point Mining, Job Substitution, Productized Service, Unbundling, Market Stacking, and Your Own Problems. The rule: run all 7 frameworks, generate at least 20 candidates, then score each on Market Size, Personal Fit, Competition, Monetization, and Speed to MVP before selecting anything to validate.

## Why

Waiting for inspiration produces nothing. Running only one framework locks the founder into a single idea class (e.g., only Reddit pain points). The scoring matrix prevents personal excitement from overriding weak fundamentals, and generating 20+ candidates before scoring provides enough comparison points for the matrix to produce signal.

## When To Use

- Solopreneur in blank-page mode: skills inventory exists, no idea selected yet.
- Quarterly idea-refresh sprint: generate 20+ candidates, score, pick 1-2 to validate.
- Combining a known skill with current pain-point data to surface SaaS angles.
- Repurposing a portfolio of past services into productized offerings (Framework 4).

## When NOT To Use

- You already have a validated idea and paying users — switch to roadmap and feature discovery.
- Market sizing or financial projections are needed — this methodology is generation, not evaluation.
- Highly technical R&D (deep tech, hardware) where pain-mining and Upwork gig analysis don't apply.
- Burnout or decision-fatigue state — adding more options makes the situation worse.

## Content

| File | What's inside |
|------|---------------|
| `content/01-frameworks.xml` | All 7 idea generation frameworks with templates and worked examples. |
| `content/02-scoring-and-mistakes.xml` | Idea scoring matrix (5 criteria, weighted), scoring guide, common mistakes, and antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/idea-discovery-session.md` | Session template: frameworks used, per-idea fields, top-3 to validate, next steps. |
| `templates/weekly-idea-capture.md` | Weekly log: problems encountered, online complaints seen, Upwork gigs noted. |
| `templates/idea-scorer.py` | Python script: reads JSON list of ideas with scores, computes weighted total, outputs top-10. |
