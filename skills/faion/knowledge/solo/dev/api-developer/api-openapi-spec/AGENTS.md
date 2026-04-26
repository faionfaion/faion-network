# OpenAPI Specification

## Summary

Describe REST APIs as machine-readable YAML/JSON contracts (OpenAPI 3.1) that drive codegen, mocking, contract testing, and reference docs. Shard sources into `paths/`, `components/schemas/`, `components/responses/`, `components/parameters/` and bundle to a single `openapi.yaml` via `redocly bundle`. Every operation must have `operationId`, `summary`, `tags`, and examples; every reusable shape must live in `components/` as a `$ref`.

## Why

A spec that is the single source of truth lets generators produce TypeScript/Python/Go clients, server stubs, mock servers, and rendered docs from one file. `oasdiff` in CI catches breaking changes before they reach consumers. Without the spec as contract, client teams diverge silently and breaking changes ship undetected.

## When To Use

- HTTP/REST APIs that need SDK clients, mocks, or contract tests
- Multi-language distributions regenerating clients on each release
- Public APIs where Swagger UI / Redoc / Mintlify serves as the reference
- Contract-first development enforced by `oasdiff` in CI
- LLM-authored backends where a strict spec prevents endpoint hallucination

## When NOT To Use

- gRPC/Protobuf services — use `.proto` + `buf` instead
- AsyncAPI / event-driven systems — use AsyncAPI 2.x/3.x for Kafka, MQTT, WebSocket envelopes
- GraphQL APIs — use SDL + `graphql-codegen`; an OpenAPI overlay adds confusion
- Highly volatile experimental endpoints where contract is not yet frozen

## Content

| File | What's inside |
|------|---------------|
| `content/01-spec-structure.xml` | OpenAPI 3.1 skeleton, component sharding, `$ref` rules, operationId/tags requirements |
| `content/02-checklist.xml` | Authoring checklist: required fields, security schemes, examples, error responses |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-skeleton.yaml` | Minimal OpenAPI 3.1 spec with User resource, pagination, JWT security, and error responses |
| `templates/openapi-bundle-check.sh` | CI script: bundle-check + Spectral lint + Redocly lint |

## Scripts

none
