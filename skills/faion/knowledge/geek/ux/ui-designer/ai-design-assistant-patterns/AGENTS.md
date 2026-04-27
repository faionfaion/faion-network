# AI Design Assistant Patterns

## Summary

Four interaction patterns for embedding AI assistance into design tools: sidebar (always-on contextual suggestions), modal (focused batch generation), inline (micro-corrections on selected elements), and review (audit passes against a structured rubric). Choose one pattern per tool — mixing them creates UX confusion. Review-mode is the most agent-native: the agent receives a design artifact, applies a rubric, and returns structured JSON feedback for a human to act on.

## Why

AI assistance without a defined interaction pattern degrades quickly: sidebar assistants give stale suggestions when context changes faster than the context window, modal assistants get abandoned after 2–3 interactions if too many clicks are required, and inline assistants in Figma plugins are sandboxed to selected nodes only. Choosing the right pattern before building prevents these failure modes.

## When To Use

- Implementing a contextual AI assistant inside a Figma plugin where the assistant reacts to selected/edited content
- Building a review-mode assistant that audits a design artifact and returns structured feedback
- Automating design documentation: converting Figma JSON or component specs into human-readable specs
- Evaluating which interaction pattern fits a given tool's UX before committing to implementation

## When NOT To Use

- The design problem is novel or strategic — assistant patterns support execution, not vision-setting
- The assistant would make irreversible changes autonomously — all AI design actions must be reversible or human-confirmed
- Context window is insufficient for the full design artifact (Figma file JSON above 200k tokens) — the assistant will hallucinate missing details
- The user base has low AI literacy — assistant patterns require users to interpret and validate output

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Four interaction patterns, selection rules, limitations |
| `content/02-agent-integration.xml` | Review-mode agent workflow, prompt patterns, service catalog, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/review-rubric-prompt.txt` | Component review prompt against accessibility, tokens, states, responsiveness |
| `templates/inline-suggestion-prompt.txt` | Inline suggestion prompt for a selected Figma layer |
| `templates/design-review.py` | Design review pipeline: spec file → structured JSON feedback |
