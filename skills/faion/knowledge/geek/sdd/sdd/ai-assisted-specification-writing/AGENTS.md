# AI-Assisted Specification Writing

## Summary

Collaborative human-AI specification creation using LLMs to draft, refine, and validate requirements. The workflow: human provides intent, AI structures questions and drafts FR list with edge cases and Given-When-Then acceptance criteria, human reviews and approves, then implementation begins. Human approval gates are mandatory at every stage.

## Why

AI-generated code quality directly correlates with specification quality. Vague intent produces hallucinated requirements; structured specs with explicit edge cases and acceptance criteria produce accurate implementations. LLMs significantly improve SRS quality when used as an intermediate reasoning step (ACL 2025 research), but human-AI synergy outperforms AI-only: LLMs draft, humans validate domain correctness.

## When To Use

- Starting a new feature where requirements are known informally but not structured
- Converting meeting notes, tickets, or PRDs into formal spec.md documents
- Reviewing an existing spec for completeness, internal conflicts, and missing acceptance criteria
- Generating implementation-plan.md task breakdowns from an approved spec

## When NOT To Use

- Highly specialized domains (medical regulatory, legal) where AI lacks domain context
- Specs already formally approved — agent review risks introducing changes to finalized docs
- When no human reviewer is available — AI-generated specs require a human approval gate before implementation
- Pure infrastructure/config tasks where the spec is trivially derived from the implementation

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow-principles.xml` | SDD-AI workflow phases, human-AI collaboration model, supported spec formats, LLM selection |
| `content/02-checklist.xml` | Phase-by-phase specification checklist: intent capture through human sign-off |
| `content/03-antipatterns.xml` | Anti-patterns: accepting AI spec without review, vague intent, missing out-of-scope, hallucinated requirements |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-md.md` | Feature specification template (FR-X, edge cases, ACs, dependencies, risks) |
| `templates/api-spec.md` | API specification template (endpoints, request/response, error codes) |
| `templates/prompt-generate.txt` | LLM prompt for initial spec generation with context structure |
| `templates/prompt-review.txt` | LLM prompt for spec review: completeness, conflicts, testability |
