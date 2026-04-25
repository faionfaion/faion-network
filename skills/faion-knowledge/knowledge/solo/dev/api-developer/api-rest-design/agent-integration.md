# Agent Integration — REST API Design

## When to use
- New public or partner-facing HTTP APIs where stable resource semantics, browser caching, and HTTP-toolchain familiarity (curl, Postman, OpenAPI) outweigh raw RPC throughput.
- CRUD-shaped domains (users, orders, posts, tickets) that map cleanly to nouns + standard verbs and benefit from HTTP cache headers, conditional requests, and CDN edge caching.
- Public docs and SDK generation flows that consume an OpenAPI spec; REST + OpenAPI is the most common pairing for codegen tools.
- Multi-team platforms where consistency (one URL grammar, one pagination convention, one error envelope) matters more than raw flexibility.
- LLM-driven backend authoring — agents pattern-match RESTful conventions reliably, especially when paired with a contract-first OpenAPI spec.

## When NOT to use
- Real-time bidirectional flows (chat, presence, live cursors) — use WebSockets / SSE / WebTransport.
- Highly graph-shaped read patterns where clients fan-out to 10+ endpoints per screen — GraphQL or BFF reduces round-trips.
- Internal hot paths needing strict typing and 10x throughput — gRPC + Protobuf is faster.
- Streaming uploads/downloads with resumability — REST works but WebDAV / TUS / S3 multipart is purpose-built.
- Cases where every endpoint is "verb-shaped" (jobs, calculations, transformations) — RPC is more honest than `POST /actions/calculate`.

## Where it fails / limitations
- **N+1 round-trips.** Mobile dashboards needing user + 5 collections trigger 6 calls. Mitigation: BFF / sparse fieldsets / `?include=` expansion / API composition at gateway.
- **Versioning drift.** `v1` and `v2` routes diverge subtly; clients pin one and rot. Plan a deprecation policy before shipping `v1`.
- **Resource-shoehorning.** Forcing actions into resources (`POST /transcoder/jobs` is fine; `PATCH /document with op=convert` is not). Allow controller resources (`POST /resources/:id:action`) sparingly.
- **PATCH semantics ambiguity.** RFC 7396 (merge-patch) vs RFC 6902 (json-patch) — pick one, document it; clients silently disagree otherwise.
- **Pagination chaos.** Page+limit, offset+limit, cursor — mixing within one API breaks SDKs. Standardize cursor pagination for stable feeds.
- **Inconsistent collection envelope.** `data`, `items`, `users`, raw array — pick one envelope (`{data, meta, links}`) and enforce.
- **Verb leakage.** `/getUser`, `/createUser`, `/userList` is RPC dressed as REST; agents copy these patterns from legacy snippets.
- **Cache invalidation.** ETag/`If-None-Match` skipped → CDN serves stale; or `Cache-Control: no-store` everywhere → no caching at all.
- **HATEOAS overreach.** Full HAL / Siren is rarely consumed by SDKs and adds payload weight; lightweight `_links` for next/prev only is usually sufficient.
- **Status-code abuse.** 200 with `{"success": false}` body, 500 for validation failures — clients can't rely on HTTP semantics.

## Agentic workflow
Drive REST design top-down: (1) a **resource-modeler** subagent extracts nouns from product spec and proposes `/resources` + sub-collections, returning an OpenAPI skeleton (paths only, no schemas); (2) a **schema-author** subagent fills `components.schemas` from data model, including pagination/error refs; (3) a **convention-linter** subagent runs `spectral` with a project ruleset enforcing plural lowercase nouns, kebab-case, status-code/method conventions; (4) a **handler-generator** subagent emits FastAPI / Express handlers from the spec via `openapi-generator`; (5) a **contract-test** subagent (`schemathesis`) fuzzes endpoints against the spec; (6) `faion-sdd-executor-agent` runs the project quality gate. Always treat OpenAPI as source of truth — code follows. Forbid hand-rolled routes that aren't in the spec.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs lint, build, contract tests.
- A purpose-built **rest-resource-modeler** — converts a product spec + ER diagram into a path tree with parameterized IDs and standard verb mapping.
- A **rest-convention-linter** — wraps spectral with project rules: plural nouns, kebab-case, no verbs in URLs, every 4xx/5xx references Problem Details.
- A **pagination-auditor** — verifies all collection endpoints use the same pagination style (cursor or offset) and emit the same `meta`/`links` shape.
- A **status-code-auditor** — checks 201 endpoints set `Location`, 204 has no body, 429 sets `Retry-After`, 401 vs 403 are correct per route.
- A **breaking-change-detector** — diffs OpenAPI specs between branches (e.g. `oasdiff`) and fails CI on incompatible changes within a major version.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scans examples and fixtures for secrets.

### Prompt pattern
Resource modeling:
```
Given the domain model in docs/domain.md, propose REST paths.
Constraints:
- Plural lowercase nouns; kebab-case for multi-word.
- Sub-collections only one level deep; deeper relations expose
  filtered top-level collections (e.g. /messages?conversation_id=).
- Cursor pagination on every collection.
- Use POST /:collection/:id:action only for non-CRUD actions
  with documented justification.
Output: openapi.yaml paths + a table mapping domain entity → resource.
```

Lint pass:
```
Run spectral on openapi.yaml with .spectral.yaml.
For every violation, propose a minimal patch and group violations
by rule. Reject any patch that changes URL grammar without a
versioning note in CHANGELOG.md.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `spectral` | Lint OpenAPI spec, custom REST conventions | https://stoplight.io/open-source/spectral |
| `redocly` | OpenAPI lint + docs preview | https://redocly.com/docs/cli |
| `oasdiff` | Detect breaking changes between OpenAPI versions | https://github.com/Tufin/oasdiff |
| `openapi-generator` | Generate server stubs + clients in many languages | https://openapi-generator.tech |
| `schemathesis` | Property-based contract testing | https://schemathesis.readthedocs.io |
| `dredd` | OpenAPI / API Blueprint contract test runner | https://dredd.org |
| `httpie` / `curl` | Manual probing during development | https://httpie.io |
| `Bruno` / `Hoppscotch` | OSS Postman alternatives, file-based, agent-friendly | https://www.usebruno.com |
| `mockoon` | Local mock API from OpenAPI | https://mockoon.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight Studio | SaaS / Desktop | partial | Visual API design; export OpenAPI for agents. |
| Postman | SaaS | yes | Collections from OpenAPI; CLI `newman` for CI. |
| Bruno | OSS Desktop | yes | Plain-text `.bru` files commit to repo. |
| Readme.io | SaaS | partial | Hosts docs + try-it; agents publish via API. |
| Mintlify | SaaS | yes | Doc-as-code from OpenAPI; agents push spec to repo. |
| Kong / AWS API Gateway | OSS / SaaS | yes | Front REST APIs; auth, rate limit, transforms. |
| Stripe / GitHub / Twilio | reference | n/a | Read public docs as gold standards for REST design. |

## Templates & scripts
See `templates.md` for OpenAPI skeleton, pagination component, error response refs. Use this `.spectral.yaml` snippet to enforce conventions:

```yaml
# .spectral.yaml — REST conventions guard.
extends: ['spectral:oas']
rules:
  paths-kebab-case:
    description: Path segments must be lowercase and kebab-case.
    given: "$.paths[*]~"
    then:
      function: pattern
      functionOptions:
        match: '^(/[a-z0-9-]+(?:/\{[a-zA-Z]+\})?)+$'
    severity: error
  no-verbs-in-paths:
    description: Use HTTP method, not verbs in URL.
    given: "$.paths[*]~"
    then:
      function: pattern
      functionOptions:
        notMatch: '/(get|create|update|delete|list|fetch)[A-Z]'
    severity: error
  resources-must-be-plural:
    description: Top-level resources are plural nouns.
    given: "$.paths[*]~"
    then:
      function: pattern
      functionOptions:
        match: '^/[a-z0-9-]+s(/.*)?$'
    severity: warn
  operation-operationId: error
  operation-summary: error
  operation-description: warn
  oas3-valid-media-example: error
```

## Best practices
- **Plural lowercase nouns**; `/users`, `/order-items`. Hyphens for multi-word.
- **Sub-collections one level deep.** Beyond that, expose filtered top-level collections (`/messages?conversation_id=...`).
- **Standard methods first.** GET / POST / PUT / PATCH / DELETE map to read / create / replace / partial-update / remove. Reach for `POST /resources/:id:action` only for non-CRUD operations.
- **Stable status codes.** 201 + `Location`, 204 no body, 207 multi-status only when justified, 409 for state conflicts, 422 for semantic validation, 429 + `Retry-After`.
- **One pagination style.** Cursor-based for stable feeds (`?cursor=...&limit=...`); offset only for small admin lists.
- **Consistent envelope** for collections: `{ data, meta: { count, nextCursor }, links: { self, next, prev } }`.
- **Cache headers.** GET endpoints set `ETag` + `Cache-Control`; respect `If-None-Match` (304).
- **Idempotency keys** on POST that creates side effects (`Idempotency-Key` header per Stripe conventions).
- **Filtering and sorting.** `?status=active&sort=-created_at,name`. Document every filterable field.
- **Sparse fieldsets** (`?fields=id,email`) and `?include=...` for related resources to reduce N+1 trips.
- **Versioning policy decided once.** URL versioning (`/v1`) is simplest; Accept-header versioning is purer but harder to debug.
- **Problem Details on every error path** (RFC 9457). Sync HTTP code with body status.
- **OpenAPI as source of truth.** Codegen handlers and clients; treat hand-edited routes as drift.

## AI-agent gotchas
- **Verb-y URLs.** Agent emits `/getUserOrders`. Lint rule with `pattern.notMatch` blocks at PR.
- **PATCH ambiguity.** Agent uses merge-patch shape but spec says json-patch (or vice versa). Document and enforce one.
- **Inconsistent collection envelope.** Mid-PR shift from `data` to `items`. Force shared `Pagination` schema component.
- **Status code drift.** 200 with `{"error": "..."}` body. Reject in `status-code-auditor`.
- **`Location` missing on 201.** Clients can't follow the new resource. Add to convention checklist.
- **Sub-collections too deep.** `/orgs/:o/teams/:t/projects/:p/issues/:i/comments/:c` becomes brittle. Cap depth at 1.
- **Mass-assigning request body.** Agent reuses the response schema for input; clients can pass `id`, `createdAt`, `role`. Define separate `Create*Request` / `Update*Request` schemas.
- **Forgetting `Retry-After`** on 429 and 503; clients hammer endpoints in tight loops.
- **Missing pagination on growing endpoints.** `/users` returns full list with no pagination — works at 100 rows, dies at 100k. Pagination must be in the contract from day one.
- **CORS overlooked.** Public APIs default-deny preflight; agent debugs handler instead of CORS config.
- **Mixing auth schemes.** Bearer on most routes, basic on legacy ones. Pin one, deprecate the other on a schedule.
- **Breaking changes within a major version.** Renamed field, removed enum value — `oasdiff` in CI catches this; without it, agents ship breaking PRs.
- **Hand-edited routes diverge from spec.** Contract tests must pass; otherwise codegen is theater.

## References
- Microsoft REST API Guidelines: https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md
- Google API Design Guide: https://cloud.google.com/apis/design
- Zalando RESTful API Guidelines: https://opensource.zalando.com/restful-api-guidelines/
- Richardson Maturity Model: https://martinfowler.com/articles/richardsonMaturityModel.html
- Stripe API reference (style guide by example): https://stripe.com/docs/api
- GitHub REST API: https://docs.github.com/en/rest
- JSON:API: https://jsonapi.org
- RFC 9457 (Problem Details): https://datatracker.ietf.org/doc/html/rfc9457
- Sibling methodologies: `solo/dev/api-developer/api-openapi-spec/`, `solo/dev/api-developer/api-versioning/`, `solo/dev/api-developer/api-error-handling/`, `solo/dev/api-developer/api-documentation/`.
