# Contract-First Development

## Summary

Design API contracts (OpenAPI spec) before writing implementation code. The spec is the source of truth: server stubs, client SDKs, mock servers, and contract tests are all generated from it. No server code is written until the spec passes `spectral lint` and human review. Spec changes are treated like code — PR review, semver, `oasdiff` breaking-change detection in CI.

## Why

Code-first leads to inconsistent APIs and integration delays when FE and BE build in parallel. A committed spec lets FE start against a Prism mock immediately. The spec also becomes a deterministic anchor for LLM-generated services — the model cannot drift from a contract it must satisfy.

## When To Use

- New API with multiple consumers (frontend, mobile, partners) planned or existing.
- Cross-team handoff where BE and FE build in parallel.
- Public or partner APIs needing stable, versioned, machine-readable contracts.
- AI-agent-generated services — spec prevents drift between iterations.

## When Not To Use

- One-off internal scripts or single-team tools where overhead exceeds value.
- Highly experimental endpoints during prototyping (spec churn dominates).
- Pure GraphQL stacks — schema-first GraphQL achieves the same with different tooling.
- gRPC — `.proto` is already the contract; different tools apply.
- Server-rendered web apps where the API is HTML forms, not JSON.

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow.xml` | Design → lint → codegen → implement → validate lifecycle with gate rules. |
| `content/02-validation.xml` | Spectral rules, openapi-core response validation, CI integration. |
| `content/03-antipatterns.xml` | Code-before-spec, hand-editing generated code, copy-pasted schemas, spec churn. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-scaffold.yaml` | Minimal OpenAPI 3.1 spec with paths, components, reusable error responses. |
| `templates/check-spec-drift.sh` | CI script: spectral lint + codegen + diff generated vs server models + oasdiff breaking check. |
| `templates/spectral.yaml` | Spectral ruleset enforcing operationId, descriptions, and schema correctness. |
