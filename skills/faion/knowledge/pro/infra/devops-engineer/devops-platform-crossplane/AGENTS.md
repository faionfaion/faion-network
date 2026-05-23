---
slug: devops-platform-crossplane
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a Crossplane composition spec: XRD shape, claim contract, security defaults, blast-radius caps, and a published self-service Database/Cache/Network abstraction.
content_id: "cbb837ea1556958d"
complexity: deep
produces: config
est_tokens: 4500
tags: [crossplane, platform, kubernetes, xrd, self-service]
---
# Crossplane Composition for Self-Service Infra

## Summary

**One-sentence:** Generates a Crossplane composition spec: XRD shape, claim contract, security defaults, blast-radius caps, and a published self-service Database/Cache/Network abstraction.

**One-paragraph:** Generates a Crossplane composition spec: XRD shape, claim contract, security defaults, blast-radius caps, and a published self-service Database/Cache/Network abstraction. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Self-service infra на Kubernetes без Terraform per dev.
- Compositions які приховують AWS/GCP/Azure plumbing від продуктових команд.
- Built-in defaults: encryption, backup, tagging, cost-cap.
- GitOps-ready CRD claims через ArgoCD/Flux.

## Applies If (ALL must hold)

- Kubernetes is the platform substrate (control plane already running).
- Platform team controls a finite set of infra abstractions (Database, Cache, Network, etc.).
- Developers should provision via CRD claim, not raw cloud SDK.

## Skip If (ANY kills it)

- Org runs Terraform-only and developer self-service is not in scope.
- Infra surface is too small (<5 abstractions) — direct Terraform modules are cheaper.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Abstraction list | table (name, cloud resources composed) | Platform team |
| Cloud credentials | ProviderConfig refs | Platform / Security |
| Policy baseline | OPA rules | Security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/devops-platform-idp-core/AGENTS.md` | IDP framing |

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
| `draft-devops-platform-crossplane` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-platform-crossplane.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-platform-idp-core]]
- [[devops-platform-policy-finops]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
