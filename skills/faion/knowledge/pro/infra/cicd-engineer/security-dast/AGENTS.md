---
slug: security-dast
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: DAST tests running applications to find vulnerabilities in production-like environments — auth bypass, injection, header misconfigurations — that SAST cannot see.
content_id: "097184cc2283a9d7"
tags: [dast, owasp-zap, nuclei, security, runtime]
---
# Dynamic Application Security Testing (DAST) in CI/CD

## Summary

**One-sentence:** DAST tests running applications to find vulnerabilities in production-like environments — auth bypass, injection, header misconfigurations — that SAST cannot see.

**One-paragraph:** DAST tests running applications to find vulnerabilities in production-like environments — auth bypass, injection, header misconfigurations — that SAST cannot see. Run DAST against staging only, on schedule or post-deploy, never against live production. OWASP ZAP suits automation; Nuclei suits template-based targeted scanning; Burp Suite is for manual pen testing engagements.

## Applies If (ALL must hold)

- Post-deploy gate to staging — run ZAP baseline on every main-branch deploy.
- Scheduled nightly/weekly full scans of the staging environment for continuous monitoring.
- Authenticated scan coverage for endpoints that require login (form auth, OAuth, API key).
- Template-based targeted scanning with Nuclei for known CVEs and misconfigurations.

## Skip If (ANY kills it)

- Scanning production without explicit written authorization and a tight scope — compliance violation risk and potential disruption.
- Replacing pen testing for novel architectures — DAST catches known patterns, not design flaws.
- PR-level gating — DAST takes minutes and requires a deployed environment; use SAST for PR gates.
- One-off scripts or APIs without a staging environment — stand up a test harness first.

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
