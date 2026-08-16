# GitOps — Progressive Delivery

## Summary

**One-sentence:** Generates a progressive-delivery config (canary or blue-green via Flagger or Argo Rollouts + automated metric-based rollback + traffic shifting via service mesh or ingress).

**One-paragraph:** Generates a progressive-delivery config (canary or blue-green via Flagger or Argo Rollouts + automated metric-based rollback + traffic shifting via service mesh or ingress). The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- K8s prod deploys де rollback-button-press critical (latency / error gates).
- Service-mesh setups (Istio / Linkerd) з ready traffic-shift primitives.
- Risk-averse environments: payments, healthcare, regulated.
- Hot deploys де canary 5% → 25% → 100% з metric checkpoints.

## Applies If (ALL must hold)

- Kubernetes deployment with measurable health signals (latency, error rate, custom SLO).
- Service mesh OR ingress controller capable of weighted traffic split.
- Production deploy cadence ≥weekly — automation overhead pays back.
- Team tolerates added complexity for rollback speed gains.

## Skip If (ANY kills it)

- No service mesh / no ingress traffic-split capability — fall back to blue-green via two deployments.
- No metric signal for the workload — gates have nothing to read.
- Static infra (VMs) — use a different progressive-delivery pattern.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Deployment manifest | K8s YAML | App team |
| Service mesh / ingress controller | name + version | Platform team |
| Metric source | Prometheus URL + queries | SRE |
| Rollout tool | flagger OR argo-rollouts | Platform team |

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
| `draft-gitops-progressive-delivery` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-instance.json` | JSON instance of a filled config artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gitops-progressive-delivery.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

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
  "tool": "flagger",
  "strategy": {
    "type": "canary",
    "steps": [
      5,
      25,
      50,
      100
    ],
    "step_duration": "5m"
  },
  "traffic_split": {
    "provider": "istio",
    "config_ref": "manifests/canary.yaml"
  },
  "metrics": {
    "success_rate": {
      "query": "sum(rate(request_success[1m]))",
      "min": 0.99
    },
    "latency_p95": {
      "query": "histogram_quantile(0.95, request_duration)",
      "max_ms": 300
    },
    "error_rate": {
      "query": "sum(rate(request_error[1m]))",
      "max": 0.01
    }
  },
  "rollback_gate": {
    "thresholds": {
      "success_rate_min": 0.99,
      "error_rate_max": 0.01
    },
    "auto_rollback": true
  },
  "owner": "sre@team.io",
  "last_reviewed": "2026-05-23"
}
```
