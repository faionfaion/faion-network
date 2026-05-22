---
slug: security-policy-as-code
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Policy as Code codifies compliance and security requirements in version-controlled, testable artifacts enforced by admission controllers.
content_id: "40f178ee37a01345"
tags: [policy-as-code, kyverno, opa, kubernetes, admission-control]
---
# Policy as Code: OPA, Kyverno, and Admission Control

## Summary

**One-sentence:** Policy as Code codifies compliance and security requirements in version-controlled, testable artifacts enforced by admission controllers.

**One-paragraph:** Policy as Code codifies compliance and security requirements in version-controlled, testable artifacts enforced by admission controllers. 96% of technical decision-makers say Policy as Code is vital for secure, scalable cloud operations. Use Kyverno (YAML, Kubernetes-native, easier) or OPA/Gatekeeper (Rego, multi-system, steeper curve). Always start in audit mode; write unit tests; enforce only after fixing existing violations.

## Applies If (ALL must hold)

- Kubernetes clusters running multi-team workloads where each team should not be able to override security baselines.
- Compliance mandates that require no privileged containers, no root users, trusted registries only, required resource limits.
- Multi-system policy enforcement beyond Kubernetes (OPA with Terraform, API gateway, CI/CD gates via Conftest).
- Image signing verification — Kyverno verifyImages validates Sigstore cosign signatures at admission time.

## Skip If (ANY kills it)

- Non-Kubernetes workloads — use native IAM policies, network ACLs, or Terraform Sentinel instead.
- Replacing application-level security — admission control governs the platform, not the app's own auth/authz.
- Enforcing policies before audit mode has been run and violations remediated — enforcement without a clean baseline blocks legitimate workloads.

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
