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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-security-iam.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[gcp-storage]]
- [[gcp-terraform-templates]]
- [[k8s-security-hardening]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config.json`

```json
{
  "project_id": "acme-prod-12",
  "owner": {
    "name": "Olena Boyko",
    "role": "head of security"
  },
  "service_accounts": [
    {
      "email": "deploy@acme-prod-12.iam.gserviceaccount.com",
      "purpose": "CI deploys via WIF",
      "roles": [
        "roles/run.developer",
        "roles/iam.serviceAccountUser"
      ]
    }
  ],
  "vpcsc_perimeter": {
    "name": "prod-perimeter",
    "restricted_services": [
      "storage.googleapis.com",
      "bigquery.googleapis.com"
    ]
  },
  "cmek_keys": [
    {
      "name": "projects/acme-kms/locations/eu/keyRings/prod/cryptoKeys/sql",
      "rotation_period_days": 90
    }
  ],
  "audit_sink": {
    "destination": "bigquery.googleapis.com/projects/acme-logs/datasets/audit",
    "retention_days": 400
  },
  "wif_pools": [
    {
      "pool_id": "github-pool",
      "provider": "github-provider",
      "issuer_uri": "https://token.actions.githubusercontent.com"
    }
  ],
  "produced_at": "2026-05-23T10:00:00Z"
}
```

### `templates/_smoke-test.json`

```json
{
  "project_id": "acme-prod-12",
  "owner": {
    "name": "Olena Boyko",
    "role": "head of security"
  },
  "service_accounts": [
    {
      "email": "deploy@acme-prod-12.iam.gserviceaccount.com",
      "purpose": "CI deploys via WIF",
      "roles": [
        "roles/run.developer",
        "roles/iam.serviceAccountUser"
      ]
    }
  ],
  "vpcsc_perimeter": {
    "name": "prod-perimeter",
    "restricted_services": [
      "storage.googleapis.com",
      "bigquery.googleapis.com"
    ]
  },
  "cmek_keys": [
    {
      "name": "projects/acme-kms/locations/eu/keyRings/prod/cryptoKeys/sql",
      "rotation_period_days": 90
    }
  ],
  "audit_sink": {
    "destination": "bigquery.googleapis.com/projects/acme-logs/datasets/audit",
    "retention_days": 400
  },
  "wif_pools": [
    {
      "pool_id": "github-pool",
      "provider": "github-provider",
      "issuer_uri": "https://token.actions.githubusercontent.com"
    }
  ],
  "produced_at": "2026-05-23T10:00:00Z"
}
```
