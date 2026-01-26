# Infrastructure Engineer Sub-Skill

> **Entry Point:** Invoked via [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md)

## When to Use

- Docker containers and Dockerfile optimization
- Docker Compose for local development
- Kubernetes deployments and Helm charts
- Infrastructure as Code with Terraform
- AWS cloud infrastructure setup
- GCP cloud infrastructure setup
- Container orchestration and scaling

## Overview

Manages infrastructure provisioning, containerization, orchestration, and cloud platforms. Sub-skill of faion-devops-engineer.

**Methodologies:** 31

## Quick Reference

| Tool | Use Case |
|------|----------|
| Docker | Containerization, local dev, CI builds |
| Kubernetes | Container orchestration, scaling |
| Helm | K8s package management |
| Terraform | Multi-cloud IaC, provisioning |
| AWS | Enterprise cloud services |
| GCP | Kubernetes, ML workloads |

## Methodologies by Category

### Docker (7)
- [docker/](docker/) - Docker infrastructure (README, checklist, examples, templates, prompts)
- [docker-compose/](docker-compose/) - Multi-container orchestration (README, checklist, examples, templates, prompts)
- docker-basics
- docker-containerization
- dockerfile-patterns

### Kubernetes (6)
- [kubernetes-deployment/](kubernetes-deployment/) - K8s deployment reference (README, checklist, examples, templates, prompts)
- [k8s-basics/](k8s-basics/) - K8s fundamentals reference (README, checklist, examples, templates, prompts)
- [k8s-resources/](k8s-resources/) - Resource requests/limits, QoS, LimitRanges, ResourceQuotas (README, checklist, examples, templates, prompts)
- [helm-basics/](helm-basics/) - Helm reference (README, checklist, examples, templates, prompts)
- [helm-advanced/](helm-advanced/) - Library charts, hooks, tests, umbrella charts (README, checklist, examples, templates, prompts)

### Terraform & IaC (6)
- [terraform/](terraform/) - Infrastructure reference (README, checklist, examples, templates, prompts)
- [terraform-basics/](terraform-basics/) - HCL syntax, providers, resources, data sources (README, checklist, examples, templates, prompts)
- [terraform-modules/](terraform-modules/) - Module development, versioning, composition (README, checklist, examples, templates, prompts)
- [terraform-state/](terraform-state/) - Remote state, locking, import, state manipulation (README, checklist, examples, templates, prompts)
- [iac-basics/](iac-basics/) - IaC principles, tools comparison, GitOps integration (README, checklist, examples, templates, prompts)
- [iac-patterns/](iac-patterns/) - Module patterns, composition, DRY, testing (README, checklist, examples, templates, prompts)

### AWS (7)
- [aws/](aws/) - AWS reference (README, checklist, examples, templates, prompts)
- [aws-architecture-foundations/](aws-architecture-foundations/) - Well-Architected, multi-account, landing zone, security foundations (README, checklist, examples, templates, prompts)
- [aws-architecture-services/](aws-architecture-services/) - Service selection, integration patterns, serverless vs containers (README, checklist, examples, templates, prompts)
- [aws-ec2-ecs/](aws-ec2-ecs/) - EC2 instances, ECS Fargate, task definitions, services (README, checklist, examples, templates, prompts)
- [aws-lambda/](aws-lambda/) - Function design, cold starts, layers, event sources (README, checklist, examples, templates, prompts)
- [aws-s3-storage/](aws-s3-storage/) - S3 bucket policies, encryption, lifecycle, replication (README, checklist, examples, templates, prompts)
- [aws-networking/](aws-networking/) - VPC, subnets, security groups, Transit Gateway (README, checklist, examples, templates, prompts)

### GCP (7)
- [gcp/](gcp/) - GCP reference (README, checklist, examples, templates, prompts)
- [gcp-arch-basics/](gcp-arch-basics/) - Resource hierarchy, projects, IAM, billing (README, checklist, examples, templates, prompts)
- [gcp-arch-patterns/](gcp-arch-patterns/) - GKE, Cloud SQL, CDN, microservices, data pipelines (README, checklist, examples, templates, prompts)
- [gcp-compute/](gcp-compute/) - VMs, instance groups, autoscaling, Spot/preemptible (README, checklist, examples, templates, prompts)
- [gcp-cloud-run/](gcp-cloud-run/) - Cloud Run services, jobs, scaling, networking, security (README, checklist, examples, templates, prompts)
- [gcp-storage/](gcp-storage/) - Cloud Storage buckets, lifecycle, IAM, CMEK, CDN (README, checklist, examples, templates, prompts)
- [gcp-networking/](gcp-networking/) - VPC, subnets, firewall rules, Cloud NAT, load balancing (README, checklist, examples, templates, prompts)

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) | Parent orchestrator |
| [faion-cicd-engineer](../faion-cicd-engineer/CLAUDE.md) | Sibling (CI/CD) |

---

*Infrastructure Engineer Sub-Skill | 31 methodologies*
