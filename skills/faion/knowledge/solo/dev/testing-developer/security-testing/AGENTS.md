---
slug: security-testing
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a layered security-testing report — SAST + DAST + SCA + secret detection — wired into the CI/CD pipeline with named coverage per stage.
content_id: "d442a7a7909d7168"
complexity: deep
produces: report
est_tokens: 4600
tags: ["security", "sast", "dast", "sca", "secrets", "testing"]
---
# Security Testing

## Summary

**One-sentence:** Generates a layered security-testing report — SAST + DAST + SCA + secret detection — wired into the CI/CD pipeline with named coverage per stage.

**One-paragraph:** Generates a layered security-testing report — SAST + DAST + SCA + secret detection — wired into the CI/CD pipeline with named coverage per stage.

**Ефективно для:**

- Solo team adding auth, payments, file upload, or crypto code.
- Pre-launch hardening for an internet-exposed service.
- Continuous PR gate to catch SAST + secrets before merge.
- Compliance audit (SOC 2, ISO 27001, PCI) needs evidence per scan type.

## Applies If (ALL must hold)

- Every change touches auth, authorization, input handling, file upload, deserialization, crypto, or session code.
- Service is internet-exposed OR handles personally identifiable data.
- CI/CD pipeline exists where SAST + secret scans can gate merge.
- Team has authority to block merges on security findings.

## Skip If (ANY kills it)

- Substitute for threat modeling — tools find known patterns; design flaws hide.
- DAST against any environment with real user data, real billing, or real downstream effects.
- Replacing manual review for critical-path code (auth, crypto, payment).
- Auto-merging security patches without human review.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| SAST tool config | yaml | semgrep / bandit / sonarqube |
| SCA tool config | yaml | dependabot / snyk / trivy |
| Secret-scan rules | yaml | gitleaks / trufflehog |
| DAST target | url | staging environment URL |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| solo-deploy-checklist | Deploy gate consumes this report. |
| server-init-bootstrap | Hardened baseline assumed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-sast-on-every-pr, r2-sca-on-every-build, r3-secrets-pre-commit-and-ci, r4-dast-nightly-staging, r5-named-security-owner | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Security Testing artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: dast-against-prod, secrets-in-history, sast-noise-overload | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-security-testing` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-security-testing` | sonnet | Bounded structural check against the output contract. |
| `review-security-testing` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/security-testing.json` | JSON skeleton matching the output contract. |
| `templates/security-testing.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-testing.py` | Validate Security Testing output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[solo-deploy-checklist]]
- [[server-init-bootstrap]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
