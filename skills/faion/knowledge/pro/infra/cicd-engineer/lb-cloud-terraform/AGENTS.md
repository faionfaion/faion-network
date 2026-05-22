---
slug: lb-cloud-terraform
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Terraform modules for AWS ALB (Application Load Balancer) and NLB (Network Load Balancer), and GCP Global HTTP(S) Load Balancer.
content_id: "5f381d4434917a8e"
tags: [terraform, aws, gcp, load-balancing, infrastructure-as-code]
---
# Cloud Load Balancer Provisioning with Terraform

## Summary

**One-sentence:** Terraform modules for AWS ALB (Application Load Balancer) and NLB (Network Load Balancer), and GCP Global HTTP(S) Load Balancer.

**One-paragraph:** Terraform modules for AWS ALB (Application Load Balancer) and NLB (Network Load Balancer), and GCP Global HTTP(S) Load Balancer. Covers: aws_lb resource with deletion protection and access logs to S3, target groups with health check configuration, HTTPS listener with ELBSecurityPolicy-TLS13-1-2-2021-06, HTTP-to-HTTPS redirect listener, security groups, and GCP backend services with CDN policy, URL maps, and managed SSL certificates.

## Applies If (ALL must hold)

- Provisioning a new cloud LB for a service on AWS or GCP using Terraform.
- Migrating from self-hosted HAProxy/Nginx to AWS ALB or GCP Cloud LB.
- Adding WAF, Shield, or Cloud Armor to an existing cloud LB via Terraform.
- Setting up NLB for TCP/UDP workloads (databases, Redis) on AWS.

## Skip If (ANY kills it)

- Kubernetes workloads — use the AWS Load Balancer Controller or GKE Ingress instead of raw aws_lb resources; the controllers manage target group registration automatically.
- Self-hosted bare-metal environments — Terraform AWS/GCP providers require cloud API access; use HAProxy plus keepalived instead.
- Azure — use azurerm_application_gateway or azurerm_frontdoor; the patterns differ from AWS/GCP.

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
