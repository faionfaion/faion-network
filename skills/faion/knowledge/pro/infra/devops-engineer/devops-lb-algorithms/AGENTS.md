---
slug: devops-lb-algorithms
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a load-balancer architecture decision record: chosen LB layer (L4/L7/DNS/Global), algorithm (round-robin / least-conn / weighted / IP-hash / consistent-hash), and session-affinity strategy.
content_id: "7ac8d743855684ac"
complexity: medium
produces: decision-record
est_tokens: 4200
tags: [load-balancing, algorithms, l4, l7, networking]
---
# Load Balancer Types and Algorithm Selection

## Summary

**One-sentence:** Generates a load-balancer architecture decision record: chosen LB layer (L4/L7/DNS/Global), algorithm (round-robin / least-conn / weighted / IP-hash / consistent-hash), and session-affinity strategy.

**One-paragraph:** Generates a load-balancer architecture decision record: chosen LB layer (L4/L7/DNS/Global), algorithm (round-robin / least-conn / weighted / IP-hash / consistent-hash), and session-affinity strategy. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Перший дизайн LB — вибір L4 vs L7 і алгоритму під workload.
- Heterogeneous backends (різна capacity) — обґрунтований Weighted Least Connections.
- Caching tier (Varnish / Redis cluster) — Consistent Hashing з rationale.
- Migration з sticky-IP на cookie-based affinity.

## Applies If (ALL must hold)

- Horizontal scaling across ≥2 backend instances is in scope.
- Traffic profile (HTTP vs TCP, request length variance, session semantics) is documented.
- Decision must be defended in an architecture review (ADR).

## Skip If (ANY kills it)

- Single-instance deployment with no HA requirement.
- Decision is already pinned by managed cloud LB defaults that team has accepted.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Traffic profile | table (RPS, p50/p99 duration, protocol) | Product / SRE |
| Backend capacity table | list (instance, capacity weight) | SRE |
| Session semantics | free-form note (stateless / sticky / sharded) | Application owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/AGENTS.md` | Parent skill context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-devops-lb-algorithms` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-lb-algorithms.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-lb-haproxy]]
- [[devops-lb-health-checks]]
- [[devops-lb-high-availability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
