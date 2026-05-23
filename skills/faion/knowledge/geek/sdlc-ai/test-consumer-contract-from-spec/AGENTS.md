---
slug: test-consumer-contract-from-spec
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a generator config + can-i-deploy pipeline that builds Pact consumer contracts deterministically from OpenAPI specs or recorded traffic instead of hand-written by an LLM.
content_id: "71b2655e3440b811"
complexity: medium
produces: code
est_tokens: 4200
tags: [pact, consumer-contract, openapi, can-i-deploy, microservices]
---
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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-consumer-contract-from-spec.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[test-mutation-feedback-loop]]
- [[test-property-based-llm-invariants]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
