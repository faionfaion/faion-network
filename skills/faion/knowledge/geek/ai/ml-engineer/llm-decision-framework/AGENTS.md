# LLM Decision Framework

## Summary

A systematic framework for choosing the right LLM enhancement strategy — prompt engineering, RAG, fine-tuning, or RAFT (hybrid) — based on data freshness, accuracy requirements, budget, latency, and team constraints. Always score prompting first before investing in retrieval or training infrastructure.

## Why

Without a structured decision process, teams default to RAG or fine-tuning prematurely and waste infrastructure budget. The framework enforces the correct evaluation order: prompting (free, immediate) → RAG (medium investment) → fine-tuning (high investment) → RAFT (highest investment). It also provides a scoreable decision matrix that an agent can apply programmatically to produce a structured recommendation with rationale.

## When To Use

- At the start of any AI feature design: choose the right architecture before writing code
- Evaluating whether to augment an existing LLM feature
- During cost optimization: deciding whether a fine-tuned cheaper model can replace an expensive general model
- When accuracy is inadequate: diagnosing if the root cause is knowledge, style, or reasoning
- Business justification for AI budget: quantify cost/benefit before committing

## When NOT To Use

- Prototype needed in under a day — default to prompt engineering, evaluate later
- Decision already made by stakeholders — use the framework to document trade-offs, not re-litigate
- Task is purely generative (creative writing) — retrieval and fine-tuning do not apply
- No eval data exists — the framework requires measurable accuracy targets; skip until measurable

## Content

| File | What's inside |
|------|---------------|
| `content/01-decision-matrix.xml` | Decision hierarchy (prompt → structured output → RAG → fine-tuning → RAFT), cost matrix, key metrics |
| `content/02-checklist.xml` | Phase-by-phase checklist: requirements, constraints, approach selection, implementation, validation |
| `content/03-examples.xml` | Six real-world decision examples with architecture, cost estimates, and rationale |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-matrix.py` | Scoring function that outputs recommendation given FeatureRequirements dataclass |
| `templates/adr.md` | Architecture Decision Record template for documenting LLM enhancement choice |
| `templates/prompt-requirements.txt` | Prompt for LLM-assisted requirements extraction and approach recommendation |
