# REST API Design

## Summary

Resource-oriented HTTP API design: noun-based URL structure, correct HTTP verb semantics and idempotency guarantees, canonical status code mapping, and optional HATEOAS links. URLs use plural nouns, lowercase kebab-case, and query params for filtering/sorting — never verbs.

## Why

Inconsistent REST design (verbs in URLs, wrong status codes, missing idempotency) forces API consumers to read implementation code instead of relying on HTTP conventions. The Richardson Maturity Model shows that level 2 REST (resources + verbs) gives the highest usability gain for the lowest implementation cost; level 3 (HATEOAS) is valuable for discoverability but optional.

## When To Use

- Designing new HTTP APIs for web or mobile clients
- Reviewing existing APIs for REST compliance before documentation or SDK generation
- Establishing naming and status-code conventions for a team

## When NOT To Use

- RPC-heavy APIs where each operation has a unique semantic (payment.capture, order.fulfill) — consider JSON-RPC or tRPC instead
- Real-time APIs (WebSocket, SSE) where HTTP verbs are irrelevant
- Internal CLI tooling where REST conventions add overhead with no consumer benefit

## Content

| File | What's inside |
|------|---------------|
| `content/01-resource-design.xml` | URL structure rules, HTTP verb semantics, idempotency table, status code mapping |
| `content/02-best-practices.xml` | Naming conventions, filtering/sorting, HATEOAS links, response envelope patterns |

## Templates

none
