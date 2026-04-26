# Research Workflows

## Summary

Three sequential research state machines orchestrated by faion-researcher: Idea
Discovery (context → ideas → user selection → pain research → niche evaluation → output),
Product Research (parse project → read SDD → module selection → sequential research →
executive-summary), and Project Naming (concept → generate candidates → user selection →
domain check → update constitution). Each runs agents one by one, writes intermediate
state to .aidocs/product_docs/, and checks for non-empty output before advancing.

## Why

Solopreneurs need an LLM to act as their entire research team in pre-spec phases.
Sequential execution is mandatory (not parallel) to avoid rate limits, ensure data
quality, and prevent cross-module contamination. The key failure mode is the agent
completing steps without writing the output files — the orchestrator must read the
file and verify non-empty before advancing.

## When To Use

- Pre-spec stage where market-research.md, competitive-analysis.md, or idea-validation.md are missing
- Solopreneur flow where an LLM acts as the entire research team
- Naming and domain validation before reserving a brand and writing constitution.md
- Refresh of stale research artifacts over 6 months old before a major roadmap revision

## When NOT To Use

- Inside an active SDD task — research belongs in backlog discovery, not execution
- When the team has signed enterprise market data contracts (Gartner, IDC, Statista paid) — feed those reports directly to faion-sdd instead
- Tactical decisions inside a 30-minute window — sequential execution makes this multi-minute work
- After spec freeze — findings contradicting signed-off spec must go through change management

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow-rules.xml` | Sequential execution rule, source citation rule, loop guard, state persistence |
| `content/02-workflow-specs.xml` | Idea Discovery, Product Research, Naming workflow step-by-step specs |

## Templates

none

## Scripts

| File | Purpose |
|------|---------|
| `scripts/check-names.sh` | Domain and handle availability batch check (whois + HTTP HEAD) |
