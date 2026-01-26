# GCP Cloud Run

> **Entry Point:** Invoked via [faion-infrastructure-engineer](../CLAUDE.md)

## Overview

Cloud Run is a fully managed serverless platform for deploying containerized applications. It supports two workload types:

| Type | Description | Use Case |
|------|-------------|----------|
| **Services** | HTTP-driven, auto-scaling | APIs, web apps, microservices |
| **Jobs** | Run-to-completion tasks | Batch processing, ETL, data pipelines |

## Key Capabilities (2025-2026)

| Feature | Details |
|---------|---------|
| Scaling | 0 to 1000+ instances, GPU support (5s startup) |
| Containers | Up to 10 per instance (sidecars) |
| Jobs | Up to 10,000 parallel tasks, 168h timeout |
| Networking | Direct VPC egress, Private Service Connect |
| Security | Binary Authorization, CMEK, IAM, Cloud Armor |
| Probes | HTTP/TCP/gRPC startup, HTTP/gRPC liveness |

## Quick Reference

### Services vs Jobs

```
Services:
- Listen for HTTP requests
- Scale based on traffic
- Auto-scale to zero
- Ingress controls (public/internal/load-balancer)

Jobs:
- Run tasks to completion
- No incoming requests
- Up to 10,000 parallel tasks
- 168 hour max timeout
```

### Resource Limits

| Resource | Service | Job |
|----------|---------|-----|
| vCPU | 1-8 | 1-8 |
| Memory | 128MB-32GB | 128MB-32GB |
| Timeout | 60min (request) | 168h (task) |
| Concurrency | 1-1000 per instance | N/A |
| Max instances | 1000+ | 10,000 tasks |
| GPU | L4, A100 | L4, A100 |

## Best Practices

### Container Optimization

1. **Minimize startup time** - impacts cold start latency
2. **Use startup CPU boost** - temporarily increase CPU during startup
3. **Set min instances > 0** - avoid cold starts for critical services
4. **Use secure base images** - Google base images or official Docker Hub
5. **Include only necessary packages** - reduce attack surface

### Scaling Configuration

```yaml
# Recommended for production
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"      # Avoid cold starts
        autoscaling.knative.dev/maxScale: "100"    # Control costs
    spec:
      containerConcurrency: 80                      # Requests per instance
      timeoutSeconds: 300                           # 5 min timeout
```

### Networking Best Practices

1. **Use Direct VPC egress** (not VPC connectors)
   - 2x throughput (up to 1Gbps per instance)
   - Lower cost (no connector compute charges)
   - Lower latency

2. **Configure ingress controls**
   - `internal` for private services
   - `internal-and-cloud-load-balancing` for GCLB
   - `all` only when public access required

3. **Use Private Service Connect** for Google APIs

### Security Best Practices

1. **Enable Binary Authorization** - deploy only signed images
2. **Use CMEK** - customer-managed encryption keys
3. **Implement least privilege IAM** - minimal roles
4. **Use Secret Manager** - never env vars for secrets
5. **Deploy Cloud Armor** - WAF for public services
6. **Enable VPC Service Controls** - data exfiltration prevention

### Jobs Best Practices

1. **Make tasks idempotent** - same result on retry
2. **Use checkpointing** - store progress to Cloud Storage
3. **Set appropriate parallelism** - respect downstream limits
4. **Configure retries** - default 3, adjust based on task type
5. **Use CLOUD_RUN_TASK_INDEX** - distribute work across tasks

## Pricing (2025)

| Resource | Rate (Standard Region) |
|----------|------------------------|
| vCPU | ~$0.000024/vCPU-second |
| Memory | ~$0.0000025/GiB-second |
| Requests | $0.40/million (beyond free tier) |
| GPU | Variable by type |

**Billing modes:**
- **Request-based** (default): Pay only during request processing
- **Instance-based**: Pay for entire instance lifetime (for background work)

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-deployment and security checklists |
| [examples.md](examples.md) | gcloud, Terraform, YAML examples |
| [templates.md](templates.md) | Production-ready templates |
| [llm-prompts.md](llm-prompts.md) | AI prompts for Cloud Run tasks |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [gcp/](../gcp/) | GCP overview |
| [gcp-compute/](../gcp-compute/) | Compute Engine |
| [gcp-networking/](../gcp-networking/) | VPC, subnets |

## Sources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Best Practices](https://docs.cloud.google.com/run/docs/tips/general)
- [Cloud Run Networking Best Practices](https://docs.cloud.google.com/run/docs/configuring/networking-best-practices)
- [Cloud Run Security](https://cloud.google.com/run/docs/securing/security)
- [Cloud Run Jobs](https://docs.cloud.google.com/run/docs/create-jobs)
- [Direct VPC Egress](https://docs.cloud.google.com/run/docs/configuring/vpc-direct-vpc)
- [Binary Authorization](https://docs.cloud.google.com/binary-authorization/docs/run/enabling-binauthz-cloud-run)
- [Cloud Run Pricing 2025](https://cloudchipr.com/blog/cloud-run-pricing)

---

*GCP Cloud Run Reference | Updated 2026-01*
