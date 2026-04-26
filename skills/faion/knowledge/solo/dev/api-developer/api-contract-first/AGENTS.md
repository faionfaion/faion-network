# API Contract-First Development

## Summary

Design the OpenAPI spec before writing any implementation code. The spec is reviewed like a PR, then used to generate server stubs, typed client SDKs, and contract test scaffolding via `openapi-generator`. CI lints the spec with Spectral on every change and validates the running implementation against the spec with `openapi-core`.

## Why

Code-first APIs drift: the implementation diverges from docs, clients break on undocumented fields, and breaking changes slip into minor releases. Contract-first inverts this — the spec is the single source of truth, reviewed before any code exists, making breaking changes visible at design time. Generated stubs enforce the contract structurally; contract tests enforce it at runtime.

## When To Use

- New APIs where frontend and backend are developed in parallel (spec enables frontend to mock immediately)
- APIs that will be versioned and shared with external consumers
- Teams that want spec-driven SDK generation to avoid hand-written client code
- When breaking change detection is required in CI

## When NOT To Use

- Internal scripts or glue APIs used only by one service — spec overhead is disproportionate
- Rapidly evolving prototypes where the contract changes every day — lock it down first
- GraphQL APIs — use SDL as the contract instead of OpenAPI

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow.xml` | Contract-first steps (design → review → generate → implement → validate → deploy) |
| `content/02-tooling.xml` | openapi-generator commands, Spectral linting rules, openapi-core validation, CI integration |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-base.yaml` | OpenAPI 3.1 spec skeleton with Payment API example (request, response, error refs) |
| `templates/spectral-rules.yaml` | .spectral.yaml extending oas ruleset with required operationId/description |
| `templates/contract-ci.yaml` | GitHub Actions workflow: lint spec, generate, diff models, run contract tests |
