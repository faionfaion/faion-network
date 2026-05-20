---
slug: framework-decomposition-patterns
tier: solo
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LLM-friendly code organization patterns for Django, Rails, Laravel, and React: service layer, selectors, DTOs, query objects, actions, and custom hooks.
content_id: "96276615e91597b6"
tags: [framework-patterns, code-organization, refactoring, llm-friendly, service-layer]
---
# Framework Decomposition Patterns

## Summary

**One-sentence:** LLM-friendly code organization patterns for Django, Rails, Laravel, and React: service layer, selectors, DTOs, query objects, actions, and custom hooks.

**One-paragraph:** LLM-friendly code organization patterns for Django, Rails, Laravel, and React: service layer, selectors, DTOs, query objects, actions, and custom hooks. The concrete rule: cap files at 150-200 lines per type so a single Read fits in LLM context — full decomposition reduces required context from 50K to 10-20K tokens.

## Applies If (ALL must hold)

- Refactoring fat controllers or God models in Django, Rails, or Laravel before LLM-assisted feature work.
- Preparing a legacy codebase for AI agents: cap files so a single Read fits in context.
- Building a new module: select the right extraction pattern before writing.
- Onboarding Claude Code to a framework codebase where token predictability matters.

## Skip If (ANY kills it)

- Tiny scripts, one-off Lambdas, or files already under 100 lines.
- Prototypes being thrown away weekly (YAGNI — You Aren't Gonna Need It).
- Frameworks with strong opinionated structure enforcing this already (Phoenix contexts, NestJS modules).
- Microservices where one service = one concern; extra layers duplicate boundaries.

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

- parent skill: `solo/dev/code-quality/`
