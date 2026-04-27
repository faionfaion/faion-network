# AI Persona Building (Lightweight)

## Summary

Lightweight single-pass persona generation: a Sonnet subagent receives a structured description of a user type with known data points and a JTBD statement, and produces a persona card. A Haiku subagent formats the card into the team's documentation template. No clustering step — suitable for early exploration or updating a single field, not for full segmentation.

## Why

Teams in early prototyping need placeholder personas to unblock design decisions before real cluster data arrives. This thin pipeline produces a usable card quickly, provided the human supplies at least 3 concrete data points and forces the agent to mark all inferred fields explicitly.

## When To Use

- Lightweight persona creation needed quickly without a dedicated researcher
- Prototyping phase where placeholder personas unblock design decisions
- Updating a single persona field across an existing library
- Generating documentation from an already-agreed behavioral cluster description
- Supplementing thin data with AI-expanded hypotheses for rapid validation planning

## When NOT To Use

- No real user data exists and the team plans to treat AI output as ground truth
- Regulated domains (healthcare, finance) where persona inaccuracy causes downstream harm
- Personas will drive hiring, pricing, or go-to-market budget without human review
- Full clustering from multi-source data is needed — use `ai-assisted-persona-building` instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-lightweight-process.xml` | Single-pass workflow; JTBD integration; required input fields; validation checkpoint |
| `content/02-anti-patterns.xml` | Gotchas: stereotypes from thin input, multi-goal personas, LLM conflating persona with user story |

## Templates

| File | Purpose |
|------|---------|
| `templates/build-persona.py` | Claude API call: user_type + data_points + jtbd → persona card Markdown |
| `templates/prompt-persona-card.txt` | Sonnet prompt enforcing data-only output with [INFERRED] tagging |
| `templates/prompt-format-card.txt` | Haiku formatting prompt: content → team template structure (no changes to content) |
