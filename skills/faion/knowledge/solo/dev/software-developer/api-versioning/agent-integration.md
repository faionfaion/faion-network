# Agent Integration — API Versioning

## When to use
- Public APIs with external consumers who can't move in lockstep with you
- Mobile apps where old client versions stay in the wild for months
- B2B integrations where SDKs are pinned per customer
- Any breaking change to a stable resource shape, status code, or auth scheme
- LLM tool-use scenarios — pin a stable version so an agent's training-time tool schema keeps working

## When NOT to use
- Internal-only APIs where you control all consumers and can deploy atomically — prefer "expand-then-contract" without versions
- Pre-1.0 / pre-launch — version churn while public is fine; commit to v1 only when an external user exists
- Pure additive changes (new optional field, new endpoint) — no version bump needed; signal via OpenAPI changelog
- Experimental endpoints behind feature flags — flag is the version axis, not URL/header

## Where it fails / limitations
- URL versioning litters call sites with `/v1` and forces routing/proxy work for every change
- Header versioning hides the version from logs, caches, and CDN routing — agents and ops both miss it
- Content-Type versioning (`application/vnd.api+json;v=2`) is standards-pure but tooling-poor
- Date-based versions (Stripe-style) are excellent for SaaS but require disciplined release notes per date
- Maintaining two versions in one codebase doubles test surface; teams underbudget this and ship subtle drift
- Sunsetting is the hard part: deprecation headers get ignored without proactive customer outreach
- Server-side feature gating ("v2 if header present, else v1") leads to combinatorial bugs

## Agentic workflow
A versioning agent classifies a proposed change as additive (no bump), behavioral (warn + flag), or breaking (new version). It generates the OpenAPI delta, opens a PR with the deprecation header on old routes, and schedules a sunset task with an explicit date in the issue tracker. A second agent monitors traffic by version using request logs and proposes sunset waves once usage drops below threshold.

### Recommended subagents
- `faion-sdd-executor-agent` — design + implement + verify with contract-test as quality gate
- A custom `api-change-classifier` (sonnet) — given a PR diff, decides additive / behavioral / breaking
- A custom `sunset-monitor` (haiku) — runs daily on access logs, reports per-version traffic share, drafts sunset PRs
- A custom `client-migrator` (sonnet) — for known SDK consumers, drafts migration code diffs from v(n) to v(n+1)

### Prompt pattern
```
Classify this OpenAPI diff: <paste>.
Decide: additive | behavioral | breaking.
If breaking: emit (a) new path/header version, (b) Deprecation + Sunset headers
on old routes set to T+180d, (c) migration note for the consumer changelog,
(d) feature flag to roll consumers per-tenant.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `oasdiff` | Diff two OpenAPI specs and classify breaking changes | https://github.com/oasdiff/oasdiff |
| `openapi-diff` (Atlassian) | Alternative spec diff | https://bitbucket.org/atlassian/openapi-diff |
| `optic` | API contract diff + changelog | https://www.useoptic.com |
| `spectral` | Lint specs incl. version naming rules | https://stoplight.io/open-source/spectral |
| `schemathesis` | Property-based test against a spec; run per version | https://schemathesis.readthedocs.io |
| `dredd` | Contract tests across versions | https://dredd.org |
| `oapi-codegen` / `openapi-generator` | Generate per-version clients | https://github.com/oapi-codegen/oapi-codegen |
| `wiremock` / `mockoon` | Stand up old-version mocks for migration testing | https://wiremock.org · https://mockoon.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe API versioning model | reference | Yes | Date-based, pinned per account; well documented |
| GitHub API | reference | Yes | Header `X-GitHub-Api-Version: 2022-11-28` |
| Mintlify / ReadMe | SaaS | Yes | Render multi-version docs from OpenAPI |
| ReDocly | SaaS+OSS | Yes | Multi-version doc bundles |
| Kong / Tyk / AWS API Gateway | OSS / SaaS | Yes | Route by header/path to versioned upstreams |
| Apigee / Azure API Management | SaaS | Yes | Built-in versioning + sunset analytics |
| Cloudflare API Shield | SaaS | Yes | Schema validation per version at edge |
| Optic / Bump.sh | SaaS | Yes | Version diff + changelog automation |

## Templates & scripts
See `templates.md` for full router patterns. Inline FastAPI multi-version mount with deprecation headers:

```python
# api/versioning.py
from datetime import datetime, timezone
from fastapi import APIRouter, Response

v1 = APIRouter(prefix="/api/v1")
v2 = APIRouter(prefix="/api/v2")

DEPRECATED_AT = "Wed, 01 Jan 2026 00:00:00 GMT"
SUNSET_AT     = "Wed, 01 Jul 2026 00:00:00 GMT"

@v1.middleware("http")
async def add_deprecation_headers(request, call_next):
    response: Response = await call_next(request)
    response.headers["Deprecation"] = DEPRECATED_AT
    response.headers["Sunset"] = SUNSET_AT
    response.headers["Link"] = '</api/v2>; rel="successor-version"'
    return response

@v1.get("/users/{user_id}")
async def get_user_v1(user_id: str):
    return {"id": user_id, "name": "..."}

@v2.get("/users/{user_id}")
async def get_user_v2(user_id: str):
    return {"data": {"id": user_id, "name": "..."}, "meta": {"v": 2}}
```

```yaml
# .spectral.yaml fragment — enforce versioning rules
rules:
  url-version-prefix:
    given: "$.paths.*~"
    then: { function: pattern, functionOptions: { match: "^/api/v[0-9]+/" } }
  deprecation-header-on-old-paths:
    given: "$.paths['/api/v1/*'].*.responses.*.headers"
    then: { field: "Deprecation", function: truthy }
```

## Best practices
- Pick one strategy per surface and never mix: URL for public REST, header for internal APIs and webhooks
- Default to the latest version when none is specified; document this clearly. Pin SDKs to a specific version
- Communicate sunsets with `Deprecation`, `Sunset`, and `Link: rel="successor-version"` headers — and email
- Maintain at least two versions concurrently; schedule sunset 6+ months out with measured traffic
- Use feature flags to roll consumers from old to new per-tenant before broad sunset
- Keep a single source of truth for behavior — implement v(n+1) atop shared services, not by copy-pasting v(n) handlers
- Track per-version usage in metrics (`http.request.version` label) and alert when v(n+1) usage stalls or v(n) usage spikes back
- Provide a versioned `OpenAPI` spec per version, not a single megafile; clients pin to one

## AI-agent gotchas
- Agents bump versions for additive changes; reviewers must enforce additive-is-not-breaking
- Agents copy a v1 handler to v2 then edit; both diverge silently — require shared service layer
- LLMs forget to add the `Deprecation`/`Sunset` headers when introducing v2 — block in lint
- When generating clients, agents target the latest spec but pin tests to old fixtures — break consumer tests silently
- Header-based versioning + CDN caching: agents miss `Vary: Accept-Version` and serve cross-version responses
- Human-in-loop checkpoint: any version sunset must require explicit go/no-go review with usage data attached
- Agents misuse query-param versioning (`?v=1`) for public APIs because it's easy to test in a browser; reject — it pollutes caches
- Date-based versioning (Stripe-style): agents generate spec dates, not all of them are real release dates — require a CHANGELOG entry per date

## References
- https://restfulapi.net/versioning/
- https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#12-versioning
- https://stripe.com/docs/api/versioning
- https://docs.github.com/en/rest/overview/api-versions
- https://datatracker.ietf.org/doc/html/rfc8594 — Sunset Header
- https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-deprecation-header — Deprecation Header
- https://www.useoptic.com — automated API change diffs
- https://github.com/oasdiff/oasdiff
