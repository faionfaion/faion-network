# Pain Point Research

## Summary

Systematic 5-step process for discovering and prioritizing user pain points: define scope, mine four source tiers (complaints, questions, forums, job boards), categorize by type, score with the Pain Intensity Matrix (frequency × severity × reach × spend × alternatives), then extract root causes via 5 Whys. Output is a ranked pain log, not a list of assumptions.

## Why

Finding pain points without a source strategy produces confirmation bias — researchers look where they expect to find what they already believe. The tiered source model forces triangulation across direct complaints (highest signal) through job boards (revealed willingness to pay). The weighted scoring formula surfaces which pains are frequent enough and severe enough to be worth solving, before any solution work begins.

## When To Use

- Early-stage discovery when no validated problem yet exists
- Competitor gap analysis: mining negative reviews to find underserved pain
- Content marketing: identifying questions your audience actively asks
- Prioritizing a backlog of improvement ideas by actual user pain vs. assumptions
- Researching a new market niche before committing to build

## When NOT To Use

- After product-market fit: qualitative pain mining is less useful than quantitative retention analysis
- When a decision needs statistical confidence: pain mining is directional, not significant
- Replacing direct user interviews: forum complaints lack context and nuance
- When the audience is too specialized with no public online presence (e.g., internal enterprise users)

## Content

| File | What's inside |
|------|---------------|
| `content/01-discovery-process.xml` | 5-step framework: scope, source tiers, categories, scoring formula, 5 Whys |
| `content/02-examples-and-antipatterns.xml` | Real examples (email marketers, course creators), common mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/pain-log.md` | Structured log with per-pain scoring fields and summary table |
| `templates/reddit-mining.md` | Reddit mining report template (posts, quotes, patterns) |
| `templates/prompt-collect.txt` | LLM prompt to collect and tabulate pain signals from specified sources |
| `templates/prompt-score.txt` | LLM prompt to apply Pain Intensity Matrix to a raw pain list |
| `templates/reddit-collector.py` | PRAW script to collect top posts matching pain keywords from a subreddit |
