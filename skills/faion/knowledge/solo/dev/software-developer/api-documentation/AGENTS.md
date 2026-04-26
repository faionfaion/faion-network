# API Documentation

## Summary

Document every API with an OpenAPI spec that includes: overview, authentication instructions, working code examples (curl + at least one SDK), all error codes with resolution hints, and a changelog. Host interactive docs via Swagger UI (`/docs`) and readable reference via Redoc (`/redoc`).

## Why

Developers abandon APIs that lack copy-paste examples or do not document errors. OpenAPI as source of truth enables auto-generated client SDKs, test stubs, and Swagger UI with zero extra work. A changelog prevents breaking-change surprises for existing consumers.

## When To Use

- Publishing any API consumed by external developers or third-party integrations
- Setting up a new FastAPI or Django project where OpenAPI is auto-generated
- Adding examples and error tables to an existing, poorly documented API
- Preparing an API for SDK generation

## When NOT To Use

- Internal micro-services with no external consumers — a brief AGENTS.md is enough
- Prototypes that will be redesigned before any consumer integrates
- CLI tools — man pages and --help flags are the right format

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Required documentation sections: overview, auth, quick start, errors, changelog |
| `content/02-openapi-examples.xml` | Rules for inline examples in OpenAPI; FastAPI app metadata setup; example schema |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-examples.yaml` | OpenAPI path with request/response examples and error refs |
| `templates/doc-structure.md` | Markdown template for a complete API reference page |
