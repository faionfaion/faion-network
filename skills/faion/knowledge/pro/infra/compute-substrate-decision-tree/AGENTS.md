---
slug: compute-substrate-decision-tree
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a decision record selecting VM vs container vs serverless for a Greenfield component with explicit trade-offs and named owner.
content_id: "0963a00bbeaf37d0"
complexity: medium
produces: decision-record
est_tokens: 4500
tags: [compute-substrate, decision-tree, infra, architecture]
---
# Compute Substrate Decision Tree

## Summary

**One-sentence:** Produces a decision record selecting VM vs container vs serverless for a Greenfield component with explicit trade-offs and named owner.

**One-paragraph:** DevOps engineers re-derive the VM-vs-container-vs-serverless decision at every Greenfield component without a shared artefact. This methodology pins a typed input form (workload shape, latency target, request profile, ops constraints), runs them through a bounded scoring rubric, and emits a decision record naming a single owner. The record is versioned and traceable so a future operator can re-open the decision without re-running the conversation.

**Ефективно для:**

- одноразового вибору між VM / контейнером / serverless при greenfield-архітектурі.
- коли потрібен auditable artefact, а не chat-обговорення для downstream consumer.
- DevOps-інженер має 30-90 хв на структуроване рішення з trade-offs.
- tier=pro команд, де rollback стоїть дорожче за upfront-аналіз.

## Applies If (ALL must hold)

- Greenfield architecture proposal with at least one compute component still un-decided.
- Workload shape (latency target, request profile, state, ops constraints) is documented.
- A named owner is accountable for the decision record downstream.
- Output will be consumed by a downstream agent or human reviewer (not discarded).

## Skip If (ANY kills it)

- The team already maintains a working compute-decision artefact — extend it, do not duplicate.
- Greenfield prototype with no production users — overhead exceeds the win.
- Regulatory / compliance context overrides the trade-off (e.g., GovCloud-only) — defer to that mandate.
- Single-use throwaway task — the contract overhead is not justified.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload spec | Markdown / ADR draft | architect |
| Latency + request profile | numbers / SLO doc | product / ops |
| Trade-off rubric | this methodology's template | faion-network |
| Named owner | string | engagement lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r1-bound-scope) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-workload-spec` | haiku | Structured extraction from ADR draft + SLO doc |
| `score-rubric` | sonnet | Per-axis trade-off scoring with bounded inputs |
| `synthesize-decision-record` | sonnet | Compose final artefact with named owner + rationale |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Decision-record skeleton with trade-off table |
| `templates/skeleton.json` | JSON shape for the decision artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-compute-substrate-decision-tree.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[compute-substrate-decision-tree]] parent skill: `pro/infra/devops-engineer/`
- [[architecture-decision-records]]
- [[capacity-planning-pre-launch]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Compute Substrate Decision Tree methodology when in doubt about scope or fit.
