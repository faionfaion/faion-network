# Agent Integration — API Documentation

## When to use
- Publishing a public or partner API where SDK adoption depends on copy-paste-able examples.
- Onboarding a new internal team to an existing service — docs become the contract.
- Generating reference docs from an OpenAPI / AsyncAPI spec as part of CI (no hand-curated reference pages).
- Producing language-specific quickstart guides from a single spec for multiple SDKs.
- LLM agents drafting docs from spec + source code — a strong skeleton (overview, quickstart, auth, endpoints, errors, SDKs, changelog) keeps output consistent.

## When NOT to use
- One-off internal scripts where a `README.md` with three curl commands is enough; full doc structure is overhead.
- Pre-spec exploration phase — docs written before the API stabilizes lie within a week and erode trust.
- Hyper-confidential APIs where examples cannot include realistic payloads (write design docs instead).
- Legacy SOAP / RPC surfaces where OpenAPI doesn't fit; pick a format that matches the protocol (WSDL, gRPC reflection).

## Where it fails / limitations
- Drift: hand-written docs lag the spec by days; the gap is invisible until users complain.
- Examples that don't compile / pass: agents and humans both write idealized snippets that never get executed; CI catches none of it unless explicitly enforced.
- Tone collapse: LLMs produce uniform marketing-grade prose that obscures gotchas; engineers stop reading.
- Versioning: maintaining v1 + v2 docs simultaneously is rarely automated; one version goes stale.
- Error coverage: docs document the happy path; 4xx/5xx scenarios and rate-limit behavior are skipped.
- Auth flows are reduced to a single Bearer line; OAuth, refresh, scopes, and rotation are under-documented.
- Search / discoverability: long flat pages (Swagger UI defaults) hide endpoints; users can't find what they need.
- SDK examples lag the SDK release; Python sample uses old client signature, etc.

## Agentic workflow
Drive doc generation as a four-stage pipeline. (1) A spec-extractor agent parses OpenAPI + source code into a normalized doc model (per endpoint: summary, params, request, responses, errors, auth, rate-limit). (2) An example-generator agent emits curl + Python + JS + Go snippets per endpoint. (3) A runner stage actually executes each curl/Python snippet against a Prism mock or staging env; failed snippets are rejected. (4) A narrative agent (sonnet) writes overview + quickstart + auth + changelog. Render with Redocly or Mintlify, deploy on every spec merge.

### Recommended subagents
- `faion-sdd-executor-agent` — gates merges on "every public endpoint has a working code sample in at least 3 languages".
- A purpose-built **example-runner** subagent (worth creating): given a code block, executes it against a sandbox; writes `pass | fail + diff`. Crucial for keeping docs honest.
- `/faion` (sdd-batch-orchestrator workflow) (skill) — sequences spec → docs → SDK update → changelog as one feature task chain.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — strip real tokens, customer IDs, internal hostnames before publishing.

### Prompt pattern
Endpoint reference generation:
```
You are a technical writer. Given the OpenAPI operation in <op>, write
a Markdown reference page with sections: Description (≤2 sentences),
Path & Method, Authentication, Path Params, Query Params, Request Body
(schema + JSON example), Responses (200/4xx/5xx + bodies), Rate Limit,
Error Codes (table), Code Samples (curl, Python, JS, Go). No prose
filler. Every example must be runnable as-is.
```

Quickstart synthesis:
```
Given the spec at <spec> and SDK at <sdk_repo>, produce a 5-step
quickstart: signup → key creation → first request → error handling →
next steps. Each step is ≤8 lines. Use real placeholder env vars
(API_KEY, BASE_URL). Verify each command actually runs against the
sandbox.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `redocly` | Lint + bundle + render OpenAPI to static site | `npm i -g @redocly/cli` ; https://redocly.com/docs/cli/ |
| `swagger-cli` | Validate + bundle multi-file OpenAPI | `npm i -g @apidevtools/swagger-cli` |
| `widdershins` | OpenAPI → Slate / Markdown | `npm i -g widdershins` |
| `mintlify` | Docs site from MDX + OpenAPI | `npm i -g mintlify` ; https://mintlify.com |
| `docusaurus` | Static docs site (with OpenAPI plugin) | `npx create-docusaurus@latest` |
| `prism` | Mock server for example execution | `npm i -g @stoplight/prism-cli` |
| `httpie` / `xh` | Lightweight curl alternative for sample testing | `brew install httpie` |
| `vale` | Prose linter for docs (style rules per repo) | https://vale.sh |
| `markdownlint-cli` | Lint Markdown structure / heading levels | `npm i -g markdownlint-cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ReadMe.com | SaaS | Yes — REST API + CLI | Hosted docs, recipes, "Try It" against live APIs. |
| Mintlify | SaaS + OSS CLI | Yes | MDX + OpenAPI; AI search; agent-driven publishing. |
| Stoplight (Elements / Studio) | SaaS + OSS | Yes — Spectral CLI | Tight Spectral integration. |
| Bump.sh | SaaS | Yes — CLI | Versioned spec hosting + diff. |
| Redocly Workflows | SaaS | Yes — API | Spec governance + hosted reference. |
| GitBook | SaaS | Partial — API | Strong narrative; weaker for spec-driven reference. |
| Docusaurus + redocusaurus | OSS | Yes | Self-hosted; agents can PR new pages. |
| Slate | OSS | Yes | Three-column docs (description / sample / response); pairs well with widdershins. |
| Postman | SaaS | Yes — API | Auto-publishes collections as docs; supports examples. |
| Theneo | SaaS | Yes | AI-first API doc generator. |

## Templates & scripts
See `templates.md` and `examples.md` in this dir. Inline doc-freshness check (≤50 lines):

```bash
#!/usr/bin/env bash
# docs-freshness.sh — fail if any operation in the spec lacks
# (a) summary, (b) at least one example response, (c) curl sample.
set -euo pipefail
spec="${1:-openapi.yaml}"
python3 - "$spec" <<'PY'
import sys, yaml, json, pathlib
data = yaml.safe_load(open(sys.argv[1]))
errs = []
for path, ops in data.get("paths", {}).items():
    if not isinstance(ops, dict): continue
    for verb, op in ops.items():
        if verb not in {"get","post","put","patch","delete"}: continue
        opid = op.get("operationId", f"{verb} {path}")
        if not op.get("summary"): errs.append(f"{opid}: missing summary")
        responses = op.get("responses", {})
        ok = next((r for c,r in responses.items() if str(c).startswith("2")), {})
        ex = ok.get("content",{}).get("application/json",{}).get("examples")
        if not ex: errs.append(f"{opid}: no JSON example on 2xx response")
        # Look for an x-codeSamples block (Redocly convention).
        if not op.get("x-codeSamples"):
            errs.append(f"{opid}: missing x-codeSamples (curl/python/js)")
for e in errs: print("DOC-FRESH:", e)
sys.exit(1 if errs else 0)
PY
```

Combine with a runner that executes every `x-codeSamples` snippet against a Prism mock and rejects non-zero exits.

## Best practices
- Treat the spec as the source of truth and generate reference docs from it on every merge — never hand-edit reference pages.
- Run every code sample in CI. Examples that don't execute are worse than no examples.
- Show errors prominently. Document `429` retry-after, `409` conflict resolution, idempotency keys, and pagination boundaries.
- Provide a "first 5 minutes" quickstart that produces a real, observable side effect (e.g., a SMS sent, a webhook delivered) — abstract examples lose users.
- Keep a curated, hand-written narrative layer (overview, concepts, auth flow) on top of generated reference. Generated-only docs read like catalogs.
- Version docs with the API. URL like `/docs/v2/...`. Deprecated endpoints stay visible with a banner pointing to the replacement.
- Maintain a machine-readable changelog (`changelog.json` or Keep a Changelog format). LLM clients use it to migrate.
- Include rate limits, quotas, and SLOs on every endpoint — clients code retry behavior off this.

## AI-agent gotchas
- LLMs hallucinate fields that don't exist in the spec; they invent plausible response bodies. Always derive examples from the spec schema, not from the prompt.
- Agents copy stale curl examples between endpoints (same payload across `/users` and `/orders`). Force per-operation example generation, not template fill-in.
- Tone homogeneity: LLM-written docs all sound the same; users skim and miss warnings. Inject explicit "Caution:" / "Pitfall:" blocks during generation and require ≥1 per high-risk endpoint.
- Examples leak real data: agents copy from staging traces and expose tokens. Run scrubber after generation.
- Versioning collapse: agents merge v1 and v2 examples into one page. Lock the agent context to a single version per run.
- Auth flows under-documented: agents stop at "send Bearer header"; never explain refresh/scope/rotation. Mandate a dedicated Authentication page section with sequence diagram (Mermaid) per flow.
- Stale SDK references: agents cite old method names. Pin the SDK commit hash in the prompt and re-render docs whenever the SDK ships a new release.
- Human-in-loop checkpoint: any breaking-change note in the changelog must be human-approved before publishing — agents are too eager to declare "minor".
- Agents skip the `Errors` section because spec lacks examples; require error examples in the spec itself, then docs follow automatically.

## References
- Diátaxis framework — https://diataxis.fr (tutorial / how-to / reference / explanation distinction).
- "Docs Like Code" — Anne Gentle. https://www.docslikecode.com
- Stripe API docs — https://stripe.com/docs/api (gold standard for SaaS API reference).
- Twilio docs structure — https://www.twilio.com/docs (quickstart pattern).
- OpenAPI Specification 3.1 — https://spec.openapis.org/oas/latest.html
- Write the Docs community — https://www.writethedocs.org
- Redocly style guide — https://redocly.com/docs/style-guides/
- Sibling methodologies in this repo: `api-rest-design/`, `api-contract-first/`, `api-openapi-spec/`, `api-versioning/`, `openapi-specification/`.
