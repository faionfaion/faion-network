# Agent Integration — API Documentation

## When to use
- Public, partner, and internal APIs that need a single, navigable reference (endpoints, schemas, examples, errors, auth, changelog) maintained alongside the code.
- Doc-as-code workflows where the OpenAPI spec is the source and rendered output (Swagger UI / Redoc / Mintlify) is regenerated on every commit.
- Multi-language client SDK distributions where docs must include curl + JS + Python + Go snippets that stay in sync.
- Hosted developer portals that surface auth flow, rate limits, plan tiers, status page, and a "Try it" sandbox to reduce time-to-first-call.
- LLM-driven documentation runs — agents excel at templating per-endpoint pages from spec metadata, but require human review on prose and security guidance.

## When NOT to use
- One-off internal scripts or service-to-service hot paths whose only consumer is the same team in the same repo — code comments + an OpenAPI spec are sufficient.
- Pre-launch / unstable APIs where docs invite premature adoption; mark as `experimental` and gate behind feature flag instead of polishing public docs.
- Plain HTML pages hand-edited per endpoint — the maintenance cost dominates; switch to spec-driven docs.
- Codebases without a stable contract (no OpenAPI, no Protobuf) — docs derived from prose alone go stale immediately. Stabilize the contract first.

## Where it fails / limitations
- **Spec-doc drift.** Docs lag the spec because nobody regenerates. Mitigation: CI generates `openapi.yaml` from code or runs Spectral lint plus `redocly preview-docs`, fails on warnings, deploys to staging on every PR.
- **Examples rot.** Hand-edited curl snippets reference old field names. Mitigation: tests verify request/response examples against the schema; agents run `schemathesis` or `dredd` on the spec.
- **Auth flow vagueness.** "Use your API key" without a step-by-step + code snippet → highest support-ticket driver. Doc the full obtain → store → send → rotate flow.
- **Rate-limit info hidden.** Devs hit 429 unprepared; doc must surface limits per plan, headers (`X-RateLimit-*`, `Retry-After`), and recommended backoff.
- **Search broken.** Many doc themes ship with weak search (no fuzzy, no symbol search). Use Algolia DocSearch or Meilisearch.
- **Versioning unclear.** v1 docs URL silently switches to v2 content; clients confused. Pin a `/v1/` path and a banner linking to `/v2/`.
- **No changelog.** Breaking changes ship without a callout; clients break. Maintain `CHANGELOG.md` rendered at `/changelog` with semver tags.
- **PII / internal hostnames in examples.** Real customer IDs leak into docs. Use deterministic fakers; gate with grep CI.
- **i18n half-done.** Translated landing page, English-only reference. Pick: English-only (most common) or full localization, not in-between.
- **Try-it sandbox hits prod.** A `Try it` button against prod triggers real charges. Provide a sandbox env (`api-sandbox.example.com`) and pre-auth test keys.

## Agentic workflow
Drive doc work spec-first: (1) a **spec-curator** subagent ensures every operation has `summary`, `description`, `operationId`, `tags`, request/response examples; (2) a **prose-author** subagent writes concept pages (auth, pagination, errors, rate limits, webhooks) using shared partials so each can be re-used in renderer; (3) a **codegen-snippets** subagent produces curl + Python + JS + Go examples per endpoint, sourcing values from spec examples; (4) a **link-and-anchor checker** verifies internal links and that every error code mentioned in prose exists in the registry; (5) `faion-sdd-executor-agent` runs lint + build + preview deploy. Agents must never edit prose without a human review pass — reference and conceptual docs are the public face of the API.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs `spectral lint`, `redocly build-docs`, link checker, doc preview deploy.
- A purpose-built **doc-snippet-generator** — emits curl + Python (httpx) + JS (fetch) + Go snippets per endpoint from spec examples.
- A **example-validator** — runs each `examples.value` payload through the request/response schema; fails on mismatch.
- A **doc-link-checker** — `lychee` or `linkinator` over rendered HTML; reports broken anchors and dead URLs.
- A **changelog-bot** — appends a CHANGELOG entry per merged PR with breaking-change detection from `oasdiff`.
- An **api-tour-author** — produces a 5-minute "Hello, API" page hitting one endpoint end-to-end with a free-tier key.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — catches real tokens / emails in examples.

### Prompt pattern
Per-endpoint reference page:
```
For each operation in openapi.yaml, render docs/reference/{tag}/{operationId}.mdx with:
- Title = operation.summary
- Description from operation.description
- HTTP method + path with `<auth required>` badge if security applies
- Parameters table (in path / query / header) sourced from openapi
- Request body schema (rendered from $ref) + 1 example
- Response 2xx + 4xx + 5xx schemas + Problem Details example
- curl + python (httpx) + js (fetch) + go (net/http) snippets
- "Errors" section enumerating documented codes from registry.
```

Auth concept page:
```
Write docs/concepts/auth.mdx covering:
1. How to obtain an API key (UI walk-through + screenshots).
2. Storing the key (env var, secret manager).
3. Sending the key (Authorization: Bearer header, never query string).
4. Rotation (60-day cadence, dual-active during rotation).
5. Scopes / permissions matrix.
6. Common errors (401 vs 403) with remediation steps.
Include a working curl + python snippet at the top.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `redocly` | OpenAPI lint + render Redoc HTML | https://redocly.com/docs/cli |
| `spectral` | Lint OpenAPI for completeness (descriptions, examples) | https://stoplight.io/open-source/spectral |
| `mintlify` | Doc framework with OpenAPI ingest | https://mintlify.com/docs |
| `docusaurus` | OSS docs framework | https://docusaurus.io |
| `vitepress` | Vue-based docs framework | https://vitepress.dev |
| `swagger-ui` | Try-it-out reference UI | https://swagger.io/tools/swagger-ui/ |
| `redoc-cli` | Standalone Redoc renderer | https://github.com/Redocly/redoc |
| `widdershins` | OpenAPI → Markdown | https://github.com/Mermade/widdershins |
| `lychee` | Fast link checker | https://github.com/lycheeverse/lychee |
| `algolia docsearch` | Hosted docs search | https://docsearch.algolia.com |
| `oasdiff` | Generate breaking-change changelog | https://github.com/Tufin/oasdiff |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Mintlify | SaaS | yes | Git-driven, OpenAPI ingest, AI search built-in. |
| Readme.io | SaaS | partial | Hosted portal with Try-it; sync via CLI/CI. |
| Stoplight | SaaS / OSS | yes | Visual API design + hosted docs. |
| Bump.sh | SaaS | yes | Spec hosting + breaking-change diffing. |
| Redocly | SaaS / OSS | yes | OSS Redoc + paid platform with versioning. |
| Postman Public Docs | SaaS | partial | Auto-generated from collections; less control. |
| GitBook | SaaS | partial | Markdown-first; OpenAPI integration is weaker. |
| Algolia DocSearch | SaaS (free for OSS) | yes | Index your docs site for fast search. |

## Templates & scripts
See `templates.md` for OpenAPI metadata blocks and concept-page skeletons. Use this script to fail CI when an operation is missing critical docs:

```bash
#!/usr/bin/env bash
# openapi-doc-coverage.sh — every op needs summary, description, operationId, tags, examples.
set -euo pipefail
SPEC="${1:-openapi.yaml}"
python - "$SPEC" <<'PY'
import sys, yaml, re
spec = yaml.safe_load(open(sys.argv[1]))
fails = []
for path, item in (spec.get("paths") or {}).items():
    for method, op in (item or {}).items():
        if method.upper() not in {"GET","POST","PUT","PATCH","DELETE"}:
            continue
        loc = f"{method.upper()} {path}"
        for field in ("summary","description","operationId","tags"):
            if not op.get(field):
                fails.append(f"{loc}: missing {field}")
        rb = (op.get("requestBody") or {}).get("content") or {}
        for ct, body in rb.items():
            if not (body.get("examples") or body.get("example")):
                fails.append(f"{loc}: requestBody {ct} missing example")
if fails:
    print("\n".join(fails))
    sys.exit(1)
print("OK")
PY
```

## Best practices
- **Spec is the source.** Reference pages render from OpenAPI; prose pages live next to the spec; CI publishes both atomically.
- **Quickstart in 5 minutes.** A copy-paste curl + working response on the landing page; everything else is secondary.
- **Auth doc is its own concept page.** Walk through obtain, store, send, rotate, errors.
- **Examples per request body** with realistic-but-fake data; promote one as `default`. Run them through the schema in CI.
- **Per-language SDK snippets** generated from spec to stay in sync; never hand-write per-endpoint duplicates.
- **Errors fully documented.** Every code in the registry has a `type` URI resolving to a docs page with cause + remediation.
- **Rate limits and pricing tier callouts** in concept pages and sticky in reference pages.
- **Changelog** with semver tags, breaking-change banner, deprecation timeline. Auto-generate from `oasdiff` when feasible.
- **Versioned URLs** (`/v1/...`) and a banner on old versions linking to current.
- **Search that actually works.** Algolia DocSearch or Meilisearch beats theme defaults.
- **Try-it sandbox** with isolated test data; never wire to prod.
- **Webhooks page.** If you ship webhooks, doc the payload, signature scheme, retry policy, IP allowlist, and a tester URL.
- **Status page + uptime page.** Link prominently; reduces "is it me or you" tickets.
- **A11y + dark mode** in the docs theme; doc consumers spend hours reading.

## AI-agent gotchas
- **Hallucinated endpoints / fields.** Agent invents `/users/:id/profile` from "intuition." Always render from spec; reject prose endpoint references not in the spec.
- **Drift between snippet and schema.** Agent updates the schema but not the curl example. Validate examples against schema in CI.
- **Pasting real tokens / customer IDs.** Pre-commit grep for token regex.
- **Vague auth prose.** "Use your API key" with no example. Force the prompt to require obtain → store → send sequence.
- **Inconsistent terminology.** "User", "account", "member" used interchangeably. Maintain a glossary and lint for synonyms.
- **Localization mid-page.** Half-translated pages worse than English-only. Pick policy.
- **`Try it` defaults pointing at prod.** Default to sandbox; require explicit env switch.
- **Missing breaking-change callouts.** Renamed enum, removed field — `oasdiff` must run in CI; don't trust agents to remember.
- **Outdated rate-limit numbers.** When pricing changes, docs lag. Source numbers from a single config file referenced in the docs.
- **Heavy screenshots without alt text.** A11y fails; `lychee --accept` ignores image alts. Mandate alt text in markdown lint.
- **Code blocks without language tag.** No syntax highlight; SEO hurt. Lint for fenced blocks.
- **Webhooks documented but no signature verification snippet.** Provide working code per language; otherwise integrators skip it.

## References
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- Redoc: https://redocly.com/docs/redoc/
- Swagger UI: https://swagger.io/tools/swagger-ui/
- Mintlify: https://mintlify.com/docs
- Stripe API docs (gold standard): https://stripe.com/docs/api
- GitHub REST API docs: https://docs.github.com/en/rest
- Algolia DocSearch: https://docsearch.algolia.com
- Sibling methodologies: `solo/dev/api-developer/api-openapi-spec/`, `solo/dev/api-developer/api-rest-design/`, `solo/dev/api-developer/api-error-handling/`, `solo/dev/api-developer/api-contract-first/`.
