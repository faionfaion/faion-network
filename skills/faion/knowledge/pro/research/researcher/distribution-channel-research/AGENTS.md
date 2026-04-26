# Distribution Channel Research

## Summary

A 5-step process for identifying and prioritizing customer acquisition channels: map customer discovery sources, score channels on a weighted fit matrix (audience/cost/time/scale/capability), model economics per channel (LTV:CAC > 3:1 as Phase-2 gate), design micro-tests ($100-500, 4-6 weeks, pre-registered kill criteria), and build a phased channel mix (1 channel first, expand after $10K MRR).

## Why

"If you build it, they will come" is a myth. Entrepreneurs pick channels based on personal preference rather than customer behavior data, or try all channels at once and master none. The fit matrix and economics model force citation of every benchmark number and predefine kill criteria before money is spent — preventing sunk-cost continuation and channel concentration risk.

## When To Use

- Pre-launch GTM planning: product hypothesis exists but no validated path to first 100 users.
- Post-launch when primary channel CAC is climbing and adjacent channels must be researched.
- B2B/B2C pivots where the buyer or buying motion changes (PLG → sales-led or vice versa).
- Solopreneur projects where bandwidth requires mastering 1 channel, not dabbling in 5.
- Periodic audit (every 2 quarters) of the active channel mix against actual customer-source data.

## When NOT To Use

- Pre-PMF — channels do not fix a broken product; tests produce misleading CAC.
- Products with strong existing organic pull (60%+ direct traffic) — formal research adds no signal.
- One-off campaigns (event launch, single press hit) where the question is creative, not channel.
- When customer interviews and attribution analytics do not exist and cannot be collected — any output is conjecture.

## Content

| File | What's inside |
|------|---------------|
| `content/01-channel-categories.xml` | Four channel categories (organic/paid/sales-led/viral), tables with timeline/cost/best-for, channel-mix portfolio by MRR stage. |
| `content/02-research-process.xml` | Steps 1-5: customer discovery map, fit matrix scoring, economics model, test framework, portfolio approach. |
| `content/03-agentic-pipeline.xml` | Subagent chain, prompt pattern, tools table, services table, best practices, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/channel-fit-scorer.py` | Scores channels from YAML input against weighted matrix, emits ranked markdown table. |
| `templates/channels.yaml` | Example input for channel-fit-scorer with three channels pre-scored. |
| `templates/channel-report.md` | Channel Research Report: discovery insights, evaluation table, economics, competitor analysis, test plan. |

## Scripts

none
