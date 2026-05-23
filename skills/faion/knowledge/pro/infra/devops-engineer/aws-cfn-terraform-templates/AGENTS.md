---
slug: aws-cfn-terraform-templates
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces production-ready AWS IaC templates (VPC, ECS Fargate, Lambda, RDS) in CloudFormation YAML and Terraform HCL with hardened defaults.
content_id: "01806b5b11f83568"
complexity: deep
produces: code
est_tokens: 4500
tags: [aws, cloudformation, terraform, iac]
---
# AWS Infrastructure-as-Code Templates (CloudFormation and Terraform)

## Summary

**One-sentence:** Produces production-ready AWS IaC templates (VPC, ECS Fargate, Lambda, RDS) in CloudFormation YAML and Terraform HCL with hardened defaults.

**One-paragraph:** Production-ready CloudFormation YAML and Terraform HCL templates for common AWS infrastructure patterns: VPC networking with multi-AZ public + private subnets, ECS Fargate services behind ALB, serverless Lambda + API Gateway stacks, RDS PostgreSQL with auto-rotating credentials via Secrets Manager, and supporting IAM / S3 / ECS configuration JSON. Templates default to hardened settings: encryption at rest, least-privilege IAM, deletion protection on stateful resources, and tagging discipline.

**Ефективно для:**

- deploying new VPC з multi-AZ public + private subnets.
- launching ECS Fargate service behind Application Load Balancer.
- setting up serverless API (Lambda + API Gateway + DynamoDB).
- RDS PostgreSQL з auto-rotating credentials via Secrets Manager.

## Applies If (ALL must hold)

- Target is AWS and the team uses CloudFormation or Terraform as the IaC tool.
- Production deployment must default to hardened settings (encryption, IAM least-privilege, deletion protection).
- Module is reusable across stacks (not a one-off resource).
- Tagging discipline is defined (project / env / owner tags mandatory).

## Skip If (ANY kills it)

- One-off CLI operations — use aws-cli-compute or aws-cli-containers-iac commands.
- Highly customized environments where a module's defaults diverge significantly — fork and adapt rather than fight the template.
- Simple single-resource changes — use `aws cloudformation update-stack` with a targeted parameter override.
- Non-AWS cloud — these templates do not generalize.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target AWS account | numeric id | platform |
| Region | string | architect |
| Tagging convention | doc | platform |
| Secrets policy | doc | security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/aws-foundations` | account + region setup assumed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-pattern` | haiku | Map workload to one of VPC / ECS / Lambda / RDS |
| `parameterise-template` | sonnet | Fill in account / region / tags / sizing |
| `harden-defaults` | opus | Cross-resource security + cost review |

## Templates

| File | Purpose |
|------|---------|
| `templates/vpc.tf` | VPC Terraform module skeleton (multi-AZ) |
| `templates/ecs-fargate.yaml` | ECS Fargate CloudFormation skeleton |
| `templates/rds-postgres.yaml` | RDS PostgreSQL CFN skeleton with Secrets Manager |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-cfn-terraform-templates.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[aws-foundations]]
- [[aws-cli-compute]]
- [[aws-cli-containers-iac]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the AWS Infrastructure-as-Code Templates (CloudFormation and Terraform) methodology when in doubt about scope or fit.
