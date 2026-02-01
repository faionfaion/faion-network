# DORA Metrics Reference

Comprehensive guide to measuring and improving software delivery performance using DORA metrics (2025-2026).

## Overview

| Aspect | Coverage |
|--------|----------|
| Framework | DORA (DevOps Research and Assessment) |
| Metrics | 5 key performance indicators |
| Focus | Software delivery performance, reliability, improvement strategies |
| Tools | Sleuth, LinearB, Jellyfish, Faros AI, GitHub/GitLab native |

## Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation and measurement checklist |
| [examples.md](examples.md) | Measurement queries and dashboard examples |
| [templates.md](templates.md) | Ready-to-use templates for tracking |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for DORA analysis |

## The Five DORA Metrics

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| **Deployment Frequency** | On-demand (multiple/day) | Weekly-monthly | Monthly-6mo | <6mo |
| **Lead Time for Changes** | <1 hour | 1 day-1 week | 1-6 months | >6mo |
| **Change Failure Rate** | 0-15% | 16-30% | 31-45% | >45% |
| **Time to Restore Service** | <1 hour | <1 day | 1 day-1 week | >1 week |
| **Reliability** | Exceeds targets | Meets targets | Partially meets | Below targets |

### Metric Definitions

| Metric | Definition | Measurement |
|--------|------------|-------------|
| **Deployment Frequency** | How often code is deployed to production | Deployments per day/week/month |
| **Lead Time for Changes** | Time from code commit to production deployment | Median time from commit to deploy |
| **Change Failure Rate** | Percentage of deployments causing incidents | Failed deploys / Total deploys |
| **Time to Restore Service** | Time to recover from a failed deployment | Median incident resolution time |
| **Reliability** | Meeting reliability targets (SLOs) | Uptime, error rates, MTBF |

## Performance Benchmarks (2025)

| Performance Level | Deploy Freq | Lead Time | CFR | MTTR | Reliability |
|-------------------|-------------|-----------|-----|------|-------------|
| **Elite** | Multiple/day | <1 hour | 0-15% | <1 hour | >99.9% |
| **High** | Weekly-monthly | 1 day-1 week | 16-30% | <1 day | 99-99.9% |
| **Medium** | Monthly-6mo | 1-6 months | 31-45% | 1 day-1 week | 95-99% |
| **Low** | <6mo | >6 months | >45% | >1 week | <95% |

**2025 Research Insight:** Elite DevOps teams deploy code 973x more frequently and recover from incidents 6570x faster than low performers.

## Why DORA Metrics Matter

### Throughput vs Stability

Before DevOps, most organizations considered throughput and stability to be a trade-off. DORA research proves that **high performers excel at both**:

| Dimension | Metrics | Elite Behavior |
|-----------|---------|----------------|
| **Throughput** | Deployment Frequency, Lead Time | Multiple deploys/day, <1 hour lead time |
| **Stability** | Change Failure Rate, MTTR | <15% failure rate, <1 hour recovery |
| **Reliability** | Meeting SLOs | Consistently exceeds targets |

### Business Impact

| Capability | Business Outcome |
|------------|------------------|
| Faster deployments | Quicker time-to-market |
| Lower failure rate | Reduced customer impact |
| Faster recovery | Higher availability |
| Better reliability | Improved customer trust |

## 2025-2026 Best Practices

### Automated Data Collection

Organizations should automate data collection from:
- CI/CD pipelines (deployments, builds)
- Version control systems (commits, PRs)
- Incident management platforms (alerts, incidents)
- Monitoring systems (availability, latency)

### Standardization

| Practice | Implementation |
|----------|----------------|
| Consistent definitions | Document what counts as a "deployment" |
| Unified tracking | Same metrics across all teams |
| Regular cadence | Weekly/monthly metric reviews |
| Baseline establishment | Set initial benchmarks before improvement |

### Holistic Analysis

Analyze all five metrics together:
- High deployment frequency + high CFR = process problems
- Low lead time + high MTTR = monitoring/tooling gaps
- High throughput + low reliability = quality issues

### Combine with Other Frameworks

| Framework | Complements DORA With |
|-----------|----------------------|
| SPACE | Developer satisfaction, collaboration |
| DevEx | Developer experience metrics |
| Value Stream | End-to-end flow efficiency |

## AI Impact (2025 Research)

The 2025 DORA Report found that AI adoption:
- **Improves throughput** (faster code generation, reviews)
- **Increases delivery instability** (higher change failure rate)
- **Requires seven critical capabilities** for full value

### AI Readiness Capabilities

1. Internal data AI-accessible
2. Working in small batches
3. Continuous integration
4. Trunk-based development
5. Test automation
6. Deployment automation
7. Monitoring and observability

## Tool Selection

| Tool | Best For | Features |
|------|----------|----------|
| **Sleuth** | DORA-focused teams | Native DORA tracking, integrations |
| **LinearB** | Engineering metrics | DORA + productivity metrics |
| **Jellyfish** | Enterprise | Business alignment, portfolio view |
| **Faros AI** | Data-driven teams | Custom metrics, warehousing |
| **GitHub** | GitHub users | Built-in insights, Actions data |
| **GitLab** | GitLab users | Built-in analytics, Value Stream |

## Key Principles

| Principle | Description |
|-----------|-------------|
| Measure consistently | Same methodology over time |
| Focus on trends | Progress matters more than absolute values |
| Identify bottlenecks | Use metrics to find constraints |
| No punishment | Don't use metrics punitively |
| Team ownership | Teams should own their metrics |
| Continuous improvement | Regular reviews and action items |

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Run terraform plan, docker build, kubectl get commands | haiku | Mechanical CLI operations |
| Review Dockerfile for best practices | sonnet | Code review, security patterns |
| Debug pod crashes, container networking issues | sonnet | Diagnosis and error analysis |
| Design multi-region failover architecture | opus | Complex distributed systems decisions |
| Write Helm values for production rollout | sonnet | Configuration and templating |
| Create monitoring strategy for microservices | opus | System-wide observability design |
| Troubleshoot Kubernetes pod evictions under load | sonnet | Performance debugging and analysis |

---

## Sources

- [DORA Official Guide](https://dora.dev/guides/dora-metrics-four-keys/)
- [DORA Metrics Complete Guide | DX](https://getdx.com/blog/dora-metrics/)
- [DORA Metrics 2025 Best Practices | Oobeya](https://www.oobeya.io/blog/dora-metrics-2025-best-practices)
- [The DORA 4 Key Metrics Become 5 | CD Foundation](https://cd.foundation/blog/2025/10/16/dora-5-metrics/)
- [DORA Metrics | Atlassian](https://www.atlassian.com/devops/frameworks/dora-metrics)
- [Understanding DORA Metrics | Octopus Deploy](https://octopus.com/devops/metrics/dora-metrics/)
- [DORA Metrics | Waydev](https://waydev.co/dora-metrics/)
- [The Fifth DORA Metric: Reliability | EchoLayer](https://echolayer.com/learn/the-fifth-dora-metric-reliability)
- [DevOps Metrics 2026 | Middleware](https://middleware.io/blog/devops-metrics-you-should-be-monitoring/)
