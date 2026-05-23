---
slug: security-testing
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Security-testing plan + report: SAST per language, dependency audit, DAST (ZAP) against staging, secrets scanning pre-commit, OWASP ASVS coverage matrix per release.
content_id: "d442a7a7909d7168"
complexity: medium
produces: report
est_tokens: 5100
tags: [security, sast, dast, dependency-audit, owasp]
---
# Security Testing

## Summary

**One-sentence:** Security-testing plan + report: SAST per language, dependency audit, DAST (ZAP) against staging, secrets scanning pre-commit, OWASP ASVS coverage matrix per release.

**One-paragraph:** Security testing fails when SAST runs once a quarter, when dependency audits ignore transitive deps, when DAST never sees auth-protected paths, when secret scanning runs only at PR (not pre-commit), and when the ASVS coverage is implicit. This methodology produces a per-release plan + report: SAST tools per language (semgrep / bandit / gosec), dependency audit via osv.dev + GitHub Advisory, ZAP authenticated scan against staging, gitleaks pre-commit + CI, and an ASVS L1 coverage matrix.

**Ефективно для:**

- Перший security pass перед production launch.
- SOC 2 / ISO 27001 готовність - треба ASVS matrix.
- Dependency hijack incident - переглянути audit pipeline.
- Secrets витекли в git - впровадити gitleaks pre-commit.
- DAST scan не покриває auth flow - налаштувати ZAP context.

## Applies If (ALL must hold)

- Service ships to production with internet exposure.
- Compliance regime (SOC 2 / ISO / GDPR) is in scope OR launch is imminent.
- Staging environment exists where DAST can run safely.
- Team can act on findings within a documented window.

## Skip If (ANY kills it)

- Project is local-only with no network surface.
- Compliance regime forbids running automated scans against this environment.
- Throwaway prototype with no production users or sensitive data.
- Security testing is delegated entirely to an external pentest firm under contract.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Language inventory | list of languages + versions | engineering |
| Dependency lockfiles | package-lock.json / poetry.lock / Cargo.lock | engineering |
| Staging URL + auth creds | test account credentials | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[supply-chain-risk-checklist-spike]] | library-level supply-chain inputs feed dependency audit section. |
| [[rate-limiting]] | DAST should account for limits to avoid self-DoS during scan. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: SAST on PR, dep audit with transitive, DAST authenticated, secrets pre-commit, ASVS matrix, fix window by severity, scan rate-limit aware | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: SAST, dep audit, DAST, secrets, ASVS matrix | ~900 |
| `content/05-examples.xml` | essential | Worked example for a SaaS release security pass | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-sast` | haiku | Language → tool mapping. |
| `configure-dast-context` | sonnet | Per-app judgement on auth flow + rate limits. |
| `draft-asvs-matrix` | sonnet | Map controls to project state. |
| `triage-findings` | opus | Stakes high; severity vs exploitability judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-security.yml` | GitHub Actions snippet wiring SAST + dep audit + secrets scan. |
| `templates/asvs-matrix.csv` | ASVS L1 coverage matrix template (markdown table). |
| `templates/bandit-config.yaml` | Bandit config: skip rules with project rationale + severity gate. |
| `templates/security-ci.yml` | Variant CI security workflow snippet (semgrep + bandit + gitleaks). |
| `templates/_smoke-test.json` | Minimum viable security report for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-testing.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[supply-chain-risk-checklist-spike]]
- [[rate-limiting]]
- [[api-error-handling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - SAST cadence, transitive coverage, DAST auth, secrets gate - onto a rule from `content/01-core-rules.xml`. Use it before any release: it catches quarterly-SAST, direct-only deps, unauth-only DAST upstream.
