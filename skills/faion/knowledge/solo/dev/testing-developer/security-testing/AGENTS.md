---
slug: security-testing
tier: solo
group: dev
domain: testing-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Layered security testing using SAST (static code analysis), DAST (dynamic attack simulation), SCA (dependency vulnerability scanning), and secret detection — integrated at every stage of the CI/CD pipeline.
content_id: "ce3cce25f7e29686"
tags: [security, sast, dast, sca, testing]
---
# Security Testing

## Summary

**One-sentence:** Layered security testing using SAST (static code analysis), DAST (dynamic attack simulation), SCA (dependency vulnerability scanning), and secret detection — integrated at every stage of the CI/CD pipeline.

**One-paragraph:** Layered security testing using SAST (static code analysis), DAST (dynamic attack simulation), SCA (dependency vulnerability scanning), and secret detection — integrated at every stage of the CI/CD pipeline. Every PR must pass SAST and secrets checks; DAST runs nightly on staging; container scans run on image build.

## Applies If (ALL must hold)

- Every change to auth, authorization, input handling, file upload, deserialization, crypto, or session code
- Pre-launch on new services before internet exposure
- Continuous: SAST + secret scanning on every PR, SCA on every build, DAST nightly on staging
- New dependency adoption (SCA before merge)
- Incident response to confirm scope and regression-test the fix
- Compliance audits (SOC 2, ISO 27001, PCI)

## Skip If (ANY kills it)

- As a substitute for threat modeling — tools find known patterns; design flaws hide from scanners
- DAST against any environment with real user data, real billing, or real downstream effects
- Replacing manual review for critical-path code (auth, crypto, payment)
- Auto-merging security patches without human review

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

- parent skill: `solo/dev/testing-developer/`
