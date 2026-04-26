# OpenAPI Specification

## Summary

Machine-readable HTTP API contract using OpenAPI 3.1. Every path operation requires `operationId`, tags, request/response schemas via `$ref`, and realistic `examples`. The spec is authored before server code; generated code (stubs, SDKs) flows from the spec, never the reverse. Breaking changes are detected with `oasdiff` in CI and require human approval.

## Why

A single OpenAPI spec replaces handwritten docs, Postman collections, and ad-hoc client code. It generates typed SDK clients for all consumers, enables Prism mock servers for parallel development, and gives `schemathesis` a basis for property-based contract testing. LLM-generated servers that must satisfy a spec cannot silently drift from the contract.

## When To Use

- Designing or evolving any HTTP/JSON API with more than one consumer.
- Documentation must stay in sync with implementation (regen docs on every spec PR).
- Generating typed SDK clients for frontend, mobile, or partners.
- Mocking endpoints for frontend while backend is in flight.
- Contract testing with Schemathesis or Dredd against staging.

## When Not To Use

- GraphQL APIs — use SDL/GraphQL schema; OpenAPI for GraphQL is awkward.
- gRPC / protobuf services — `.proto` is the contract.
- Trivial internal endpoints with one consumer (same team).
- Server-rendered HTML apps (Django templates, Rails views).
- Streaming APIs (SSE, WebSockets with rich semantics) — AsyncAPI is the right spec.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | OpenAPI 3.1 structure: info, servers, paths, components, security, tags. |
| `content/02-components.xml` | Reusable schemas, parameters, responses, securitySchemes; $ref rules. |
| `content/03-antipatterns.xml` | Duplicate schemas instead of $ref, missing operationId, LLM format hallucinations, spec drift. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-user-api.yaml` | Full OpenAPI 3.1 example: users CRUD with pagination, error responses, bearer auth. |
| `templates/validate-openapi.sh` | Pre-commit gate: spectral + redocly lint + examples validation + oasdiff breaking check. |
| `templates/spectral.yaml` | Spectral ruleset: operationId required, tag-defined, no $ref-siblings. |
