# Agent Integration — Contract-First API Development

## When to use
- Multi-team / multi-language API platforms where producers (backend) and consumers (frontend, mobile, partner SDKs) develop in parallel from a shared OpenAPI / AsyncAPI / Protobuf contract.
- B2B partner integrations where the contract is a published, versioned artifact subject to change-management; agreement happens before code.
- LLM-driven backend authoring — agents thrive on a strict spec; codegen + contract tests catch drift before merge.
- Migration projects (legacy → modular monolith → microservices) where the spec freezes external behavior while internals change.
- SDK-distribution products (Stripe-like) where TypeScript / Python / Go clients must regenerate from one source on every release.

## When NOT to use
- Solo prototypes / spike code where the API is volatile and round-trip codegen overhead exceeds the design value.
- Teams without OpenAPI / Protobuf fluency — premature contracts written by non-fluent authors produce worse APIs than code-first iteration.
- Domains where the contract genuinely cannot be predicted (research / ML scoring with evolving outputs); use code-first + spec-export later.
- Internal scripts and one-shot integrations whose lifetime is shorter than the contract round-trip.

## Where it fails / limitations
- **Spec-impl drift.** Devs hand-edit handlers without updating the spec; clients and docs lag. Mitigation: contract tests in CI (`schemathesis`/`dredd`) plus `oasdiff` to fail breaking PRs.
- **Generated stub limitations.** `openapi-generator` output has rough edges per language (FastAPI Python generator does not match modern idioms). Treat generators as starting points, not final code.
- **Generator version churn.** Output changes between generator versions; lock the version, regenerate intentionally.
- **Spec-as-bottleneck.** Every change requires a spec PR + review; teams revert to ad-hoc fields. Mitigation: lightweight RFC review for non-breaking, full review for breaking.
- **Versioning paralysis.** Fear of breaking clients leads to spec freeze; introduce additive changes freely (new fields, new endpoints) with `oasdiff` enforcement.
- **Schema duplication.** Inline schemas across operations diverge subtly. Use `$ref` for every shared shape.
- **Mock-prod gap.** Mock servers (`prism`, `mockoon`) feed clients fake data that masks producer bugs. Pair mocks with contract tests against real implementation.
- **Polyglot codegen quirks.** Discriminated unions, `nullable: true`, allOf/oneOf/anyOf each have language-specific gotchas; agents pick patterns the generator handles poorly.
- **Spec format drift** between OpenAPI 3.0, 3.1, 3.2, AsyncAPI 2.x/3.x. Pin a version; document migration cost before bumping.
- **Contract for synchronous only.** REST/OpenAPI captures request/response; event payloads need AsyncAPI; gRPC needs Protobuf. Don't try to fit events into OpenAPI.

## Agentic workflow
Drive contract-first in five stages: (1) a **spec-author** subagent translates a feature brief into spec deltas (paths, schemas, security, error refs), opens a spec-only PR; (2) a **spec-linter** subagent runs `spectral` + custom REST/REST-style rules and `oasdiff` against `main` to flag breaking changes; (3) a **codegen-runner** subagent regenerates server stubs (commit `generated/` directory), client SDKs (one repo per language), mocks, and docs; (4) an **impl-author** subagent fills handler bodies, importing only generated models; (5) a **contract-tester** subagent runs `schemathesis` against the implementation, asserting every operation matches its 2xx/4xx/5xx schemas. Always merge spec PR first, codegen second, impl third — never mix in one PR. `faion-sdd-executor-agent` runs the standard quality gate at every step.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — runs lint/build/test gate plus contract tests.
- A purpose-built **spec-author** — produces openapi.yaml diffs from feature briefs, refusing to introduce inline schemas.
- A **spec-reviewer** — reviews spec PRs against project rules (kebab-case paths, plural resources, every error references Problem Details, every operation has examples).
- A **breaking-change-bot** — runs `oasdiff` between PR head and `main`; fails on incompatible changes, posts changelog comment.
- A **codegen-orchestrator** — re-runs `openapi-generator` for each target (server, ts-client, py-client, go-client) and commits to designated paths.
- A **mock-server-runner** — boots `prism mock openapi.yaml` for frontend agents during development.
- A **contract-fuzzer** — `schemathesis run --checks=all` against the running impl in CI.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scans spec examples for tokens / PII.

### Prompt pattern
Spec-only PR:
```
Add operation POST /payments/refund.
Schema:
- input: { paymentId: uuid (required), amount?: integer (cents), reason?: string }
- 200: Refund (id, paymentId, amount, status, createdAt)
- 4xx: reference components.responses.ProblemDetail (codes:
  PAYMENT_NOT_FOUND, REFUND_AMOUNT_EXCEEDS, REFUND_ALREADY_ISSUED).
Constraints:
- Reuse existing components (Refund, Payment).
- Add operationId=refundPayment.
- Tag: Payments. Idempotency-Key header required.
- Provide one realistic example per response.
Output a unified diff against openapi.yaml only.
```

Generator step:
```
Run openapi-generator-cli for:
- python-fastapi → ./server/generated
- typescript-axios → ./packages/ts-sdk/src/generated
- go → ./go-sdk/generated
With config templates from .openapi-generator/.
Commit only files under generated/ paths.
Print which generated files now differ from main and require
manual import-side updates (controllers, exports).
```

Impl step:
```
Implement the refund endpoint by extending the generated stub.
Constraints:
- Import only models from server/generated.
- All errors via ProblemDetail.from_code(...).
- Add idempotency check using Idempotency-Key header.
- Cover with pytest contract tests using schemathesis.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openapi-generator-cli` | Multi-language server + client codegen | https://openapi-generator.tech |
| `openapi-typescript-codegen` | Lightweight TS client codegen | https://github.com/ferdikoomen/openapi-typescript-codegen |
| `swagger-codegen` | Older codegen, still used in some shops | https://swagger.io/tools/swagger-codegen/ |
| `spectral` | Lint OpenAPI / AsyncAPI | https://stoplight.io/open-source/spectral |
| `redocly` | Lint + bundle + render | https://redocly.com/docs/cli |
| `oasdiff` | Breaking-change detection | https://github.com/Tufin/oasdiff |
| `schemathesis` | Property-based contract testing | https://schemathesis.readthedocs.io |
| `dredd` | Contract test runner against running API | https://dredd.org |
| `prism` | Mock server + proxy validation | https://stoplight.io/open-source/prism |
| `mockoon` | Local OpenAPI mock | https://mockoon.com |
| `buf` | Protobuf linting + breaking-change detection | https://buf.build |
| `connect-go` | Schema-first RPC framework over Protobuf | https://connectrpc.com |
| `asyncapi-cli` | Lint + render AsyncAPI specs | https://www.asyncapi.com/tools/cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight Studio | SaaS / Desktop | partial | Visual spec editing; export YAML for agents. |
| Bump.sh | SaaS | yes | Spec hosting + diff-based changelog. |
| SwaggerHub | SaaS | yes | Hosted spec versioning + codegen. |
| Speakeasy | SaaS | yes | Polished SDK generation from OpenAPI / AsyncAPI. |
| Fern | SaaS | yes | Spec-driven SDK + docs platform. |
| Apicurio Registry | OSS | yes | Schema registry for OpenAPI / Protobuf / Avro. |
| Buf Schema Registry | SaaS / OSS | yes | Protobuf-first registry; breaking-change CI. |
| Prism Cloud | SaaS | yes | Hosted mocks for distributed teams. |

## Templates & scripts
See `templates.md` for `openapi.yaml` skeleton, `.openapi-generator-ignore`, and CI workflow. Use this script to enforce spec-first commits:

```bash
#!/usr/bin/env bash
# spec-first-guard.sh — block PRs that change handlers without spec.
set -euo pipefail
BASE="${1:-origin/main}"
DIFF=$(git diff --name-only "$BASE"...HEAD)
HANDLERS=$(echo "$DIFF" | grep -E '^server/(routers|controllers|handlers)/' || true)
SPEC=$(echo "$DIFF" | grep -E '(^|/)openapi\.ya?ml$' || true)
GENERATED=$(echo "$DIFF" | grep -E '/generated/' || true)
if [ -n "$HANDLERS" ] && [ -z "$SPEC" ]; then
  echo "FAIL — handler change without openapi.yaml change."
  echo "Handlers changed:"; echo "$HANDLERS"
  exit 1
fi
if [ -n "$SPEC" ] && [ -z "$GENERATED" ]; then
  echo "FAIL — spec changed but generated/ not updated. Run codegen."
  exit 1
fi
echo "OK"
```

## Best practices
- **Spec PR before code PR.** Review and merge contract changes alone; never bundle with implementation.
- **Generated code is committed** but read-only — `.openapi-generator-ignore` lists hand-written extensions; CI verifies regeneration is a no-op.
- **Pin generator version** in CI; bump intentionally with a changelog entry covering output diffs.
- **`oasdiff` in CI** to flag breaking changes; require an explicit `breaking-change` label and bumped major version to merge.
- **Mock + contract tests** at every level: frontend devs hit `prism` mock; backend impl validated by `schemathesis` against the spec.
- **Schema component library.** Reuse `$ref`s for `User`, `Pagination`, `ProblemDetail`, `Money`, etc. Forbid inline duplicates.
- **Versioning policy** baked in: URL-versioned `/v1`, additive within version, deprecated fields tagged `deprecated: true` for ≥2 minor releases.
- **Examples per response.** Even 4xx — clients learn error shapes from realistic examples, not prose.
- **Linter ruleset committed** (`.spectral.yaml`); enforce in CI; add custom rules for project conventions (idempotency-key headers, problem-details refs, etc.).
- **One spec, one repo** for the source of truth. Mirror to a public docs repo on release.
- **Schema registry** when many specs share schemas (Apicurio, Buf); avoid copy-paste.
- **AsyncAPI for events.** Don't bend OpenAPI to describe events; use AsyncAPI alongside.

## AI-agent gotchas
- **Editing handlers without touching spec.** Spec-first guard script in pre-commit + CI.
- **Hand-editing `generated/`.** Disabled in `.gitattributes` linguist-generated, plus CI re-runs and diffs.
- **Inline schema duplication.** Agent inlines a `User`-shaped object inside `requestBody` instead of `$ref`. Reject in spec review.
- **Inventing fields not yet in spec.** Generated client SDK lacks the field; integration breaks. Always model in spec first.
- **Breaking change disguised as "fix".** Rename `userId` → `user_id`. `oasdiff` must run; without it, agents ship breaking changes.
- **Generator version drift across services.** Two services on different generator versions emit incompatible client types. Lock per-org.
- **`anyOf` / `oneOf` overuse.** Generators handle inconsistently; pick `oneOf` with discriminator for tagged unions, otherwise simplify.
- **Mock-only validation.** Frontend dev passes against `prism` but real impl mismatches. Always run contract tests against the impl.
- **Examples that fail validation.** Agent writes example payloads that break the schema (wrong enum, missing field). Validate examples in CI.
- **Forgetting `Idempotency-Key` headers** on POST that creates side effects; clients hit duplicate creation. Spec rule + handler middleware.
- **`additionalProperties: true` left default.** Spec accepts unknown fields silently; agents lean on this; later strictification breaks integrations. Decide policy at design time.
- **Spec for sync APIs only.** Event payloads documented in prose; consumers don't have a typed schema. Switch to AsyncAPI.
- **Stale CHANGELOG.** Generated changelog from `oasdiff` is more reliable than agent-written prose.

## References
- OpenAPI Specification 3.1: https://spec.openapis.org/oas/v3.1.0
- AsyncAPI: https://www.asyncapi.com
- OpenAPI Generator: https://openapi-generator.tech
- Spectral: https://stoplight.io/open-source/spectral
- oasdiff: https://github.com/Tufin/oasdiff
- Schemathesis: https://schemathesis.readthedocs.io
- Prism mock server: https://stoplight.io/open-source/prism
- buf (Protobuf-first contract management): https://buf.build
- Speakeasy SDK generation: https://www.speakeasy.com
- Sibling methodologies: `solo/dev/api-developer/api-openapi-spec/`, `solo/dev/api-developer/api-rest-design/`, `solo/dev/api-developer/api-versioning/`, `solo/dev/api-developer/api-documentation/`.
