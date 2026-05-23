---
slug: strangler-fig-migration-pattern
tier: pro
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Incremental framework-upgrade pattern that grows the new system route-by-route beside the legacy one, avoiding the big-bang branch.
content_id: "d424428bec41642f"
complexity: deep
produces: playbook-step
est_tokens: 4100
tags: [strangler-fig, migration, framework-upgrade, refactor]
---
# Strangler Fig Migration Pattern

## Summary

**One-sentence:** Incremental framework-upgrade pattern that grows the new system route-by-route beside the legacy one, avoiding the big-bang branch.

**One-paragraph:** Incremental framework-upgrade pattern that grows the new system route-by-route beside the legacy one, avoiding the big-bang branch. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-strangler-fig-migration-pattern.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Vue 2→3, Next pages→app router, Rails major upgrade, Django major upgrade.
- Active product з прод-юзерами — big-bang refactor неприпустимий.
- Кодова база ≥30k LOC, де ROI rewrite < ROI incremental cutover.
- CI/CD здатне deployити обидва системи паралельно за route prefix або feature flag.

## Applies If (ALL must hold)

- Active product with paying users — downtime/regression budget tight
- Routable seam exists (HTTP routes, RPC endpoints, or feature flags) for traffic split
- Both legacy and new framework can run side-by-side in production
- Team can dedicate a multi-sprint commitment to walk the routes

## Skip If (ANY kills it)

- Greenfield rewrite — no legacy to strangle; ship the new system directly
- ≤5k LOC monolith — full rewrite cheaper than process overhead of strangler
- No routable seam — monolith cannot be split route-by-route
- Team won't freeze legacy post-cutover — strangler half-finished is worse than legacy

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-strangler-fig-migration-pattern` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strangler-fig-migration-pattern.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[v1-to-v2-migration-playbook]]
- [[test-pyramid-rebalance-playbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
