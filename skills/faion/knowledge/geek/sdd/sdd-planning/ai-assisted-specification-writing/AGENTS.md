# AI-Assisted Specification Writing (SDD Planning)

## Summary

AI-assisted specification workflow at the planning layer: translate a product concept or backlog item into spec.md + implementation-plan.md before the design phase. The agent reads feature intent, asks clarifying questions, generates FR list with Given-When-Then acceptance criteria, then generates task breakdown with token estimates. Human approval is required before implementation tasks are created.

## Why

The planning layer bottleneck in SDD is spec quality. Agents generating implementation plans from under-specified features create tasks executed out of order that fail mid-sprint. Separating the spec generation call from the plan generation call — with a human review gate between them — catches ambiguity before it propagates into implementation tasks. Token estimates (not time) keep planning honest about execution cost.

## When To Use

- Translating a product backlog item or Linear/GitHub issue into a structured spec.md
- Sprint planning: generating draft specs for upcoming sprint items for team review
- When a feature ticket has vague or missing acceptance criteria
- Iteratively refining a rough draft spec through AI dialogue
- Generating implementation-plan.md task breakdowns from an approved spec

## When NOT To Use

- As a substitute for stakeholder discovery, user research, or business requirements sessions
- Regulatory artifacts (FDA, GDPR DPA) — legal precision is beyond AI spec reliability
- Real-time collaborative specification during a live meeting — async drafting loop doesn't fit synchronous sessions
- When no product context is available — agent cannot invent business model or market requirements

## Content

| File | What's inside |
|------|---------------|
| `content/01-planning-workflow.xml` | Planning-layer agent workflow, prompt patterns, agentic gotchas, recommended subagents |
| `content/02-checklist.xml` | 5-phase planning checklist: intent capture, AI-assisted requirements, structure, quality gates, human approval |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-spec-plan.txt` | XML prompt: draft spec.md + implementation-plan.md from feature intent |
| `templates/prompt-refine.txt` | XML prompt: refine draft spec based on reviewer feedback |
| `templates/linear-to-spec.sh` | Shell script: scaffold spec.md from Linear issue via GraphQL API |
