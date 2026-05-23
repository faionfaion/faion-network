---
slug: helm-values-diff-reviewer
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Renders the values delta for a Helm bump as a reviewable artefact: rendered-manifest diff + risk classification per change + named approver per risk tier, so silent values changes cannot ship to prod."
content_id: "88610fab8fd1309f"
complexity: medium
produces: report
est_tokens: 5000
tags: [helm, k8s, diff-review, release, infra]
---
# Helm Values Diff Reviewer

## Summary

**One-sentence:** Renders the values delta for a Helm bump as a reviewable artefact: rendered-manifest diff + risk classification per change + named approver per risk tier, so silent values changes cannot ship to prod.

**One-paragraph:** Renders the values delta for a Helm bump as a reviewable artefact: rendered-manifest diff + risk classification per change + named approver per risk tier, so silent values changes cannot ship to prod. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Helm chart upstream is bumped on a cadence (≥ once per release cycle).
- Named release-owner can sign off on the diff and tag risk per change.
- CI can render `helm template` for both `from` and `to` versions on the PR.

## Skip If (ANY kills it)

- Chart is internally owned and values surface is < 5 keys — review can be inline in PR.
- Team does not run Helm at all (raw manifests + Kustomize) — use a Kustomize-diff variant.
- No named release-owner — defer until ownership is resolved.

**Ефективно для:**

- Команди де Helm bumps періодично ламають prod через silent values changes.
- Реліз-менеджери що потребують один аркуш для аудиту bump-перед-merge.
- GitOps-флоу де ArgoCD сам синхронізує — потрібен gate перед PR merge.
- Аудит-ready середовища (SOC2 / ISO27001) з вимогою release-trail.

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
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from header + section list. |
| `populate-evidence` | sonnet | Per-row evidence link + summary judgment. |
| `outcome-synthesis` | opus | Cross-cycle synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Report skeleton with frontmatter + sections + evidence anchors per row. |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-helm-values-diff-reviewer.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
