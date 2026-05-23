---
slug: helm-advanced
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Production Helm chart spec (config): library charts, hooks, tests, umbrella composition, checksum annotations, required-values guards, resource-policy keep."
content_id: "591cce887ab2c5f0"
complexity: deep
produces: config
est_tokens: 4200
tags: [helm, kubernetes, library-charts, hooks, umbrella-charts]
---
# Helm Advanced Patterns

## Summary

**One-sentence:** Production Helm chart spec (config): library charts, hooks, tests, umbrella composition, checksum annotations, required-values guards, resource-policy keep.

**One-paragraph:** Production Helm chart spec (config): library charts, hooks, tests, umbrella composition, checksum annotations, required-values guards, resource-policy keep. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Building reusable template helpers shared across ≥ 5 application charts.
- Adding lifecycle hooks (pre-upgrade migrations, post-install smoke tests, pre-delete cleanup).
- Composing multi-service releases (app + DB + cache) via an umbrella chart.
- Hardening an existing chart with checksum annotations, required-values, resource-policy keep.

## Skip If (ANY kills it)

- Single-service deployment with one Deployment + one Service — use raw kubectl apply.
- Operator-orchestrated workloads — use the operator's CRDs, not Helm.

**Ефективно для:**

- Platform teams що ship ≥ 10 charts з повторюваними patterns.
- Migrations що потребують pre-upgrade Job.
- Validated releases з helm test post-install.
- GitOps з ArgoCD/Flux і Helm-driven manifests.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Helm ≥ 3.12 | binary | platform team |
| Existing application chart(s) | Helm chart | team |
| Test framework choice (helm test / chart-testing) | decision | platform team |
| values.schema.json (optional) | JSON schema | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/helm-basics` | Chart structure + templating syntax fundamentals. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Mechanical template fill from prerequisites table. |
| `populate-policy` | sonnet | Per-clause translation into config fields with judgment. |
| `review-breach-cases` | opus | Cross-engagement risk + failure-mode synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.json` | Config skeleton matching the output schema. |
| `templates/_smoke-test.json` | Minimum viable filled artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-helm-advanced.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[helm-basics]]
- [[k8s-deployment-workloads]]
- [[iac-patterns-module-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
