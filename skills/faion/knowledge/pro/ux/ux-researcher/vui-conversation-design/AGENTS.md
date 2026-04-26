# VUI Conversation Design

## Summary

VUI conversation design structures intent-based dialog flows for voice interfaces: defining intents, slots, prompt classes (open, directed, option, confirmation), happy paths, and all repair branches (no-match, no-input, max-retry, escape-to-human). The method applies to Alexa Skills, Google Actions, IVR systems, and in-app voice features that use a defined intent+entity NLU model.

## Why

Voice UI removes visual affordances — the user cannot scan options or re-read instructions. Every dialog node must handle failure gracefully or the conversation terminates in frustration. Designing repair branches first (before happy path) forces honest coverage and surfaces ambiguity while cost is low. Confirmation strategy (implicit vs explicit) and retry-cap discipline are the two decisions that most visibly affect real-world satisfaction.

## When To Use

- Authoring intent-based dialog flows with defined intents and slots.
- Writing prompt copy in all four classes (open, directed, option, confirmation) and tagging for analytics.
- Migrating a chatbot script to voice where brevity, prosody, and turn-taking change the requirements.
- Adding repair coverage (no-match, no-input, escalation) to an existing dialog graph.

## When NOT To Use

- LLM-only freestyle conversation without pre-defined intents — that needs RAG-driven or agentic dialog methodology.
- Pure GUI form-filling — no turn-taking benefit from VUI design patterns.
- Asynchronous chat (email, ticketing) where real-time constraint is absent.
- One-shot commands with no follow-up (smart-home toggle) — dialog flow is degenerate.

## Content

| File | What's inside |
|------|---------------|
| `content/01-dialog-components.xml` | Conversation components (wake word, intent, entity, prompt, confirmation, error handling), prompt class rules, dialog flow patterns. |
| `content/02-repair-design.xml` | No-match, no-input, max-retry, escape-to-human rules; confirmation strategy; retry variation requirements. |
| `content/03-antipatterns.xml` | Common VUI design failures and agent-specific gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dialog-flow.json` | Skeleton dialog graph node structure with required transition fields. |
| `templates/prompt-palette.txt` | Prompt-class palette: 3-5 variant slots per node, tagged for analytics. |
| `templates/repair-check.ts` | TypeScript linter: flags nodes missing no-match, no-input, or max-retry transitions. |
