# Kubernetes

## Summary

Kubernetes production readiness requires: always set resource requests AND limits, configure liveness + readiness + startup probes, enforce `runAsNonRoot: true` + `readOnlyRootFilesystem: true` + `allowPrivilegeEscalation: false` + `capabilities.drop: ["ALL"]` on every container, and define a PodDisruptionBudget for every Deployment with more than one replica. Never use `latest` image tags in production.

## Why

99.94% of clusters are over-provisioned (average CPU at 10%, memory at 23%) because teams skip resource requests. Without requests, the scheduler cannot make correct placement decisions, leading to node resource contention and OOMKilled events. Without security context hardening, a container escape escalates directly to cluster-admin. PDBs prevent maintenance windows from killing all replicas simultaneously.

## When To Use

- Deploying any containerized workload that needs horizontal scaling, rolling updates, or self-healing
- Multi-service application where service discovery via DNS is needed
- Workloads requiring persistent storage with automated provisioning
- Environments where GitOps (ArgoCD/Flux) manages the desired state

## When NOT To Use

- Single-container application with no scaling needs — Docker Compose or a simple VM is simpler
- Stateful workloads with complex data replication not supported by a Kubernetes Operator — managed databases are a better fit
- Batch/ETL workload that runs infrequently — serverless (Cloud Run, Lambda) avoids paying for idle nodes
- Team has no Kubernetes operational experience and production SLO is tight — operational learning curve is high

## Content

| File | What's inside |
|------|---------------|
| `content/01-production-config.xml` | Resource requests/limits, health probes, security context, PDB, anti-affinity, image policy |
| `content/02-scaling-observability.xml` | HPA, VPA, Karpenter, deployment strategies (rolling/blue-green/canary), RED metrics, GitOps checklist |

## Templates

| File | Purpose |
|------|---------|
| `templates/deployment-secure.yaml` | Production Deployment with full security context, probes, resources, PDB |
| `templates/hpa.yaml` | HPA with CPU + custom metric targets |
| `templates/networkpolicy-default-deny.yaml` | Default-deny NetworkPolicy with explicit ingress/egress |
| `templates/prompt-review.txt` | LLM prompt for reviewing a Kubernetes manifest for production readiness |
