# DevOps Engineer Skill

## Overview

Technical skill for DevOps and infrastructure operations. Orchestrates containerization, orchestration, infrastructure as code, cloud services, and CI/CD pipelines.

**Agent:** faion-devops-agent

---

## Directory Structure

```
faion-devops-engineer/
├── CLAUDE.md           # This file
├── SKILL.md            # Skill definition and methodologies
└── references/         # Technical reference documentation
    ├── docker.md
    ├── kubernetes.md
    ├── terraform.md
    ├── aws.md
    ├── gcp.md
    ├── platform-engineering.md
    ├── gitops.md
    ├── aiops.md
    ├── dora-metrics.md
    ├── finops.md
    └── security-as-code.md
```

---

## Subfolders

| Folder | Description |
|--------|-------------|
| `references/` | Technical documentation for Docker, Kubernetes, Terraform, AWS, GCP, and modern DevOps practices |

---

## Key Files

| File | Description | Lines |
|------|-------------|-------|
| `SKILL.md` | Skill definition with methodologies, workflows, commands, checklists | ~330 |
| `references/docker.md` | Container development: Dockerfile, Compose, multi-stage builds, security | ~1140 |
| `references/kubernetes.md` | K8s operations: kubectl, Helm, deployments, services, networking | ~960 |
| `references/terraform.md` | IaC with Terraform: HCL syntax, modules, state management, providers | ~1090 |
| `references/aws.md` | AWS CLI operations: EC2, S3, Lambda, IAM, VPC, ECR, ECS | ~1480 |
| `references/gcp.md` | gcloud CLI: Compute Engine, Cloud Run, GKE, BigQuery, IAM | ~1400 |
| `references/platform-engineering.md` | Internal Developer Platforms (IDP), self-service, golden paths | ~50 |
| `references/gitops.md` | Git as source of truth, ArgoCD, Flux, progressive delivery | ~80 |
| `references/aiops.md` | AI-powered operations, anomaly detection, auto-remediation | ~70 |
| `references/dora-metrics.md` | Four key DevOps metrics for performance measurement | ~35 |
| `references/finops.md` | Cloud cost optimization, AI workload costs | ~55 |
| `references/security-as-code.md` | Policy as Code with OPA, Gatekeeper, Kyverno | ~60 |

---

## Methodologies (26)

### Docker (docker.md)

- Multi-stage builds, Docker Compose, security scanning, layer optimization

### Kubernetes (kubernetes.md)

- Resource management, Helm charts, ConfigMaps/Secrets, Ingress/networking

### Terraform (terraform.md)

- Module design, state management, workspaces, testing

### AWS (aws.md)

- IAM best practices, VPC design, cost optimization, disaster recovery

### GCP (gcp.md)

- IAM & service accounts, VPC & networking, GKE operations, cost optimization

### Modern DevOps Practices

- Platform Engineering: platform-engineering.md
- GitOps: gitops.md
- AIOps: aiops.md
- DORA Metrics: dora-metrics.md
- FinOps: finops.md
- Security as Code: security-as-code.md

---

## Quick Reference

### Tool Selection

| Tool | Use Case |
|------|----------|
| Docker | Containerization, local dev, CI builds |
| Kubernetes | Container orchestration, scaling |
| Terraform | Multi-cloud IaC, infrastructure provisioning |
| Pulumi | IaC with programming languages |
| Ansible | Configuration management |

### Cloud Providers

| Provider | Strengths |
|----------|-----------|
| AWS | Most services, enterprise, mature |
| GCP | Kubernetes, ML, BigQuery |
| Azure | Microsoft ecosystem, hybrid |
| Hetzner | Cost-effective, EU data residency |

### CI/CD Tools

| Tool | Best For |
|------|----------|
| GitHub Actions | GitHub repos, simple pipelines |
| GitLab CI | GitLab repos, full DevOps platform |
| ArgoCD | GitOps, Kubernetes deployments |
| Jenkins | Complex pipelines, self-hosted |

---

## Common Commands

```bash
# Docker
docker build -t app:latest .
docker compose up -d

# Kubernetes
kubectl apply -f deployment.yaml
kubectl get pods,svc,deploy

# Terraform
terraform init && terraform plan
terraform apply

# AWS
aws configure
aws s3 sync ./dist s3://bucket/

# GCP
gcloud auth login
gcloud config set project my-project
gcloud run deploy my-service --image=gcr.io/project/image --region=us-central1
```

---

*Total: 11 reference files*
