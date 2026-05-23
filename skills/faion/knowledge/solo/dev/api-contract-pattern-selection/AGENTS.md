---
slug: api-contract-pattern-selection
tier: solo
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Per-API decision record routing the contract style to one of {OpenAPI 3.1, GraphQL SDL, tRPC, JSON-RPC, gRPC, none-internal-only} based on consumer count, tooling needs, schema-evolution rate, and ...
content_id: "3a21afa82f8f8023"
complexity: medium
produces: decision-record
est_tokens: 4200
tags: [dev, solo, api-design, contract-first, openapi, graphql, trpc]
---
# API Contract Pattern Selection

## Summary

**One-sentence:** Per-API decision record routing the contract style to one of {OpenAPI 3.1, GraphQL SDL, tRPC, JSON-RPC, gRPC, none-internal-only} based on consumer count, tooling needs, schema-evolution rate, and team boundary.

**One-paragraph:** Solo devs default to whatever framework ships with — usually OpenAPI from FastAPI or none-at-all from Flask. The pick is rarely justified. This methodology asks four observable questions (consumer count, tooling needs, evolution rate, team boundary) and emits a decision record naming the contract style + the next-step setup tickets. Output conforms to the schema. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- API Contract Pattern Selection — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `api-contract-pattern-selection` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Greenfield service OR significant rewrite where the contract style is genuinely open.
- API is consumed by ≥2 distinct callers (web + mobile, internal + external, multiple SDK languages).

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Internal-only function call boundary that never crosses processes — no contract needed.
- Existing contract style has accumulated >6mo of production traffic — migration cost outweighs choice.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-rest-design]] | REST design baseline — what the OpenAPI 3.1 path produces |
| [[api-graphql]] | GraphQL baseline — what the SDL path produces |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-api-contract-pattern-selection-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-api-contract-pattern-selection.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-contract-pattern-selection.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[api-contract-first]]
- [[api-openapi-spec]]
- [[api-rest-design]]
- [[api-graphql]]

## Decision tree

See `content/06-decision-tree.xml`. Maps (consumer_count, tooling, evolution_rate, team_boundary) → contract style. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
