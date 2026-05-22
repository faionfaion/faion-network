---
slug: aws-infra-llm-prompts
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Parameterized LLM prompt templates for AWS infrastructure design conversations.
content_id: "34846cb544b697a2"
tags: [aws, llm-prompts, infrastructure-design, prompt-engineering, cloud-architecture]
---
# AWS Infrastructure Design — LLM Prompt Templates

## Summary

**One-sentence:** Parameterized LLM prompt templates for AWS infrastructure design conversations.

**One-paragraph:** Parameterized LLM prompt templates for AWS infrastructure design conversations. Each prompt includes context variables, workload characteristics, constraints, and required output format to produce actionable designs rather than generic advice.

## Applies If (ALL must hold)

- Starting a new AWS architecture design conversation and need structured context elicitation.
- Reviewing an existing architecture for security, cost, or reliability gaps using LLM analysis.
- Generating IAM policies, DR runbooks, or scaling configurations via LLM assistance.
- Planning database or workload migrations to AWS.

## Skip If (ANY kills it)

- Direct CLI operations — use aws-cli-compute or aws-cli-containers-iac.
- Generating actual infrastructure code from scratch — use templates from aws-cfn-terraform-templates as the base instead.
- Compliance documentation — LLM output needs expert review for HIPAA/PCI/SOC2 submissions.

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

- parent skill: `pro/infra/devops-engineer/`
