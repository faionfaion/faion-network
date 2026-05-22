---
slug: security-testing
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Security testing identifies vulnerabilities before exploitation through static analysis (SAST), dynamic testing (DAST), dependency scanning, and OWASP Top 10 scenario tests.
content_id: "ce3cce25f7e29686"
tags: [security, testing, owasp, sast, ci]
---
# Security Testing

## Summary

**One-sentence:** Security testing identifies vulnerabilities before exploitation through static analysis (SAST), dynamic testing (DAST), dependency scanning, and OWASP Top 10 scenario tests.

**One-paragraph:** Security testing identifies vulnerabilities before exploitation through static analysis (SAST), dynamic testing (DAST), dependency scanning, and OWASP Top 10 scenario tests. Core rule: assert exact HTTP status codes (401/403/400) — not just "not 500" — and assert absence of sensitive data in responses, not just "request did not crash."

## Applies If (ALL must hold)

- Pre-deploy gate after any change touching auth, sessions, file upload, deserialization, or SQL queries
- After bumping dependencies (transitive CVEs surface via pip-audit, npm audit)
- Wiring SAST + secrets scan + dep-audit into CI before opening the project to outside contributors
- Reviewing AI-generated PRs — LLMs frequently re-introduce SQL string concatenation and missing CSRF

## Skip If (ANY kills it)

- Pre-commit on every save — DAST/fuzzing is too slow; restrict to PR/CI or nightly
- As a substitute for threat modelling — testing only finds what you tell it to look for
- For business-logic flaws (price tampering, IDOR via valid-but-wrong IDs) — those need handwritten scenario tests
- Penetration testing of production without written authorization (legal exposure)

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

- parent skill: `solo/dev/software-developer/`
