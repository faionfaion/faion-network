# AI Research Tool Categories

## Summary

A phase-and-budget decision map for selecting research tools across seven categories: exploration, competitor intel, user interviews, survey analysis, sentiment, synthesis, and synthetic research. Agents use this map as a decision tree; given phase and budget, they output a stack recommendation with API availability flags.

## Why

The AI research tool market is dense and changes rapidly. Picking the wrong tool mid-sprint is expensive to reverse; tool sprawl beyond 3 tools per sprint creates coordination overhead that exceeds analytical benefit. A structured map with budget tiers and API-availability signals prevents both failure modes.

## When To Use

- Planning a research stack at the start of a new project or research sprint.
- Selecting tools for a specific research phase (discovery → synthesis → validation).
- Budget-scoping a research operation (free vs. mid vs. enterprise).
- Choosing the right tool per research question type before committing to a SaaS contract.

## When NOT To Use

- As a substitute for evaluating data privacy requirements — always check data processing agreements.
- When the question is fully addressable with a single tool already in use — avoid tool sprawl.
- For purely qualitative synthesis where Claude alone suffices — no additional tooling needed.

## Content

| File | What's inside |
|------|---------------|
| `content/01-category-map.xml` | Seven categories with tools per phase and budget tier. |
| `content/02-agent-workflow.xml` | Decision-tree workflow, prompt patterns, API-friendly tool matrix, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-selector.py` | Python: phase + budget → filtered tool list from the category map. |
| `templates/stack-prompt.txt` | Prompt for stack recommendation with API-availability and watch-out fields. |
