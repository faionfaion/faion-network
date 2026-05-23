---
slug: k8s-version-upgrade-runbook-template
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: End-to-end runbook spec for major-version K8s upgrade: API deprecation audit, addon compat, etcd backup, control-plane upgrade, node-pool rolling refresh, validation, rollback.
content_id: "1a980cfbf5397ce7"
complexity: deep
produces: spec
est_tokens: 4300
tags: [k8s, upgrade, runbook, spec, infra]
---
# K8s Version Upgrade Runbook Template

## Summary

**One-sentence:** End-to-end runbook spec for major-version K8s upgrade: API deprecation audit, addon compat, etcd backup, control-plane upgrade, node-pool rolling refresh, validation, rollback.

**One-paragraph:** End-to-end runbook spec for major-version K8s upgrade: API deprecation audit, addon compat, etcd backup, control-plane upgrade, node-pool rolling refresh, validation, rollback. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Кластер у production, треба перейти з 1.27 на 1.29 з мінімальним downtime.
- API deprecations (policy/v1beta1, autoscaling/v2beta2) ще лежать у маніфестах — потрібен audit.
- Addons (CNI, ingress) мають version matrix, що залежить від control-plane версії.
- Команда хоче канонічний runbook замість ad-hoc upgrade — щоб повторити кожні 6 місяців.

## Applies If (ALL must hold)

- Cluster is being upgraded across at least one minor version (e.g. 1.27 -> 1.29)
- Cluster runs production workloads with SLOs (cannot 'just delete and recreate')
- Cluster has addons (CNI, ingress controller, monitoring) that need compatibility check
- Etcd backup target is available (S3 / GCS) and tested

## Skip If (ANY kills it)

- Minor patch upgrades inside same minor — use the simpler patch flow
- Workload rolling-update mechanics — use k8s-rolling-update
- Cluster-internal canary deployment — use k8s-canary-progressive

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger context | Markdown / ticket / transcript | upstream task |
| Named owner | string (handle, email, role) | team roster |
| Storage location | URL / repo path | artefact store |
| Prior cycle artefact (if any) | this methodology's output | last run |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/AGENTS.md` | parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/sdd` | SDD discipline for artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + run-the-checklist + skip-this-methodology conclusions | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid + invalid + forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom / root-cause / fix | ~700 |
| `content/04-procedure.xml` | essential | step-by-step procedure (input/action/output/decision-gate) | ~700 |
| `content/05-examples.xml` | essential | one worked end-to-end example with inputs and final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | root-question + branches + conclusion refs to 01-core-rules | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment over bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high or evidence chain is required |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | working skeleton matching the `produces=spec` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-k8s-version-upgrade-runbook-template.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Is the upgrade across at least one minor version on a production cluster with SLOs?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
