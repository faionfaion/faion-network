---
slug: k8s-vpa-rightsizing-runbook
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Practical recipe for K8s vertical-pod-autoscaler recommend → HPA reconcile → cluster cost reduction, with rollout safety gates.
content_id: "4211b697159cedcf"
tags: [k8s,vpa,hpa,rightsizing,cost-optimization,runbook]
---
# K8s VPA Rightsizing Runbook

## Summary

**One-sentence:** Practical recipe for K8s vertical-pod-autoscaler recommend → HPA reconcile → cluster cost reduction, with rollout safety gates.

**One-paragraph:** The `k8s-resource-requests-limits` methodology covers what requests + limits mean; this methodology covers HOW to actually go from "I set them once" to "they match real usage." VPA in recommend mode produces target CPU + memory per workload, but applying those recommendations naively breaks HPA scaling, evicts pods, and tanks SLOs. This methodology defines the 6-stage rollout: enable VPA in recommend mode → soak for 7+ days → reconcile with HPA min/max envelopes → canary update on 10% → measure throttling + OOMKills → graduate to full rollout → schedule recurring recompute. Mechanism: explicit guard rails per stage, named gates, and a rollback recipe. Primary output: a per-cluster cost reduction documented in % savings AND a per-workload requests/limits update audit log.

## Applies If (ALL must hold)

- cluster has ≥ 20 long-running workloads (Deployment / StatefulSet)
- VPA controller installed OR can be installed safely
- HPA used on ≥ 30% of workloads
- cluster cost ≥ $1k / month (saving floor for the runbook overhead)
- on-call team has playbook authority during rollout window

## Skip If (ANY kills it)

- cluster is &lt; 20 workloads — manual rightsizing cheaper than VPA infra
- workloads are batch / short-lived jobs only — VPA recommendations meaningless
- cluster has Cluster Autoscaler in tight-fit mode — VPA changes need separate sequencing
- regulated environment requires fixed-resource pinning (no autoscaling allowed)
- cluster has critical workloads with documented anti-VPA exemption

## Prerequisites (must be true before starting)

- Metrics server running, history ≥ 14 days
- VPA CRDs installed
- inventory of workloads with HPA + their current requests/limits
- baseline cluster cost (cloud bill or `kubecost` snapshot)
- maintenance window scheduled for canary rollout

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/k8s-resource-requests-limits` | Foundation: what requests + limits mean |
| `pro/infra/infrastructure-engineer/k8s-scaling-availability` | HPA mechanics; this runbook reconciles VPA with HPA |
| `pro/infra/devops-engineer/aws-cost-optimization` | Optional cluster-level cost framing |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: recommend-first, soak window, HPA reconciliation, canary 10%, OOMKill rollback gate | ~1000 |
| `content/02-output-contract.xml` | essential | Per-workload audit log, savings calculation, gate decisions | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (premature apply, HPA conflict, eviction storm, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `vpa_recommendation_parser` | haiku | Extract per-workload target CPU/mem from VPA CRDs |
| `hpa_envelope_reconciler` | sonnet | Adjust min/max replicas given new per-pod sizing |
| `canary_safety_evaluator` | sonnet | Read throttling + OOM metrics, decide promote/rollback |
| `savings_calculator` | haiku | Convert pre/post requests × replica × node-cost into $ savings |

## Templates

| File | Purpose |
|------|---------|
| `templates/vpa-recommend-config.yaml` | VPA CRD in recommend mode |
| `templates/rollout-gates.md` | Per-stage gate criteria (soak, canary, full) |
| `templates/rollback-recipe.md` | Step-by-step rollback to prior requests |
| `templates/savings-report.md` | Per-workload before/after savings table |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/collect-vpa-recommendations.sh` | Pull per-workload recommendations into a CSV | Soak end |
| `scripts/oomkill-monitor.sh` | Watch OOMKills during canary | Canary window |
| `scripts/apply-rightsizing.sh` | Apply rightsizing PR with annotations | Promote stage |
| `scripts/savings-calc.py` | Compute pre/post $ delta | Post-rollout |

## Related

- parent skill: `pro/infra/infrastructure-engineer/`
- peer methodology: `k8s-resource-requests-limits`, `k8s-scaling-availability`
- external: [VPA GitHub](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) · [Kubecost VPA guide](https://blog.kubecost.com/blog/vertical-pod-autoscaler/)
