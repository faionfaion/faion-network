---
name: faion-devops-engineer
description: "DevOps Engineer orchestrator: coordinates faion-infrastructure-engineer (Docker, K8s, Terraform, AWS/GCP) and faion-cicd-engineer (CI/CD, monitoring, GitOps, security). 58 total methodologies across 2 sub-skills."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---

# DevOps Engineer Orchestrator

**Communication: User's language. Config/code: English.**

## Purpose

Orchestrates DevOps activities by coordinating two specialized sub-skills:
- **faion-infrastructure-engineer** - Infrastructure, cloud, containerization
- **faion-cicd-engineer** - CI/CD, monitoring, security, operations

---

## Sub-Skills

### faion-infrastructure-engineer
**Focus:** Infrastructure provisioning, containerization, orchestration, cloud platforms

**Methodologies (30):**
- Docker (6): containerization, Compose, patterns, optimization
- Kubernetes (6): basics, resources, deployment, Helm
- Terraform & IaC (6): basics, modules, state, patterns
- AWS (7): foundations, services, EC2/ECS, Lambda, S3, networking
- GCP (6): basics, patterns, compute, Cloud Run, storage, networking

**When to use:**
- Docker containers and multi-stage builds
- Kubernetes deployments and Helm charts
- Infrastructure as Code with Terraform
- AWS/GCP cloud infrastructure setup
- Container orchestration

---

### faion-cicd-engineer
**Focus:** CI/CD pipelines, monitoring, observability, security, operations

**Methodologies (28):**
- CI/CD & GitOps (7): GitHub Actions, GitLab CI, Jenkins, ArgoCD
- Monitoring (5): Prometheus, Grafana, ELK, AIOps
- Security (6): secrets, SSL/TLS, security as code, nginx, load balancing
- Backup & Cost (4): backup strategies, FinOps
- Modern Practices (2): Platform Engineering, DORA metrics
- Azure (2): compute, networking
- Optimization (2): Docker optimization

<<<<<<< HEAD
| Reference | Content | Lines |
|-----------|---------|-------|
| [docker.md](docker.md) | Containers, Compose, multi-stage builds | ~1140 |
| [kubernetes.md](kubernetes.md) | K8s resources, Helm, operators | ~960 |
| [terraform.md](terraform.md) | IaC, modules, state management | ~1090 |
| [aws.md](aws.md) | AWS CLI, services, IAM, networking | ~1480 |
| [gcp.md](gcp.md) | gcloud CLI, GCE, GKE, Cloud Run, BigQuery | ~1400 |
| [ref-platform-engineering.md](ref-platform-engineering.md) | Platform Engineering, IDPs | ~50 |
| [ref-gitops.md](ref-gitops.md) | GitOps, ArgoCD, Flux | ~80 |
| [ref-aiops.md](ref-aiops.md) | AIOps, anomaly detection | ~70 |
| [ref-dora-metrics.md](ref-dora-metrics.md) | DORA metrics | ~35 |
| [finops.md](finops.md) | Cloud cost optimization | ~55 |
| [ref-security-as-code.md](ref-security-as-code.md) | Policy as Code | ~60 |

**Total:** ~6,270 lines of technical reference
=======
**When to use:**
- CI/CD pipeline setup
- Monitoring and observability
- Logging and alerting
- Security and secrets management
- Backup and disaster recovery
- Cost optimization
- GitOps workflows
>>>>>>> claude

---

## Quick Decision Tree

| Need | Sub-Skill | Reason |
|------|-----------|--------|
| Dockerfile, Docker Compose | infrastructure-engineer | Containerization |
| K8s deployment, Helm | infrastructure-engineer | Orchestration |
| Terraform, IaC | infrastructure-engineer | Infrastructure provisioning |
| AWS/GCP setup | infrastructure-engineer | Cloud platforms |
| GitHub Actions, GitLab CI | cicd-engineer | CI/CD pipelines |
| Prometheus, Grafana | cicd-engineer | Monitoring |
| Secrets, SSL/TLS | cicd-engineer | Security |
| ArgoCD, GitOps | cicd-engineer | GitOps deployment |
| Backup strategies | cicd-engineer | Operations |
| Cost optimization | cicd-engineer | FinOps |

---

## Common Workflows

### Full Stack Deployment
```
1. infrastructure-engineer: Create Dockerfile
2. infrastructure-engineer: Setup K8s cluster
3. infrastructure-engineer: Provision cloud resources with Terraform
4. cicd-engineer: Setup CI/CD pipeline
5. cicd-engineer: Configure monitoring and alerts
6. cicd-engineer: Setup backup and disaster recovery
```

### New Project Setup
```
1. infrastructure-engineer: docker-containerization
2. infrastructure-engineer: docker-compose for local dev
3. cicd-engineer: github-actions-cicd
4. infrastructure-engineer: iac-basics with Terraform
5. cicd-engineer: secrets-management
6. cicd-engineer: prometheus-monitoring
```

### Production Deployment
```
1. infrastructure-engineer: kubernetes-deployment
2. infrastructure-engineer: helm-charts
3. cicd-engineer: argocd-gitops
4. cicd-engineer: prometheus-monitoring
5. cicd-engineer: elk-stack-logging
6. cicd-engineer: backup-basics
```

---

## Tool Selection Guide

### Containerization
| Tool | Sub-Skill | Use Case |
|------|-----------|----------|
| Docker | infrastructure-engineer | Containerization, local dev |
| Kubernetes | infrastructure-engineer | Container orchestration |
| Helm | infrastructure-engineer | K8s package management |

### Cloud Providers
| Provider | Sub-Skill | Strengths |
|----------|-----------|-----------|
| AWS | infrastructure-engineer | Most services, enterprise |
| GCP | infrastructure-engineer | Kubernetes, ML, BigQuery |
| Azure | cicd-engineer | Microsoft ecosystem |

### CI/CD Tools
| Tool | Sub-Skill | Best For |
|------|-----------|----------|
| GitHub Actions | cicd-engineer | GitHub repos, simple pipelines |
| GitLab CI | cicd-engineer | GitLab repos, full DevOps |
| Jenkins | cicd-engineer | Complex pipelines, self-hosted |
| ArgoCD | cicd-engineer | GitOps, K8s deployments |

### Monitoring
| Tool | Sub-Skill | Purpose |
|------|-----------|---------|
| Prometheus | cicd-engineer | Metrics collection |
| Grafana | cicd-engineer | Dashboards and visualization |
| ELK Stack | cicd-engineer | Log aggregation and analysis |

---

## Orchestration Logic

### Single Sub-Skill Tasks
If task clearly belongs to one domain, invoke that sub-skill directly.

### Multi Sub-Skill Tasks
For tasks spanning both domains, coordinate sequentially:
1. infrastructure-engineer for cloud/container setup
2. cicd-engineer for pipeline/monitoring setup

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-net | Parent orchestrator |
| faion-software-developer | Provides code to deploy |
| faion-ml-engineer | ML model deployment |

---

## Sub-Skill Details

<<<<<<< HEAD
| Issue | Action |
|-------|--------|
| Unknown cloud provider | Ask user or check existing config |
| Complex infrastructure | Read reference files for patterns |
| Multi-cloud setup | Combine relevant references |
=======
### faion-infrastructure-engineer
- **Files:** 30 methodology files
- **Key areas:** Docker, K8s, Terraform, AWS, GCP
- **SKILL.md:** [faion-infrastructure-engineer/SKILL.md](faion-infrastructure-engineer/SKILL.md)

### faion-cicd-engineer
- **Files:** 28 methodology files
- **Key areas:** CI/CD, monitoring, security, GitOps
- **SKILL.md:** [faion-cicd-engineer/SKILL.md](faion-cicd-engineer/SKILL.md)
>>>>>>> claude

---

*DevOps Engineer Orchestrator v2.0*
*2 Sub-Skills | 58 Total Methodologies*
*Infrastructure + CI/CD/Monitoring*
