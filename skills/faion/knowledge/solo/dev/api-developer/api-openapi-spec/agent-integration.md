# Agent Integration — OpenAPI Specification

## When to use
- HTTP / REST APIs that need a machine-readable contract for codegen, mocking, contract testing, and reference docs.
- Multi-language SDK distribution where TS / Python / Go / Java clients regenerate from a single source on each release.
- Public APIs where developer adoption depends on Swagger UI / Redoc / Mintlify-rendered reference docs.
- Internal API platforms standardizing on contract-first development with `oasdiff`-enforced compatibility.
- Agentic backend authoring — a strict OpenAPI spec is the most reliable scaffolding for LLMs to extend without hallucinating endpoints / fields.

## When NOT to use
- gRPC / Protobuf services — use `.proto` + `buf` instead; OpenAPI shoehorned around RPC fights tooling.
- AsyncAPI / event-driven systems — use AsyncAPI 2.x/3.x for Kafka, MQTT, WebSocket message envelopes.
- GraphQL — use the GraphQL SDL and tools like `graphql-codegen`; a partial OpenAPI overlay adds confusion.
- Highly volatile experimental endpoints — generating clients from each iteration is overhead; freeze the contract before publishing.

## Where it fails / limitations
- **Spec rot.** Code outpaces spec; clients break silently. Mitigation: contract tests (`schemathesis`/`dredd`) and `oasdiff` in CI.
- **OpenAPI 3.0 vs 3.1 mismatch.** Generators / linters trail; some tools only support 3.0. Pin a version per service.
- **Polymorphism quirks.** `oneOf` + `discriminator` is the only reliable polymorphism pattern; `anyOf` / `allOf` mixes confuse generators.
- **Nullable inconsistency.** OpenAPI 3.1 follows JSON Schema (`type: [string, "null"]`); 3.0 uses `nullable: true`. Mixing breaks codegen.
- **Inline schema explosion.** Operations carry duplicated inline shapes; refactors miss one. Always `$ref` shared schemas.
- **Generator quality varies wildly** by language and target framework. `python-fastapi` generator output is rough; `typescript-axios` is solid; `go` is OK. Audit before commit.
- **Spec-as-docs only.** Teams ship spec but never use mocks / codegen / contract tests; spec becomes write-once.
- **`additionalProperties: true` default** allows unknown fields; later strict validation breaks clients.
- **Examples drift from schema.** Hand-edited examples violate the schema. Linters catch with `oas3-valid-media-example`.
- **Security scheme misuse.** Bearer / OAuth2 / API key all defined but only one used; spec confuses doc readers.
- **No multi-file structure.** A 5,000-line `openapi.yaml` is unmaintainable. Bundle via `redocly bundle` from `paths/` and `components/` shards.

## Agentic workflow
Drive OpenAPI work top-down: (1) a **structure-author** subagent shards spec into `paths/`, `components/schemas/`, `components/responses/`, `components/parameters/` and bundles via `redocly bundle`; (2) a **schema-author** subagent maintains `$ref`-only operations — every shape lives in `components/schemas`; (3) a **lint-and-diff** subagent runs `spectral` with project ruleset plus `oasdiff` against `main`; (4) a **codegen-orchestrator** regenerates clients/server stubs, mocks, docs; (5) a **contract-tester** runs `schemathesis` against the running impl. `faion-sdd-executor-agent` runs lint/build/test gates. Forbid hand-edited inline schemas via lint; treat spec as the source of truth.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate: lint, bundle, codegen, contract tests.
- A purpose-built **spec-bundler** — runs `redocly bundle paths/_root.yaml -o openapi.yaml` and commits a single deployable file alongside the source shards.
- A **spec-linter** — runs `spectral` with custom rules (no inline schemas, kebab-case paths, every operation has `operationId`/`summary`/`tags`/examples, error responses reference Problem Details).
- A **breaking-change-bot** — `oasdiff breaking` between PR head and `main`; posts changelog comment.
- A **discriminator-validator** — checks every `oneOf` has `discriminator.propertyName` mapping all variants.
- A **example-validator** — runs `examples.value` against schema; rejects mismatches.
- A **client-codegen** — re-runs `openapi-generator` for ts / python / go targets; commits to `generated/` dirs.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scans examples for tokens / PII.

### Prompt pattern
Schema authoring:
```
Add component schema CreateInvoiceRequest under components/schemas/.
Required: customerId (uuid), amount (integer, min 1), currency
(enum USD/EUR/GBP), lineItems (array, min 1, max 100).
Optional: dueDate (date), memo (string, max 500), metadata
(additionalProperties: string, max 20 keys).
Provide one realistic example.
Reuse Money component if amount + currency repeat.
Output a unified diff against components/schemas/ only.
```

Operation wiring:
```
Add POST /invoices that accepts CreateInvoiceRequest, returns
201 + Invoice + Location header. Errors:
- 400 ValidationError (Problem Details, code VALIDATION_ERROR)
- 402 PaymentRequired (code TIER_LIMIT_REACHED)
- 409 IdempotencyConflict (code IDEMPOTENCY_KEY_REUSED)
Require Idempotency-Key header (component parameter ref).
Tag: Invoices. operationId: createInvoice.
Output diffs only to paths/invoices.yaml.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `redocly` | Lint, bundle, build static docs | https://redocly.com/docs/cli |
| `spectral` | Lint with built-in + custom rules | https://stoplight.io/open-source/spectral |
| `swagger-cli` | Validate + bundle | https://github.com/APIDevTools/swagger-cli |
| `openapi-generator-cli` | Multi-language codegen | https://openapi-generator.tech |
| `openapi-typescript` | TypeScript types from spec | https://github.com/drwpow/openapi-typescript |
| `openapi-fetch` | Typed fetch client from `openapi-typescript` types | https://github.com/drwpow/openapi-typescript |
| `oasdiff` | Breaking-change detection | https://github.com/Tufin/oasdiff |
| `schemathesis` | Property-based contract tests | https://schemathesis.readthedocs.io |
| `prism` | Mock server + proxy validation | https://stoplight.io/open-source/prism |
| `mockoon` | Local mock | https://mockoon.com |
| `vacuum` | Fast OpenAPI linter (Go) | https://quobix.com/vacuum/ |
| `optic` | API change tracking + diff CI | https://www.useoptic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight Studio | SaaS / Desktop | partial | Visual editing; export YAML. |
| SwaggerHub | SaaS | yes | Spec hosting + codegen + collab. |
| Bump.sh | SaaS | yes | Spec hosting + diff-driven changelog. |
| Redocly App | SaaS | yes | Hosted Redoc + workflow CI. |
| Apicurio Registry | OSS | yes | Schema registry for OpenAPI / Avro / Protobuf. |
| Speakeasy | SaaS | yes | High-quality SDK generation. |
| Fern | SaaS | yes | Spec-driven SDK + docs platform. |
| Mintlify | SaaS | yes | Doc framework with OpenAPI ingest. |
| Postman | SaaS | yes | Import OpenAPI; generate collections. |

## Templates & scripts
See `templates.md` for `openapi.yaml` skeleton, sharded layout, `.spectral.yaml` rules. Use this gate to keep `openapi.yaml` and source shards in sync:

```bash
#!/usr/bin/env bash
# openapi-bundle-check.sh — bundled output must equal sources.
set -euo pipefail
SRC="${1:-openapi/_root.yaml}"
OUT="${2:-openapi.yaml}"
TMP=$(mktemp)
npx --yes @redocly/cli@latest bundle "$SRC" -o "$TMP" >/dev/null
if ! diff -q "$TMP" "$OUT" >/dev/null; then
  echo "FAIL — $OUT is stale; run: redocly bundle $SRC -o $OUT"
  diff -u "$OUT" "$TMP" | head -200
  exit 1
fi
npx --yes @stoplight/spectral-cli lint "$OUT" --fail-severity=warn
npx --yes @redocly/cli@latest lint "$OUT"
echo "OK"
```

## Best practices
- **Shard sources** under `paths/`, `components/schemas/`, `components/responses/`, `components/parameters/`; bundle to a single `openapi.yaml` for tooling.
- **`$ref` everything reusable.** No inline schemas in operations beyond trivial enums.
- **Every operation:** `operationId`, `summary`, `description`, `tags`, request/response examples, error refs.
- **Common error responses** (`Unauthorized`, `Forbidden`, `NotFound`, `TooManyRequests`, `ValidationError`) live in `components/responses/` and are referenced from each operation.
- **Pin OpenAPI version** (3.1 if your toolchain supports JSON Schema 2020-12, otherwise 3.0).
- **Discriminator on `oneOf`** for tagged unions; ensure mapping covers every variant.
- **Examples per response.** Even 4xx — clients learn error shapes from realistic examples.
- **Server URLs** for prod / staging / sandbox; mark sandbox in description.
- **Security schemes** declared once and applied at operation or root level; document scopes for OAuth2.
- **Document deprecation** via `deprecated: true` and a `x-deprecation-date` extension; remove only on major version bump.
- **`oasdiff` in CI** plus a labeled `breaking-change` flag required to merge incompatible changes.
- **Contract tests** (`schemathesis run --checks=all`) against a running impl on every PR.
- **Codegen output committed** with `linguist-generated` attribute so reviewers can skip generated diffs.

## AI-agent gotchas
- **Inline schema duplication.** Agent inlines a `User`-shaped object instead of `$ref`. Lint blocks via custom rule.
- **3.0 vs 3.1 confusion.** Agent uses `nullable: true` in a 3.1 doc; tools accept it but it's deprecated. Pin and lint version.
- **`oneOf` without discriminator.** Generators emit unsafe types; runtime parsing breaks.
- **Examples that fail validation.** Agent writes `example: { ... }` violating the schema. `oas3-valid-media-example` rule catches.
- **Operations missing `operationId`.** Codegen produces `path_method` ugly names. Always require `operationId`.
- **`additionalProperties` default true.** Agent unknowingly allows unknown fields; later strictification breaks clients. Set explicitly.
- **Forgetting `Location` on 201.** Spec sample missing the header; client SDKs can't follow new resources.
- **Bundling from wrong root.** Agent bundles a `paths/users.yaml` rather than `_root.yaml`; output is partial.
- **Hand-editing bundled `openapi.yaml`.** Bundle script overwrites; agents lose edits. Edit only sources.
- **Multiple security schemes declared but only one applied.** Doc readers confused. Remove unused schemes.
- **Generator output drift.** Agent regenerates with a different generator version; massive diff. Lock version per service.
- **Polyglot anyOf.** Generators handle inconsistently; pick `oneOf` with discriminator or simplify.
- **Renaming fields with no deprecation.** `oasdiff` must run; without it, agents ship breaking changes.
- **Spec validates but server emits different shape.** Run `schemathesis` to catch impl drift.

## References
- OpenAPI Specification 3.1: https://spec.openapis.org/oas/v3.1.0
- OpenAPI Specification 3.0.x: https://spec.openapis.org/oas/v3.0.4
- OpenAPI Generator: https://openapi-generator.tech
- Spectral: https://stoplight.io/open-source/spectral
- Redocly CLI: https://redocly.com/docs/cli
- oasdiff: https://github.com/Tufin/oasdiff
- Schemathesis: https://schemathesis.readthedocs.io
- Stripe API spec: https://github.com/stripe/openapi
- GitHub OpenAPI: https://github.com/github/rest-api-description
- Sibling methodologies: `solo/dev/api-developer/api-rest-design/`, `solo/dev/api-developer/api-contract-first/`, `solo/dev/api-developer/api-documentation/`, `solo/dev/api-developer/api-versioning/`.
