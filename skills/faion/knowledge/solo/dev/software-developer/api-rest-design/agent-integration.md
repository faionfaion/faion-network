# Agent Integration — REST API Design

## When to use
- Designing a new HTTP API surface from scratch (greenfield service, internal microservice, public SaaS).
- Adding endpoints to an existing API where naming, status codes, and pagination must stay consistent across teams.
- Auditing an inconsistent API to refactor toward Richardson Level 2/3 maturity before publishing SDKs.
- Generating server stubs and SDKs from a spec (pairs with `api-contract-first` and `api-openapi-spec`).
- LLM agents drafting endpoint sets from a domain model — gives a fixed grammar so output is deterministic and reviewable.

## When NOT to use
- Asynchronous, event-driven flows where Webhook + Pub/Sub is a better fit (use AsyncAPI, not REST).
- Streaming, large bidirectional payloads, ultra-low latency — gRPC, WebSocket, or SSE are better.
- Complex graph traversal queries with N+1 fan-out — GraphQL beats REST for client-driven shape selection.
- Internal RPC between services that share an owner — overhead of resource modeling is wasted; use protobuf RPC.
- Hyper-tailored mobile responses where round-trip count matters — consider BFF or GraphQL.

## Where it fails / limitations
- "RESTful" is under-specified: teams diverge on PUT vs PATCH semantics, on 404 vs 410, on whether 200 with `errors[]` is acceptable.
- Resource modeling fails for verb-heavy actions (`/sendEmail`, `/refundCharge`). Forcing them into `POST /actions/<verb>` ages badly.
- Bulk operations are not standardized — every API invents its own batch endpoint, and idempotency under partial failure is hard.
- Pagination is not part of the spec; offset, cursor, and link-header styles all coexist and break clients silently.
- HATEOAS is rarely consumed by clients; building Level 3 hypermedia is mostly wasted effort outside of niche domains.
- Error shape is unstandardized (RFC 7807 / Problem+JSON helps but is not universal); LLM clients struggle to parse heterogeneous error bodies.
- Versioning strategy (URL, header, media type) leaks into design and forces tradeoffs no individual endpoint can fix.

## Agentic workflow
Drive REST design as a three-pass loop. Pass 1: a domain-modeling agent maps entities, relationships, and aggregates from the spec/PRD into a resource tree. Pass 2: an endpoint-generator agent produces a matrix of `(resource, verb, status code, request schema, response schema)` rows, applying the rules table from `README.md`. Pass 3: a critic agent runs the `checklist.md` items against the matrix (plural nouns, idempotency claim valid, 201+`Location`, no verbs in path) and rejects rows that fail. Persist the result as an OpenAPI 3.1 file, then hand to `api-contract-first` for stub generation. Re-run pass 3 on every diff.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — owns REST conformance as a quality gate inside SDD task execution; rejects PRs whose new endpoints fail the checklist.
- A purpose-built **rest-design-critic** subagent (worth creating): system prompt = the rules table + status-code table; only output is `pass | fail + reasons[]`. Cheap (haiku) and runs on every diff.
- `/faion` (sdd-batch-orchestrator workflow) (skill) — sequences design → spec → stub → impl → contract test for each new endpoint as ordered SDD tasks.
- `password-scrubber-agent` — scrub example payloads in the spec before publishing publicly; example bodies often leak real customer IDs and tokens.

### Prompt pattern
Resource enumeration:
```
You are a REST API designer. Given the domain model in <model>, output
a resource tree as nested bullets. For each resource: list HTTP methods
that are valid, the request body schema, the success status code, and
1-2 expected error codes. Use plural lowercase nouns with hyphens. No
verbs in paths. Cite the rule from rest-api-design/README.md for any
non-obvious choice.
```

Critic pass:
```
For each row in the endpoint matrix, return PASS or FAIL with rule ID:
- R1 plural noun, R2 lowercase + hyphen, R3 idempotency matches verb,
- R4 201 includes Location, R5 4xx vs 5xx semantics correct,
- R6 no verbs in path, R7 query params for filter not subpaths.
Output a markdown table.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `spectral` | Lint OpenAPI for naming, status, response shape rules | `npm i -g @stoplight/spectral-cli` ; https://stoplight.io/open-source/spectral |
| `redocly` | Lint + preview docs from spec | `npm i -g @redocly/cli` ; https://redocly.com/docs/cli/ |
| `oasdiff` | Detect breaking changes between spec versions | https://github.com/Tufin/oasdiff |
| `openapi-generator` | Generate stubs/clients in 50+ languages | https://openapi-generator.tech/ |
| `httpie` / `xh` | Hand-test endpoints during design loop | `brew install httpie` / `cargo install xh` |
| `vacuum` | Fast OpenAPI linter (Go), pluggable rules | https://quobix.com/vacuum/ |
| `prism` | Mock server from OpenAPI spec, contract validation | `npm i -g @stoplight/prism-cli` |
| `gh` CLI | Open issues for design rule violations directly from critic agent output | https://cli.github.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight Studio | SaaS + desktop | Partial — API + Spectral CLI | Visual designer; agents drive via Spectral rules. |
| SwaggerHub | SaaS | Yes — REST API | Hosted spec governance + style guides. |
| Postman | SaaS | Yes — REST API + CLI (`newman`) | Spec import + contract test runs in CI. |
| Bump.sh | SaaS | Yes — CLI + API | Diff and document specs over time; good for change review. |
| Redocly | SaaS + OSS CLI | Yes | Style guides ship as JSON; agents can extend. |
| Apicurio | OSS | Yes | Self-hosted spec registry. |
| Hoppscotch | OSS | Yes — CLI | Lightweight Postman alternative; scriptable. |
| ReadMe.com | SaaS | Yes — API | Published docs from spec; supports recipes. |

## Templates & scripts
See `templates.md` and `examples.md` in this dir for endpoint matrices and example specs. Inline lint-on-commit (≤50 lines):

```bash
#!/usr/bin/env bash
# rest-lint.sh — fail commit if new/changed paths violate REST rules.
set -euo pipefail
spec="${1:-openapi.yaml}"
[[ -f "$spec" ]] || { echo "spec not found: $spec"; exit 2; }

# 1. Spectral with strict ruleset.
npx --yes @stoplight/spectral-cli lint "$spec" \
  --ruleset https://unpkg.com/@stoplight/spectral-rulesets@latest/dist/oas/index.json \
  --fail-severity=warn

# 2. Custom checks: plural nouns, no verbs, hyphens-only.
python3 - "$spec" <<'PY'
import re, sys, yaml
spec = yaml.safe_load(open(sys.argv[1]))
errs = []
verbs = {"get","create","update","delete","fetch","list","find","make","do"}
for path in spec.get("paths", {}):
    segs = [s for s in path.split("/") if s and not s.startswith("{")]
    for s in segs:
        if "_" in s: errs.append(f"{path}: underscore in segment '{s}'")
        if s != s.lower(): errs.append(f"{path}: non-lowercase '{s}'")
        if s.lower() in verbs: errs.append(f"{path}: verb in path '{s}'")
        # Crude singular check: warn when last char != 's' and not opaque id.
        if s == segs[-1] and not s.endswith("s") and len(s) > 3:
            errs.append(f"{path}: possibly singular collection '{s}'")
for e in errs: print("REST-LINT:", e)
sys.exit(1 if errs else 0)
PY
```

Wire into pre-commit so style drift never lands on `main`.

## Best practices
- Pick one pagination style (cursor recommended) and embed it into the style guide; ban offset for any list expected to grow past ~10k rows.
- Standardize error bodies on RFC 7807 (Problem Details) — fixed `type`, `title`, `status`, `detail`, `instance`. LLM clients can parse this reliably.
- Reserve POST for unsafe non-idempotent creation; use PUT for "create-or-replace at known URL", PATCH (with JSON Merge Patch or JSON Patch — pick one and document) for partial.
- Always return the canonical resource representation on POST/PUT/PATCH — saves a round-trip and makes clients deterministic.
- Use 422 for semantic validation, 400 only for malformed syntax. Tools like FastAPI default this correctly; preserve the convention.
- Encode versioning in URL prefix (`/v1/...`) for public APIs; header-based versioning is harder for caches and CDNs and confuses agents.
- Document idempotency with `Idempotency-Key` header on POSTs that mutate; otherwise retries during partial failures will double-charge / double-create.
- Treat the OpenAPI spec as the source of truth and generate the rest. Hand-written docs drift; generated SDKs and contract tests do not.

## AI-agent gotchas
- LLMs default to verb-style endpoints (`POST /createUser`) because that mirrors function names in their training data. Force the resource-noun convention in the system prompt and reject violations.
- Agents under-use 4xx vs 5xx distinction — they will return 500 for validation errors. Provide the status-code table as part of the prompt.
- Agents invent custom error envelopes per endpoint. Lock the error schema (Problem+JSON) in the spec and reference it from every operation.
- Pagination drift: agents pick `offset/limit` for some endpoints and `cursor` for others within the same spec. Enforce one style at the style-guide level.
- Idempotency claims hallucinated: agents tag PATCH as idempotent because it "feels safe". Cross-check by code-generating a property test that calls the endpoint twice and diffs state.
- Long-running operations: agents respond with 200 + "in progress" body instead of 202 + status URL. Add the LRO pattern (RFC 7240, `Prefer: respond-async`) to the prompt.
- Bulk endpoints: agents emit `POST /users` with array body, breaking the singular-vs-collection contract. Force `POST /users:batchCreate` (Google AIP-136) or a separate `/batch` resource.
- Human-in-loop checkpoint: schema breaking changes (field removed, type narrowed, required added) must be human-approved. Run `oasdiff breaking` in CI and fail-close.
- Agents skip the `Location` header on 201 responses because the SDK templates do; add a Spectral rule that fails when 201 is missing `headers.Location`.

## References
- Roy Fielding — "Architectural Styles and the Design of Network-based Software Architectures" (2000), Ch. 5. https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- Microsoft REST API Guidelines — https://github.com/microsoft/api-guidelines
- Google API Improvement Proposals (AIPs) — https://google.aip.dev/
- Zalando RESTful API and Event Guidelines — https://opensource.zalando.com/restful-api-guidelines/
- Richardson Maturity Model — https://martinfowler.com/articles/richardsonMaturityModel.html
- RFC 7807 (Problem Details for HTTP APIs) — https://datatracker.ietf.org/doc/html/rfc7807
- RFC 5789 (PATCH) and RFC 7396 (JSON Merge Patch) — https://datatracker.ietf.org/doc/html/rfc7396
- Sibling methodologies in this repo: `api-contract-first/`, `api-openapi-spec/`, `api-versioning/`, `api-error-handling/`, `api-rate-limiting/`, `rest-api-design/`.
