# Agent Integration — REST API Design

## When to use
- Designing a new HTTP API for a web/mobile client or third-party consumer
- Refactoring an RPC-shaped endpoint (`/getUsers`, `/doThing`) into resource-oriented routes
- Reviewing PR diffs for status-code, method-semantic, or naming drift
- Generating client SDKs or OpenAPI specs that depend on consistent route shapes
- Onboarding LLM agents that will call the API — predictable verbs/nouns reduce tool-use errors

## When NOT to use
- Internal RPC between trusted services with strict latency budgets — gRPC fits better
- Highly relational graph queries with many shapes per page — GraphQL avoids round-trips
- Server-streamed events (logs, ticks, model output) — SSE/WebSockets/HTTP streaming
- Pure file transfer pipelines — S3-style presigned URLs beat REST envelopes
- One-off webhook receivers where shape is dictated by the sender

## Where it fails / limitations
- HATEOAS links rarely get used by real clients; over-investing wastes design budget
- "Resource-oriented" forces awkward modeling of actions ("approve order") — accept `POST /orders/{id}/approvals` instead of bending verbs
- Filter/sort/pagination semantics are not standardized; teams reinvent them per endpoint
- Bulk operations don't fit cleanly; `POST /batch` or RFC 7396 patches end up bespoke
- LLM agents misuse `PUT` vs `PATCH` and pick `200` where `201`/`204` is correct — needs explicit linting

## Agentic workflow
Run a design pass with a planning subagent that produces an OpenAPI sketch from the user's resource list, then a reviewer subagent that lints route shapes (plural nouns, kebab-case, no verbs, correct method-status pairing). Implementation agents consume the sketch to scaffold routers, serializers, and tests. Wire the linter into CI so PRs that drift from the design are blocked, not just commented on.

### Recommended subagents
- `faion-sdd-executor-agent` — feature-level design → spec → impl loop with quality gates
- A custom `api-design-reviewer` (sonnet) — checks routes against the rule table below; reads OpenAPI YAML and PR diffs
- A custom `openapi-scaffolder` (haiku) — generates router boilerplate from a vetted spec

### Prompt pattern
```
Design REST routes for resource <X> with operations <create/list/get/update/delete/<custom>>.
Rules: plural nouns, kebab-case, no verbs in path, sub-resources for ownership.
Return: route table | method | status code | request shape | response shape.
Then output an OpenAPI 3.1 fragment.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `spectral` | Lint OpenAPI/AsyncAPI specs against rulesets (Stoplight) | `npm i -g @stoplight/spectral-cli` · https://stoplight.io/open-source/spectral |
| `redocly lint` | Strict OpenAPI validation + style guide | `npm i -g @redocly/cli` |
| `openapi-generator-cli` | Generate clients/servers from spec | `npm i -g @openapitools/openapi-generator-cli` |
| `httpie` / `curl` | Manual smoke tests during agent loops | https://httpie.io |
| `hurl` | Repeatable HTTP test files; LLM-readable | https://hurl.dev |
| `schemathesis` | Property-based tests driven by OpenAPI | `pip install schemathesis` |
| `dredd` | Contract-test API against spec | `npm i -g dredd` |
| `bruno` / `posting` | Local-first API clients with Git-versioned collections | https://www.usebruno.com · https://posting.sh |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight Studio | SaaS+OSS | Partial | Visual OpenAPI editor; agents drive via Spectral CLI instead |
| Postman / Bruno | SaaS / OSS | Yes | Bruno stores collections as files — agents can edit/run via CLI |
| Insomnia | OSS | Partial | Has CLI (`inso`) for spec lint and run |
| ReadMe / Mintlify / Redocly | SaaS | Yes | Render OpenAPI to docs sites; webhook-driven |
| Apidog / SwaggerHub | SaaS | Partial | UI-first; agents prefer Spectral+Git workflow |
| Cloudflare API Gateway / Kong | SaaS / OSS | Yes | Enforce schemas at edge; agents push specs via API |

## Templates & scripts
See `templates.md` and `examples.md` for full route tables. Inline Spectral ruleset to enforce REST conventions in CI:

```yaml
# .spectral.yaml
extends: ["spectral:oas"]
rules:
  paths-kebab-case:
    given: "$.paths.*~"
    then: { function: pattern, functionOptions: { match: "^/[a-z0-9/{}-]+$" } }
  no-verbs-in-paths:
    given: "$.paths.*~"
    then:
      function: pattern
      functionOptions: { notMatch: "(get|post|create|update|delete|fetch|do)[A-Z]" }
  plural-collection-names:
    description: Collections must be plural nouns
    given: "$.paths.*~"
    then: { function: pattern, functionOptions: { match: ".*s(/\\{[^}]+\\})?$" } }
  status-code-201-on-post:
    given: "$.paths..post.responses"
    then: { field: "201", function: truthy }
```

## Best practices
- Lock the route-shape rules in a `Spectral` ruleset committed to the repo so CI, not reviewers, enforces them
- Use `Location` header on `201`; never invent a custom field for the new resource ID
- Pagination: pick one — cursor for streams, offset for finite listings — and apply globally (`?limit`, `?cursor`/`?offset`)
- Use `?fields=a,b,c` and `?expand=...` consistently rather than per-endpoint shape flags
- Reserve `PUT` for full replacement; `PATCH` for partial. Most CRUD wants `PATCH` — agents default to `PUT` incorrectly
- Return errors as RFC 7807 `application/problem+json` so clients/LLMs parse a stable shape
- Document idempotency keys on `POST` for charge/order endpoints; without them retries cause double-creates

## AI-agent gotchas
- LLMs invent `/api/getUserById/{id}` patterns from training data; lint must catch verb prefixes
- Agents pick `200 OK` everywhere; require a per-route status-code annotation in the spec stage
- When generating SDKs from spec, agents will hallucinate query params not in the schema — pin generation to the committed spec digest
- Human-in-loop checkpoint: any breaking change (removed field, narrowed type, status-code shift) must trigger explicit reviewer approval, not auto-merge
- Agents forget to set `Content-Type: application/json` on examples, then build wrong test fixtures
- Sub-resource depth >2 (`/a/{id}/b/{id}/c/{id}`) is a code smell agents happily produce; flag and refactor

## References
- https://www.rfc-editor.org/rfc/rfc7231 — HTTP/1.1 Semantics
- https://www.rfc-editor.org/rfc/rfc7807 — Problem Details for HTTP APIs
- https://www.rfc-editor.org/rfc/rfc8594 — The Sunset HTTP Header
- https://github.com/microsoft/api-guidelines
- https://opensource.zalando.com/restful-api-guidelines/
- https://cloud.google.com/apis/design
- https://stoplight.io/open-source/spectral
