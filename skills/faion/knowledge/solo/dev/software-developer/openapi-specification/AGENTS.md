# OpenAPI Specification

## Summary

OpenAPI 3.1 as the single source of truth for HTTP/JSON APIs: one canonical `openapi.yaml` at repo root, all schemas and error responses under `components/` referenced via `$ref`, mandatory `operationId` on every operation, and CI gates (Spectral lint + `oasdiff` breaking-change check) that block merges introducing undocumented or breaking changes.

## Why

API documentation drifts from implementation within days unless the spec is machine-checked. A single spec enables typed client SDK generation across languages, mock servers for FE/BE parallel development, contract tests (schemathesis), and automated breaking-change detection — all from one file. Duplicated schemas and missing `required` arrays are the top two sources of generated-client bugs.

## When To Use

- Designing a new HTTP/JSON API where clients, servers, mocks, tests, and docs must stay in sync.
- Generating typed clients (TS, Python, Go) instead of hand-writing N SDKs.
- Contract-first work between FE and BE where one side is agent-built.
- Documenting an existing API before refactor.
- Public API surface where SDK generation and developer docs are expected.

## When NOT To Use

- Pure internal RPCs between trusted services — use Protobuf/gRPC/tRPC; OpenAPI adds ceremony for no gain.
- GraphQL APIs — schema is the contract; OpenAPI is irrelevant.
- Event-driven / pub-sub — use AsyncAPI instead.
- Tiny one-endpoint webhook receivers — overhead exceeds value.
- Server-driven UI payloads over a stream, not REST.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | OpenAPI 3.1 spec structure: paths, components, schemas, parameters, responses, security. |
| `content/02-rules.xml` | Mandatory rules: $ref reuse, operationId, required arrays, error schema consistency, CI gates. |
| `content/03-antipatterns.xml` | Schema duplication, missing required, oneOf without discriminator, security block omissions, YAML reformatting noise. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-base.yaml` | Minimal OpenAPI 3.1 skeleton with User CRUD, shared Error schema, bearerAuth, pagination parameters. |
| `templates/openapi-ci.yml` | GitHub Actions workflow: Redocly lint + Spectral lint + oasdiff breaking-change gate. |

## Scripts

(none)
