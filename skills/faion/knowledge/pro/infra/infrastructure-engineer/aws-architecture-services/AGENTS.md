---
slug: aws-architecture-services
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Production-ready AWS service-selection spec: Lambda vs containers vs hybrid, EventBridge vs Step Functions vs SQS/SNS, Well-Architected six-pillar review with Terraform skeletons and Graviton-first compute defaults."
content_id: "16f26b4e8ba6f512"
complexity: deep
produces: spec
est_tokens: 5000
tags: [aws, architecture, serverless, containers, well-architected, infra]
---
# AWS Architecture Services

## Summary

**One-sentence:** Production-ready AWS service-selection spec: Lambda vs containers vs hybrid, EventBridge vs Step Functions vs SQS/SNS, Well-Architected six-pillar review with Terraform skeletons and Graviton-first compute defaults.

**One-paragraph:** Production-ready AWS service-selection spec: Lambda vs containers vs hybrid, EventBridge vs Step Functions vs SQS/SNS, Well-Architected six-pillar review with Terraform skeletons and Graviton-first compute defaults. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- A new AWS workload is in design or an existing one is up for Well-Architected review.
- Team has AWS commercial agreement + Terraform discipline + a named architect.
- Compute / data / event-routing decisions must be defended in a versioned spec.

## Skip If (ANY kills it)

- GCP or Azure target — use gcp-arch-patterns or the Azure suite instead.
- Pure Terraform syntax question — use terraform-basics.
- VPC-only design — use aws-networking + aws-vpc-design.

**Ефективно для:**

- Архітектори що вибирають compute (Lambda / ECS / EKS) для нового workload.
- Команди що проєктують event-driven системи (EventBridge / Step Functions / SQS / SNS).
- Огляд існуючої AWS-інфри за Well-Architected six-pillar review.
- Terraform для EKS / Aurora / ALB / CloudFront / API Gateway з PR-rationale.

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
| `scripts/validate-aws-architecture-services.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
