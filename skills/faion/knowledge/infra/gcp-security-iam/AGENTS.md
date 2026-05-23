# GCP Security and IAM

## Summary

**One-sentence:** GCP IAM least-privilege config: Workload Identity Federation, VPC Service Controls, CMEK rotation, audit-log routing produced as Terraform-friendly JSON policy.

**One-paragraph:** GCP IAM least-privilege config: Workload Identity Federation, VPC Service Controls, CMEK rotation, audit-log routing produced as Terraform-friendly JSON policy. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Configuring IAM roles and service accounts for a new GCP project.
- Eliminating service-account key files from CI/CD pipelines via Workload Identity Federation.
- Implementing data-exfiltration controls around Cloud Storage / BigQuery (VPC-SC).
- Running quarterly IAM audit with IAM Recommender drift detection.

## Skip If (ANY kills it)

- Network topology design — use gcp-networking-vpc methodology.
- Compute or GKE cluster provisioning — use gcp-compute-gke / k8s-* methodologies.

**Ефективно для:**

- GCP-only orgs з production workloads на Cloud Run + GKE.
- Команди що мігрують з key-file SA на keyless OIDC (GitHub Actions, GitLab).
- Compliance-driven setups з SOC2 / ISO27001 vault-rotation cadence.
- Audit-ready IAM з named human-owner на кожен SA.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| GCP project + Org policies enabled | gcloud | platform team |
| Workload Identity Pool naming spec | doc | security team |
| List of CI providers (OIDC issuers) | list | devops team |
| Named SA owner per service | RACI | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft` | Upstream networking + tier conventions. |
| `pro/security/server-craft` | Cross-domain security baseline. |

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
| `scripts/validate-gcp-security-iam.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[gcp-storage]]
- [[gcp-terraform-templates]]
- [[k8s-security-hardening]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
