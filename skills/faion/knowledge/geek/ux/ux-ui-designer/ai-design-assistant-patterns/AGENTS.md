# AI Design Assistant Patterns

## Summary

Methodology for selecting and specifying AI assistant interaction patterns within design tools: sidebar (persistent, long tasks), modal (single-shot high-stakes generation), and inline (micro-suggestions on selection). Covers trigger conditions, response formats, fallback states, human confirmation requirements, and anti-patterns that erode trust.

## Why

AI assistants in design tools fail not because of model quality but because of mismatched interaction patterns. Sidebar assistants on small screens cause context switch fatigue; modals break flow when canvas reference is needed; inline suggestions trigger too eagerly and reduce trust. Matching the pattern to task duration, output type, and disruption tolerance is the concrete design decision this methodology makes.

## When To Use

- Defining how an AI assistant should surface inside a design tool for a product feature
- Auditing an existing AI assistant UX for interaction pattern anti-patterns
- Generating design specifications for contextual, generative, or review-type AI assistants
- Selecting which assistant pattern (sidebar / modal / inline) fits a given task complexity

## When NOT To Use

- When the AI capability itself is undefined — choose capability first, then interaction pattern
- Fully automated pipelines where no human interaction is expected during the AI task
- Mobile-first interfaces with minimal screen real estate where persistent sidebar degrades UX
- Purely mechanical tasks needing no conversational affordance (batch export, resize)

## Content

| File | What's inside |
|------|---------------|
| `content/01-pattern-selection.xml` | Three pattern types, selection criteria table, trigger rules, anti-patterns |
| `content/02-spec-and-gotchas.xml` | Spec fields, error/fallback states, copy review rules, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-decision-matrix.md` | Scored matrix for sidebar vs modal vs inline selection |
| `templates/pattern-spec.md` | Per-feature AI assistant spec template |
| `templates/prompt-assistant-spec.txt` | Prompt for generating a full interaction pattern spec |
