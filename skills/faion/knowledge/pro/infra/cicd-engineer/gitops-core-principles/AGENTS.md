---
slug: gitops-core-principles
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a GitOps-adoption config (declarative-state baseline + Git-as-source-of-truth policy + tool choice ArgoCD vs Flux + push-vs-pull model + phased rollout) per the OpenGitOps four principles.
content_id: "a840289f5145487a"
complexity: medium
produces: config
est_tokens: 4300
tags: [gitops, argocd, flux, kubernetes, ci-cd]
---
# GitOps — Core Principles

## Summary

**One-sentence:** Generates a GitOps-adoption config (declarative-state baseline + Git-as-source-of-truth policy + tool choice ArgoCD vs Flux + push-vs-pull model + phased rollout) per the OpenGitOps four principles.

**One-paragraph:** Generates a GitOps-adoption config (declarative-state baseline + Git-as-source-of-truth policy + tool choice ArgoCD vs Flux + push-vs-pull model + phased rollout) per the OpenGitOps four principles. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Kubernetes platform де cluster state has drifted з repo.
- Audit-trail vacuum: 'хто змінив production yesterday' немає відповіді.
- Multi-cluster fleet де ручні kubectl apply не масштабуються.
- Migration з push-based CD на pull-based GitOps.

## Applies If (ALL must hold)

- Kubernetes-based platform (≥1 cluster).
- Audit + reproducibility requirements (regulated industry, compliance).
- Team comfortable with declarative IaC (Helm / Kustomize / pure YAML).
- Git repo can be the single source of truth (no out-of-band manual changes).

## Skip If (ANY kills it)

- Non-Kubernetes platform — apply alternative declarative tooling.
- Team relies on kubectl edit / manual operations as primary workflow.
- Single-developer dev cluster with no audit need.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cluster inventory | YAML (name, env, kube_context) | Platform team |
| Current deployment process | doc | Eng team |
| Git host | URL | Platform team |
| Tool preference | argocd OR flux | Platform team |

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
| `draft-gitops-core-principles` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gitops-core-principles.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
