# AI Research Tools (geek/market-researcher)

## Summary

A two-layer agent structure for AI-driven market research pipelines: an orchestrator
(Sonnet) selects the right tool for each research stage based on task type and
available credentials, then dispatches sub-queries to stage-specific tools. The
orchestrator merges outputs, flags gaps where no tool produced coverage, and signals
a human checkpoint before synthesis. Each stage gets exactly one primary tool.

## Why

No single AI tool covers all market research stages. Assigning the same tool to
multiple stages hides coverage gaps and produces biased, citation-poor results.
Agents default to Claude or ChatGPT for all stages when not given explicit tool
assignments. Tool outputs also have different schemas (Perplexity returns citation
URLs; SerpAPI returns structured JSON; Google Trends returns DataFrames); the
orchestrator must normalize before merging.

## When To Use

- Building or auditing the tool stack for a market research pipeline
- Deciding which AI tool handles which stage of a multi-step project
- Replacing manual research workflows with agent-driven equivalents
- Onboarding a new agent to an existing research pipeline

## When NOT To Use

- When a single tool already covers the full research scope
- Proprietary or regulated research contexts requiring auditable, non-AI sources
- When the research team lacks API credentials for candidate tools
- One-off ad hoc queries where tool overhead exceeds research value

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline-rules.xml` | Two-layer orchestrator rules, stage assignment, normalization requirement |
| `content/02-tool-reference.xml` | CLI/SaaS table, prompt pattern, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/stage-dispatcher.py` | Orchestrator that selects tool per stage and generates stage queries |
| `templates/research-pipeline-prompt.txt` | XML prompt for multi-stage research pipeline |
