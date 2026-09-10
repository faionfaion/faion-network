# GraphQL API Design

## Summary

**One-sentence:** Designs a GraphQL service schema-first: Relay cursor pagination, per-request DataLoaders, mutation payloads with typed error unions, and depth/complexity limits.

**One-paragraph:** Designs a GraphQL service schema-first: Relay cursor pagination, per-request DataLoaders, mutation payloads with typed error unions, and depth/complexity limits. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- New GraphQL service designed schema-first with SDL reviewed by humans + consumed by codegen.
- Multiple distinct clients (web, mobile, partner) need different shapes of the same domain.
- Schema has nested reads with field-level auth (SaaS dashboards with org/role).
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- New GraphQL service designed schema-first with SDL reviewed by humans + consumed by codegen.
- Multiple distinct clients (web, mobile, partner) need different shapes of the same domain.
- Schema has nested reads with field-level auth (SaaS dashboards with org/role).

## Skip If (ANY kills it)

- Public cacheable read API — REST + CDN wins.
- Single-client, single-team CRUD with no nested reads — overhead of DataLoader + depth/complexity not paid back.
- File upload / streaming-binary workloads — use REST or gRPC.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain entity model | diagram or doc | team |
| Client query mock list | *.graphql samples | frontend |
| Auth/permission model | table of roles → fields | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[api-rest-design]] | Some clients may also need REST endpoints next to GraphQL |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 testable rules (payload+userErrors, directive auth, naming, opaque IDs, run + skip leaves) with rationale + source | 1800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden patterns + allowed transformations | 1200 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns with symptom + root-cause + fix | 1300 |
| `content/04-procedure.xml` | essential | 8-step end-to-end procedure incl. auth-directive authoring + naming audit | 1300 |
| `content/05-examples.xml` | reference | Two full worked examples end-to-end with the trace and the resulting artefact | 1200 |
| `content/06-decision-tree.xml` | essential | Root question + 13 branches incl. the shape gates → conclusion(ref=rule-id); skip leaf always reachable | 900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schema-design` | opus | Domain modelling + nullability decisions need strongest judgement. |
| `resolver-implementation` | sonnet | Mechanical SDL → resolver + DataLoader wiring. |
| `permission-audit` | haiku | Grep-style scan for missing permission_classes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.graphql` | SDL skeleton: Node/Timestamped interfaces, Relay Connection/Edge/PageInfo, Payload with userErrors, @auth directive |
| `templates/dataloader.py` | Strawberry DataLoaders: per-request batching, key-order preservation, 1:N grouping, context factory |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graphql-api-design.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-rest-design]]
- [[api-authentication]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the use case multi-client with nested reads or single-client CRUD?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
