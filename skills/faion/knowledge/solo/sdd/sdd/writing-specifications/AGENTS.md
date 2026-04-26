# Writing Specifications

## Summary

A specification answers WHAT to build and WHY. It functions as the anti-hallucination anchor for LLM execution agents: every FR-X must be a SHALL statement meeting SMART criteria, and every acceptance criterion must use concrete values in Given-When-Then format. The spec is not considered complete until a second, fresh-context agent outputs "SPEC APPROVED" after running the AC coverage checklist (happy path, error handling, boundary conditions, security, performance, accessibility).

## Why

Traditional specs were alignment artifacts for humans. LLM agents require specs that act as programming interfaces: structured requirements with measurable thresholds replace narrative context and implied constraints. Without an explicit "Out of Scope" section, agents implement out-of-scope features. The "curse of instructions" — model adherence drops with more than 200 FRs — forces ruthless prioritization and phase splitting.

## When To Use

- Before any LLM-assisted implementation: the spec is the primary context document
- When requirements come as vague requests — transform them into structured FR-X + AC-X artifacts
- Writing CLAUDE.md or project rules using the three-tier boundary system (Always / Ask First / Never)
- Any feature affecting multiple files, teams, or external APIs

## When NOT To Use

- Bug fix with a known root cause and clear fix — write the fix, not a spec
- Configuration-only change — no functional requirements to specify
- One-off script or throwaway prototype — overhead exceeds value
- When requirements are so volatile they will change before implementation starts

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Spec vs design vs impl-plan distinctions; six core areas for LLM execution; three-tier boundary system; ambiguity avoidance table |
| `content/02-requirements.xml` | SMART criteria, FR format, MoSCoW prioritization, Given-When-Then AC, coverage checklist |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-full.md` | Full feature spec with user personas, FRs, NFRs, ACs, boundaries |
| `templates/spec-mvs.md` | Minimal viable spec for simple single-task features |
| `templates/spec-api.md` | REST/GraphQL API endpoint spec with request/response/error shapes |
| `templates/spec-component.md` | UI component spec with props, variants, states, accessibility |
| `templates/prompt-spec.txt` | Prompts for writing and reviewing specs for LLM executability |
| `templates/check-spec.sh` | Shell script validating FR-X, AC-X, Given/When/Then presence and flagging vague terms |
