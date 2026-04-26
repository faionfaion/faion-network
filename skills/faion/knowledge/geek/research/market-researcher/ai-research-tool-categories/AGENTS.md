# AI Research Tool Categories

## Summary

A phase-to-tool classification for AI research pipelines: map each research task to
its phase (exploration, competitor intel, interview analysis, survey, sentiment,
synthesis, synthetic research), then select the appropriate tool from the approved
category map. Lock tool selection per project at planning time, not per query.

## Why

Tool categories shift quickly and "agent-friendly" vendor claims diverge from actual
API reliability. Having an explicit category map prevents agents from defaulting to
Claude/ChatGPT for all stages — which produces citation-poor results for competitive
and market data stages. A Haiku agent handles classification; a Sonnet agent handles
comparison of candidate tools against agent-friendliness, cost, and coverage.

## When To Use

- Selecting the right research tool before starting a multi-stage project
- Building a reusable tool-selection decision tree for recurring research workflows
- Auditing an existing research stack against coverage gaps by phase
- Onboarding a new agent to a research pipeline by mapping tasks to approved tools

## When NOT To Use

- When you already know the tool for the job — skip categorization overhead
- When the research budget is fixed and only one or two tools are available
- During execution of an already-designed pipeline — this methodology is for planning, not running
- When tool categories are stable and budget is locked — most valuable at procurement / pipeline design time

## Content

| File | What's inside |
|------|---------------|
| `content/01-category-map.xml` | Phase-to-tool map, budget tiers, rules for lock-in and API testing |
| `content/02-agentic-patterns.xml` | Prompt templates, CLI/SaaS table, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-recommender.py` | Haiku-based phase mapper: task description → recommended tool set |
| `templates/tool-selection-prompt.txt` | XML prompt for tool selection and comparison tasks |
