# Design Critique

## Summary

Design critique is a structured conversation about a design where participants analyze work against defined goals and principles, providing specific and actionable feedback. Every piece of feedback must follow: Observation → Principle/Goal → Impact → (Optional suggestion). Feedback not tied to a stated goal is opinion, not critique.

## Why

Unstructured design reviews become opinion battles where personal preferences override user evidence. Structured critique produces specific, goal-anchored feedback that the designer can act on. The Observation → Principle → Impact chain forces reviewers to justify feedback, filtering taste from insight.

## When To Use

- Pre-session preparation: generating a structured critique brief from design goals and constraints
- Async critique: reviewing a design description against stated goals and producing structured feedback
- Post-session synthesis: organizing critique notes into prioritized action items
- Solo work: using an agent as a structured sounding board when no human reviewers are available
- Training designers to give and receive goal-based feedback

## When NOT To Use

- Replacing human critique sessions — critique is partly a social alignment process that builds shared design language
- When design goals are undefined — critique without objectives degrades to preference-based feedback
- Final production polish decisions — agent cannot assess micro-interaction feel or animation timing
- When stakeholder buy-in is the primary goal — human-led critique creates co-ownership

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Roles, stage-appropriate feedback types, five-step critique process, async format |
| `content/02-rules.xml` | Feedback quality rules, receiving feedback, facilitator rules, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/critique-session.md` | Full critique session doc: context, design goals, notes, action items, decisions |
| `templates/feedback-framework.md` | Observation → Principle → Impact → Suggestion format with worked example |
| `templates/figma-elements.sh` | Bash script to extract Figma frame element names via REST API for agent input |
