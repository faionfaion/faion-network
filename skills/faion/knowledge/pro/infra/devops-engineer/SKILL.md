---
name: faion-devops-engineer
description: "DevOps orchestrator: infrastructure and CI/CD."
tier: pro
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> Part of **faion** umbrella — read on-demand, not individually invocable.

# DevOps Engineer Orchestrator

**Communication: User's language. Config/code: English.**

## Purpose

Orchestrates DevOps activities by coordinating two specialized sub-skills:
- **faion-infrastructure-engineer** - Infrastructure, cloud, containerization
- **faion-cicd-engineer** - CI/CD, monitoring, security, operations

---

## Context Discovery

### Auto-Investigation

Check for existing infrastructure and DevOps setup:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `Dockerfile` | `Glob("**/Dockerfile*")` | Docker used |
| `docker-compose.yml` | `Glob("**/docker-compose*.yml")` | Compose setup |
| `*.tf` files | `Glob("**/*.tf")` | Terraform used |
| `k8s/` or `kubernetes/` | `Glob("**/k8s/**")` | Kubernetes configs |
| `.github/workflows/` | `Glob("**/.github/workflows/*.yml")` | GitHub Actions |
| `.gitlab-ci.yml` | `Glob("**/.gitlab-ci.yml")` | GitLab CI |
| `Jenkinsfile` | `Glob("**/Jenkinsfile")` | Jenkins used |
| AWS config | `Grep("aws\|AWS", "**/*.tf")` | AWS provider |
| GCP config | `Grep("google\|gcp", "**/*.tf")` | GCP provider |

**Read existing configs:**
- Dockerfile for current setup
- docker-compose for service architecture
- CI/CD workflows for deployment pipeline

### Discovery Questions

Use `AskUserQuestion` to understand DevOps needs.

#### Q1: DevOps Goal

```yaml
question: "What DevOps task do you need help with?"
header: "Task"
multiSelect: false
options:
  - label: "Containerize application"
    description: "Docker, multi-stage builds"
  - label: "Set up CI/CD pipeline"
    description: "Automated builds, tests, deployment"
  - label: "Infrastructure provisioning"
    description: "Cloud resources, Terraform, IaC"
  - label: "Kubernetes deployment"
    description: "K8s configs, Helm charts"
  - label: "Monitoring & observability"
    description: "Metrics, logs, alerts"
```

**Routing:**
- "Containerize" → `Skill(faion-infrastructure-engineer)` → docker-*
- "CI/CD" → `Skill(faion-cicd-engineer)` → github-actions/gitlab-ci
- "Infrastructure" → `Skill(faion-infrastructure-engineer)` → terraform-*
- "Kubernetes" → `Skill(faion-infrastructure-engineer)` → kubernetes-*
- "Monitoring" → `Skill(faion-cicd-engineer)` → prometheus, grafana

#### Q2: Cloud Provider (if infrastructure task)

```yaml
question: "Which cloud provider are you using?"
header: "Cloud"
multiSelect: false
options:
  - label: "AWS"
    description: "Amazon Web Services"
  - label: "GCP"
    description: "Google Cloud Platform"
  - label: "Azure"
    description: "Microsoft Azure"
  - label: "Hetzner / DigitalOcean"
    description: "Budget-friendly VPS"
  - label: "Self-hosted / On-premise"
    description: "Own servers"
```

**Routing:**
- "AWS" → aws-* methodologies
- "GCP" → gcp-* methodologies
- "Azure" → azure patterns (limited)
- "Hetzner/DO" → Simpler setup, manual provisioning
- "Self-hosted" → Docker Compose, systemd, nginx

#### Q3: CI/CD Platform (if CI/CD task)

```yaml
question: "Where is your code hosted?"
header: "Platform"
multiSelect: false
options:
  - label: "GitHub"
    description: "Use GitHub Actions"
  - label: "GitLab"
    description: "Use GitLab CI"
  - label: "Bitbucket"
    description: "Use Bitbucket Pipelines"
  - label: "Self-hosted"
    description: "Jenkins, ArgoCD, or other"
```

**Routing:**
- "GitHub" → github-actions-*
- "GitLab" → gitlab-ci-*
- "Bitbucket" → Basic pipeline config
- "Self-hosted" → jenkins or argocd-gitops

#### Q4: Current State

```yaml
question: "What's your current setup?"
header: "Current"
multiSelect: false
options:
  - label: "Nothing (greenfield)"
    description: "Starting from scratch"
  - label: "Local only (no deployment)"
    description: "Runs on laptop, need production"
  - label: "Basic deployment (manual)"
    description: "Have server, deploy manually"
  - label: "Have CI/CD, need improvements"
    description: "Pipeline exists, need optimization"
```

**Context impact:**
- "Greenfield" → Full setup, best practices from start
- "Local only" → Containerize first, then deploy
- "Manual" → Add CI/CD, automate deployment
- "Improvements" → Optimize existing, add monitoring

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

**When to use:**
- CI/CD pipeline setup
- Monitoring and observability
- Logging and alerting
- Security and secrets management
- Backup and disaster recovery
- Cost optimization
- GitOps workflows

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

### faion-infrastructure-engineer
- **Files:** 30 methodology files
- **Key areas:** Docker, K8s, Terraform, AWS, GCP
- **SKILL.md:** [faion-infrastructure-engineer/SKILL.md](faion-infrastructure-engineer/SKILL.md)

### faion-cicd-engineer
- **Files:** 28 methodology files
- **Key areas:** CI/CD, monitoring, security, GitOps
- **SKILL.md:** [faion-cicd-engineer/SKILL.md](faion-cicd-engineer/SKILL.md)

---

## Methodologies (61 in this folder)

### Core Containers & Orchestration (6)
- `docker` — Docker reference
- `docker-image-optimization` — Image size and layer optimization
- `docker-language-templates` — Per-language Dockerfile templates
- `docker-security-hardening` — Container hardening
- `docker-llm-prompts` — LLM prompts for Docker
- `kubernetes-deployment` — K8s deployment reference

### IaC (5)
- `terraform` — Terraform reference
- `terraform-iac` — Terraform IaC patterns
- `helm-charts` — Helm chart patterns
- `gitops` — GitOps overview
- `argocd-gitops` — Argo CD GitOps

### CI/CD (3)
- `github-actions-cicd` — GitHub Actions CI/CD
- `gitlab-cicd` — GitLab CI
- `jenkins-pipelines` — Jenkins pipelines

### Monitoring & Observability (8)
- `prometheus-monitoring` — Prometheus metrics
- `grafana-dashboards` — Grafana dashboarding
- `aiops` — AIOps practices
- `dora-metrics` — DORA performance metrics
- `devops-elk-architecture` — ELK architecture
- `devops-elk-beats-collection` — Beats collectors
- `devops-elk-index-management` — ELK index management
- `devops-elk-logstash-pipeline` — Logstash pipelines
- `devops-elk-queries-alerting` — ELK queries + alerting

### Security & Networking (4)
- `secrets-management` — Secrets vaulting
- `security-as-code` — Security as code
- `nginx-configuration` — Nginx configuration
- `ssl-tls-setup` — SSL/TLS setup

### Load Balancing (6)
- `devops-lb-algorithms` — LB algorithms
- `devops-lb-haproxy` — HAProxy patterns
- `devops-lb-health-checks` — Health checks
- `devops-lb-high-availability` — LB HA
- `devops-lb-kubernetes` — K8s LB
- `devops-lb-ssl-tls` — LB TLS termination

### Backups (1)
- `backup-strategies` — Backup strategy reference

### AWS Architecture (8)
- `aws-cli-compute` — AWS CLI compute commands
- `aws-cli-containers-iac` — AWS CLI containers/IaC
- `aws-cfn-terraform-templates` — CloudFormation/Terraform
- `aws-well-architected-checklists` — WAF checklists
- `aws-infra-llm-prompts` — LLM prompts for AWS
- `devops-aws-three-tier` — AWS three-tier architecture
- `devops-aws-service-selection` — Service selection
- `devops-aws-serverless-api` — Serverless API
- `devops-aws-monitoring-dr` — Monitoring + DR
- `devops-aws-terraform-cicd` — Terraform CI/CD on AWS

### Azure (1)
- `azure-architecture` — Azure architecture overview

### GCP Architecture (5)
- `gcp` — GCP reference
- `gcp-landing-zone` — GCP landing zone
- `gcp-network-architecture` — GCP network architecture
- `gcp-gke-architecture` — GKE architecture
- `gcp-storage-cdn` — Storage + CDN

### Platform Engineering (5)
- `devops-platform-backstage` — Backstage IDP
- `devops-platform-crossplane` — Crossplane control plane
- `devops-platform-golden-paths` — Golden paths
- `devops-platform-idp-core` — IDP core
- `devops-platform-policy-finops` — Policy + FinOps

### FinOps (6)
- `finops` — FinOps overview
- `finops-devops-cost-alerts` — Cost alerts
- `finops-devops-cost-commitments` — Commitment pricing
- `finops-devops-cost-kubernetes` — K8s cost optimization
- `finops-devops-cost-rightsizing` — Rightsizing
- `finops-devops-cost-tagging` — Cost tagging

---

*DevOps Engineer Orchestrator v2.0*
*2 Sub-Skills | 58 Total Methodologies*
*Infrastructure + CI/CD/Monitoring*
