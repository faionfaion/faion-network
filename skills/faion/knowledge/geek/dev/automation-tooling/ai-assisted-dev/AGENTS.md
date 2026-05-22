---
slug: ai-assisted-dev
tier: geek
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for using AI coding assistants (Claude Code, Cursor, Copilot) effectively: match tool to task type, use structured prompts, always review AI output before accepting, and never auto-accept security-critical code.
content_id: "06a87f8279519726"
tags: [ai-coding, claude-code, cursor, copilot, code-review]
---
# AI-Assisted Development

## Summary

**One-sentence:** Patterns for using AI coding assistants (Claude Code, Cursor, Copilot) effectively: match tool to task type, use structured prompts, always review AI output before accepting, and never auto-accept security-critical code.

**One-paragraph:** Patterns for using AI coding assistants (Claude Code, Cursor, Copilot) effectively: match tool to task type, use structured prompts, always review AI output before accepting, and never auto-accept security-critical code. AI increases defect rate 4x when used without review discipline.

## Applies If (ALL must hold)

- Setting up a project workflow where Claude Code, Cursor, or Copilot will be primary development tools.
- Deciding which AI tool to assign to which task type (planning vs. implementation vs. autocomplete).
- Building a CI step that uses AI for automated test generation or code review commentary.
- Onboarding a developer to AI coding tools — establishing safe review habits from the start.

## Skip If (ANY kills it)

- Security-critical auth or payment logic where AI-suggested code must never be accepted without line-by-line human review.
- Compliance-sensitive environments (healthcare, finance) where AI tool output has not been approved by legal/compliance.
- Teams lacking the experience to review AI output critically — premature AI adoption creates hidden defect accumulation.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/dev/automation-tooling/`
