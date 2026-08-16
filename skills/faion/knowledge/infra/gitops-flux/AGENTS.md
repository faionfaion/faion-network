# Flux CD — Setup and Operation

## Summary

**One-sentence:** Generates a Flux config (GitRepository + Kustomization + HelmRelease + ImagePolicy CRDs + multi-source reconciliation + notification controller) for Kubernetes GitOps without a UI.

**One-paragraph:** Generates a Flux config (GitRepository + Kustomization + HelmRelease + ImagePolicy CRDs + multi-source reconciliation + notification controller) for Kubernetes GitOps without a UI. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Multi-tenant clusters з суворою CRD-decoupled isolation.
- Helm-heavy stacks (Flux HelmRelease + ImagePolicy для auto-bump).
- Automation-first teams без потреби в built-in UI.
- Multi-source реконсіляція (Git + Helm + OCI / S3 bucket).

## Applies If (ALL must hold)

- Decision to adopt Flux (not ArgoCD) is signed off by platform.
- Kubernetes ≥1.27 with CRD support.
- Helm-heavy or Kustomize-heavy workload (Flux excels here).
- Multi-team setup with isolation requirements.

## Skip If (ANY kills it)

- Decision was ArgoCD — use the ArgoCD methodology instead.
- Cluster K8s version <1.25 — Flux controllers require modern API surface.
- Single-team single-cluster — ArgoCD UI may be a better starter.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cluster admin access | kubeconfig | Platform team |
| Git repo with desired-state YAML | URL + read token | Platform team |
| Helm chart sources | OCI / HTTP URLs | App teams |
| Notification channel | Slack / Teams webhook | SRE |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-gitops-flux` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-instance.json` | JSON instance of a filled config artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gitops-flux.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config-instance.json`

```json
{
  "sources": [
    {
      "kind": "GitRepository",
      "name": "platform-state",
      "url": "https://github.com/acme/platform-state.git"
    }
  ],
  "kustomizations": [
    {
      "name": "platform",
      "source_ref": "platform-state",
      "path": "./clusters/prod",
      "prune": true
    }
  ],
  "helmreleases": [
    {
      "name": "ingress",
      "chart_ref": "oci://ghcr.io/acme/charts/ingress",
      "image_automation": true
    }
  ],
  "notifications": {
    "provider": "slack",
    "channel": "#platform-flux"
  },
  "tenants": [
    {
      "name": "team-a",
      "namespace": "tenant-a",
      "rbac_ref": "rbac/team-a.yaml"
    }
  ],
  "owner": "platform@team.io",
  "last_reviewed": "2026-05-23"
}
```
