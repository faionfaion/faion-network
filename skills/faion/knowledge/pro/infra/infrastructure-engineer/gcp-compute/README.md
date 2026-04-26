# GCP Compute Engine

**Layer:** 3 (Technical Skill)
**Used by:** faion-devops-agent, faion-infrastructure-engineer

## Overview

Comprehensive reference for Google Cloud Platform Compute Engine covering VMs, instance groups, autoscaling, and Spot/preemptible instances.

## Scope

| Component | Coverage |
|-----------|----------|
| VMs | Creation, management, machine types, images, disks |
| Instance Templates | Reusable VM configurations |
| Managed Instance Groups (MIGs) | Regional/zonal MIGs, health checks |
| Autoscaling | Horizontal, vertical, predictive, schedule-based |
| Spot/Preemptible VMs | Cost optimization, fault tolerance |
| GKE Node Pools | Kubernetes compute resources |

## Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview |
| [checklist.md](checklist.md) | Production readiness checklist |
| [examples.md](examples.md) | gcloud CLI commands and patterns |
| [templates.md](templates.md) | Terraform and YAML templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for infrastructure tasks |

## Key Concepts

### VM Provisioning Models

| Model | Discount | Max Runtime | Preemption | Use Case |
|-------|----------|-------------|------------|----------|
| Standard | 0% | Unlimited | No | Production workloads |
| Spot | Up to 91% | Unlimited | Yes (30s warning) | Batch, fault-tolerant |
| Preemptible | Up to 91% | 24 hours | Yes (30s warning) | Legacy, migrate to Spot |

**Recommendation:** Use Spot VMs instead of Preemptible. Spot VMs have no 24-hour limit and support more features.

### Machine Type Families

| Family | Prefix | Optimization | Use Case |
|--------|--------|--------------|----------|
| E2 | `e2-` | Cost | Dev/test, small workloads |
| N2 | `n2-` | Balanced | General-purpose |
| N2D | `n2d-` | AMD EPYC | Cost-effective general |
| C2 | `c2-` | Compute | HPC, gaming servers |
| C3 | `c3-` | Latest compute | CPU-intensive, AI inference |
| M2/M3 | `m2-`, `m3-` | Memory | In-memory DBs, SAP |
| A2/A3 | `a2-`, `a3-` | GPU | ML training, inference |

### Autoscaling Signals

| Signal | Description | Best For |
|--------|-------------|----------|
| CPU Utilization | Scale based on average CPU | Web apps, APIs |
| Cloud Monitoring Metrics | Custom metrics (queue depth, latency) | Event-driven workloads |
| Load Balancing Capacity | Requests per second | HTTP(S) services |
| Schedule | Time-based scaling | Predictable traffic patterns |
| Predictive | ML-based forecasting | Long initialization apps |

### Regional vs Zonal MIGs

| Aspect | Zonal MIG | Regional MIG |
|--------|-----------|--------------|
| Availability | Single zone | Multi-zone (up to 3) |
| Recommended min | 1+ | 3+ (1 per zone) |
| Zonal outage | Service down | Partial capacity |
| Use case | Dev/test, cost-sensitive | Production |

## Best Practices Summary

### VMs

1. Use instance templates for consistent deployments
2. Enable OS Login for SSH access management
3. Use Shielded VMs for security-sensitive workloads
4. Apply labels for cost allocation and organization

### Instance Groups

1. Use regional MIGs for production (multi-zone distribution)
2. Set minimum instances to 3 for regional MIGs
3. Configure autohealing with appropriate health checks
4. Use rolling updates with maxUnavailable and maxSurge

### Autoscaling

1. Set initialization period longer than VM startup time
2. Enable predictive autoscaling for apps with long init time (>2 min)
3. Use scale-in controls to prevent rapid downscaling
4. Configure multiple signals (CPU + custom metrics)

### Spot VMs

1. Use MIGs with autohealing to recreate preempted VMs
2. Implement 30-second shutdown scripts to save state
3. Distribute across multiple zones for availability
4. Mix Spot and standard VMs for critical workloads

## Quick Reference

### Common gcloud Commands

```bash
# List instances
gcloud compute instances list

# Create VM
gcloud compute instances create my-vm \
    --zone=us-central1-a \
    --machine-type=e2-medium

# Create Spot VM
gcloud compute instances create my-spot-vm \
    --zone=us-central1-a \
    --provisioning-model=SPOT \
    --instance-termination-action=STOP

# Set autoscaling
gcloud compute instance-groups managed set-autoscaling my-mig \
    --zone=us-central1-a \
    --min-num-replicas=2 \
    --max-num-replicas=10 \
    --target-cpu-utilization=0.6
```


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| VM instance group setup | sonnet | Scaling configuration |
| Autoscaling policy definition | sonnet | Performance tuning |
| Spot VM usage strategy | sonnet | Cost optimization |

## Sources

- [Compute Engine Documentation](https://cloud.google.com/compute/docs)
- [Autoscaling Groups of Instances](https://docs.cloud.google.com/compute/docs/autoscaler)
- [Spot VMs](https://cloud.google.com/compute/docs/instances/spot)
- [Preemptible VMs](https://cloud.google.com/compute/docs/instances/preemptible)
- [Create and Use Spot VMs](https://cloud.google.com/compute/docs/instances/create-use-spot)
- [Understanding Autoscaler Decisions](https://docs.cloud.google.com/compute/docs/autoscaler/understanding-autoscaler-decisions)
- [High Scalability Autoscaling Tutorial](https://cloud.google.com/compute/docs/tutorials/high-scalability-autoscaling)
- [GKE Spot VMs](https://cloud.google.com/kubernetes-engine/docs/concepts/spot-vms)
- [GCP Cost Optimization (Cast AI)](https://cast.ai/blog/gcp-cost-optimization/)

---

*GCP Compute Engine Reference v2.0*
*Layer 3 Technical Skill*
*Used by: faion-infrastructure-engineer*
