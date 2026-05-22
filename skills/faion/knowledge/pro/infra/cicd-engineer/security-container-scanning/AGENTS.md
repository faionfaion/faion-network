---
slug: security-container-scanning
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: 87% of production container images contain at least one major vulnerability (2024 Cloud Native Security Report).
content_id: "446e608408e6db10"
tags: [container-security, trivy, sbom, cosign, sigstore]
---
# Container Security Scanning and Image Signing

## Summary

**One-sentence:** 87% of production container images contain at least one major vulnerability (2024 Cloud Native Security Report).

**One-paragraph:** 87% of production container images contain at least one major vulnerability (2024 Cloud Native Security Report). Scan every image build in CI with Trivy (all-in-one: OS, library, IaC, secrets) or Grype (SBOM-focused); generate a CycloneDX SBOM per build; sign with Sigstore cosign keyless OIDC. Block on CRITICAL+HIGH before any registry push.

## Applies If (ALL must hold)

- Every project that builds and pushes a container image — scan before the push step.
- Generating an SBOM for compliance (FedRAMP, SOC2, NIST SSDF) or supply chain audit.
- Signing images for admission control verification (Kyverno verifyImages, OPA, Cosign policy).
- Scanning IaC configs (Dockerfile, K8s manifests, Terraform) for misconfigurations in the same pipeline.

## Skip If (ANY kills it)

- Projects that do not use containers — apply filesystem SAST/SCA instead.
- Using container scanning as a substitute for SAST — it finds known CVEs in packages, not application-level vulnerabilities in your own code.
- Blocking on every MEDIUM finding at the start — begin with CRITICAL+HIGH only.

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
