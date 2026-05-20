---
slug: sec-trivy-pinned-supply-chain-scan
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every container image, Helm chart, Terraform module, Kubernetes manifest, and release tarball passes through trivy fs (filesystem) plus trivy image (containers) in CI.
content_id: "fd057ef748748d46"
tags: [security, supply-chain, trivy, sbom, container-scanning]
---
# Trivy with Pinned-Version Supply-Chain Scan + SBOM

## Summary

**One-sentence:** Every container image, Helm chart, Terraform module, Kubernetes manifest, and release tarball passes through trivy fs (filesystem) plus trivy image (containers) in CI.

**One-paragraph:** Every container image, Helm chart, Terraform module, Kubernetes manifest, and release tarball passes through trivy fs (filesystem) plus trivy image (containers) in CI. The job fails on HIGH or CRITICAL CVEs and on misconfigurations, blocking merge. Each release tag also generates an SBOM in CycloneDX or SPDX and attaches it to the GitHub Release. Trivy itself is pinned by SHA — the action is referenced as aquasecurity/trivy-action@<sha> and the binary version in CI is set explicitly to a known-clean release, never latest.

## Applies If (ALL must hold)

- Any repo that produces a container image, IaC artifact, or release tarball.
- Any agent-driven dependency bump or base-image upgrade — agent runs trivy image on the candidate before opening the PR.
- Polyglot monorepos that need one scanner across Dockerfile, terraform/, helm/, k8s/, and package-lock.json.
- Release pipelines that must attach an SBOM for EU CRA or US EO 14028 compliance.

## Skip If (ANY kills it)

- Pure documentation, asset, or static-blog repos with no container, IaC, or distributable binary — no supply-chain surface to scan.
- Highly air-gapped environments where Trivy's online DB updates are impossible — switch to a mirrored offline DB or substitute Anchore Enterprise with a private feed; do not run the scanner with stale signatures.
- Notebook-only research repos where dependency churn is constant and signal-to-noise is too low — use Snyk or Renovate-driven advisories instead and gate at deploy time.
- The exact tag aquasecurity/trivy@v0.69.4 and aquasecurity/trivy-action@v0.30.0 (compromised) — never use those refs anywhere.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
