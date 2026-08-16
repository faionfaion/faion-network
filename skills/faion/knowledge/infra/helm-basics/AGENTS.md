# Helm Basics

## Summary

**One-sentence:** Helm chart bootstrap spec (config): Chart.yaml + values.yaml + templates/ + Chart.lock with environment-specific values files and release-lifecycle conventions.

**One-paragraph:** Helm chart bootstrap spec (config): Chart.yaml + values.yaml + templates/ + Chart.lock with environment-specific values files and release-lifecycle conventions. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Wrapping a multi-resource Kubernetes application in a Helm chart.
- Managing dev / staging / prod values with one chart + per-env values file.
- Adopting a public chart (Bitnami, Jetstack) into a project.
- Integrating Helm with a GitOps controller (ArgoCD / Flux).

## Skip If (ANY kills it)

- Single Deployment + Service — `kubectl apply -k` is simpler.
- Pure operator-managed workloads — the operator owns lifecycle, not Helm.

**Ефективно для:**

- Стартові проекти що хочуть multi-env templating без Kustomize bloat.
- Teams що публікують charts в Artifact Hub або private registry.
- Atomic releases з `--atomic` + rollback.
- Charts з reusable subcharts (Postgres, Redis, MinIO).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Helm ≥ 3.12 installed locally + in CI | binary | platform team |
| Kubernetes cluster (kind / minikube / cloud) | cluster | team |
| Application manifests (Deployment/Service/Ingress/ConfigMap) | yaml | team |
| Repo for chart storage (OCI / classic) | registry | platform team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/k8s-basics` | Kubernetes object model + kubectl. |

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
| `scripts/validate-helm-basics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[helm-advanced]]
- [[k8s-deployment-workloads]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config.json`

```json
{
  "chart_name": "acme-app",
  "chart_version": "0.3.1",
  "api_version": "v2",
  "templates": [
    "deployment.yaml",
    "service.yaml",
    "ingress.yaml",
    "configmap.yaml"
  ],
  "values_files": [
    "values.yaml",
    "values.dev.yaml",
    "values.staging.yaml",
    "values.prod.yaml"
  ],
  "dependencies": [
    {
      "name": "postgresql",
      "version": "15.5.0",
      "repository": "oci://registry-1.docker.io/bitnamicharts"
    }
  ],
  "lockfile_committed": true,
  "owner": {
    "name": "Olena Boyko",
    "role": "platform lead"
  },
  "produced_at": "2026-05-23T10:00:00Z"
}
```

### `templates/_smoke-test.json`

```json
{
  "chart_name": "acme-app",
  "chart_version": "0.3.1",
  "api_version": "v2",
  "templates": [
    "deployment.yaml",
    "service.yaml",
    "ingress.yaml",
    "configmap.yaml"
  ],
  "values_files": [
    "values.yaml",
    "values.dev.yaml",
    "values.staging.yaml",
    "values.prod.yaml"
  ],
  "owner": {
    "name": "Olena Boyko",
    "role": "platform lead"
  },
  "produced_at": "2026-05-23T10:00:00Z"
}
```
