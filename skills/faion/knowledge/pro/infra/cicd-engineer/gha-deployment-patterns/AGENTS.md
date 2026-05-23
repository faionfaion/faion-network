---
slug: gha-deployment-patterns
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a CD config (staged deploys with environment protection + reusable workflows + composite actions + canary/blue-green choice + release automation with changelog).
content_id: "5298bb89298c0d59"
complexity: deep
produces: config
est_tokens: 4300
tags: [github-actions, cd, deployment, reusable-workflows, release]
---
# GitHub Actions — Deployment Patterns

## Summary

**One-sentence:** Generates a CD config (staged deploys with environment protection + reusable workflows + composite actions + canary/blue-green choice + release automation with changelog).

**One-paragraph:** Generates a CD config (staged deploys with environment protection + reusable workflows + composite actions + canary/blue-green choice + release automation with changelog). The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Multi-env deploys (dev → staging → prod) з environment protection.
- Canary / blue-green rollouts з metric-based rollback.
- Centralized reusable workflows для DRY-up CD pipelines.
- Release automation: changelog generation + git tag + GitHub Release.

## Applies If (ALL must hold)

- Repository deploys to ≥2 environments (e.g. staging + prod).
- Deployment is automatable (no manual UI clicks required).
- Health metrics exist for the deployed service (HTTP 2xx ratio, P95 latency, error rate).
- Release cadence is at least weekly — automation overhead pays back.

## Skip If (ANY kills it)

- Single-env deploy without progression (a personal project).
- Deployments require manual UI steps that cannot be scripted — fix tooling first.
- No service health metrics — rollback gates have no signal to act on.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Environment list | YAML (name, url, approvers) | Platform team |
| Service health metrics | Prometheus / Datadog query refs | SRE |
| Reusable workflow library | repo + path | CI team |
| Release notes template | MD template | PM / engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

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
| `draft-gha-deployment-patterns` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gha-deployment-patterns.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
