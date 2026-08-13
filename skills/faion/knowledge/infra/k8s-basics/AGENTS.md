# Kubernetes Basics

## Summary

**One-sentence:** Workload baseline spec (config): Deployment + Service + ConfigMap + Secret + RBAC ServiceAccount; namespace, labels, probes, container security context defaults.

**One-paragraph:** Workload baseline spec (config): Deployment + Service + ConfigMap + Secret + RBAC ServiceAccount; namespace, labels, probes, container security context defaults. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Deploying an application to Kubernetes for the first time.
- Migrating a docker-compose stack to k8s manifests.
- Establishing baseline labels, namespaces, and probes for a new service.
- Wiring RBAC ServiceAccount for app-side cloud auth.

## Skip If (ANY kills it)

- Pure serverless workload (Cloud Run / Lambda) - k8s not needed.
- Existing service already on k8s with stable manifests (use rolling-update / scaling methodology instead).

**Ефективно для:**

- Стартовий deployment з 1-3 containers.
- Stateless services без persistent storage.
- Standard ClusterIP / LoadBalancer / NodePort patterns.
- Standard liveness + readiness + startup probes.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Kubernetes cluster (kind / GKE / EKS / AKS) | cluster | platform team |
| kubectl context for the cluster | kubeconfig | team |
| Container image in a registry | OCI image | team |
| Namespace assigned to the service | k8s ns | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft` | Container fundamentals. |

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
| `scripts/validate-k8s-basics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[k8s-deployment-workloads]]
- [[k8s-resource-requests-limits]]
- [[k8s-security-hardening]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config.json`

```json
{
  "name": "acme-api",
  "namespace": "acme-prod",
  "image": "registry.example.com/acme/api:1.4.0",
  "labels": {
    "app.kubernetes.io/name": "acme-api",
    "app.kubernetes.io/instance": "acme-api-prod",
    "app.kubernetes.io/component": "api"
  },
  "probes": {
    "readiness": {
      "httpGet": {
        "path": "/healthz",
        "port": 8080
      },
      "periodSeconds": 5
    },
    "liveness": {
      "httpGet": {
        "path": "/healthz",
        "port": 8080
      },
      "periodSeconds": 10,
      "initialDelaySeconds": 30
    }
  },
  "security_context": {
    "runAsNonRoot": true,
    "runAsUser": 10001
  },
  "resources": {
    "requests": {
      "cpu": "100m",
      "memory": "128Mi"
    },
    "limits": {
      "cpu": "500m",
      "memory": "512Mi"
    }
  },
  "owner": {
    "name": "Andriy Koval",
    "role": "platform engineer"
  },
  "produced_at": "2026-05-23T10:00:00Z"
}
```

### `templates/_smoke-test.json`

```json
{
  "name": "acme-api",
  "namespace": "acme-prod",
  "image": "registry.example.com/acme/api:1.4.0",
  "labels": {
    "app.kubernetes.io/name": "acme-api",
    "app.kubernetes.io/instance": "acme-api-prod",
    "app.kubernetes.io/component": "api"
  },
  "probes": {
    "readiness": {
      "httpGet": {
        "path": "/healthz",
        "port": 8080
      },
      "periodSeconds": 5
    },
    "liveness": {
      "httpGet": {
        "path": "/healthz",
        "port": 8080
      },
      "periodSeconds": 10,
      "initialDelaySeconds": 30
    }
  },
  "security_context": {
    "runAsNonRoot": true,
    "runAsUser": 10001
  },
  "resources": {
    "requests": {
      "cpu": "100m",
      "memory": "128Mi"
    },
    "limits": {
      "cpu": "500m",
      "memory": "512Mi"
    }
  },
  "owner": {
    "name": "Andriy Koval",
    "role": "platform engineer"
  },
  "produced_at": "2026-05-23T10:00:00Z"
}
```
