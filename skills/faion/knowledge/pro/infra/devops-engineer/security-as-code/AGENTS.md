---
slug: security-as-code
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Security as Code embeds protection mechanisms directly into every phase of the software delivery lifecycle.
content_id: "04d9ea9b8acb60f4"
tags: [devsecops, policy-as-code, opa, kyverno, vulnerability-scanning]
---
# Security as Code (Policy as Code)

## Summary

**One-sentence:** Security as Code embeds protection mechanisms directly into every phase of the software delivery lifecycle.

**One-paragraph:** Security as Code embeds protection mechanisms directly into every phase of the software delivery lifecycle. Instead of treating security as a final checkpoint, DevSecOps integrates security controls, automated testing, and governance from code authoring through deployment.

## Applies If (ALL must hold)

- Kubernetes clusters requiring admission control — enforce resource limits, deny privileged containers, require trusted registries
- Terraform/Pulumi IaC pipelines — block public S3, unencrypted RDS, missing tags before apply
- Container CI/CD — scan images for CRITICAL/HIGH CVEs, block on threshold
- Regulated environments requiring SOC2, HIPAA, PCI-DSS, or GDPR compliance automation
- Supply chain hardening — SBOM generation, artifact signing with Sigstore/Cosign

## Skip If (ANY kills it)

- Proof-of-concept environments where policy overhead slows iteration without security benefit
- Legacy monoliths with no CI/CD pipeline — manual gate review may be more practical than retrofitting PaC
- Solo developer projects with no compliance requirement — lightweight linting suffices over a full OPA/Kyverno stack

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
