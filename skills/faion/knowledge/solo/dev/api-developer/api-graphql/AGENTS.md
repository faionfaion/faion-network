---
slug: api-graphql
tier: solo
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: GraphQL schema-design spec pinning schema-first authoring, DataLoader on every relation, Relay-style cursor pagination, depth + complexity limits on public endpoints, and persisted queries for prod...
content_id: "9bae98bcbe71424a"
complexity: deep
produces: spec
est_tokens: 4900
tags: [api-developer, graphql, dataloader, schema-first, federation, relay-pagination]
---
# API GraphQL Design

## Summary

**One-sentence:** GraphQL schema-design spec pinning schema-first authoring, DataLoader on every relation, Relay-style cursor pagination, depth + complexity limits on public endpoints, and persisted queries for production clients.

**One-paragraph:** GraphQL solves multi-resource fetching but adds N+1 risk, query-depth attacks, and schema-evolution traps. The methodology fixes schema-first authoring (SDL is source of truth), DataLoader on every relation field, cursor-based pagination per Relay, query depth + complexity caps, and persisted queries for trusted clients. Output is the GraphQL spec artefact + the rollout checklist. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- API GraphQL Design — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `api-graphql` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Client genuinely benefits from multi-resource fetching (mobile, complex dashboards).
- Server can implement DataLoader-equivalent batching and complexity analysis.
- Operator has resources to maintain SDL + resolvers + persisted queries.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- API serves a single-screen mobile client with one entity — REST is simpler.
- Team lacks GraphQL ops experience (no persisted queries, no complexity caps) — exposure beats benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-rest-design]] | Baseline HTTP semantics; GraphQL still rides HTTP |
| [[api-contract-first]] | Schema-first discipline analogous to OpenAPI-first |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/05-examples.xml` | essential | Worked end-to-end example anchored to the output contract | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-api-graphql-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-api-graphql.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-graphql.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[api-rest-design]]
- [[api-contract-first]]
- [[api-rate-limiting]]
- [[api-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (consumer needs, server capacity, ops maturity) to full-graphql / hybrid-with-rest-mutations / skip-stay-rest. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
