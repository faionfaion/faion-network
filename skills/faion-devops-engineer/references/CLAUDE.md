# DevOps References

## Overview

Technical reference documentation for DevOps tools and practices. Each file provides comprehensive patterns, commands, and best practices for its respective technology.

---

## Files

### docker.md (~1140 lines)

Container development and deployment best practices.

**Contents:**
- Dockerfile patterns and base image selection
- Multi-stage builds for optimized images
- Docker Compose for multi-container apps
- Layer caching and optimization
- Security: non-root users, secrets, scanning
- Networking: bridge, host, overlay modes
- Volumes and storage management
- Registry operations and tagging

### kubernetes.md (~960 lines)

Kubernetes operations with kubectl, Helm, and Kustomize.

**Contents:**
- kubectl resource management commands
- Deployment, Service, ConfigMap, Secret manifests
- Namespace and RBAC operations
- Helm chart creation and management
- Kustomize overlays and patches
- Pod debugging and troubleshooting
- Resource requests/limits and QoS
- Ingress and networking configuration

### terraform.md (~1090 lines)

Infrastructure as Code with Terraform.

**Contents:**
- HCL syntax: resources, data sources, variables, outputs
- Expressions: conditionals, loops, dynamic blocks
- Module design and composition patterns
- State management: remote backends, locking
- Workspace-based environment separation
- Multi-provider configurations
- Testing with Terratest
- Import and state manipulation

### aws.md (~1480 lines)

AWS CLI operations and cloud infrastructure patterns.

**Contents:**
- CLI configuration and profile management
- EC2: instances, AMIs, security groups
- S3: bucket operations, sync, policies
- Lambda: deployment, invocation, layers
- IAM: users, roles, policies, MFA
- VPC: subnets, routing, NAT, peering
- ECR/ECS: container registry and orchestration
- CloudFormation and CDK basics

### best-practices-2026.md (~330 lines)

Modern DevOps practices and methodologies for 2026.

**Contents:**
- M-OPS-017: Platform Engineering and Internal Developer Platforms
- M-OPS-018: GitOps with ArgoCD and Flux
- M-OPS-019: AIOps for anomaly detection and auto-remediation
- M-OPS-020: DORA metrics for DevOps performance
- M-OPS-021: FinOps and cloud cost optimization
- M-OPS-022: Security as Code with OPA and Kyverno

---

## Usage

Load relevant reference files when working on specific technologies:

| Task | Reference |
|------|-----------|
| Writing Dockerfiles | docker.md |
| Kubernetes deployments | kubernetes.md |
| Infrastructure provisioning | terraform.md |
| AWS service configuration | aws.md |
| Modern practices/patterns | best-practices-2026.md |

---

*Total: ~4,870 lines of technical reference*
