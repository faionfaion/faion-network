---
slug: aws-ec2-ecs
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "EC2 + ECS Fargate production spec: task definitions, service auto-scaling, capacity providers, IAM task roles, network mode, observability hookups, and rollout discipline (blue/green via CodeDeploy)."
content_id: "57a0dc9c316051dd"
complexity: deep
produces: spec
est_tokens: 5000
tags: [aws, ec2, ecs, fargate, containers, infra]
---
# AWS EC2 + ECS

## Summary

**One-sentence:** EC2 + ECS Fargate production spec: task definitions, service auto-scaling, capacity providers, IAM task roles, network mode, observability hookups, and rollout discipline (blue/green via CodeDeploy).

**One-paragraph:** EC2 + ECS Fargate production spec: task definitions, service auto-scaling, capacity providers, IAM task roles, network mode, observability hookups, and rollout discipline (blue/green via CodeDeploy). The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Service is or will be containerised and runs on AWS.
- Team prefers managed-control-plane over self-managed K8s.
- Named platform-lead can sign off on baseline ECS pattern.

## Skip If (ANY kills it)

- Workload requires GPU + > 24h jobs — use EC2 directly or SageMaker.
- Team mandate is EKS / Kubernetes — use aws-eks methodology.
- Single Lambda function is sufficient — use aws-lambda.

**Ефективно для:**

- Команди що мігрують з EC2-VMs на ECS Fargate.
- Сервіси яким потрібна container orchestration без K8s overhead.
- Stateless services з 1-100 task replicas і ALB / NLB ingress.
- Аудит-ready (PCI / SOC2) ECS deployments.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev` | Parent role context. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-ec2-ecs.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
