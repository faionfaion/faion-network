---
slug: security-supply-chain
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Supply chain attacks target dependencies, build tooling, and secrets in CI rather than the application code itself.
content_id: "e531f377a52beebe"
tags: [supply-chain, secret-scanning, sca, slsa, sbom]
---
# Supply Chain Security: Secrets, SCA, SBOM, and SLSA

## Summary

**One-sentence:** Supply chain attacks target dependencies, build tooling, and secrets in CI rather than the application code itself.

**One-paragraph:** Supply chain attacks target dependencies, build tooling, and secrets in CI rather than the application code itself. Defend with: secret scanning on every commit and history rewrite when leaks hit main; SCA (Software Composition Analysis) for dependency CVEs; SBOM generation per build; lock files for all dependency manifests; SLSA provenance attestation. Automate dependency updates with Dependabot or Renovate with a capped auto-merge policy.

## Applies If (ALL must hold)

- Every project with external dependencies — SCA is the minimum viable supply chain control.
- Any repo where developers commit secrets (API keys, tokens, certs) accidentally — secret scanning pre-commit + CI is non-negotiable.
- Projects that ship artifacts externally or to regulated industries — SBOM generation and SLSA attestation are increasingly mandatory.
- Standing up a "security PR bot" that auto-opens fix PRs for known-vulnerable dependencies.

## Skip If (ANY kills it)

- Replacing code review for novel dependency selection — SCA catches known CVEs, not design choices like overly broad transitive dependency trees.
- Auto-merging dependency updates that include major version bumps — require human review for breaking changes even if CI passes.
- One-off scripts with no external dependencies — overhead exceeds value.

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
