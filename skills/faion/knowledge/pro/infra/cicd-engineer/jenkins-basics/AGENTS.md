---
slug: jenkins-basics
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Jenkins is an open-source automation server with Groovy-based Declarative (recommended) and Scripted pipeline syntax defined in Jenkinsfiles.
content_id: "443bdb4a409575f7"
tags: [jenkins, pipeline, cicd, declarative, kubernetes]
---
# Jenkins Basics

## Summary

**One-sentence:** Jenkins is an open-source automation server with Groovy-based Declarative (recommended) and Scripted pipeline syntax defined in Jenkinsfiles.

**One-paragraph:** Jenkins is an open-source automation server with Groovy-based Declarative (recommended) and Scripted pipeline syntax defined in Jenkinsfiles. Use Declarative pipelines for all new pipelines — they support restart-from-stage and syntax validation at load time. Use Shared Libraries to share pipeline code across projects. Use the Kubernetes agent for dynamic build agents — never run builds on the controller node.

## Applies If (ALL must hold)

- Enterprise environments with existing Jenkins infrastructure and established pipelines
- On-premises deployments with strict network isolation or compliance requirements
- Pipelines requiring heavy customization via plugins not available in GitLab CI or GitHub Actions
- Multi-branch projects with complex branching strategies (Organization Folder + Multibranch Pipeline)

## Skip If (ANY kills it)

- New projects on GitHub — GitHub Actions is simpler and has zero infrastructure cost
- New projects on GitLab — GitLab CI is integrated and eliminates a separate server
- Small teams or solo projects — Jenkins administration overhead is not justified
- Projects that need serverless/ephemeral CI — prefer cloud-native CI tools

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/cicd-engineer/`
