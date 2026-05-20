---
slug: runbook-as-code-pattern
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Runbook as Code Pattern: the pro-tier infra practice of keeping runbooks in the service repo, tested in CI, and deep-linked from alerts — independent of the geek-tier AI-input format.
content_id: "a84ddb716d4bc342"
tags: [runbook-as-code-pattern, infra, pro]
---
# Runbook as Code Pattern

## Summary

**One-sentence:** Treat each runbook as a versioned file in the service repo, with CI checks for link rot and command syntax, and a stable URL/anchor that every alert deep-links to so on-call lands on the exact step that matches the firing rule.

**One-paragraph:** The geek-tier methodology `inc-runbook-as-markdown-tagged-steps` exists but is framed as an AI-input format. The baseline "runbook lives in the repo, is reviewed with the service, is tested in CI, is deep-linked from alerts" practice is foundational pro-tier infra and should not be gated to geek. This methodology codifies that baseline: repo location convention, mandatory front-matter for alert-to-anchor mapping, CI checks (link rot, dead command references, anchor uniqueness), and the alert-rule field that must carry the runbook URL. Output is a per-service runbook file that lives next to the code it operates, is reviewed like code, and is unreachable from production alerts only when something is wrong.

## Applies If (ALL must hold)

- the service emits production alerts that page humans (Pagerduty, Opsgenie, etc.)
- the service has a code repo where the runbook can co-live
- the team has CI for the repo
- tier == pro or higher

## Skip If (ANY kills it)

- runbooks must live in a separate runbook-store-of-record (regulated environments where on-call docs are managed in a GRC tool)
- the service is in pre-production with no paging alerts
- the team has already adopted `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps` and that adoption covers the same baseline — that methodology supersedes this one for AI-driven on-call

## Prerequisites

- alerting platform that supports a `runbook_url` field per rule
- repo with CI capacity to run a fast (< 60s) link/anchor check
- the service team owns both code and alerts (no separate "ops team writes our runbooks")

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill |
| `pro/infra/alert-triage-decision-tree` | the upstream alert pattern this runbook structure complements |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: repo-colocation, anchor-per-alert, ci-link-and-anchor-check, alert-rule-carries-url, review-with-code | ~1100 |

## Related

- parent skill: `pro/infra/devops-engineer`
- upstream playbook: `role-devops-engineer/Design SLOs + error budgets before first deploy`
- geek-tier specialisation: `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
