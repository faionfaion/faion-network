---
slug: lb-cloud-terraform
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates Terraform HCL for AWS ALB/NLB or GCP Global HTTP(S) LB with TLS-1.2+ listener, S3/CS access logs, deletion protection, target groups, and WAF wiring.
content_id: "fcd8641dfca8130b"
complexity: medium
produces: code
est_tokens: 5000
tags: [terraform, aws, gcp, load-balancing, infrastructure-as-code]
---
# Cloud Load Balancer Provisioning with Terraform

## Summary

**One-sentence:** Generates Terraform HCL for AWS ALB/NLB or GCP Global HTTP(S) LB with TLS-1.2+ listener, S3/CS access logs, deletion protection, target groups, and WAF wiring.

**One-paragraph:** Terraform modules for AWS ALB (Application Load Balancer), AWS NLB (Network Load Balancer), and GCP Global HTTP(S) Load Balancer. Covers: `aws_lb` resource with deletion protection and access logs to S3, target groups with health-check configuration, HTTPS listener with `ELBSecurityPolicy-TLS13-1-2-2021-06`, HTTP-to-HTTPS redirect listener, security groups, and GCP backend services with CDN policy, URL maps, managed SSL certificates, and Cloud Armor binding. Aimed at cloud-native teams replacing self-hosted HAProxy/Nginx with managed LBs.

**Ефективно для:**

- Greenfield AWS/GCP service: ALB або Global LB як точка входу.
- Migration: HAProxy / Nginx self-hosted → AWS ALB або GCP Cloud LB через Terraform.
- WAF + Shield (AWS) / Cloud Armor (GCP) attachment поверх існуючого LB.
- NLB для TCP/UDP workloads (DB proxies, Redis, gaming) на AWS.
- Modular Terraform: dev/stage/prod через `terraform workspace` + var-files.

## Applies If (ALL must hold)

- Provisioning a new cloud LB for a service on AWS or GCP using Terraform.
- Migrating from self-hosted HAProxy / Nginx to AWS ALB or GCP Cloud LB.
- Adding WAF, Shield, or Cloud Armor to an existing cloud LB via Terraform.
- Setting up NLB for TCP/UDP workloads (databases, Redis) on AWS.

## Skip If (ANY kills it)

- Kubernetes workloads — use AWS Load Balancer Controller or GKE Ingress; the controllers manage target group registration automatically.
- Self-hosted bare-metal environments — Terraform AWS/GCP providers need cloud API access; use HAProxy + keepalived.
- Azure — use `azurerm_application_gateway` or `azurerm_frontdoor`; patterns differ from AWS/GCP.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| VPC + subnet IDs | strings | network module |
| ACM / GCS-managed cert ARN/ID | string | cert module |
| Backend target list | IPs / instance IDs / NEG | service module |
| Access-log bucket | S3 / GCS bucket | logging module |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-technology-selection]] | Confirms ALB vs NLB vs Global LB before writing Terraform. |
| [[lb-monitoring]] | Access-log + metric wiring depends on LB choice. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: deletion-protection-on, tls-1-2-min-policy, access-logs-enabled, http-to-https-redirect, security-group-tight | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-lb-product` | sonnet | ALB vs NLB vs Global LB decision tree. |
| `emit-terraform` | sonnet | Structured HCL authoring. |
| `lint-tfsec-tflint` | haiku | Mechanical static analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/alb.tf` | Complete AWS ALB module: lb + listener + target group + redirect + S3 logs |
| `templates/gcp-global-lb.tf` | GCP Global HTTP(S) LB: backend service + URL map + managed cert + Cloud Armor |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-cloud-terraform.py` | Validate the Terraform artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-technology-selection]]
- [[lb-monitoring]]
- [[lb-layer-selection]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (cloud provider, protocol, geographic reach, WAF need) to a concrete LB product + Terraform shape, each leaf referencing a rule from `01-core-rules.xml`.
