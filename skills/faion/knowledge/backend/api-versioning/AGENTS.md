# API Versioning

## Summary

**One-sentence:** Versions a REST API only on breaking changes via URL path (/api/vN), runs N and N-1 simultaneously, emits Deprecation/Sunset headers, and enforces sunset with 410 Gone.

**One-paragraph:** Versions a REST API only on breaking changes via URL path (/api/vN), runs N and N-1 simultaneously, emits Deprecation/Sunset headers, and enforces sunset with 410 Gone. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Public API has external consumers that cannot be redeployed in lockstep (partners, mobile, third-party).
- Pending change is breaking: renamed/removed field, type change, new required input.
- Long-tail clients (mobile apps shipped to stores >12 months ago) still hit production.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Public API has external consumers that cannot be redeployed in lockstep (partners, mobile, third-party).
- Pending change is breaking: renamed/removed field, type change, new required input.
- Long-tail clients (mobile apps shipped to stores >12 months ago) still hit production.

## Skip If (ANY kills it)

- Internal API with a single consumer redeployed atomically — backward-compatible fields beat versions.
- Pending change is additive (new field, new optional input, new endpoint) — never bump a version.
- GraphQL API — use @deprecated + persisted queries instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OpenAPI spec at HEAD | openapi.yaml/json | repository |
| OpenAPI spec at main | openapi.yaml/json | git show main:openapi.yaml |
| Sunset policy | .aidocs/api/sunset.yaml | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-rest-design]] | REST contract conventions this versioning sits on top of |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-version-bump` | sonnet | Apply additive-first rule + read oasdiff report. |
| `draft-v2-router` | sonnet | Mechanical: copy v1 handler to v2 module + edit response shape. |
| `draft-deprecation-headers` | haiku | Boilerplate Deprecation/Sunset/Link header middleware. |

## Templates

| File | Purpose |
|------|---------|
| `templates/versioned_router.py` | FastAPI v1/v2 router scaffold with frozen v1 module |
| `templates/oasdiff-ci.sh` | CI breaking-change gate: oasdiff diff + .changelog-pending enforcement |
| `templates/_smoke-test.py` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-versioning.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[api-rest-design]]
- [[api-authentication]]
- [[api-rate-limiting]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the pending change a breaking semantic change?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
