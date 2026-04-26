# API-First Development

## Summary

Design the OpenAPI 3.1 specification before writing any implementation code. The spec is the contract: it drives mock server generation (Prism), server stub generation (OpenAPI Generator), client SDK creation, and contract testing (schemathesis/dredd). The spec must be kept in sync with the implementation via CI contract tests — a spec that lies is worse than no spec.

## Why

Code-first APIs produce inconsistent designs, undocumented edge cases, and breaking changes for consumers. API-first enables frontend and backend teams to work in parallel (frontend against the mock, backend against the spec), generates boilerplate automatically, and gives LLMs a machine-readable contract that dramatically reduces hallucinations during code generation.

## When To Use

- Starting a new API — design the spec before writing any implementation code
- Frontend and backend developed in parallel — spec enables Prism mock server for frontend
- Generating server stubs, client SDKs, or TypeScript types from spec rather than writing by hand
- Onboarding an LLM to implement or test an API — full OpenAPI spec as context eliminates ambiguity
- Multiple consumers (web, mobile, third-party) will use the API — spec is the shared contract

## When NOT To Use

- Internal one-off scripts or single-consumer CLI tools with no formal contract
- Rapidly prototyping throw-away spikes — write code first, extract spec after it stabilizes
- GraphQL APIs — GraphQL has its own SDL-first approach; OpenAPI does not map cleanly
- Simple CRUD with no external consumers — spec maintenance overhead exceeds benefit

## Content

| File | What's inside |
|------|---------------|
| `content/01-spec-design.xml` | OpenAPI 3.1 structure, schema design rules, versioning, Spectral linting |
| `content/02-toolchain.xml` | Workflow: spec → lint → mock → generate stubs → contract test; tool roles |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-skeleton.yaml` | OpenAPI 3.1 spec skeleton with all required sections |
| `templates/spectral-ruleset.yaml` | Spectral ruleset for org-standard spec linting |
