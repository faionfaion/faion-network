---
slug: security-dast
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a DAST CI config (ZAP or Nuclei) that scans STAGING only, with explicit scope file, scheduled cadence, and SARIF upload — never targets production.
content_id: "1b8c172d347249e6"
complexity: medium
produces: config
est_tokens: 4000
tags: [dast, owasp-zap, nuclei, security, runtime]
---

# Dynamic Application Security Testing (DAST) in CI/CD

## Summary

**One-sentence:** Produces a DAST CI config (ZAP or Nuclei) that scans STAGING only, with explicit scope file, scheduled cadence, and SARIF upload — never targets production.

**One-paragraph:** DAST finds the runtime vulnerabilities SAST cannot see — auth bypass, SSRF, missing security headers, injection vectors that depend on real HTTP responses. The non-negotiable: target STAGING only, with a scope-file allow/deny list (no third-party services, no payment, no email senders, no destructive endpoints), scheduled cadence + post-deploy gate, and SARIF upload to GitHub Security. Tool choice: ZAP for general automation, Nuclei for template-based CVE / misconfig hunting. Output: workflow YAML + .zap/rules.tsv (or Nuclei target list) + scheduled run cadence.

**Ефективно для:**

- Post-deploy gate to staging — ZAP baseline (passive) на кожному merge.
- Nightly/weekly full scans staging environment.
- Authenticated scan coverage (form auth / OAuth / API key) — endpoints behind login.
- Template-based targeted scanning (Nuclei) для відомих CVE + misconfig.

## Applies If (ALL must hold)

- A dedicated staging / pre-prod environment exists that mirrors production.
- Service exposes HTTP endpoints reachable by the CI worker.
- Scope file (allowlist + denylist of paths) can be authored.

## Skip If (ANY kills it)

- No staging environment exists — stand one up first; DAST against production is a compliance violation.
- PR-level gating need — DAST is minutes-slow + requires a deploy; use SAST at PR.
- Replacing pen testing for novel architectures — DAST catches known patterns, not design flaws.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Staging URL | FQDN of pre-prod environment | deploy pipeline |
| Scope file | .zap/rules.tsv OR Nuclei target list | security team |
| Authentication recipe | form / OAuth / API key | app team |
| Run cadence | post-deploy + nightly / weekly | security cadence policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[security-sast]] | DAST is the shift-right complement of SAST |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: staging-only, scope-file-required, pin-templates, scheduled-cadence, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for DAST CI config + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: prod-target, no-scope-file, head-of-templates, no-cadence | 800 |
| `content/04-procedure.xml` | essential | 5 steps: pick tool → scope → auth → schedule → upload SARIF | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on tool + cadence → rule | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-tool` | haiku | ZAP / Nuclei / Burp — deterministic on use case. |
| `compose-workflow` | sonnet | Assemble the CI YAML with auth + scope file include. |
| `triage-findings` | sonnet | Reduce noise + write FAIL/IGNORE rules in scope file. |

## Templates

| File | Purpose |
|------|---------|
| `templates/zap-baseline.yml` | GitHub Actions workflow: ZAP baseline scan against staging post-deploy + nightly |
| `templates/.zap/rules.tsv` | ZAP rules scope file: PASS / WARN / FAIL / IGNORE per rule id |
| `templates/nuclei-scan.yml` | GitHub Actions workflow: Nuclei targeted scan with pinned templates |
| `templates/_smoke-test.json` | Minimum DAST CI config artefact used by validate-security-dast.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-dast.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[security-sast]]
- [[security-container-scanning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when wiring DAST into a new pipeline or auditing an existing one.
