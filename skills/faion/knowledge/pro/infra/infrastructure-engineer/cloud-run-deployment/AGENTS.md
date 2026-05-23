---
slug: cloud-run-deployment
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Cloud Run deployment spec: revision tagging, traffic split (canary / blue-green), service account least-privilege, secret access via Secret Manager, container image hardening, ingress controls, observability hooks."
content_id: "85f1ad7d6ef06616"
complexity: deep
produces: spec
est_tokens: 5000
tags: [gcp, cloud-run, deployment, traffic-split, revisions, infra]
---
# Cloud Run Deployment

## Summary

**One-sentence:** Cloud Run deployment spec: revision tagging, traffic split (canary / blue-green), service account least-privilege, secret access via Secret Manager, container image hardening, ingress controls, observability hooks.

**One-paragraph:** Cloud Run deployment spec: revision tagging, traffic split (canary / blue-green), service account least-privilege, secret access via Secret Manager, container image hardening, ingress controls, observability hooks. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Service deploys to Cloud Run via automated pipeline.
- Named platform-lead can sign off on deployment pattern.
- Service handles non-trivial traffic OR sensitive data.

## Skip If (ANY kills it)

- Service runs on GKE / Cloud Functions Gen 1.
- One-off prototype with no production traffic.
- Team has mature deploy pattern + audit-ready already.

**Ефективно для:**

- Команди що деплоять Cloud Run у production через CI/CD (Cloud Build / GitHub Actions).
- Canary rollouts через traffic-split (10% → 50% → 100%).
- Security-conscious deploys з Secret Manager + Artifact Registry.
- Migration з App Engine / GKE на Cloud Run.

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
| `solo/dev/software-architect/architecture-decision-records` | Base ADR format the output extends. |
| `pro/dev/software-architect` | Role/operating context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cloud-run-deployment.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
