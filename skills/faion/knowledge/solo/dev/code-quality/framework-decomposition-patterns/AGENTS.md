# Framework Decomposition Patterns

## Summary

LLM-friendly code organization patterns for Django, Rails, Laravel, and React: service layer, selectors, DTOs, query objects, actions, and custom hooks. The concrete rule: cap files at 150-200 lines per type so a single Read fits in LLM context — full decomposition reduces required context from 50K to 10-20K tokens.

## Why

Fat controllers and God models degrade LLM task success from ~95% (decomposed) to ~60% (monolithic) because the agent must load disproportionate context to reason about a single behavior. Service layers separate reads (selectors) from writes (services), which also lets agents reason about cache invalidation and side effects without scanning the entire model.

## When To Use

- Refactoring fat controllers or God models in Django, Rails, or Laravel before LLM-assisted feature work
- Preparing a legacy codebase for AI agents: cap files so a single Read fits in context
- Building a new module: select the right extraction pattern before writing
- Onboarding Claude Code to a framework codebase where token predictability matters

## When NOT To Use

- Tiny scripts, one-off Lambdas, or files already under 100 lines
- Prototypes being thrown away weekly (YAGNI)
- Frameworks with strong opinionated structure enforcing this already (Phoenix contexts, NestJS modules)
- Microservices where one service = one concern; extra layers duplicate boundaries

## Content

| File | What's inside |
|------|---------------|
| `content/01-universal-principles.xml` | File size limits by type; universal patterns (service, selector, DTO, composition, hooks); LLM context benefit table |
| `content/02-framework-patterns.xml` | Django service+selectors, Rails service objects, Laravel actions+DTOs, React hooks — key patterns and rules per framework |

## Templates

| File | Purpose |
|------|---------|
| `templates/find-fat-files.sh` | Bash one-liner: top-20 longest Python app files (excludes tests/migrations) |
| `templates/find-fat-components.mjs` | Node script: list React components over 150 LOC for hook extraction |
