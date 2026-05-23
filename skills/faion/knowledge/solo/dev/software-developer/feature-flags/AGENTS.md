---
slug: feature-flags
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Gate incomplete or experimental code behind runtime flags so deploy is decoupled from release, with explicit ownership and a documented lifecycle.
content_id: "27146dfdb4e5606d"
complexity: medium
produces: code
est_tokens: 4000
tags: [feature-flags, release-management, trunk-based-dev, progressive-rollout, kill-switch]
---
# Feature Flags

## Summary

**One-sentence:** Gate incomplete or experimental code behind runtime flags so deploy is decoupled from release, with explicit ownership and a documented lifecycle.

**One-paragraph:** Feature flags gate incomplete or experimental code behind runtime toggles, decoupling deployment from release. Every flag has an owner, an expiry date, a lifecycle (off → canary → rollout → on → cleanup), and a removal PR queued. Flags ship in a central registry; their evaluation is pure (no side effects); kill-switches are mandatory for risky changes. Output is the flag registry plus the code patterns for evaluation + cleanup.

**Ефективно для:**

- Trunk-based development without long-lived branches.
- Progressive rollouts (canary 1% → 10% → 50% → 100%).
- A/B experiments wired to analytics.
- Kill-switches for risky integrations or third-party dependencies.

## Applies If (ALL must hold)

- Continuous delivery culture: deploys ship hourly to daily.
- Risk-tier or experiment-tier features need progressive exposure.
- Codebase can carry runtime flag evaluations cheaply (web/mobile/backend, not embedded).
- Engineering owns flag lifecycle (creation + cleanup), not just product.

## Skip If (ANY kills it)

- Single-tenant or on-prem deploys where there is no central runtime to flip flags.
- Hardware/firmware where flag evaluation costs cycle budget.
- Embedded systems with no remote config channel.
- Tiny app where deploy is the release — flags add overhead without payoff.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Flag platform chosen (LaunchDarkly, Statsig, GrowthBook, in-house) + version | config | platform |
| Flag registry location (file path or service URL) | URL/path | platform |
| Owner-and-expiry policy | ADR | tech-lead |
| Analytics integration for variant assignment | endpoint | data |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[trunk-based-development]] | Flags enable trunk-based shipping of incomplete work. |
| [[logging-patterns]] | Flag evaluations are logged for observability. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (owner + expiry, pure evaluation, central registry, kill-switch for risky, cleanup PR queued, no nested flags >2) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for flag entry + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: register → wire → roll out → monitor → cleanup | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `flag_registry_entry` | sonnet | Mechanical: owner + expiry + variants + targeting. |
| `evaluation_wiring` | sonnet | Add evaluation calls + analytics integration. |
| `cleanup_pr_queue` | sonnet | Stub the removal PR when the flag is created. |

## Templates

| File | Purpose |
|------|---------|
| `templates/flag-registry.json` | Flag registry schema with owner, expiry, variants, targeting |
| `templates/flag-manager.py` | Python flag manager wrapping evaluation + logging |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-flags.py` | Validate flag registry entries against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[trunk-based-development]]
- [[logging-patterns]]
- [[ab-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps deploy cadence, exposure-risk, and platform maturity to a rule from `01-core-rules.xml`, telling the agent whether to wire a flag or skip when the runtime can't carry it. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
