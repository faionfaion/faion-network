---
slug: aws-cli-setup
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "AWS CLI v2 + IAM Identity Center (SSO) baseline config: named profiles, short-lived credentials, MFA enforcement, no long-lived access keys committed to disk in plain text."
content_id: "bc92af0a00757e53"
complexity: medium
produces: config
est_tokens: 4200
tags: [aws, cli, credentials, sso, iam, infra]
---
# AWS CLI Setup

## Summary

**One-sentence:** AWS CLI v2 + IAM Identity Center (SSO) baseline config: named profiles, short-lived credentials, MFA enforcement, no long-lived access keys committed to disk in plain text.

**One-paragraph:** AWS CLI v2 + IAM Identity Center (SSO) baseline config: named profiles, short-lived credentials, MFA enforcement, no long-lived access keys committed to disk in plain text. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Team uses AWS and developers run `aws` CLI locally.
- ≥ 1 AWS account exists with IAM Identity Center (SSO) configured or required by org policy.
- A named security-lead can approve the baseline config.

## Skip If (ANY kills it)

- Single user / single account hobby — defaults are fine.
- No SSO in the org (yet) — set up Identity Center before applying this baseline.
- Team already on IAM-roles-only via aws-vault / leapp with no changes pending.

**Ефективно для:**

- Команди що мають ≥ 2 AWS accounts (prod / staging / dev).
- Розробники яким потрібен local AWS CLI access на щодня.
- Аудити безпеки що вимагають short-lived credentials замість access keys.
- Onboarding нових інженерів з зрозумілим credential flow.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev` | Parent role context. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Template fill of allow-lists + env-var blocks. |
| `populate-policy` | sonnet | Per-clause translation into config fields. |
| `breach-protocol-review` | opus | Cross-engagement risk + breach-response synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/policy.yaml` | YAML config skeleton with allow-list / deny-list / telemetry-overrides / audit-cadence. |
| `templates/_smoke-test.yaml` | Minimum viable filled policy. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-cli-setup.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
