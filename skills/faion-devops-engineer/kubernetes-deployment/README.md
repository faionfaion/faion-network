---
id: kubernetes-deployment
name: "Kubernetes Deployment Strategies"
domain: OPS
skill: faion-devops-engineer
category: "devops"
version: "2.0.0"
updated: "2026-01"
---

# Kubernetes Deployment Strategies

## Overview

Kubernetes deployment strategies determine how application updates are rolled out to production. Choosing the right strategy balances deployment speed, risk mitigation, resource efficiency, and rollback capabilities.

**Key statistic:** 80% of Kubernetes outages stem from deployment errors, making strategy selection critical.

## Strategy Comparison

| Strategy | Downtime | Risk | Complexity | Resource Cost | Rollback Speed |
|----------|----------|------|------------|---------------|----------------|
| Recreate | Yes | High | Low | Low | Slow |
| Rolling Update | No | Medium | Low | Medium | Medium |
| Blue-Green | No | Low | Medium | High (2x) | Instant |
| Canary | No | Very Low | High | Medium | Instant |
| A/B Testing | No | Very Low | High | Medium | Instant |

## Built-in Kubernetes Strategies

### 1. Recreate

Terminates all existing pods before creating new ones.

**Use when:**
- Application cannot run multiple versions simultaneously
- Development/staging environments
- Database schema migrations requiring exclusive access

**Drawbacks:**
- Causes downtime
- No gradual validation

### 2. Rolling Update (Default)

Gradually replaces old pods with new ones, maintaining availability throughout.

**Configuration:**
- `maxUnavailable`: Maximum pods that can be unavailable (default: 25%)
- `maxSurge`: Maximum pods above desired count (default: 25%)

**Use when:**
- Zero-downtime deployments required
- Application supports running multiple versions
- Standard production deployments

## Advanced Strategies (Argo Rollouts)

### 3. Blue-Green

Runs two identical environments: blue (current) and green (new). Traffic switches entirely after validation.

**Components:**
- `activeService`: Routes production traffic to stable version
- `previewService`: Routes test traffic to new version
- `autoPromotionEnabled`: Controls automatic vs manual promotion
- `scaleDownDelaySeconds`: Delay before terminating old version

**Use when:**
- Need instant rollback capability
- Full environment testing before promotion
- Critical applications requiring validation gates

**Trade-offs:**
- Requires 2x resources during deployment
- All-or-nothing traffic switch

### 4. Canary

Gradually shifts traffic percentage to new version while monitoring metrics.

**Components:**
- `setWeight`: Traffic percentage to canary
- `pause`: Halt for validation (optional duration)
- `analysis`: Automated metric validation
- Traffic management via service mesh (Istio, Linkerd)

**Use when:**
- Risk-averse deployments
- Metric-driven promotion decisions
- Large user bases requiring gradual rollout
- A/B testing combined with deployment

**Best for:**
- High-traffic production systems
- Applications with comprehensive observability
- Teams with mature monitoring practices

## Progressive Delivery Workflow

```
Code Change → Build → Deploy Canary (5%) → Analyze Metrics
                                              ↓
                    ← Rollback (if failed) ← Analysis Pass?
                                              ↓ (yes)
                    Increase Traffic (25%) → Analyze → ... → Full Promotion (100%)
```

## Tool Selection Guide

| Scenario | Recommended Strategy | Tool |
|----------|---------------------|------|
| Simple apps, low traffic | Rolling Update | Native K8s |
| Critical apps, need instant rollback | Blue-Green | Argo Rollouts |
| High-traffic, metric-driven | Canary | Argo Rollouts + Service Mesh |
| Feature flags, user segments | A/B Testing | Argo Rollouts + Feature Flags |
| GitOps workflow | Any | Argo Rollouts + Argo CD |

## Argo Rollouts vs Native Kubernetes

| Feature | Native K8s Deployment | Argo Rollouts |
|---------|----------------------|---------------|
| Rolling Update | Yes | Yes |
| Blue-Green | Manual | Built-in |
| Canary | Manual | Built-in |
| Traffic Management | No | Ingress/Service Mesh |
| Automated Analysis | No | Yes (Prometheus, Datadog) |
| Rollback Automation | Manual | Metric-driven |
| GitOps Integration | Basic | Deep (Argo CD) |

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre/post deployment checklists |
| [examples.md](examples.md) | Complete YAML examples |
| [templates.md](templates.md) | Reusable templates |
| [llm-prompts.md](llm-prompts.md) | AI-assisted deployment prompts |

## Quick Start

1. **Start with Rolling Updates** - Learn fundamentals
2. **Add health checks** - Liveness, readiness, startup probes
3. **Implement Blue-Green** - When instant rollback needed
4. **Graduate to Canary** - When metrics automation mature
5. **Add Analysis** - Prometheus/Datadog integration

## References

- [Kubernetes Deployment Docs](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Argo Rollouts Documentation](https://argo-rollouts.readthedocs.io/)
- [Progressive Delivery with Argo](https://argoproj.github.io/rollouts/)

## Sources

- [Kubernetes Deployment Strategies 2025](https://octopus.com/devops/kubernetes-deployments/)
- [Argo Rollouts Blue-Green](https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/)
- [Argo Rollouts Canary](https://argo-rollouts.readthedocs.io/en/stable/features/canary/)
- [Kubernetes Best Practices 2025](https://kodekloud.com/blog/kubernetes-best-practices-2025/)
- [Spacelift K8s Strategies](https://spacelift.io/blog/kubernetes-deployment-strategies)
