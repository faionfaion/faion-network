# API Documentation

## Summary

A methodology for producing developer-facing API documentation that includes a Quick Start with working curl commands, authentication flow, OpenAPI endpoint descriptions with multiple request/response examples, an error code table, SDK references, and a changelog. Documentation stays in sync with the implementation by using tests to validate examples.

## Why

Developers abandon APIs with poor documentation — missing authentication examples and absent error tables are the top complaints. OpenAPI's `examples` field lets you embed multiple named request variants directly in the spec; Swagger UI renders them as selectable try-it-out presets. Keeping examples verified by tests prevents docs from drifting from the actual API behaviour.

## When To Use

- Launching a new API to external or internal consumers
- Migrating from ad-hoc Markdown docs to an OpenAPI-driven setup
- When support tickets repeatedly ask for authentication examples or error code meanings
- Generating client SDKs from the spec

## When NOT To Use

- Purely internal service-to-service APIs where code is the contract and no SDK is needed
- Prototype APIs under active design flux — write docs after the contract stabilises
- Micro-service mesh where service mesh observability tools (Envoy, Istio) already surface contracts

## Content

| File | What's inside |
|------|---------------|
| `content/01-doc-structure.xml` | Required doc sections, quick-start pattern, authentication block, changelog format |
| `content/02-openapi-examples.xml` | OpenAPI examples field usage, FastAPI metadata setup, multi-example patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/fastapi-metadata.py` | FastAPI app with title, description, version, auth docs, Swagger/Redoc URLs |
| `templates/openapi-examples.yaml` | OpenAPI path item with multiple named request/response examples |
