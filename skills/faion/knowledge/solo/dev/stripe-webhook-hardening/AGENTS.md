---
slug: stripe-webhook-hardening
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Stripe webhook hardening report: secret rotation cadence, timestamp tolerance, raw-body integrity, IP and rate limits, audit log of forged-event attempts, signed off by a named owner.
content_id: "af330e78321b533b"
complexity: medium
produces: report
est_tokens: 5200
tags: [stripe, webhook, hardening, security, rotation]
---
# Stripe Webhook Hardening

## Summary

**One-sentence:** Stripe webhook hardening report: secret rotation cadence, timestamp tolerance, raw-body integrity, IP and rate limits, audit log of forged-event attempts, signed off by a named owner.

**One-paragraph:** Builds on the handler pattern with hardening focused on attack surface and forensics. Covers Stripe-Signature timestamp tolerance (replay-window cap), webhook secret rotation procedure, raw-body integrity (no JSON.parse before verify), rate limits at the edge, IP allowlist when feasible, and an audit log of failed verifications. Produces a hardening report that pins each control to an observable check plus a remediation SLA.

**Ефективно для:**

- Pre-launch hardening - закрити webhook attack surface перед першим billing event.
- Post-incident після forged event - встановити audit + secret rotation.
- Compliance audit (SOC 2 / PCI) - продемонструвати controls по webhook.
- Перехід з shared secret на per-endpoint - впровадити cadence rotation.
- Аудит rate limits після brute-force - підняти hard cap + alerting.

## Applies If (ALL must hold)

- Stripe webhook handler is in production (at least one live event consumed).
- Team has secret manager (Vault, AWS Secrets Manager, 1Password CLI, etc.).
- Edge layer (CDN, API gateway, or reverse proxy) where rate-limit + IP rules can be applied.
- Audit log destination (DB table, log aggregator) accepts the events.

## Skip If (ANY kills it)

- Greenfield prototype with no production traffic - delay hardening until launch.
- Test-mode webhook only - hardening cost not justified.
- Compliance overrides this guidance (legal mandate) - defer to legal.
- Already covered by an enterprise WAF + audit stack maintained by another team.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Webhook handler in prod | endpoint URL + secret name | engineering |
| Secret manager | rotation API + IAM role | platform |
| Edge layer | ability to configure rate limit + IP allowlist | platform |
| Audit destination | table or log stream with retention >= 90 days | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stripe-webhook-handler-pattern]] | the base handler this hardens. |
| [[security-testing]] | wider security context the hardening plugs into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: timestamp tolerance, secret rotation, raw-body integrity, edge rate limit, audit log, skip-gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: tolerance, rotation, raw-body, edge controls, audit | ~800 |
| `content/05-examples.xml` | essential | Worked example: 90d rotation + 5min tolerance + WAF rate-limit | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals to a rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-current-controls` | sonnet | Inventory of current controls plus gap analysis. |
| `design-rotation-cadence` | sonnet | Cadence vs ops cost per-team judgement. |
| `write-audit-rule` | haiku | Templated log-filter snippet. |
| `review-attack-surface` | opus | Stakes high; cross-control synthesis decides launch. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hardening-report.md` | Markdown skeleton for the hardening report (controls + SLA + sign-off). |
| `templates/rotation-runbook.md` | Webhook-secret rotation runbook with rollback plan. |
| `templates/_smoke-test.json` | Filled-in minimum viable hardening report for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stripe-webhook-hardening.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[stripe-webhook-handler-pattern]]
- [[security-testing]]
- [[structured-logging-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree checks preconditions, then timestamp tolerance, then rotation cadence, then edge controls, then audit destination. Every leaf maps to a rule id from `content/01-core-rules.xml`, with skip-this-methodology as the default for pre-prod work.
