---
slug: api-contract-first
tier: solo
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Workflow spec: write OpenAPI 3.1 before code, review the spec like a PR, generate server stubs + SDKs, validate the implementation against the spec at runtime; the spec is the single source of truth.
content_id: "3b66652d93b80901"
complexity: medium
produces: spec
est_tokens: 4900
tags: [api-developer, contract-first, openapi, code-generation, spectral]
---
# API Contract-First Workflow

## Summary

**One-sentence:** Workflow spec: write OpenAPI 3.1 before code, review the spec like a PR, generate server stubs + SDKs, validate the implementation against the spec at runtime; the spec is the single source of truth.

**One-paragraph:** Code-first APIs drift: the served shape diverges from the documented shape, SDKs lag, and consumer teams hit silent breaking changes. Contract-first inverts the loop — spec is written and reviewed first, the server is generated from the spec, runtime validation rejects responses that drift. Output is the contract-first workflow spec naming the OpenAPI document, the generator, the CI gate, and the runtime validator. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- API Contract-First Workflow — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `api-contract-first` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Greenfield API OR pre-launch service where the contract style is still open.
- ≥2 consumer teams or external SDKs depend on the API.
- Operator has CI capacity to enforce contract checks on every PR.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Internal one-team API with a single Python caller — contract overhead exceeds value.
- Existing code-first API >6mo old — migration cost likely exceeds drift cost; gate breaking changes instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-openapi-spec]] | How to author the OpenAPI document itself |
| [[api-rest-design]] | REST baseline the contract describes |

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
| `fill-api-contract-first-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-api-contract-first.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-contract-first.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[api-openapi-spec]]
- [[api-rest-design]]
- [[api-documentation]]
- [[api-testing]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (greenfield vs brownfield, consumer count, CI capacity) to full contract-first / partial contract-first / skip-and-gate-breaking-changes. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
