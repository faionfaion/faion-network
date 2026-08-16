# Consumer Contract Tests Generated from OpenAPI / Traffic

## Summary

**One-sentence:** Point an MCP server or skill at the canonical artifact (OpenAPI / recorded HTTP traffic / typed client) to generate consumer Pact files plus matching client tests, committed as the source of truth and never hand-edited.

**One-paragraph:** Pact consumer contracts have one classic weakness: the consumer team has to write them, and when an LLM hand-rolls Pact JSON it drifts from the actual provider spec, making can-i-deploy noise. The fix is to generate the consumer Pact file from a canonical source (OpenAPI, recorded HTTP traffic, or typed client code) plus the matching client test. The generated contract is committed and never edited by hand. PactFlow reports up to 60% reduction in test creation time and the AI-generated contracts are deterministic enough to gate provider deploys with can-i-deploy.

**Ефективно для:**

- Microservices fleet, де consumer и provider deploy independently.
- OpenAPI-first projects: можна генерувати contracts механічно.
- PactFlow / Pact Broker users, що хочуть AI-assist без drift.
- Legacy services з recorded traffic як source-of-truth.

## Applies If (ALL must hold)

- Microservices repo where consumer and provider deploy independently.
- Canonical artifact exists: OpenAPI, gRPC proto, recorded HTTP traffic, or typed client.
- PactFlow / Pact Broker already wired into CI for can-i-deploy.

## Skip If (ANY kills it)

- Monolith with one process — no consumer/provider boundary.
- No canonical spec yet — write the OpenAPI first.
- Team enforces contracts by code-review only, no Pact infra.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OpenAPI spec or traffic capture | YAML / HAR | provider repo |
| PactFlow / Pact Broker creds | API token | 1Password |
| Client test framework | config (pytest/jest) | consumer repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/canigo-deploy.yml` | CI workflow that runs the generator and gates merge on Pact `can-i-deploy`. |
| `templates/pactflow-mcp-prompt.txt` | Prompt template for invoking PactFlow MCP generator with the pinned source. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-consumer-contract-from-spec.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[test-mutation-feedback-loop]]
- [[test-property-based-llm-invariants]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/canigo-deploy.yml`

```yaml
# Provider release pipeline step: gate deploy on can-i-deploy.
# Drop into .github/workflows/release.yml AFTER tests pass and BEFORE any push/publish.

- name: can-i-deploy
  env:
    PACT_BROKER_BASE_URL: ${{ secrets.PACT_BROKER_BASE_URL }}
    PACT_BROKER_TOKEN: ${{ secrets.PACT_BROKER_TOKEN }}
  run: |
    npx --yes @pact-foundation/pact-cli can-i-deploy \
      --pacticipant "${PROVIDER_NAME}" \
      --version "${{ github.sha }}" \
      --to-environment production \
      --retry-while-unknown 6 \
      --retry-interval 10

- name: publish image
  if: success()
  run: |
    docker push "${REGISTRY}/${PROVIDER_NAME}:${{ github.sha }}"

- name: record-deployment
  if: success()
  env:
    PACT_BROKER_BASE_URL: ${{ secrets.PACT_BROKER_BASE_URL }}
    PACT_BROKER_TOKEN: ${{ secrets.PACT_BROKER_TOKEN }}
  run: |
    npx --yes @pact-foundation/pact-cli broker record-deployment \
      --pacticipant "${PROVIDER_NAME}" \
      --version "${{ github.sha }}" \
      --environment production
```

### `templates/pactflow-mcp-prompt.txt`

```text
# PactFlow MCP / skill prompt fragment for generating consumer Pacts.
# Inputs: OPENAPI_PATH, CONSUMER, PROVIDER, OUT_PATH, LANG (ts|py|java).
# Output: pact JSON at OUT_PATH plus a matching client test file under tests/contract/.
# Run via: pactflow-mcp generate (or invoke the Pact AI skill with the same args).

ROLE: You generate a CONSUMER Pact contract and matching client test from an OpenAPI spec.
INPUT:
  - OpenAPI: ${OPENAPI_PATH}
  - Consumer name: ${CONSUMER}
  - Provider name: ${PROVIDER}
  - Output Pact path: ${OUT_PATH}
  - Output client test language: ${LANG}

RULES:
  1. Use the spec as the single source of truth for paths, methods, status codes, schemas.
  2. For every endpoint the consumer actually calls (resolve from imports/usages in the
     consumer codebase), emit one interaction.
  3. Use schema-aware matchers (term, regex, like) — NEVER literal-only bodies.
  4. Add explicit provider states only when the spec includes example values you can map.
  5. Emit the client test in ${LANG} using the project's existing test framework
     (jest/pytest/junit) and the official Pact DSL for that language.
  6. Do NOT invent endpoints not in the spec. Fail loudly if the consumer code references
     an endpoint missing from the spec.

OUTPUT:
  - ${OUT_PATH} (committed)
  - tests/contract/${CONSUMER}-${PROVIDER}.test.${LANG} (committed)
  - One-line summary printed to stdout: "<N> interactions, <M> matchers, <K> states".
```
