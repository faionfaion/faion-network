# API Contract-First Development

## Summary

Write the OpenAPI spec before any implementation code, get it reviewed like a PR, then generate server stubs and client SDKs from it. The spec is the source of truth; CI validates that the running implementation still matches it. Breaking changes require spec version bumps.

## Why

Designing the API surface in YAML forces deliberate decisions about resource shapes, error responses, and versioning before any code exists — reversing those decisions is cheap at spec stage, expensive after clients integrate. Code generation eliminates drift between spec and implementation. Spectral linting catches naming and structure violations automatically.

## When To Use

- Starting a new API that will have external consumers or multiple client teams
- Adding a significant new resource or workflow to an existing API
- Integrating with a partner that requires a published contract
- Any API where mobile and backend teams work in parallel

## When NOT To Use

- Internal APIs consumed only by one service written by the same team
- Rapid prototyping where the API shape is still being discovered
- APIs that are wrappers over a third-party spec (just import their spec)
- Micro-services that communicate exclusively over gRPC/protobuf

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow.xml` | Design → review → generate → implement → validate → deploy steps; CI integration rules |
| `content/02-tooling.xml` | openapi-generator commands for Python/TypeScript; Spectral lint rules; openapi-core validation |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-base.yaml` | Minimal OpenAPI 3.1 spec with one POST endpoint, request/response schemas, and error ref |
| `templates/contract-ci.yaml` | GitHub Actions workflow: lint spec, generate server, compare models, run contract tests |
