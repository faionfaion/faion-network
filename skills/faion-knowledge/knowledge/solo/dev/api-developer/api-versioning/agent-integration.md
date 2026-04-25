# Agent Integration — API Versioning

## When to use
- Public APIs with external consumers you cannot redeploy in lockstep (partners, mobile apps shipped to stores, third-party integrations).
- Major contract changes (renamed/removed fields, changed types, new required inputs) — additive changes never need a version bump.
- Two-team handoffs where the producer ships ahead of consumers and needs a bridge.
- Long-tail clients (mobile apps from 2 years ago still hitting prod).
- Migrations: feature-flag-style rollout of v2 alongside v1.

## When NOT to use
- Internal-only API with one consumer redeployed atomically — backward-compat fields + tombstones beat versions.
- Additive changes (new field, new endpoint, new optional input) — never a new version.
- GraphQL — use `@deprecated` + field evolution + persisted queries instead of paths.
- Tiny app you control end-to-end — versioning ceremony eats cycles you don't have.
- After-the-fact for breaking changes already merged. The fix is a hotfix + comms, not retroactive `/v2`.

## Where it fails / limitations
- Maintaining 3+ active majors gets exponentially expensive. Cap at 2 supported majors with a sunset policy.
- Header / Accept-version routing breaks naive HTTP caches and CDNs that key on URL only.
- Date-based versioning (Stripe-style) requires per-customer pinning and a transformation pipeline — heavy for small teams.
- Query-param versioning poisons CDN cache keys.
- "Internal" v2 that diverges silently from v1 → endless duplication. Without a clear deprecation date, v1 lives forever.
- Mobile clients that don't update strand v1 in production indefinitely; sunset must be enforced with HTTP responses, not just blog posts.
- Versioning gives a false sense of safety: callers still break on response body shape changes you didn't think were "breaking".

## Agentic workflow
The agent's job is to detect breaking changes before they ship and to enforce the sunset lifecycle. Pin a contract diff tool (`oasdiff`, `graphql-inspector`) into CI. On any spec edit, the gate runs the diff; if breaking, the change requires either a new `/v2` route, a header switch, or an explicit "breaking — minor bump" override approved by a human. Agents never delete v1 routes — they mark `Deprecation`/`Sunset` headers, log usage, and only the human triggers the final removal after the sunset date.

### Recommended subagents
- `faion-sdd-execution` — quality gate that runs `oasdiff` and fails on breaking changes without a version directive.
- A `version-router` agent (Sonnet) — wires v1/v2 routers, copies handlers to v2 module, plans the migration table.
- A `sunset-comms` agent (Haiku) — drafts deprecation notices, changelog entries, partner emails from the diff.
- `nero-tools` — schedules sunset reminders via `tg-send` to the on-call channel.

### Prompt pattern
```
Compare openapi/v1.yaml HEAD~1 → HEAD with oasdiff.
For each BREAKING change, decide:
  (a) revert and find an additive alternative;
  (b) move the change to /api/v2 alongside v1;
  (c) document it as accepted breaking change with explicit version bump.
Output: oasdiff report + decision table + a patch that either reverts or
duplicates the handler under /v2.
```

```
Generate Deprecation/Sunset headers for routes listed in
ops/sunset.yaml that hit their `deprecate_at` date. Update the response
middleware. Do not remove handlers — that is a separate PR after
sunset_at and 0 30-day usage.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `oasdiff` | OpenAPI 3 diff with breaking-change detection | `brew install tufin/tap/oasdiff` |
| `openapi-diff` (atlassian) | Older OpenAPI diff, JSON output | `npm i -g openapi-diff` |
| `graphql-inspector` | GraphQL schema diff with breaking-change rules | `npm i -g @graphql-inspector/cli` |
| `buf breaking` | Protobuf breaking-change check | `brew install bufbuild/buf/buf` |
| `pact-broker` | Consumer-driven contract verification across versions | `brew install pact-foundation/pact-ruby-standalone/pact-ruby-standalone` |
| `httpie` | Hand-test header/path versioning | `pip install httpie` |
| `vacuum` | OpenAPI quality + lint with versioning rules | `brew install daveshanley/vacuum/vacuum` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Stripe API versioning model | Reference | — | Date-based per-account pinning — copy the model, not the infra |
| Apollo GraphOS | SaaS | Yes — Rover CLI | Schema registry + breaking-change gates |
| Buf Schema Registry (BSR) | SaaS + OSS | Yes — `buf` CLI | Protobuf registry with breaking checks |
| Postman API versioning | SaaS | Yes — REST API | Mock servers per version |
| Stoplight | SaaS | Yes — REST API | OpenAPI registry with diff |
| Bump.sh | SaaS | Yes — `bump` CLI | API changelog + diff service |
| ReadMe API Hub | SaaS | Yes — REST API | Dev docs with version switcher |
| AWS API Gateway stages | SaaS | Yes — IaC | Stage-based routing as crude versioning |

## Templates & scripts
See `templates.md` for path-versioning, header-versioning, and Sunset-header middleware.

CI breaking-change gate (drop into `.github/workflows/`):

```bash
#!/usr/bin/env bash
set -euo pipefail
git fetch origin main:main
oasdiff breaking origin/main:openapi.yaml openapi.yaml \
  --fail-on ERR --format json > /tmp/diff.json
n=$(jq 'length' /tmp/diff.json)
if [ "$n" -gt 0 ]; then
  echo "::error::$n breaking changes detected"
  jq -r '.[] | "  \(.id) \(.path) \(.text)"' /tmp/diff.json
  if ! grep -qE '^v[0-9]+: breaking' .changelog-pending; then
    echo "::error::No 'v<N>: breaking' line in .changelog-pending — add or revert."
    exit 1
  fi
fi
```

## Best practices
- Default to additive evolution. New field nullable, new endpoint, new optional input — no version bump.
- Major version only for breaking semantic changes. URL path versioning (`/api/v1/...`) is the boring, cacheable, debuggable choice.
- Support N and N-1; announce sunset 6 months ahead, enforce 12 months for partner APIs.
- Always emit `Deprecation`, `Sunset`, and `Link: rel=successor-version` headers from deprecated routes.
- Track per-version usage in metrics (`http_requests_total{version="v1"}`). You cannot sunset what you cannot measure.
- Provide a migration guide + automated codemod when feasible. Stripe-style dual-running with a version pin is the gold standard.
- Never let v2 silently change a v1 response shape. v1 routes freeze; v2 lives in a separate module/router.
- Include the version in error responses (`X-API-Version`) so client logs can attribute regressions.
- For SDKs: pin the API version at SDK build time; SDK majors trail API majors.
- Persisted queries (GraphQL) and Protobuf with `buf breaking` are stronger guarantees than path versioning — prefer them when the stack allows.

## AI-agent gotchas
- Agents conflate "any change → new version". 90% of changes are additive — push back. Make the SDD gate require a justified breaking-change line in `.changelog-pending` to bump.
- LLMs deduplicate v1/v2 handlers "to be DRY", silently introducing breaking changes in v1. Lock v1 routes behind read-only flags or a separate package the agent cannot edit.
- Generated client SDKs that auto-update can leak v2 fields into v1 consumers if codegen is misconfigured. Pin SDK versions to API versions explicitly.
- Sunset enforcement is forgotten. Cron a job that, on `sunset_at`, returns 410 Gone with a body pointing to v2. Agents draft the migration but humans flip the switch.
- Header-based routing is sometimes "implemented" by an agent as a body-field switch — that's not versioning, that's mode-switching. Reject in review.
- Date-based versioning needs a transformation pipeline (request/response rewriters per version). Agents will try to fold versions into business logic with `if version == ...` branches. That's the bug factory. Centralize in middleware.
- Agents reading the Stripe blog will copy date-based versioning to a 2-person team. Push back: header or path versioning is the right default at small scale.
- When sunsetting, agents may want to delete v1 code. Force two PRs: (1) flip to 410 Gone, (2) — only after 30 days of zero traffic — delete code.

## References
- https://datatracker.ietf.org/doc/html/rfc8594 (Sunset header)
- https://datatracker.ietf.org/doc/html/rfc9745 (Deprecation header)
- https://stripe.com/blog/api-versioning
- https://stripe.com/docs/api/versioning
- https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#12-versioning
- https://github.com/Tufin/oasdiff
- https://buf.build/docs/breaking
- https://restfulapi.net/versioning/
