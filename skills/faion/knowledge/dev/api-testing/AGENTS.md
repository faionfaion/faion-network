# API Testing

## Summary

**One-sentence:** Organizes API tests as a pyramid (unit → integration with OpenAPI schema validation → cross-team Pact contracts → minimal E2E) and gates OpenAPI breaking changes in CI.

**One-paragraph:** Produces an API test suite plus the CI gate that enforces it. Many unit tests, fewer integration tests run against TestClient/httpx that always validate the response body against the OpenAPI schema (status code alone is not enough), targeted Pact contract tests only where teams or services interact, and the smallest possible number of end-to-end tests. CI snapshots `openapi.json` per PR and uses `oasdiff` to classify changes as breaking vs non-breaking before merge.

**Ефективно для:** REST/JSON API команд, що шиплять часто й потребують детермінованої регресії плюс стабільних споживацьких контрактів.

## Applies If (ALL must hold)

- The service exposes a REST/JSON API with an OpenAPI document (drf-spectacular, FastAPI auto-generated, or hand-maintained).
- A test runner is in place (pytest, jest, vitest).
- CI can post per-PR artifacts (the openapi.json snapshot).
- At least one downstream consumer exists OR a public spec must remain stable.

## Skip If (ANY kills it)

- Internal-only RPC with a single consumer co-deployed (no need for Pact; inline tests suffice).
- GraphQL-only API — different validation tooling; load a GraphQL-specific methodology instead.
- Prototype phase where the schema is still volatile (defer the contract gate until schema freeze).
- Service has no OpenAPI document AND cannot have one — the methodology core relies on schema-validated assertions.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `openapi.json` (or `.yaml`) | OpenAPI 3.x | drf-spectacular / FastAPI / hand-maintained |
| Test runner config | TOML/JSON | repo root |
| List of cross-team consumers | YAML | service catalog / team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/code-coverage` | Coverage gate this suite plugs into. |
| `free/dev/software-developer/django-pytest` | Runner pattern when the API is Django/DRF. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: pyramid shape, schema-validated bodies, Pact only at boundaries, oasdiff in CI, response-schema fixtures, Schemathesis fuzzing | ~1100 |
| `content/02-output-contract.xml` | essential | Schema for the produced test-suite report (counts per layer, schema-coverage %, oasdiff classification) | ~800 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: status-code-only asserts, schema drift, E2E inversion, in-app Pact, snapshot-only, untested 4xx paths | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: layer audit → schema-validate → oasdiff CI → Pact boundary → fuzzing | ~700 |
| `content/06-decision-tree.xml` | essential | Where each new test goes (unit / integration / contract / E2E) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author integration tests with schema validation | sonnet | Mechanical, deterministic. |
| Design Pact contracts at team boundaries | opus | Needs API-design judgement. |
| Wire oasdiff CI step | sonnet | Configuration. |
| Triage Schemathesis fuzz findings | opus | Root-cause judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/api-contract-check.sh` | Pre-merge CI step: snapshot openapi.json, run oasdiff against base, fail on breaking change. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-testing.py` | Validates the produced test-suite report against `02-output-contract.xml`. | After running the test suite, before publishing the report artifact. |

## Related

- [[code-coverage]] — coverage gate.
- [[django-api]] — DRF API patterns this suite tests.
- [[code-review]] — PR review pattern that consumes the report.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes each new test into one of {unit, integration-with-schema, contract, E2E} from observable inputs (does it touch I/O? does it cross a team boundary?), so the suite stays pyramid-shaped over time.
