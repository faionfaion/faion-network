# Infrastructure as Code Basics

## Summary

**One-sentence:** IaC adoption decision-record (config): tool choice (Terraform vs Pulumi vs CDK), state backend, secret strategy, CI pattern, baseline module catalogue.

**One-paragraph:** IaC adoption decision-record (config): tool choice (Terraform vs Pulumi vs CDK), state backend, secret strategy, CI pattern, baseline module catalogue. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Greenfield project choosing an IaC tool for the first time.
- Replacing a hand-rolled `*.sh` provisioning script with declarative code.
- Multi-environment bootstrap where consistent shape across dev/staging/prod matters.
- Onboarding a team that has only used cloud consoles (click-ops).

## Skip If (ANY kills it)

- One-shot experiment that will be torn down within a week.
- Edge devices with no consistent network — IaC needs a control plane.

**Ефективно для:**

- Стартові проекти без legacy state.
- Команди де ≥ 2 engineers редагують infra.
- GitOps target (ArgoCD / Flux / Atlantis).
- Compliance-driven setups що потребують diff-able audit trail.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cloud account + admin access | GCP / AWS / Azure | platform team |
| Source repo + CI | git + CI/CD | team |
| State backend candidate (GCS/S3/Azure Blob) | object store | platform team |
| Secret manager choice (Vault / Cloud Secret Manager) | decision | security team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft` | Server fundamentals. |

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
| `templates/decision-record.json` | Decision-record skeleton matching the output schema. |
| `templates/_smoke-test.json` | Minimum viable filled artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-iac-basics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[iac-patterns-module-design]]
- [[gcp-terraform-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
