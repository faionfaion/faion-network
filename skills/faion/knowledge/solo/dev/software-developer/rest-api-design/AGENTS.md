# REST API Design

## Summary

Resource-oriented HTTP API design conventions: plural noun paths, correct HTTP method
semantics, standard status codes, and consistent filter/pagination parameters. Core rule: paths
use plural nouns in kebab-case with no verbs (`/users`, not `/getUsers`); POST returns 201 +
Location header; DELETE returns 204; errors use RFC 7807 `application/problem+json`.

## Why

APIs without consistent shape cause integration failures, client SDK mismatches, and
maintenance nightmares. LLM agents misuse PUT vs PATCH and pick 200 everywhere; a Spectral
ruleset committed to the repo enforces conventions in CI rather than relying on reviewers.

## When To Use

- Designing a new HTTP API for a web/mobile client or third-party consumer
- Refactoring RPC-shaped endpoints (`/getUsers`, `/doThing`) into resource-oriented routes
- Reviewing PR diffs for status-code, method-semantic, or naming drift
- Generating client SDKs or OpenAPI specs that depend on consistent route shapes

## When NOT To Use

- Internal RPC between trusted services with strict latency budgets — gRPC fits better
- Highly relational graph queries with many shapes per page — GraphQL avoids round-trips
- Server-streamed events (logs, ticks) — SSE/WebSockets
- Pure file transfer pipelines — S3-style presigned URLs beat REST envelopes
- One-off webhook receivers where shape is dictated by the sender

## Content

| File | What's inside |
|------|---------------|
| `content/01-resource-design.xml` | Path conventions, HTTP method table, status code table, anti-patterns |
| `content/02-advanced-patterns.xml` | HATEOAS, pagination, filtering, bulk ops, idempotency keys |

## Templates

| File | Purpose |
|------|---------|
| `templates/spectral-ruleset.yaml` | Spectral ruleset enforcing plural nouns, kebab-case, POST→201 in CI |
