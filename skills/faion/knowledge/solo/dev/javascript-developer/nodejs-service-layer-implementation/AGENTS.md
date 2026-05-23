---
slug: nodejs-service-layer-implementation
tier: solo
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Node.js service layer implementation spec: TypeScript Controller-Service-Repository code (Express + Prisma), error middleware, and per-layer test pattern.
content_id: "de1bcc26b6ccbadb"
complexity: deep
produces: code
est_tokens: 4200
tags: [nodejs, typescript, express, architecture, prisma]
---
# Node.js Service Layer Implementation

## Summary

**One-sentence:** Node.js service layer implementation spec: TypeScript Controller-Service-Repository code (Express + Prisma), error middleware, and per-layer test pattern.

**One-paragraph:** Node.js service layer implementation spec: TypeScript Controller-Service-Repository code (Express + Prisma), error middleware, and per-layer test pattern. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script `scripts/validate-nodejs-service-layer-implementation.py` enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- Node.js Service Layer Implementation — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `nodejs-service-layer-implementation` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Architecture decisions in nodejs-service-layer-architecture have been agreed.
- Stack is Express + Prisma (or a swap-equivalent: Fastify + Drizzle).
- TypeScript strict mode is enabled or about to be.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Architecture phase incomplete — run nodejs-service-layer-architecture first.
- Project is JavaScript-only with no TS migration planned — implementation patterns differ enough to warrant a sibling methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[nodejs-service-layer-architecture]] | Workflow context: related methodology in the same family |

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
| `fill-nodejs-service-layer-implementation-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-nodejs-service-layer-implementation.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nodejs-service-layer-implementation.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[nodejs-service-layer-architecture]]
- [[react-component-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (architecture readiness, stack fit, TS adoption) to full-impl / partial-impl / defer. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
