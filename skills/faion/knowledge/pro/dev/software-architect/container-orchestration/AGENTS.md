---
slug: container-orchestration
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Kubernetes declarative model (desired state reconciliation) enables self-healing, horizontal scaling, and zero-downtime deployments — but misconfigured resource requests cause OOM kills and poor scheduling, missing liveness/readiness probes cause traffic to reach broken pods, and over-privileged service accounts create security blast radius.
content_id: "17e82a4e721cefe2"
tags: [kubernetes, container, orchestration, pod, deployment, autoscaling, security, storage]
---
# Container Orchestration

## Summary

**One-sentence:** Kubernetes declarative model (desired state reconciliation) enables self-healing, horizontal scaling, and zero-downtime deployments — but misconfigured resource requests cause OOM kills and poor scheduling, missing liveness/readiness probes cause traffic to reach broken pods, and over-privileged service accounts create security blast radius.

**One-paragraph:** Kubernetes declarative model (desired state reconciliation) enables self-healing, horizontal scaling, and zero-downtime deployments — but misconfigured resource requests cause OOM kills and poor scheduling, missing liveness/readiness probes cause traffic to reach broken pods, and over-privileged service accounts create security blast radius. Each pattern addresses a specific operational failure mode.

## Applies If (ALL must hold)

- Authoring or reviewing a Deployment / StatefulSet / DaemonSet manifest before merge — apply the pre-merge checklist below.
- Deploying a new service to a Kubernetes cluster (select pod pattern, set probes, set resource limits).
- Choosing a deployment strategy for a high-risk release (canary vs blue-green) — use the decision tree in the deployment-strategies section.
- Configuring autoscaling for queue-backed or event-driven workloads — use KEDA flowchart.
- Hardening a Kubernetes workload: RBAC, network policies, pod security standards (PSS).
- Migrating Docker Compose to Kubernetes manifests — run `kompose convert` then apply this methodology over the output.
- Investigating an incident: OOMKilled pod, CrashLoopBackOff, ImagePullBackOff, traffic hitting unready pod — use the verify section as a triage runbook.

## Skip If (ANY kills it)

- Single-VM or bare-metal deployment without container runtime — use systemd/supervisor instead.
- Serverless function with sub-second invocation pattern — K8s cold-start overhead is not justified.
- Development environment where Docker Compose is sufficient — K8s adds operational overhead with no benefit.
- Stateful workloads requiring POSIX file locking across nodes — ReadWriteMany volumes add complexity.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/dev/software-architect/`
