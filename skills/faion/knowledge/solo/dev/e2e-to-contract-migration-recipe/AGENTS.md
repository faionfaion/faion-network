---
slug: e2e-to-contract-migration-recipe
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Stepwise recipe to convert a slow / flaky e2e test into a fast contract test pair (provider-side + consumer-side) using Pact or a JSON-Schema gateway; produces a migration spec listing which e2e cases moved, which stay, and why."
content_id: "596d871d2a27b93a"
complexity: deep
produces: spec
est_tokens: 4900
tags: ["dev", "solo", "testing", "contract-tests", "e2e", "migration"]
---
# E2E-to-Contract Migration Recipe

## Summary

**One-sentence:** Stepwise recipe to convert a slow / flaky e2e test into a fast contract test pair (provider-side + consumer-side) using Pact or a JSON-Schema gateway; produces a migration spec listing which e2e cases moved, which stay, and why.

**One-paragraph:** Stepwise recipe to convert a slow / flaky e2e test into a fast contract test pair (provider-side + consumer-side) using Pact or a JSON-Schema gateway; produces a migration spec listing which e2e cases moved, which stay, and why. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Microservice surfaces where the contract is HTTP + JSON Schema.
- Webhook-emitting systems where the consumer is third-party but emits a recorded shape.
- Solo / small-team projects where e2e infra (Selenium grids, headless Chrome) is overkill.
- Suites where flake-induced CI re-runs already cost more than rewriting.

## Applies If (ALL must hold)

- Test suite has ≥1 e2e test taking >30s OR flaking >1x/week.
- The system-under-test has a stable HTTP / gRPC / message contract between two named components.
- Both components are owned by the same team / operator (or an inter-team contract exists).
- Tooling for contract tests is acceptable (Pact, Schemathesis, OpenAPI generator).

## Skip If (ANY kills it)

- Contract is in flux week-to-week — contract tests will out-of-date faster than e2e flakes.
- Test exists solely to assert UI rendering pixels — contract tests cannot cover.
- Only one component exists (no consumer) — contract testing has no second side.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[behavior-parity-verification]] | upstream context this methodology builds on |
| [[characterization-test-recipes]] | sibling discipline cited in decision tree |

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
| `fill-e2e-to-contract-migration-recipe-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-e2e-to-contract-migration-recipe.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-e2e-to-contract-migration-recipe.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[behavior-parity-verification]]
- [[characterization-test-recipes]]
- [[flaky-test-elimination]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
