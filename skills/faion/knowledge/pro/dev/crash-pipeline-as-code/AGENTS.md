---
slug: crash-pipeline-as-code
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "f6f80615d9d65213"
summary: Crash-tracking pipeline (Sentry / Crashlytics / Bugsnag) defined as code — symbol upload, sourcemap upload, alert rules, dashboards, retention — checked in and gated like any other infrastructure.
tags: [crash-reporting, sentry, crashlytics, observability, infra-as-code, mobile-ship]
---
# Crash Pipeline as Code

## Summary

**One-sentence:** Defines the crash-tracking and observability pipeline (symbol/source-map upload, alert rules, dashboards, retention) as code under version control — so a new release does not lose deobfuscation, an alert rule does not vanish in a console click, and Production Readiness is checkable in a PR.

**One-paragraph:** Crash reporting (Sentry, Crashlytics, Bugsnag, Datadog APM) is set up manually in most teams: a developer uploads dSYMs from their laptop, clicks alert rules into the web console, draws a dashboard. Six months later: symbols missing for one release, alert rule deleted by accident, dashboard owned by a person who left. The methodology pins the move: every artifact of the crash pipeline lives in code (CI step for symbol upload, IaC for alert rules where the vendor supports it, dashboard-as-code, retention as a setting in a config file). Output: a `crash-pipeline/` folder reviewed and deployed alongside the app, with PR-gated production-readiness on every release.

## Applies If (ALL must hold)

- Project ships mobile builds OR web/native apps with non-trivial native code.
- A crash-reporting vendor is in use (Sentry, Crashlytics, Bugsnag, Datadog).
- The team has felt the pain of un-symbolicated crashes OR missing alerts at least once.
- Vendor supports configuration via API / Terraform / config-as-code.

## Skip If (ANY kills it)

- Pure server-side stack with no native or web client — error tracking is different.
- Vendor exclusively web-console (no API for rules/dashboards) — methodology degrades; document the manual steps in a runbook instead.
- Single-developer app pre-launch — set up the basics, this methodology applies after first release.
- Project uses self-hosted error tracker with no IaC integration — apply only the symbol-upload + retention parts.

## Prerequisites

- Crash-tracking vendor selected and project set up.
- CI pipeline exists.
- Service-account credentials for vendor's API (stored in secret manager).
- A release-versioning scheme (build numbers, semantic versions, or commit SHA).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/ci-fundamentals` | CI pipeline assumed; this adds crash-pipeline jobs. |
| `pro/dev/software-developer/observability-essentials` | Observability vocabulary (alert, SLO, runbook) assumed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: symbols-in-CI, dSYM verification, alert-rules-in-code, dashboard-as-code, retention | ~1000 |
| `content/02-output-contract.xml` | essential | crash-pipeline/ folder shape; per-release symbol manifest; alert-rule schema | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: silent upload failure, drifted rules, expired token, etc. | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `write-symbol-upload-step` | sonnet | Coding task: per-platform commands |
| `convert-console-rules-to-code` | sonnet | Mechanical: export rules and rewrite as IaC |
| `dashboard-design-review` | opus | Judgment: choose right charts + alert thresholds |

## Templates

| File | Purpose |
|------|---------|
| `templates/crash-pipeline/` | Folder skeleton: ci-jobs/, alert-rules/, dashboards/, retention.yaml |
| `templates/sentry-terraform-stub/` | Sentry-specific Terraform example |
| `templates/symbol-upload-actions/` | GitHub Actions snippets per platform |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/verify-symbol-upload.sh` | Post-release: confirm vendor returned 200 for symbol upload AND symbols are deobfuscating | Post-release |

## Related

- parent skill: `pro/dev/software-developer/`
- peer methodology: `observability-essentials`, `pre-release-checklist`, `mobile-ship-process`
- external: [Sentry docs](https://docs.sentry.io/) · [Firebase Crashlytics](https://firebase.google.com/docs/crashlytics) · [Bugsnag](https://www.bugsnag.com/)
